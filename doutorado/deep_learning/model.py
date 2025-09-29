import torch
import torch.nn as nn
import onnxruntime as ort
import numpy as np

# Corrected model definition
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, 1)
        self.relu = nn.ReLU()
        # Define the pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        # The input size to the linear layer is now correct
        self.fc = nn.Linear(16 * 111 * 111, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        # Add the pooling layer here
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# Instantiate the corrected model
model = SimpleModel()
model.eval()

# Create a dummy input tensor
dummy_input = torch.randn(1, 3, 224, 224)

# Export the model to ONNX
torch.onnx.export(model,
                  dummy_input,
                  "simple_model.onnx",
                  export_params=True,
                  opset_version=17,
                  do_constant_folding=True,
                  input_names=['input'],
                  output_names=['output'])

print("Model has been exported to simple_model.onnx")