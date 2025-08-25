#version 430
layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;

layout(binding = 0, rgba32f) readonly uniform image2D currentFrame;
layout(binding = 1, rgba32f) readonly uniform image2D previousFrame;
layout(binding = 2, rgba32f) writeonly uniform image2D outputFrame;

uniform float threshold; // Sensitivity for motion detection

void main() {
    ivec2 pixelCoord = ivec2(gl_GlobalInvocationID.xy);
    ivec2 imageSize = imageSize(currentFrame);

    // Skip if out of bounds
    if (pixelCoord.x >= imageSize.x || pixelCoord.y >= imageSize.y) return;

    // Read current and previous frame pixels
    vec3 current = imageLoad(currentFrame, pixelCoord).rgb;
    vec3 previous = imageLoad(previousFrame, pixelCoord).rgb;

    // Compute absolute difference
    vec3 diff = abs(current - previous);

    // Sum differences across channels (luminance-based)
    float diffSum = diff.r + diff.g + diff.b;

    // Apply threshold to detect motion
    vec3 outputColor;
    if (diffSum > threshold) {
        outputColor = vec3(1.0); // White for motion
    } else {
        outputColor = vec3(0.0); // Black for no motion
        // Alternative: outputColor = current * 0.5; // Dimmed original frame
    }

    // Write to output
    imageStore(outputFrame, pixelCoord, vec4(outputColor, 1.0));
}