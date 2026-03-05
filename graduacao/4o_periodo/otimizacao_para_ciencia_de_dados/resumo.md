- **Definições de Matriz**
    - a) **Positiva semi-definida:**  **$A \geq 0  \text{ se } x^\top A x \geq 0 \quad \forall x \in \mathbb{R}^n$** 
    - b) **Positiva definida:**  **$A > 0  \text{ se } x^\top A x > 0 \quad \forall x \in \mathbb{R}^n \setminus \{0\}$** 

    - c) **Negativa semi-definida:**  **$A \leq 0 \text{ se } x^\top A x \leq 0 \quad \forall x \in \mathbb{R}^n$**

    - d) **Negativa definida:** **$A < 0 \text{ se } x^\top A x < 0 \quad \forall x \in \mathbb{R}^n \setminus \{0\}$**

    - e) **Indefinida:**  **$A \text{ é indefinida se } \exists \text{ }x, y \in \mathbb{R}^n \text{ tais que } x^\top A x > 0 \text{ e } y^\top A y < 0$**
- **Autovalores**
    - a) **$A \ge  0 \iff \text{autovalores não-negativos}$**
    - b) **$A \gt  0 \iff \text{autovalores positivos}$**
    - c) **$A \text{ é indefinida}\iff \text{autovalores negativos e positivos}$**

- **Pontos de Mínimos**
    - **Global:**  **$f(x^*) \le f(x)\text{ }\forall x \in C$** 
    - **Local:** 
        - **$\exist \text{ }r \gt 0 \text{ , } f(x^*) \le f(x) \text{ , } \forall x \in C \cap B(x^*, r)$**
        - **$B(x^*, r) = \set{x \in \R^n : \| x - x^*\|_2 \le r}$**

- **Derivada Direcional**
    - Derivada direcional de **$f$** em **$x$** na direção **$d$**: **$
f'(x,d) = \lim_{t^+ \rightarrow 0^+} {\frac{f(x + td) - f(x)}{t}}$**

- **Gradiente**
    - **Propriedades**
    **$1. \text{  }f'(x,d) = \langle \nabla f(x), d\rangle = \nabla f(x)^Td \\  \\ 2. \text{ }f(y) \approx f(x) + \nabla f(x)^T(y-x) + O(\|y - x\|)$** 
- **Hessiana**
    - A função deve ser continuamente duas vezes diferênciável.
    - **$\nabla^2 f(x)_{i,j} = \frac{\partial^2 f}{\partial x_i \partial x_j}$**
    - Propiedades:
        - Para todo **$y \in B(x,r), \exist \text{ } \xi \in [x, y]: $**
            - **$f(y) = f(x) + \nabla f(x)^T (y-x) + \frac{1}{2} (y-x)^T \nabla^ 2 f(\xi )(y-x)$**
        - Para todo **$y \in B(x,r)$** vale 
            - **$f(y) \approx f(x) + \nabla f(x)^T(y-x) + \frac{1}{2}(y-x)^T\nabla^2f(x)(y-x) + O(\|y-x\|)$**

- **Direção de Descida:** **$d$** é uma direção de descida no ponto **$x$** se **$\left< d, \nabla f(x) \right> < 0$**

- **SubGradiente:** **$g_x$** é subgradiente de **$f$** em **$x$** se: **$f(y) \ge f(x) + \left< g_x, y - x \right>, \text{ } \forall y \in \R^n$**
    - **Conjunto dos subgradientes em $x$:** **$\partial f(x) = \set{g \in \R^n : f(y) \ge f(x) + \left< g, y - x \right>, \text{ } \forall y \in \R^n}$**
    - **Convexidade:** **$f$** convexa **$\iff$** **$\partial f(x) \neq \varnothing$**

