# **Introduction**

## **1.2 Examples**

- Chess movements;
- An adaptive controller adjustes parameters of a petroleum refinery's operation in real time;
- A gazelle calf struggles to its feet minutes after beign born. Half an hour later it is running at 20 miles per hour;
- A mobile robot decides whether it should enter a new room in search of more trash to collect or start trying to find its way back to its battery recharging station.

All these examples involve interaction between an active decision-making agent and its environment. The agent's seeks to achieve a goal despite uncertainty about its enviroment. The agent's actions are permitted to affect the future state of the environment

## **1.3 Elements of Reinforcement Learning**

- **Policy:** defines the learning agent's way of behaving at a given time. In some cases the policy may be a simple function or lookup table, whereas in others it may involve extensive computation such as a search process. The policy is the core of reinforcement learning agent in the sense that it alone is sufficient to determine behavior.

- **Reward Signal:** defines the goal of a reinforcement learning problem. On each time step, the environment sends to the reinforcements learning agent a single number called the *reward*. The reward signal is the primary basis for altering the policy.

- **Value Function:** specifies what is good in the long run. The value state of a state is the total amount of reward an agent can expect to accumulate over the future, starting from that state.

Action choices are made based on value judgments.

# Part I: Tabular Solution Methods

In this part the state and action spaces are small enough for the approximate value functions to be represented as arrays, or tables.


## Chapter 2 Multi-armed Bandits

A simplified version of the reinforcement learning problem: There is only one state. An dactions taken does not interfer in the future more thant one step.

### 2.1 A k-armed Bandit Problem

In our k-armed bandit problem, each of the actions has an expected or mean reward given that that action is selected; let us call this the value of that action.
- **$A_t$:** action selected on time step $t$.
- **$R_t$:** the corresponding reward.
- **$q_*(a)$** is the value of an arbitrary action a, and it is the expected reward given that $a$ is selected.

**$$
q_*(a) = E[R_t|A_t=a]$$**

We assume that we do not know the action values with certainty, although you may have estimates. We denote the estimated value of action $a$ at time step $t$ as $Q_t(a)$. We would like $Q_t(a)$ to be close to $q_*(a)$
Exploitation is the right thing to do to maximize the expected reward on the one step, but exploration may produce the greater total reward in the long run.

### 2.2 Action-value Methods

We beging by looking more closely at methods for estimating the values of actions and for using the estimates to make actions selection decisions (*action-value methods*).One natural way to estimate this is by averaging the rewards actually received:

**$$
Q_t(a) = \frac{\sum_{t=1}^{t-1}R_i*\mathbb{I}_{A_i=a}}{\sum_{t=1}^{t-1}\mathbb{I}_{A_i=a}}$$**

Of course this is just one way to estimate action values, and not necessarily the best one.
The simplest action selection rule is to select one of the actions with the highest estimated value.
**$$
A_t = argmax_aQ_t(a)$$**

Greedy action selection always exploits current knowledge to maximize immediate reward; it spends no time at all sampling apparently inferior actions to see if they might really be better. A simple alternative is to behave greedly most of the time, but every once in a while, say with small probability $\epsilon$, instead select randomly from among all the actions with equal probability. We call methods using this near-greedy action selection rule **$\epsilon-greedy$** methods.

### 2.4 Incremental Implementation

The action-value methods we have discussed so far all estimate action values sample avareges of observer rewards. We can now try to compute an computationally efficient manner, with constant memory and constant per-time-step computation.
To simplify notation we concentrate on a single action. Let $R_i$ now denote the reward received after the *i*th selection of this action.
**$$
Q_n = \frac{R_1 + R_2 + \dots + R_{n-1}}{n-1}
  $$**

We do not want to save every action taken at every step and reward given at that step. We can simply do the following:

**$$
Q_{n+1} = Q_n + \frac{1}{n}[R_n - Q_n]
  $$**

The update rule above is of a form that occurs frequently throughout this book. The general form is

***NewEstimate* $\leftarrow$ *OldEstimate* + *StepSize*[*Target* $-$ *OldEstimate*]**

The step-size parameter is denoted by $\alpha$ or, more generally, by **$\alpha_t(a)$**

    A Simple bandit algorithm

    Initialize, for a = 1 to k:
        Q(a) <- 0
        N(a) <- 0
    
    Loop forever:
            / argmax_a Q(a) with probability 1 - e
        A <-|
            \ a random action with probability e
        R <- bandit(A)
        N(A) <- N(A) + 1
        Q(A) <- Q(A) + (1/N(A))[R - Q(A)]

### 2.5 Tracking a Nonstationary Problem

In cases where the problem is nonstationary, it makes sense to give more weight to recent rewards than to long-past rewards. One of the most popular ways of doing this is to use a constant step-size parameter.

**$$
Q_{n+1}=Q_n + \alpha[R_n - Q_n]$$**

Which is the same has the following:

**$$
Q_{n+1}=(1-\alpha)^nQ_1 + \sum_{i=1}^n\alpha(1-\alpha)^{n-i}R_i$$**

