#version 430
layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;

layout(binding = 0, rgba32f) readonly uniform image2D inputImage;
layout(binding = 1, rgba32f) writeonly uniform image2D outputImage;

uniform float threshold; // Threshold for edge detection (0.0 to 1.0)

void main() {
    ivec2 pixelCoord = ivec2(gl_GlobalInvocationID.xy);
    ivec2 imageSize = imageSize(inputImage);

    // Skip if out of bounds
    if (pixelCoord.x >= imageSize.x || pixelCoord.y >= imageSize.y) return;

    // Sobel kernels
    float sobelX[9] = float[](
        -1.0, 0.0, 1.0,
        -2.0, 0.0, 2.0,
        -1.0, 0.0, 1.0
    );
    float sobelY[9] = float[](
        -1.0, -2.0, -1.0,
         0.0,  0.0,  0.0,
         1.0,  2.0,  1.0
    );

    // Sample 3x3 neighborhood
    float luminance[9];
    int index = 0;
    for (int dy = -1; dy <= 1; dy++) {
        for (int dx = -1; dx <= 1; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x >= 0 && coord.x < imageSize.x && coord.y >= 0 && coord.y < imageSize.y) {
                vec3 color = imageLoad(inputImage, coord).rgb;
                // Convert to luminance (ITU-R 601)
                luminance[index] = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b;
            } else {
                luminance[index] = 0.0; // Edge pixels
            }
            index++;
        }
    }

    // Apply Sobel kernels
    float gx = 0.0;
    float gy = 0.0;
    for (int i = 0; i < 9; i++) {
        gx += sobelX[i] * luminance[i];
        gy += sobelY[i] * luminance[i];
    }

    // Compute gradient magnitude
    float magnitude = sqrt(gx * gx + gy * gy);

    // Apply threshold
    float outputValue = magnitude > threshold ? magnitude : 0.0;
    // Normalize to [0, 1] for display (magnitude can be > 1.0)
    outputValue = clamp(outputValue, 0.0, 1.0);

    // Output as grayscale
    vec3 outputColor = vec3(outputValue);
    // Alternative: Overlay on dimmed original
    // vec3 original = imageLoad(inputImage, pixelCoord).rgb;
    // outputColor = mix(original * 0.5, vec3(1.0), outputValue);

    imageStore(outputImage, pixelCoord, vec4(outputColor, 1.0));
}