- **Função Suave:** **$f$** é **$L$-suave** (**$L > 0$**): 
    - **$ \iff$** 
        - **$f \text{ é diferenciavel; e }$** 
        - **$||\nabla f(y) - \nabla f(x)||_2  | \le L||y - x||_2 \text{ , } \forall \text{ }y,x \in \R^n$**
    - **$\text{Consequência: } |f(y) - [f(x) + \left< \nabla f(x), y-x\right>] \le L||y - x||_2 \text{ , } \forall \text{ }y,x \in \R^n$**
    - Se **$f$** é $L$-suave e **$\alpha = \frac{\beta}{L} | \beta \in \left(0,2\right)$**. Então:
        - **$\min_{t \in T} ||\nabla f(x^t)||^2_2 \le \frac{1}{T}\sum_{t=1}^T{||\nabla f(x^t)||_2^2} \le (\frac{2 / \beta}{2 - \beta})\frac{L(f(x^t) - f^*)}{T}$**

---

- **Função M-Lipschitz contínua:** 
    - **$|f(y) - f(x)| \le M ||y - x||_2 \text{ }\forall y, x \in \R^n $**
    - **$|f(y) - [f(x) + \left< g_x, y-x\right>] | \le M||y - x||_2 \text{ , } \forall \text{ }y,x \in \R^n$**
    - **$\iff ||g_x||_2 \le M, \forall g_x \in \R^n$**

- **Operador Proximal $prox_g(x):=$** **$\argmin_{y \R^n} \set{g(y) + \frac{1}{2} {||y - x||_2^2}}$**

- **Norma Preconizada:** **$||x||_A := \sqrt{\left<x, Ax \right>} $**

- **Número de Condição $\kappa$:**  **$\frac{\lambda_{maior}}{\lambda_{menor}}$** 
    - **$\kappa \approx 1$** (Ideal)  
    - **$\kappa >> 1$** (Convergência lenta, oscilatória e difícil)  

- **Projeção Ortogonal:** 
    - **$\sqcap_{x \in C}[y]$:** projeção ortogonal x de y no conjunto C
    - **Hiperplano: $H:= \set{a^Tx = b }\Rightarrow$** **$\sqcap_{x \in H}[y] = y - \frac{a^Ty - b}{||a||_2^2}a$**
    - **Semi-espaço: $C:= \set{a^Tx \le b }\Rightarrow$** **$\sqcap_{x \in C}[y] = y - \frac{\max{\set{0, a^Ty - b}}}{||a||_2^2}a$**
    


- **Condições de Otimalidade de Primeira Ordem:**
    - **Condição Necessária:** **$x^*$** é um ótimo local **$\Rightarrow \nabla f(x^*) = 0$** (Ponto Estacionário)
- **Condições de Otimalidade de Segunda Ordem:**
    - **Condição Necessária:** **$x^*$** é um ponto de mínimo local e **$f$** é **$C^2$** **$\Rightarrow \nabla f(x^*) = 0$** e **$\nabla^2 f(x^*) \ge 0$** (Hessiana Positiva Semi-Definida)
    - **Condição Suficiente:** **$\nabla f(x^*) = 0$** e **$\nabla^2 f(x^*) > 0 \Rightarrow x^*$** é um ponto de mínimo local **estrito** (Hessiana Positiva Definida)

- **Condição Suficiente para Solução Global:**
    - Se **$\nabla^2 f(x) \ge 0 \text{ } \forall x\in\R^n$**. Então: **$x^*$ é estacionário $\Rightarrow$ **$x^*$** é ponto de mínimo global**

- **Ponto de Sela:**
    - **$\nabla f(x^*) = 0$** e **$\nabla^2f(x^*)$** é indefinida


- **Existência de Pontos Ótimos**
    - **Teorema de Weierstrass:**- Seja **$f$** uma função **contínua** sobre um conjunto **$U$** **compacto** (fechado/limitado). Então **$f$** tem ponto de mínimo e máximo globais em **$U$**
    - Se **$f$** é **contínua** e **coerciva**, então **$f$** tem um ponto de mínimo global.
        - **Coercividade:** **$\lim_{\|x\| \rightarrow \infty}f(x) = \infty$**

