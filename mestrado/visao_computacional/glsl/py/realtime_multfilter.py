import glfw
from OpenGL.GL import *
import numpy as np
import cv2

# Load GLSL compute shaders
shader_files = {
    'kuwahara': 'GLSL/kuwahara_compute.glsl',
    'motion': 'GLSL/motion_detection.glsl',
    'sobel': 'GLSL/sobel_compute.glsl',
    'emboss': 'GLSL/emboss_compute.glsl',
    'freichen': 'GLSL/freichen_compute.glsl'
}

compute_shader_sources = {}
for name, file in shader_files.items():
    with open(file, 'r') as f:
        compute_shader_sources[name] = f.read()

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
window = glfw.create_window(1280, 720, "Real-Time Multi-Filter", None, None)
if not window:
    glfw.terminate()
    raise Exception("Window creation failed")

glfw.make_context_current(window)
print(f"OpenGL Version: {glGetString(GL_VERSION).decode()}")

# Create shader programs
compute_programs = {name: create_program(None, None, source) for name, source in compute_shader_sources.items()}
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

# Initialize video writer
recording = False
out = None
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Create textures
input_texture = glGenTextures(1)
intermediate_texture = glGenTextures(1)
output_texture = glGenTextures(1)
previous_texture = glGenTextures(1)  # For motion detection

# Input texture
glBindTexture(GL_TEXTURE_2D, input_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Intermediate texture
glBindTexture(GL_TEXTURE_2D, intermediate_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Output texture
glBindTexture(GL_TEXTURE_2D, output_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Previous texture (for motion detection)
glBindTexture(GL_TEXTURE_2D, previous_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Set uniforms for each filter
for name, program in compute_programs.items():
    glUseProgram(program)
    if name == 'kuwahara':
        glUniform1i(glGetUniformLocation(program, "kernelSize"), 11)
    elif name == 'motion':
        glUniform1f(glGetUniformLocation(program, "threshold"), 0.4)
    elif name == 'sobel':
        glUniform1f(glGetUniformLocation(program, "threshold"), 0.05)
    elif name == 'emboss':
        glUniform1f(glGetUniformLocation(program, "intensity"), 0.7)
    elif name == 'freichen':
        glUniform1f(glGetUniformLocation(program, "threshold"), 0.1)

# Initialize filter state
current_filter = 'none'  # Start with raw feed
chain_filters = False  # Toggle chaining (e.g., Kuwahara + Sobel)

# Read initial frame for previous_texture (motion detection)
ret, frame = cap.read()
if not ret:
    cap.release()
    glfw.terminate()
    raise Exception("Failed to capture initial frame")
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame_data = (frame_rgb.astype(np.float32) / 255.0)
glBindTexture(GL_TEXTURE_2D, previous_texture)
glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GL_RGB, GL_FLOAT, frame_data)

# Keyboard callback
def key_callback(window, key, scancode, action, mods):
    global current_filter, chain_filters, recording, out
    if action == glfw.PRESS:
        if key == glfw.KEY_0:
            current_filter = 'none'
            print("Filter: Raw Feed")
        elif key == glfw.KEY_1:
            current_filter = 'kuwahara'
            print("Filter: Kuwahara")
        elif key == glfw.KEY_2:
            current_filter = 'motion'
            print("Filter: Motion Detection")
        elif key == glfw.KEY_3:
            current_filter = 'sobel'
            print("Filter: Sobel")
        elif key == glfw.KEY_4:
            current_filter = 'emboss'
            print("Filter: Emboss")
        elif key == glfw.KEY_5:
            current_filter = 'freichen'
            print("Filter: Frei-Chen")
        elif key == glfw.KEY_C:
            chain_filters = not chain_filters
            print(f"Chaining Filters: {'On' if chain_filters else 'Off'}")
        elif key == glfw.KEY_R:
            if not recording:
                out = cv2.VideoWriter('output_multifilter.mp4', fourcc, 30.0, (1280, 720))
                recording = True
                print("Recording started")
            else:
                out.release()
                out = None
                recording = False
                print("Recording stopped")

glfw.set_key_callback(window, key_callback)

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

    # Apply filter(s)
    if current_filter == 'none':
        # Copy input to output for raw feed
        glBindTexture(GL_TEXTURE_2D, output_texture)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GL_RGB, GL_FLOAT, frame_data)
    elif chain_filters:
        # Chain Kuwahara + Sobel
        # Kuwahara: input -> intermediate
        glUseProgram(compute_programs['kuwahara'])
        glBindImageTexture(0, input_texture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
        glBindImageTexture(1, intermediate_texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
        group_x = (width + 15) // 16
        group_y = (height + 15) // 16
        glDispatchCompute(group_x, group_y, 1)
        glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        # Sobel: intermediate -> output
        glUseProgram(compute_programs['motion'])
        glBindImageTexture(0, intermediate_texture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
        glBindImageTexture(1, output_texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
        glDispatchCompute(group_x, group_y, 1)
        glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
    else:
        # Single filter
        if current_filter == 'motion':
            # Motion detection uses previous and current frames
            glUseProgram(compute_programs[current_filter])
            glBindImageTexture(0, input_texture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
            glBindImageTexture(1, previous_texture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
            glBindImageTexture(2, output_texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
        else:
            glUseProgram(compute_programs[current_filter])
            glBindImageTexture(0, input_texture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
            glBindImageTexture(1, output_texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
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

    # Read back for video recording
    if recording and out is not None:
        glReadBuffer(GL_FRONT)
        frame_buffer = glReadPixels(0, 0, 1280, 720, GL_RGB, GL_UNSIGNED_BYTE)
        frame_array = np.frombuffer(frame_buffer, dtype=np.uint8).reshape((720, 1280, 3))
        frame_array = np.flipud(frame_array)
        frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

    # Update previous texture for motion detection
    glBindTexture(GL_TEXTURE_2D, previous_texture)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GL_RGB, GL_FLOAT, frame_data)

# Cleanup
cap.release()
if out is not None:
    out.release()
glDeleteTextures([input_texture, intermediate_texture, output_texture, previous_texture])
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(2, [vbo, ebo])
for program in compute_programs.values():
    glDeleteProgram(program)
glDeleteProgram(render_program)
glfw.destroy_window(window)
glfw.terminate()