This is sometimes called an exponential recency-weighted avarege

### 2.6 Optimistic Initial Values

All the methods we have discussed so far are dependent to some extent on the initial action-value estimates, $Q_1(a)$. For the sample-average methods, the bias disappears once all actions have been selected at leats once, but for methods with constant $\alpha$, the bias is permanent, though decreasing over time.
Initial action values can also be used as a simple way to encorage exploration. If we set all the initial values to +5, then the system does a fair ammount of exploration before going to the best way possible, covering more ground.

We call this technique for encouraging exploration ***optimistic initial values***. But ut is not well suited to nonstationary problems because its drive for exploration is inherently temporary. If the task changes, creating a renewed need for exploration, this method cannot help.

### 2.7 Upper-Confidence-Bound Action Selection

Exploration is needed because there is always uncertainty about the accuracy of the action-value estimates. It would be better to select amoung the non-greedy actions according to their potential for actually being optimal, taking into account both how close their estimates are to being maximal and the uncertainties in thos estimates.

One effective way of doing this:
**$$
A_t = \argmax_a \left[ Q_t(a) + x\sqrt{\frac{ln(t)}{N_t(a)}}\right]$$**


$N_t(a)$ denotes the number of times that action $a$ has been selected prior to time $t$ and the number $c > 0$ controls the degree of exploration. 

### 2.8 Gradient Bandit Algorithms

In this section we consider learning a numerical *preference* for each action $a$, which we denote $H_t(a)$. The larger the preference, the more often that action i staken, but the preference has no interpretation in terms of reward. The action probabilities are determined according to a *soft-max distribution* :

**$$
Pr(A_t=a) = \frac{e^{H_t(a)}}{\sum_{b=1}^ke^{H_t(b)}} = \pi_t(a)$$**

where $\pi_t(a)$ denotes the probability of taking action $a$ at time $t$.

There is a natural learning algorithm for this setting based on the idea of stochastic gradient ascent. On each step, after selecting action $A_t$ and receiving the reward $R_t$, the action preferences are updated by:

**$$
H_{t+1}(A_t) = H_t(A_t) + \alpha(R_t - \overline{R_t})(1 - \pi_t(A_t)) \text{,  and} \\
H_{t+1}(a) = H_t(a) - \alpha(R_t - \overline{R_t})\pi_t(a), \text{for all $a \neq A_t$ }$$**


The \overline{R_t} term serves as a baseline with which the reward is compared.

### 2.9 Associative Search (Contextual Bandits)

So far we have consideren **only nonassociative tasks**, that is, tasks in which there is no need to associate **different actions with different situations**. However, usually there is more than one situation, and the goal is to **learn a policy**: a mapping from situation to the actions that are best in those situations.
Now suppose there are many k-armed bandits, and each one is presented to you in a different time step and is chosen randomly, but there is a color for each one of the bandits. 
This is an example of an **associative search task**, so called because it involves both trial-and-error learning to *search* for the best actions, and association of these actions with the situations in which they are the best. Associative search tasks are intermediate between the k-armed bandit problem and the full reinforcement learning problem.

## Chapter 3 Finite Markov Decision Processes

MDPs are a classical formalization of sequential decision making. **MDPs involve delayed reward** and the need to tradeoff immediate and delayed reward. Whereas in bandit problems we estimated the value $q_*(a)$ of each action $a$, **in MDPs we estimate the value $q_*(s,a)$** of each action $a$ in each state $s$, or we estimate the **value $v_*(s)$ of each state given optimal action selections**


### 3.1 The Agent-Enviroment Interface

The learner and decision maker is called *agent*. The thing it interacts with, comprising everything outside the agent, is called the *environment*.

In a *finite* MDP, the sets of states, actions, and rewards ($S, A,\text{and } R$ ) all have a finite number of elements. For particular values of these random variables, $s' \isin S$ and $r \isin R$, there is a probability of thoso values occurring at time $t$, given particular values of the preceding state and action:

**$$
p(s',r|s,a) = Pr(S_t = s', R_t = r | S_{t-1} = s, A_{t-1} = a)$$**

The state must include information about all aspects of the past agent-environment interaction that make a difference for the future. If it does, then the state is said to have the **Markov property**.

We can as well compute the *state-transition probabilities*:

**$$
p(s'|s,a) = Pr(S_t = s' | S_{t-1} = s, A_{t-1}) = \sum_{r \isin R}p(s',r|s,a)$$**

We can also compute the expected rewards for state-action pairs as a two-argument function r:

**$$
r(s,a) = E[R_t|S_{t-1}=s , A_{t-1} = a] = \sum_{r \isin R}r\sum_{s' \isin S}p(s',r | s,a)$$**

and the expected rewards for state-action-next-state triples as a three-argument function:

**$$
r(s,a,s') = \sum_{r \isin R}r\frac{p(s',r|s,a)}{p(s'|s,a)}$$**


The general rule we follow is that **anything that cannot be changed arbitrarily by the agent is considered to be outside of it and thus part of its environment**.






