- **Funções Quadráticas**
    - **$f(x) = x^TAx + 2b^Tx + c$** , onde $A$ é matriz, $b$ é vetor e $c$ é escalar
    - **$\nabla f(x) = 2Ax + 2b$** e **$\nabla^2f(x) = 2A$**  
    - **$A \ge 0:$** $x$ é ponto de mínimo global $\iff Ax = -b$
    - **$A \gt 0:$** $x = -A^{-1}b$ é o único mínimo global

---
---
---

- **Otimização Convexa**
    - **Conjunto Convexo:** **$C$** é convexo **$\iff \forall \text{ } x, y \in C$** temos **$\lambda x + (1 - \lambda)y \in C\text{ }$**  **$\forall \text{ }\lambda \in [0, 1]$**
    - **Função Convexa:** 
        - **$f$** convexa se: **$f(\lambda x + (1 - \lambda)y) \le \lambda f(x) + (1 - \lambda)f(y)$**  **$\forall \text{ } x,y \in C$**  
        - **Condição de Primeira Ordem:** **$f$** é convexa **$\iff$** **$\text{ } f(y) \ge f(x) + \left<\nabla f(x), y - x\right>\text{ }\forall \text{ } x,y\in C$**
        - **Condição de Segunda Ordem:** **$f \text{ é} \text{ convexa} \iff \nabla^2f(x)\ge 0 \text{ } \forall \text{ }x \in C$**
        - **Convexidade Forte:** **$\nabla^2 f(x) > m \text{ , Para algum } m \gt 0$**
        - **Quadrática:** Se **$A$** é simétrica e **$f(x) = x^TAx + 2b^Tx +c$**, então **$f { é }\text{ convexa } \iff A \ge 0 $**

    - **Desigualdade de Jensen:** Seja **$f$** convexa num conjunto **$C$** convexo, então:
        - Para quaisquer **$x_1, \dots, x_n \in C$** e quaisquer pesos **$\lambda_1, \dots, \lambda_n$** tais que **$\lambda_i \ge 0$** e **$\sum_{i=1}^{n}{\lambda_i} = 1$**, vale: **$f\left(\sum_{i=1}^{n}{\lambda_i x_i}\right) \le \sum_{i=1}^{n}{\lambda_i f(x_i)}$**

    - Seja **$f \text{ não }\text{convexa}: C \rightarrow \R$** então **$x^*$** min local **$\Rightarrow \left<\nabla f(x), x - x^*\right> \ge 0 \text{ } \forall \text{ } x \in C$** 
    - Seja **$f \text{convexa}: C \rightarrow \R$** então **$x^*$** min local **$\iff \left<\nabla f(x), x - x^*\right> \ge 0 \text{ } \forall \text{ } x \in C$** 
    - **Propriedades:**
        - Somas de **$f_s$** convexas é convexa
        - **$f(Ax + b)$** é convexa se **$f$** é convexa
        - Se **$f$** é convexa e **$g$** é convexa **não decresente**, então **$g(f(x))$** é convexa
        - O "máximo" de funções convexas é convexa: **$f(x) = \max_i f_i(x)$** é convexo

- **Otimização com Restrições Lineares**
    - **Condições KKT:**  Condições que devem ser atendidas para haver otimilidade
        - **$minimize_x \text{ } f(x)$** sujeito à:
            - **$a_i^Tx \le b_i, i= [1..m]$**
            -  **$c_j^Tx = d_j, j=[1..p]$**
        - **a)** Se **$x^*$** é mínimo local, então existem **$\lambda_1,.., \lambda_m \ge 0$** e **$\mu_1, \mu_p \in \R$** tais que:
            - **$\nabla f(x^*) + \sum_{i=1}^m{\lambda_i a_i} + \sum_{j=1}^p{\mu_j c_j} = 0$**
            - **$\lambda_i(a_i^Tx^* - b_i) = 0 \text{ | } i = [1..m]$** 
            - **$a_i^Tx^* - b_i \le 0\text{ |  } i = [1..m]$**
            - **$c_j^Tx^* - d_j = 0\text{ | } j = [1..p]$**
        - **b)** Se **$f$** convexa, então **$x^*$** é sol. glob. **$\iff \exist \text{ }\lambda_1,.., \lambda_m \ge 0$** e **$\mu_1, \mu_p \in \R$** satisfazendo KKT

