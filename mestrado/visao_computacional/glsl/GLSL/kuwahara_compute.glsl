#version 430
layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;

layout(binding = 0, rgba32f) readonly uniform image2D inputImage;
layout(binding = 1, rgba32f) writeonly uniform image2D outputImage;

uniform int kernelSize; // Odd number, e.g., 5

void main() {
    ivec2 pixelCoord = ivec2(gl_GlobalInvocationID.xy);
    ivec2 imageSize = imageSize(inputImage);

    // Skip if out of bounds
    if (pixelCoord.x >= imageSize.x || pixelCoord.y >= imageSize.y) return;

    int a = (kernelSize - 1) / 2;

    // Define four quadrants (Q1, Q2, Q3, Q4) as in Python code
    vec3 mean[4];
    float variance[4];

    // Q1: [y : y + a + 1, x : x + a + 1]
    vec3 sum = vec3(0.0);
    float count = 0.0;
    for (int dy = 0; dy <= a; dy++) {
        for (int dx = 0; dx <= a; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x < imageSize.x && coord.y < imageSize.y) {
                sum += imageLoad(inputImage, coord).rgb;
                count += 1.0;
            }
        }
    }
    mean[0] = sum / count;

    // Compute variance for Q1
    sum = vec3(0.0);
    for (int dy = 0; dy <= a; dy++) {
        for (int dx = 0; dx <= a; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x < imageSize.x && coord.y < imageSize.y) {
                vec3 color = imageLoad(inputImage, coord).rgb - mean[0];
                sum += color * color; // Element-wise square
            }
        }
    }
    variance[0] = (sum.r + sum.g + sum.b) / count; // Approximate trace of covariance

    // Q2: [y : y + a + 1, x - a : x + 1]
    sum = vec3(0.0);
    count = 0.0;
    for (int dy = 0; dy <= a; dy++) {
        for (int dx = -a; dx <= 0; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x >= 0 && coord.x < imageSize.x && coord.y < imageSize.y) {
                sum += imageLoad(inputImage, coord).rgb;
                count += 1.0;
            }
        }
    }
    mean[1] = sum / count;

    // Variance for Q2
    sum = vec3(0.0);
    for (int dy = 0; dy <= a; dy++) {
        for (int dx = -a; dx <= 0; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x >= 0 && coord.x < imageSize.x && coord.y < imageSize.y) {
                vec3 color = imageLoad(inputImage, coord).rgb - mean[1];
                sum += color * color;
            }
        }
    }
    variance[1] = (sum.r + sum.g + sum.b) / count;

    // Q3: [y - a : y + 1, x - a : x + 1]
    sum = vec3(0.0);
    count = 0.0;
    for (int dy = -a; dy <= 0; dy++) {
        for (int dx = -a; dx <= 0; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x >= 0 && coord.x < imageSize.x && coord.y >= 0 && coord.y < imageSize.y) {
                sum += imageLoad(inputImage, coord).rgb;
                count += 1.0;
            }
        }
    }
    mean[2] = sum / count;

    // Variance for Q3
    sum = vec3(0.0);
    for (int dy = -a; dy <= 0; dy++) {
        for (int dx = -a; dx <= 0; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x >= 0 && coord.x < imageSize.x && coord.y >= 0 && coord.y < imageSize.y) {
                vec3 color = imageLoad(inputImage, coord).rgb - mean[2];
                sum += color * color;
            }
        }
    }
    variance[2] = (sum.r + sum.g + sum.b) / count;

    // Q4: [y - a : y + 1, x : x + a + 1]
    sum = vec3(0.0);
    count = 0.0;
    for (int dy = -a; dy <= 0; dy++) {
        for (int dx = 0; dx <= a; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x < imageSize.x && coord.y >= 0 && coord.y < imageSize.y) {
                sum += imageLoad(inputImage, coord).rgb;
                count += 1.0;
            }
        }
    }
    mean[3] = sum / count;

    // Variance for Q4
    sum = vec3(0.0);
    for (int dy = -a; dy <= 0; dy++) {
        for (int dx = 0; dx <= a; dx++) {
            ivec2 coord = pixelCoord + ivec2(dx, dy);
            if (coord.x < imageSize.x && coord.y >= 0 && coord.y < imageSize.y) {
                vec3 color = imageLoad(inputImage, coord).rgb - mean[3];
                sum += color * color;
            }
        }
    }
    variance[3] = (sum.r + sum.g + sum.b) / count;

    // Find quadrant with minimum variance
    float minVariance = variance[0];
    int minIndex = 0;
    for (int i = 1; i < 4; i++) {
        if (variance[i] < minVariance) {
            minVariance = variance[i];
            minIndex = i;
        }
    }

    // Write the mean of the minimum variance quadrant to output
    imageStore(outputImage, pixelCoord, vec4(mean[minIndex], 1.0));
}