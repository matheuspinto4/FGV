# data_loader.py
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
import config

def get_adjacency_matrix():
    """Constrói a topologia do grafo (Esqueleto + Interações)"""
    num_parts = 7
    num_mice = 2
    total_nodes = num_parts * num_mice
    
    # Matriz vazia
    A = torch.zeros((total_nodes, total_nodes))
    
    # 1. Conexões Físicas (Intra-rato)
    # Índices baseados na ordem alfabética provável ou definida: 
    # [ear_left, ear_right, hip_left, hip_right, neck, nose, tail_base] (exemplo)
    # AJUSTE estes índices conforme a ordem real das colunas após o pivot!
    skeleton = [(5, 4), (0, 4), (1, 4), (4, 2), (4, 3), (2, 6), (3, 6)] 
    
    for m in range(num_mice):
        offset = m * num_parts
        for i, j in skeleton:
            src, dst = i + offset, j + offset
            A[src, dst] = 1
            A[dst, src] = 1 # Grafo não direcionado

    # 2. Conexões de Interação (Inter-rato) - Todos com todos para simplificar
    for i in range(num_parts):
        for j in range(num_parts):
            src = i # Rato 1
            dst = j + num_parts # Rato 2
            A[src, dst] = 1
            A[dst, src] = 1

    # 3. Self-loops e Normalização
    A = A + torch.eye(total_nodes)
    D = torch.sum(A, dim=1)
    D_inv_sqrt = torch.pow(D, -0.5)
    D_inv_sqrt[torch.isinf(D_inv_sqrt)] = 0.
    D_mat = torch.diag(D_inv_sqrt)
    A_norm = torch.mm(torch.mm(D_mat, A), D_mat)
    
    return A_norm.float()

class MouseDataset(Dataset):
    def __init__(self, tracking_path, annotation_path, seq_len=30):
        print("Carregando e processando dados... isso pode demorar um pouco.")
        
        # Carregar Tracking
        df_track = pd.read_parquet(tracking_path)
        # Pivotar: Index=Frame, Colunas=(Mouse, Bodypart, Coord)
        df_pivot = df_track.pivot_table(index='video_frame', columns=['mouse_id', 'bodypart'], values=['x', 'y'])
        
        # Preencher NaNs
        df_pivot = df_pivot.interpolate(method='linear').fillna(0)
        
        # Normalizar coordenadas (StandardScaler manual para manter estrutura)
        raw_data = df_pivot.values
        self.mean = raw_data.mean(axis=0)
        self.std = raw_data.std(axis=0) + 1e-6
        raw_data = (raw_data - self.mean) / self.std
        
        # Carregar Annotations
        df_annot = pd.read_parquet(annotation_path)
        
        # Criar Labels Frame a Frame
        self.labels = np.zeros(len(df_pivot), dtype=int)
        
        # Mapeamento de ações
        self.action_map = {act: i for i, act in enumerate(df_annot['action'].unique())}
        # Garanta que 'none' ou similar seja 0 ou tratado
        print(f"Mapa de Ações: {self.action_map}")
        
        for _, row in df_annot.iterrows():
            start, stop = int(row['start_frame']), int(row['stop_frame'])
            if start < len(self.labels):
                stop = min(stop, len(self.labels))
                action_idx = self.action_map.get(row['action'], 0)
                self.labels[start:stop] = action_idx

        # Criar Sequências (Sliding Window)
        # Formato final desejado: (N, Channels, Time, Nodes)
        # O pivot gera colunas achatadas. Precisamos remodelar.
        # Supondo ordem: [x_m1_p1, x_m1_p2... y_m1_p1...] -> É complexo, simplificamos:
        
        self.sequences = []
        self.targets = []
        
        # NOTA: Para datasets gigantes, usar generator em vez de lista
        # Usando stride de 10 para reduzir tamanho no exemplo
        stride = 10 
        num_frames = len(raw_data)
        
        # Reshape para (Frames, Nodes, Channels)
        # A ordem das colunas do pivot precisa ser verificada. 
        # Assumindo que o pandas ordenou: x_mouse1_..., y_mouse1_...
        # Aqui simplificamos para criar o tensor
        data_tensor = torch.tensor(raw_data, dtype=torch.float32)
        # Hack para reshape correto: (Frames, 28) -> (Frames, 2, 14)
        # Isso depende estritamente da ordem das colunas do seu pivot
        data_tensor = data_tensor.view(num_frames, 2, config.NUM_NODES) 
        
        for i in range(0, num_frames - seq_len, stride):
            # Transpor para (Channels, Time, Nodes)
            seq = data_tensor[i:i+seq_len].permute(1, 0, 2) 
            label = self.labels[i + seq_len - 1] # Prediz o último frame da janela
            
            self.sequences.append(seq)
            self.targets.append(label)

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return self.sequences[idx], self.targets[idx]