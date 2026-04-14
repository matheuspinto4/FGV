# config.py

# Parâmetros de Dados
SEQ_LENGTH = 30         # Tamanho da janela (frames)
NUM_NODES = 14          # 7 partes do corpo * 2 ratos
INPUT_CHANNELS = 2      # Coordenadas X e Y
NUM_CLASSES = 4         # Ex: sniff, attack, other, none (ajuste conforme seu dataset)

# Parâmetros de Treino
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 10
TRAIN_SPLIT = 0.8

# Caminhos (Ajuste para os seus arquivos)
TRACKING_PATH = r"\kaggle\input\ratinho\upload\cleaned_data\tracking\CalMS21_supplemental.parquet"
ANNOTATION_PATH = r"\kaggle\input\ratinho\upload\cleaned_data\annotation\CalMS21_supplemental.parquet"