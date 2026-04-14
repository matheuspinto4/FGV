# main.py
import torch
from torch.utils.data import DataLoader, random_split
import config
import data_loader
import model
import numpy as np

def train():
    # 1. Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando dispositivo: {device}")

    # 2. Dados
    A = data_loader.get_adjacency_matrix().to(device)
    dataset = data_loader.MouseDataset(config.TRACKING_PATH, config.ANNOTATION_PATH, config.SEQ_LENGTH)
    
    train_size = int(len(dataset) * config.TRAIN_SPLIT)
    test_size = len(dataset) - train_size
    train_ds, test_ds = random_split(dataset, [train_size, test_size])
    
    train_loader = DataLoader(train_ds, batch_size=config.BATCH_SIZE, shuffle=True)
    
    # 3. Modelo
    net = model.MouseActionNet(num_classes=len(dataset.action_map), A=A).to(device)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=config.LEARNING_RATE)

    # 4. Loop de Treino
    print("Iniciando Treinamento...")
    net.train()
    for epoch in range(config.EPOCHS):
        total_loss = 0
        correct = 0
        total = 0
        
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
            optimizer.zero_grad()
            outputs = net(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += y_batch.size(0)
            correct += (predicted == y_batch).sum().item()
            
        print(f"Epoch {epoch+1}/{config.EPOCHS} | Loss: {total_loss/len(train_loader):.4f} | Acc: {100 * correct/total:.2f}%")

    # Salvar o modelo treinado
    torch.save(net.state_dict(), "mouse_action_model.pth")
    print("Modelo salvo!")
    return dataset.action_map

def predict_new_data(model_path, data_sample, action_map):
    """
    Simula a previsão em dados novos.
    data_sample: Tensor (1, 2, 30, 14) -> Um trecho de vídeo de 30 frames
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Recriar estrutura
    A = data_loader.get_adjacency_matrix().to(device)
    net = model.MouseActionNet(num_classes=len(action_map), A=A).to(device)
    
    # Carregar pesos
    net.load_state_dict(torch.load(model_path))
    net.eval()
    
    with torch.no_grad():
        data_sample = data_sample.to(device)
        logits = net(data_sample)
        probs = torch.nn.functional.softmax(logits, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
    
    # Inverter mapa para pegar nome
    idx_to_action = {v: k for k, v in action_map.items()}
    return idx_to_action[pred_idx], probs.cpu().numpy()

if __name__ == "__main__":
    # Rodar Treino
    action_map = train()
    
    # --- TESTE DE PREVISÃO (Simulação) ---
    print("\n--- Testando Previsão ---")
    # Vamos pegar um dado aleatório do dataset só para testar o formato
    ds = data_loader.MouseDataset(config.TRACKING_PATH, config.ANNOTATION_PATH)
    sample_X, sample_y = ds[50] # Pega o 50º exemplo
    
    # Adicionar dimensão de batch (1, 2, 30, 14)
    sample_X = sample_X.unsqueeze(0) 
    
    prediction, probabilities = predict_new_data("mouse_action_model.pth", sample_X, action_map)
    
    real_action = [k for k, v in action_map.items() if v == sample_y][0]
    print(f"Ação Real: {real_action}")
    print(f"Ação Prevista: {prediction}")
    print(f"Confiança: {probabilities.max():.4f}")