import os
import matplotlib.pyplot as plt
import numpy as np
import torch
from pettingzoo.mpe import simple_speaker_listener_v4

# 1. ALTERAÇÃO: Importar MADDPG ao invés de MATD3
from agilerl.algorithms import MADDPG 
from agilerl.algorithms.core.registry import HyperparameterConfig, RLParameter
from agilerl.components.multi_agent_replay_buffer import MultiAgentReplayBuffer
from agilerl.hpo.mutation import Mutations
from agilerl.hpo.tournament import TournamentSelection
from agilerl.utils.utils import (
    create_population,
    default_progress_bar,
    make_multi_agent_vect_envs,
)

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("===== AgileRL Online Multi-Agent Demo - MADDPG Implementation =====")

    # 2. ALTERAÇÃO: Rede Neural mais robusta. 
    # [64] é muito pouco para capturar nuances. [128, 128] oferece mais capacidade.
    NET_CONFIG = {
        "latent_dim": 128, # Aumentado de 64 para 128
        "encoder_config": {
            "hidden_size": [128, 128],  # Duas camadas de 128
        },
        "head_config": {
            "hidden_size": [128, 128],  # Duas camadas de 128
        },
    }

    # Define the initial hyperparameters
    INIT_HP = {
        "POPULATION_SIZE": 4,
        "ALGO": "MADDPG",  # 3. ALTERAÇÃO: Mudamos o algoritmo aqui
        "BATCH_SIZE": 256,  # 4. ALTERAÇÃO: Aumentado para 256 para gradientes mais estáveis
        "O_U_NOISE": True,
        "EXPL_NOISE": 0.1,
        "MEAN_NOISE": 0.0,
        "THETA": 0.15,
        "DT": 0.01,
        "LR_ACTOR": 0.001,   # Ligeiramente aumentado para convergência mais rápida inicial
        "LR_CRITIC": 0.001,
        "GAMMA": 0.95,
        "MEMORY_SIZE": 100000,
        "LEARN_STEP": 100,
        "TAU": 0.01,
        "POLICY_FREQ": 2,
    }

    num_envs = 8

    def make_env():
        return simple_speaker_listener_v4.parallel_env(continuous_actions=True)

    env = make_multi_agent_vect_envs(env=make_env, num_envs=num_envs)

    observation_spaces = [env.single_observation_space(agent) for agent in env.agents]
    action_spaces = [env.single_action_space(agent) for agent in env.agents]

    INIT_HP["AGENT_IDS"] = env.agents

    # Mutation config for RL hyperparameters
    hp_config = HyperparameterConfig(
        lr_actor=RLParameter(min=1e-4, max=1e-2),
        lr_critic=RLParameter(min=1e-4, max=1e-2),
        batch_size=RLParameter(min=64, max=512, dtype=int), # Ajustado range min
        learn_step=RLParameter(
            min=20, max=200, dtype=int, grow_factor=1.5, shrink_factor=0.75
        ),
    )

    # Create a population
    # Nota: create_population detecta automaticamente a classe MADDPG pela string "MADDPG"
    pop = create_population(
        INIT_HP["ALGO"],
        observation_spaces,
        action_spaces,
        NET_CONFIG,
        INIT_HP,
        hp_config=hp_config,
        population_size=INIT_HP["POPULATION_SIZE"],
        num_envs=num_envs,
        device=device,
    )

    # Configure the multi-agent replay buffer
    field_names = ["obs", "action", "reward", "next_obs", "done"]
    memory = MultiAgentReplayBuffer(
        INIT_HP["MEMORY_SIZE"],
        field_names=field_names,
        agent_ids=INIT_HP["AGENT_IDS"],
        device=device,
    )

    tournament = TournamentSelection(
        tournament_size=2,
        elitism=True,
        population_size=INIT_HP["POPULATION_SIZE"],
        eval_loop=1,
    )

    mutations = Mutations(
        no_mutation=0.2,
        architecture=0.2,
        new_layer_prob=0.2,
        parameters=0.2,
        activation=0,
        rl_hp=0.2,
        mutation_sd=0.1,
        rand_seed=1,
        device=device,
    )

    max_steps = 2_000_000 
    learning_delay = 1000 # 5. ALTERAÇÃO: Pequeno delay para encher o buffer antes de treinar
    evo_steps = 10_000 
    eval_steps = None 
    eval_loop = 1 
    elite = pop[0] 
    total_steps = 0
    
    training_scores_history = []

    # TRAINING LOOP
    print("Training MADDPG...")
    pbar = default_progress_bar(max_steps)
    
    # ... (O restante do loop de treinamento permanece idêntico ao original) ...
    # Copie o restante do loop while do seu arquivo original aqui para baixo.
    # Vou resumir para não ficar gigante, mas a lógica do loop é a mesma.
    
    while np.less([agent.steps[-1] for agent in pop], max_steps).all():
        pop_episode_scores = []
        for agent in pop:
            agent.set_training_mode(True)
            obs, info = env.reset()
            scores = np.zeros(num_envs)
            completed_episode_scores = []
            steps = 0
            
            # Loop de evolução
            for idx_step in range(evo_steps // num_envs):
                action, raw_action = agent.get_action(obs=obs, infos=info)
                next_obs, reward, termination, truncation, info = env.step(action)
                
                scores += np.sum(np.array(list(reward.values())).transpose(), axis=-1)
                total_steps += num_envs
                steps += num_envs

                memory.save_to_memory(
                    obs, raw_action, reward, next_obs, termination, is_vectorised=True
                )

                # Learning logic (mesma do original)
                if agent.learn_step > num_envs:
                    learn_step = agent.learn_step // num_envs
                    if (idx_step % learn_step == 0 and len(memory) >= agent.batch_size and memory.counter > learning_delay):
                        experiences = memory.sample(agent.batch_size)
                        agent.learn(experiences)
                elif (len(memory) >= agent.batch_size and memory.counter > learning_delay):
                    for _ in range(num_envs // agent.learn_step):
                        experiences = memory.sample(agent.batch_size)
                        agent.learn(experiences)

                obs = next_obs
                
                # Reset logic (mesma do original)
                term_array = np.array(list(termination.values())).transpose()
                trunc_array = np.array(list(truncation.values())).transpose()
                for idx, (d, t) in enumerate(zip(term_array, trunc_array)):
                    if np.any(d) or np.any(t):
                        completed_episode_scores.append(scores[idx])
                        agent.scores.append(scores[idx])
                        scores[idx] = 0
                        agent.reset_action_noise([idx])

            pbar.update(evo_steps // len(pop))
            agent.steps[-1] += steps
            pop_episode_scores.append(completed_episode_scores)

        # Evaluate population
        fitnesses = [
            agent.test(env, max_steps=eval_steps, loop=eval_loop)
            for agent in pop
        ]
        mean_scores = [
            (np.mean(episode_scores) if len(episode_scores) > 0 else 0)
            for episode_scores in pop_episode_scores
        ]
        
        population_mean_score = np.mean([score for score in mean_scores if isinstance(score, (int, float))])
        training_scores_history.append(population_mean_score)

        pbar.write(f"Global steps {total_steps} | Scores: {mean_scores}")

        elite, pop = tournament.select(pop)
        pop = mutations.mutation(pop)

        for agent in pop:
            agent.steps.append(agent.steps[-1])

    # Save logic
    path = "./models/MADDPG" # Alterar nome da pasta
    filename = "MADDPG_trained_agent.pt" # Alterar nome do arquivo
    os.makedirs(path, exist_ok=True)
    save_path = os.path.join(path, filename)
    elite.save_checkpoint(save_path)
    
    # Plotting code remains the same...
    plt.figure(figsize=(12, 6))
    plt.plot(training_scores_history, linewidth=2)
    plt.title('Evolução das Pontuações (MADDPG)', fontsize=14)
    plt.xlabel('Iterações de Evolução', fontsize=12)
    plt.ylabel('Pontuação Média', fontsize=12)
    plt.grid(True, alpha=0.3)
    plot_path = os.path.join(path, "training_scores_evolution.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    
    pbar.close()
    env.close()