import torch
import torch.nn as nn
import onnx
import onnxruntime as ort
import numpy as np
from PIL import Image

# A simplified feed-forward style transfer network
class StyleTransferNet(nn.Module):
    def __init__(self):
        super(StyleTransferNet, self).__init__()
        # A real network would have more complex layers
        self.conv1 = nn.Conv2d(3, 16, kernel_size=9, stride=1, padding=4)
        self.bn1 = nn.BatchNorm2d(16)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(16, 3, kernel_size=9, stride=1, padding=4)
    
    def forward(self, x):
        return self.conv2(self.relu1(self.bn1(self.conv1(x))))

def load_and_preprocess_image(image_path, size=256):
    """Loads and preprocesses an image for the network."""
    image = Image.open(image_path).convert('RGB')
    image = image.resize((size, size))
    image = np.array(image).transpose(2, 0, 1).astype(np.float32) / 255.0
    return image[np.newaxis, :, :, :]

# Step 1: Instantiate the style transfer network
print("1. Initializing and 'training' a dummy style transfer network...")
# A real model would be loaded from a file (e.g., torch.load('style_model.pth'))
model = StyleTransferNet()
model.eval()
print("Model initialized successfully.")

# Step 2: Export the network to ONNX
print("\n2. Exporting model to ONNX format...")
dummy_input = torch.randn(1, 3, 256, 256)
onnx_file_path = "style_transfer.onnx"
torch.onnx.export(model,
                  dummy_input,
                  onnx_file_path,
                  export_params=True,
                  opset_version=17,
                  input_names=['input'],
                  output_names=['output'])
print(f"Model exported successfully to '{onnx_file_path}'.")

# Step 3: Load and preprocess your content image
local_image_path = 'eu.jpg' # << Change this line
print(f"\n3. Loading and preprocessing content image from '{local_image_path}'...")
try:
    input_np = load_and_preprocess_image(local_image_path)
    print("Image preprocessed successfully.")
except FileNotFoundError:
    print(f"Error: The image file '{local_image_path}' was not found.")
    exit()

# Step 4: Perform inference with ONNX Runtime
print("\n4. Running inference with ONNX Runtime...")
try:
    providers = ['OpenVINOExecutionProvider']
    session = ort.InferenceSession(onnx_file_path, providers=providers)
    print("Using OpenVINOExecutionProvider for GPU acceleration.")
except Exception as e:
    print(f"OpenVINO provider not found or failed. Falling back to CPU. Error: {e}")
    session = ort.InferenceSession(onnx_file_path, providers=['CPUExecutionProvider'])

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
output_ort = session.run([output_name], {input_name: input_np})[0]
print("Inference successful!")

# Step 5: Post-process and save the stylized image
print("\n5. Saving the stylized image...")
# Convert the output back to an image format
output_image = output_ort[0].transpose(1, 2, 0)
output_image = (output_image * 255.0).clip(0, 255).astype(np.uint8)
stylized_image = Image.fromarray(output_image)
stylized_image_path = "stylized_image.jpg"
stylized_image.save(stylized_image_path)
print(f"Stylized image saved to '{stylized_image_path}'.")