- **Langrangeano e KKT Geral**
    - **$minimize_x \text{ } f(x)$** sujeito à:
        - **$g_i(x) \le 0, i= [1..m]$**
        -  **$h_j(x) = 0, j=[1..p]$**
    - **Lagrangeano:** **$L(x, \lambda, \mu) := f(x) + \lambda^Tg(x) + \mu^Th(x)$**
    - **$L(x, \lambda, \mu) := f(x) + \sum_{i=1}^m\lambda_ig_i(x) + \sum_{j=1}^p\mu_jh_j(x)$**
    - **Gradiente do Lagrangeano:** **$\nabla_xL(x, \lambda, \mu) := \nabla f(x) + \sum_{i=1}^m\lambda_i\nabla g_i(x) + \sum_{j=1}^p\mu_j\nabla h_j(x)$**
    - **Condição KKT (Geral):** Se **$x^*$** é um mínimo local e **LICQ** é satisfeita em **$x^*$**, então **$\exist \lambda \ge 0, \mu \in \R$** tal que:
        - **1. Estacionariedade:** **$\nabla_xL(x^*, \lambda, \mu)= 0$**
        - **2. Viabilidade Primal:** **$g_i(x^*) \le 0$** ,  **$h_j(x^*) = 0$**
        - **3. Multiplicadores:** **$\lambda_i \ge 0$**
        - **4. Complementaridade:** **$\lambda_i g_i(x^*) = 0$**

- **LICQ:**(Condição de Qualificação de Independência Linear) 
    - Determina quais pontos são regulares (i.e., onde as Condições KKT podem ser aplicadas).
    - Seja **$I(x^*) := \set{i \in [m]:g_i(x^*) = 0}$** o conjunto de restrições ativas em **$x^*$**. 
    - A LICQ é satisfeita em **$x^*$** se o conjunto dos gradientes das restrições ativas é linearmente independente:
        - **$\set{\nabla g_i(x^*):i \in I(x^*)}\cup\set{\nabla h_j(x^*): j \in [p]}$**

- **Condições KKT: problema convexo**
    - As condições KKT em um problema convexo são **suficientes** para o ponto ser um mínimo.
 
- **Condição de Slater em Convexos:**
    - Garante a existência de de multiplicadores de lagrange ($\lambda$)
    - Sejam **$g_i$** funções convexas em **$\R^n$** e **$h_J$** e **$s_q$** funcões afins. Dizemos que a condição de Slater generalizada é satisfeita para as funções **$\set{g_i }^m_{ i=1} \cup \set{h_j }^p_{ j=1} \cup \set{s_k }^q_{ k=1}$** se existe **$\hat x \in Rn$** tal que
        - **$g_i (\hat x) < 0, i = [1 ..  m]$** não-afins
        - **$h_j (\hat x) ≤ 0, j = [1 ..  p]$** afim
        - **$s_k (\hat x) = 0, k = [1 ..  q]$** afim

