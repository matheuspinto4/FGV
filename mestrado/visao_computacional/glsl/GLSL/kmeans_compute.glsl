#version 430
layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;

layout(binding = 0, rgba32f) readonly uniform image2D inputImage;
layout(binding = 1, rgba32f) writeonly uniform image2D outputImage;

uniform vec3 clusterCenters[32]; // Array of up to k=16 cluster centers (RGB)
uniform int k; // Number of clusters

void main() {
    ivec2 pixelCoord = ivec2(gl_GlobalInvocationID.xy);
    ivec2 imageSize = imageSize(inputImage);

    // Skip if out of bounds
    if (pixelCoord.x >= imageSize.x || pixelCoord.y >= imageSize.y) return;

    // Read pixel color
    vec3 pixelColor = imageLoad(inputImage, pixelCoord).rgb;

    // Find closest cluster center
    float minDistance = 1e6;
    vec3 closestColor = vec3(0.0);
    for (int i = 0; i < k; i++) {
        float distance = length(pixelColor - clusterCenters[i]);
        if (distance < minDistance) {
            minDistance = distance;
            closestColor = clusterCenters[i];
        }
    }

    // Output quantized color
    imageStore(outputImage, pixelCoord, vec4(closestColor, 1.0));
}