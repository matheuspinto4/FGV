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

    // Frei-Chen kernels
    float sqrt2 = sqrt(2.0);
    float G1[9] = float[](
        -1.0,  0.0,  1.0,
        -sqrt2, 0.0, sqrt2,
        -1.0,  0.0,  1.0
    );
    float G2[9] = float[](
        -1.0, -sqrt2, -1.0,
         0.0,   0.0,   0.0,
         1.0,  sqrt2,  1.0
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

    // Apply Frei-Chen kernels
    float g1 = 0.0;
    float g2 = 0.0;
    for (int i = 0; i < 9; i++) {
        g1 += G1[i] * luminance[i];
        g2 += G2[i] * luminance[i];
    }

    // Compute edge magnitude
    float magnitude = sqrt(g1 * g1 + g2 * g2);

    // Apply threshold
    float outputValue = magnitude > threshold ? magnitude : 0.0;
    // Normalize to [0, 1] for display
    outputValue = clamp(outputValue, 0.0, 1.0);

    // Output as grayscale
    vec3 outputColor = vec3(outputValue);
    // Alternative: Overlay on dimmed original
    // vec3 original = imageLoad(inputImage, pixelCoord).rgb;
    // outputColor = mix(original * 0.5, vec3(1.0), outputValue);

    imageStore(outputImage, pixelCoord, vec4(outputColor, 1.0));
}