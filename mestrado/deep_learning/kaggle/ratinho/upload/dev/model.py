# model.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphConv(nn.Module):
    def __init__(self, in_channels, out_channels, A):
        super(GraphConv, self).__init__()
        self.A = nn.Parameter(A, requires_grad=False)
        self.conv = nn.Conv2d(in_channels, out_channels, 1)

    def forward(self, x):
        # x: (N, C, T, V)
        x = self.conv(x)
        
        n, c, t, v = x.size()
        x = x.view(n, c * t, v)
        x = torch.matmul(x, self.A) # Propagação no Grafo
        x = x.view(n, c, t, v)
        return x

class STGCN_Block(nn.Module):
    def __init__(self, in_c, out_c, A, stride=1):
        super().__init__()
        self.gcn = GraphConv(in_c, out_c, A)
        self.tcn = nn.Sequential(
            nn.BatchNorm2d(out_c),
            nn.ReLU(),
            # Kernel (9,1) = Olha 9 frames no tempo, 1 nó no espaço
            nn.Conv2d(out_c, out_c, (9, 1), padding=(4, 0), stride=(stride, 1)),
            nn.Dropout(0.2)
        )

    def forward(self, x):
        x = self.gcn(x)
        x = self.tcn(x)
        return x

class MouseActionNet(nn.Module):
    def __init__(self, num_classes, A):
        super().__init__()
        
        self.layer1 = STGCN_Block(2, 32, A)
        self.layer2 = STGCN_Block(32, 64, A)
        self.layer3 = STGCN_Block(64, 128, A)
        
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        # x input: (Batch, 2, Seq_Len, Nodes)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        
        # Global Average Pooling sobre Tempo e Vértices
        x = F.avg_pool2d(x, x.size()[2:])
        x = x.view(x.size(0), -1)
        
        return self.fc(x)