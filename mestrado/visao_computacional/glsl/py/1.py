import glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image

imagePath = 'beatriz.jpg'

# Load GLSL shader from file
with open("kuwahara_compute.glsl", "r") as f:
    compute_shader_source = f.read()

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW initialization failed")

# Create invisible window
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(640, 480, "Kuwahara Compute", None, None)
if not window:
    glfw.terminate()
    raise Exception("Window creation failed")

glfw.make_context_current(window)

# Compile compute shader
shader = glCreateShader(GL_COMPUTE_SHADER)
glShaderSource(shader, compute_shader_source)
glCompileShader(shader)
if not glGetShaderiv(shader, GL_COMPILE_STATUS):
    raise Exception(glGetShaderInfoLog(shader).decode())

program = glCreateProgram()
glAttachShader(program, shader)
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    raise Exception(glGetProgramInfoLog(program).decode())

glDeleteShader(shader)

# Load input image (replace with your image path)
image = Image.open(imagePath).convert("RGB")
image_data = np.array(image, dtype=np.float32) / 255.0  # Normalize to [0, 1]
height, width, _ = image_data.shape

# Create input texture
input_texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, input_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, image_data)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Create output texture
output_texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, output_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGB, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Bind textures to image units
glBindImageTexture(0, input_texture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
glBindImageTexture(1, output_texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)

# Set kernel size uniform
for kernel_size in range(1,100,2):

    glUseProgram(program)
    glUniform1i(glGetUniformLocation(program, "kernelSize"), kernel_size)

    # Dispatch compute shader
    group_x = (width + 15) // 16  # Ceiling division
    group_y = (height + 15) // 16
    glDispatchCompute(group_x, group_y, 1)
    glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

    # Read output texture
    glBindTexture(GL_TEXTURE_2D, output_texture)
    output_data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGB, GL_FLOAT)
    output_data = np.frombuffer(output_data, dtype=np.float32).reshape(height, width, 3)

    # Save output image
    output_image = Image.fromarray((output_data * 255.0).astype(np.uint8))
    output_image.save(f"output_kuwahara_{kernel_size}.png")

    # Cleanup
glDeleteTextures([input_texture, output_texture])
glDeleteProgram(program)
glfw.destroy_window(window)
glfw.terminate()