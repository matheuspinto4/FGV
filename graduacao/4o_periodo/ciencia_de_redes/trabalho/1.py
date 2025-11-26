import networkx as nx
import random
import matplotlib.pyplot as plt

def run_sis_simulation(G, beta, mu, initial_infected=5, t_max=300):
    """
    Executa uma simulação do modelo SIS em uma rede.

    Parâmetros:
    - G: O grafo (rede) NetworkX.
    - beta: Taxa de infecção por aresta.
    - mu: Taxa de recuperação.
    - initial_infected: Número de nós infectados iniciais.
    - t_max: Número máximo de passos de tempo.
    
    Retorna:
    - Uma lista com o número de infectados em cada passo de tempo.
    """
    
    N = G.number_of_nodes()
    
    # Dicionário para rastrear o estado de cada nó: 0=Suscetível, 1=Infectado
    state = {node: 0 for node in G.nodes()}
    
    # 1. Infectar os nós iniciais
    initial_nodes = random.sample(list(G.nodes()), initial_infected)
    for node in initial_nodes:
        state[node] = 1
        
    infected_history = []
    infected_count = initial_infected
    infected_history.append(infected_count)
    
    # 2. Loop da Simulação
    for t in range(t_max):
        
        # Se a epidemia morrer, pare cedo
        if infected_count == 0:
            infected_history.extend([0] * (t_max - t)) # Preenche o resto
            break
            
        # Dicionário para armazenar as mudanças de estado
        # Isso garante que todas as mudanças ocorram "simultaneamente"
        nodes_to_update = {}
        
        # Identifica os nós infectados atuais
        current_infected = [node for node, s in state.items() if s == 1]
        
        # 3. Processo de Infecção (S -> I)
        # Para ser eficiente, olhamos apenas para os vizinhos suscetíveis
        # dos nós já infectados.
        susceptible_neighbors_of_infected = set()
        for i in current_infected:
            for j in G.neighbors(i):
                if state[j] == 0: # Se o vizinho 'j' é suscetível
                    susceptible_neighbors_of_infected.add(j)
        
        for j in susceptible_neighbors_of_infected:
            # j é um nó suscetível com pelo menos um vizinho infectado
            
            # Contamos quantos vizinhos infectados 'j' tem
            k_i = 0
            for neighbor in G.neighbors(j):
                if state[neighbor] == 1:
                    k_i += 1
            
            # Probabilidade de ser infectado
            # P(inf) = 1 - P(não ser inf. por nenhum vizinho)
            prob_infection = 1 - (1 - beta)**k_i
            
            if random.random() < prob_infection:
                nodes_to_update[j] = 1 # Marcar para infecção
                
        # 4. Processo de Recuperação (I -> S)
        for i in current_infected:
            if random.random() < mu:
                # Mesmo que tenha sido marcado para infecção
                # (o que é impossível), a recuperação tem precedência
                # ou simplesmente não o infectamos.
                # Aqui, como 'i' já está infectado,
                # apenas checamos a recuperação.
                if i not in nodes_to_update: # Não foi recém-infectado
                    nodes_to_update[i] = 0 # Marcar para recuperação

        # 5. Aplicar todas as atualizações
        for node, new_state in nodes_to_update.items():
            state[node] = new_state
            
        # 6. Registrar contagem
        infected_count = sum(state.values())
        infected_history.append(infected_count)
        
    return infected_history

# --- Configuração Principal ---

# 1. Parâmetros da Rede e Simulação
N = 10000
avg_k = 20
p = avg_k / (N - 1) # Probabilidade de aresta para rede ER
t_max = 300         # Passos de tempo da simulação

# Parâmetros da epidemia
beta = 0.02
mu_values = [0.1, 0.4, 0.5] # Casos (a), (b), (c)

# 2. Gerar a Rede (apenas uma vez)
print(f"Gerando rede Erdos-Renyi G(N, p) com N={N}, <k>~{avg_k}...")
# Usamos uma seed para que a rede seja sempre a mesma,
# tornando as simulações comparáveis.
G = nx.erdos_renyi_graph(N, p, seed=42)
print("Rede gerada com sucesso.")
print(f"Número de nós: {G.number_of_nodes()}")
avg_degree_actual = sum(dict(G.degree()).values()) / N
print(f"Grau médio real: {avg_degree_actual:.2f}")

# 3. Rodar as Simulações
results = {}
for mu in mu_values:
    R0 = (beta * avg_k) / mu
    print(f"\nIniciando simulação: beta={beta}, mu={mu} (R0_teórico ≈ {R0:.2f})")
    
    # Define uma seed para a simulação (reprodutibilidade)
    random.seed(123) 
    
    history = run_sis_simulation(G, beta, mu, initial_infected=5, t_max=t_max)
    results[mu] = history
    print(f"Simulação concluída. Infectados no final (t={t_max}): {history[-1]}")

# 4. Plotar os Resultados
print("\nGerando gráfico...")
plt.figure(figsize=(12, 8))

for mu, history in results.items():
    R0 = (beta * avg_k) / mu
    label = f"Caso (μ={mu}): R_0 approx {R0:.1f}"
    if R0 > 1:
        label += " (Endêmico)"
    elif R0 == 1:
        label += " (Crítico)"
    else:
        label += " (Extinção)"
        
    plt.plot(history, label=label, lw=2)

plt.title(f"Simulação Modelo SIS em Rede Erdos-Renyi (N={N}, <k>≈{avg_k}, β={beta})")
plt.xlabel("Passo de Tempo (t)")
plt.ylabel("Número de Indivíduos Infectados")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()