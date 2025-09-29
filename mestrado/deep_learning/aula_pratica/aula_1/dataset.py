from torch.utils.data import Dataset 
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

# O torch.utils.data.Dataset é uma abstração que
# permite carregar e manipular datasets grandes

# Carregando um dataset:

training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)

test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor()
)

# Iterando e Visualizando
