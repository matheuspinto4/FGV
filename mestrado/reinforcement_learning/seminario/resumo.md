# **Abstract**

O artigo relata que no mundo real, as matrizes de recompensas para o agente são extremamente esparsas e, nesses casos, a curiosidade de um agente pode o levar a preencher e explorar mais o seu ambiente.

A curiosidade é formulada como o erro da abilidade de um agente de prever as consequências de suas ações em um espaço visual de características aprendidas por um modelo auto-supervisionado. 

# **Introduction**

O Artigo relata que apenas explorações ao acaso podem não ser o suficiente para preencher as lacunas vazias da matriz de políticas, que no mundo prático são esparsas. 

Como seres humanos, nos acostumamos a lidar com recompensas que são tão esparsas que podemos experimentá-los apenas uma ou duas vezes na vida, ou nenhuma. Quando mais novos, podemos aprender habilidades que se tornam úteis no futuro, quando realmente estivermos ganhando uma recompensa. Estas habilidades podem ser aprendidas através da curiosidade de um agente em explorar e testar.

# **Curiosity-Driven Exploration** 

O agente deles é composto de dois subsistemas: um gerador de recompensa cuja saída é um sinal de recompensa movida a curiosidade e uma política cuja saída é uma sequência de ações para maximizar o sinal de recompensa.

Seja a recompensa curiosa intrínseca gerada pelo agente no tempo $t$ ser denotada por $r_t^i$ 

