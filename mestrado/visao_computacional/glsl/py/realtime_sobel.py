import glfw
from OpenGL.GL import *
import numpy as np
import cv2

# Load GLSL compute shader
with open("sobel_compute.glsl", "r") as f:
    compute_shader_source = f.read()

# Vertex and fragment shaders for rendering
vertex_shader_source = """
#version 330 core
layout(location = 0) in vec2 position;
layout(location = 1) in vec2 texCoord;
out vec2 vTexCoord;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    vTexCoord = texCoord;
}
"""

fragment_shader_source = """
#version 330 core
in vec2 vTexCoord;
out vec4 fragColor;
uniform sampler2D texture0;
void main() {
    fragColor = texture(texture0, vTexCoord);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise Exception(glGetShaderInfoLog(shader).decode())
    return shader

def create_program(vertex_source, fragment_source=None, compute_source=None):
    program = glCreateProgram()
    if vertex_source:
        vs = compile_shader(vertex_source, GL_VERTEX_SHADER)
        glAttachShader(program, vs)
    if fragment_source:
        fs = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
        glAttachShader(program, fs)
    if compute_source:
        cs = compile_shader(compute_source, GL_COMPUTE_SHADER)
        glAttachShader(program, cs)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise Exception(glGetProgramInfoLog(program).decode())
    if vertex_source:
        glDeleteShader(vs)
    if fragment_source:
        glDeleteShader(fs)
    if compute_source:
        glDeleteShader(cs)
    return program

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW initialization failed")

# Create window
window = glfw.create_window(1280, 720, "Real-Time Sobel Filter", None, None)
if not window:
    glfw.terminate()
    raise Exception("Window creation failed")

glfw.make_context_current(window)
print(f"OpenGL Version: {glGetString(GL_VERSION).decode()}")

# Create shader programs
compute_program = create_program(None, None, compute_shader_source)
render_program = create_program(vertex_shader_source, fragment_shader_source)

# Set up quad for rendering (y-axis and x-axis corrected)
vertices = np.array([
    # Position   # TexCoord
    -1.0, -1.0,  1.0, 1.0,  # Bottom-left
     1.0, -1.0,  0.0, 1.0,  # Bottom-right
     1.0,  1.0,  0.0, 0.0,  # Top-right
    -1.0,  1.0,  1.0, 0.0   # Top-left
], dtype=np.float32)
indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
ebo = glGenBuffers(1)

glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))
glEnableVertexAttribArray(1)

glBindVertexArray(0)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    glfw.terminate()
    raise Exception("Failed to open webcam")

# Get webcam resolution
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create textures
input_texture = glGenTextures(1)
output_texture = glGenTextures(1)

# Input texture
glBindTexture(GL_TEXTURE_2D, input_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Output texture
glBindTexture(GL_TEXTURE_2D, output_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Set threshold uniform
threshold = 0.1 # Adjust for edge sensitivity
glUseProgram(compute_program)
glUniform1f(glGetUniformLocation(compute_program, "threshold"), threshold)

# Main loop
while not glfw.window_should_close(window):
    # Capture frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Convert BGR to RGB and normalize
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_data = (frame_rgb.astype(np.float32) / 255.0)

    # Update input texture
    glBindTexture(GL_TEXTURE_2D, input_texture)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GL_RGB, GL_FLOAT, frame_data)

    # Bind textures to image units
    glBindImageTexture(0, input_texture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
    glBindImageTexture(1, output_texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)

    # Run compute shader
    glUseProgram(compute_program)
    group_x = (width + 15) // 16
    group_y = (height + 15) // 16
    glDispatchCompute(group_x, group_y, 1)
    glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

    # Render to screen
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(render_program)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, output_texture)
    glUniform1i(glGetUniformLocation(render_program, "texture0"), 0)
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    glBindVertexArray(0)

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup
cap.release()
glDeleteTextures([input_texture, output_texture])
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(2, [vbo, ebo])
glDeleteProgram(compute_program)
glDeleteProgram(render_program)
glfw.destroy_window(window)
glfw.terminate()