- **Método do Gradiente:** 
    - **GD (batch)** usa um lote do conjunto para dar um passo, já o **SGD (estocástico)** dá um passo a cada dado, o que faz dele mais instável e oscilatório, porém é mais barato computacionalmente.
    - **$x^{t+1} = x^t - \alpha \nabla f(x^t)$**
    - **$f$** **suave**: **$f(x^{t + 1}) \le f(x^t) - \alpha (1 - \frac{\alpha L}{2}) ||\nabla f(x^t)||^2$**
    
    - **$f$ suave e convexo:**
        - se **$\alpha \in (0, 2/L)$**, então: **$||x^{t + 1} - x^*||_2^2 \le ||x^t - x^*||_2^2 - \alpha \left( 2 - \frac{1}{ 1 - (\alpha L / 2)}(f(x^t) - f^*) \right)$**
        - **$\alpha = \beta / L : \beta \in (0, 1) $**, então: **$f(x^T) - f^* \le \frac{1}{T} \sum^T_{t=1}{(f(x^t) - f^*)} \le \left( \frac{\beta^{-1} - 1/2}{ 1 - \beta}\right)\frac{L ||x^1 - x^*||_2^2}{T}$**


- **Método do SubGradiente:** 
    - Não é um método de descida, só garante que a distância até o ótimo diminui
    - **Normal:**
        - **$x^{t+1} = x^{t} - \alpha _t g^t : g^t \in \partial f(x^t)$**.  **Return** **$\bar{x}^t = \sum_{t = 1}^T{\frac{\alpha _ t}{ \sum_{l = 1}^{T}}}x^t$**
        
        
        
        - **$||x^{t+1} - x^*||_2^2 \le ||x^t - x^*||_2^2 - \alpha_t (f(x^t) - f^*) + M^2 \alpha_t^2$**
        
        -  **$f(x^T) - f^* \le \frac{1}{T} \sum^T_{t=1}{(f(x^t) - f^*)} \le \frac{||x^1 - x^*||_2^2 + M^2 \sum_{t=1}^T \alpha_t^2}{\sum_{t=1}^t{\alpha_t}}$**
        

    - **Projetado (Para Restrições):**  
        - **$x \in C \Rightarrow x^{t + 1} = \sqcap_{x \in C}[x^t - \alpha_tg^t]$**

    - **Proximal (Para Regularização):**
        - Minimizar **$f(x) + g(x)$**: $f$ suave e $g$ não suave
        - Dois passos:
            - **$\bar{x}^{t} = \argmin_{x \in \R^n} \set{f(x^t) + \left< g^t, x - x^t\right> + \frac{1}{2 \alpha_t} ||x - x^t||_2^2} = x^t - \alpha_t g^t $**
            - **$x^{t + 1} = \argmin_{x\in\R^n} ||g(x) - (x^t - \alpha_tg^t)||_2^2 = prox_{\alpha_tg(\bar{x}^t)}$**


- **Método de Newton:** 
    - Apresenta uma convergência local e custa caro por iteração. Porém converge mais rapidamente que o GD.
    - **$x^{t + 1} := x^t - \left[\nabla^2 f(x^t) \right]^{-1} \nabla f(x^t)\text{ .Return  } x^T$** 

    - **${x}^{t + 1} = \argmin_{x \in \R^n} \set{f(x^t) + \left< \nabla f(x^t), x - x^t\right> + \frac{1}{2} ||x - x^t||_{\nabla^2 f(x^t)}^2}$**

    - **$x^{t + 1} = \argmin_{x\in\R^n} ||x - (\nabla f(x^t))||_{\nabla^2 f(x^t)}^2$**

<!-- - **Problema Dual:** Seja **$f^*$** a solução de um problema de otimização e **$L(x, \lambda, \mu)$** o seu lagrangeano. A função objetivo dual **$q(\lambda, \mu) = \min_{x \in C} L(x, \lambda, \mu)$**
    - **Domínio:** **$dom(q) := \set{(\lambda, \mu) \in \R^m \times \R^p : q(\lambda, \mu) \gt - \infty}$**
    - **Problema Dual:** **$q^* := \max_{(\lambda, \mu)}q(\lambda, \mu); \text{ s.t. } (\lambda, \mu) \in dom(q)$**
    - **Dualidade Fraca:** **$q^* \le f^*$**
    - **Dualidade Forte:** **$q^* = f^*$**
    - **Problema Convexo:** garante a dualidade forte.
     -->