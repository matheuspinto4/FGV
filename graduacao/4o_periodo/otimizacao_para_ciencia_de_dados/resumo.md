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
    - **$
\nabla^2 f(x) =
\begin{bmatrix}
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \\
\frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots & \frac{\partial^2 f}{\partial x_2 \partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial^2 f}{\partial x_n \partial x_1} & \frac{\partial^2 f}{\partial x_n \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_n^2}
\end{bmatrix}
$**
    - Propiedades:
        - Para todo **$y \in B(x,r), \exist \text{ } \xi \in [x, y]: $**
            - **$f(y) = f(x) + \nabla f(x)^T (y-x) + \frac{1}{2} (y-x)^T \nabla^ 2 f(\xi )(y-x)$**
        - Para todo **$y \in B(x,r)$** vale 
            - **$f(y) \approx f(x) + \nabla f(x)^T(y-x) + \frac{1}{2}(y-x)^T\nabla^2f(x)(y-x) + O(\|y-x\|)$**

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

- **Otimização Convexa**
    - **Conjunto Convexo:** **$C$** é convexo **$\iff \forall \text{ } x, y \in C$** temos **$\lambda x + (1 - \lambda)y \in C\text{ }$**  **$\forall \text{ }\lambda \in [0, 1]$**
    - **Função Convexa:** **$f$** convexa se: **$f(\lambda x + (1 - \lambda)y) \le \lambda f(x) + (1 - \lambda)f(y)$**  **$\forall \text{ } x,y \in C$**  

    - **Desigualdade de Jensen:** Seja **$f$** convexa num conjunto **$C$** convexo, então:
        - Para quaisquer **$x_1, \dots, x_n \in C$** e quaisquer pesos **$\lambda_1, \dots, \lambda_n$** tais que **$\lambda_i \ge 0$** e **$\sum_{i=1}^{n}{\lambda_i} = 1$**, vale: **$f\left(\sum_{i=1}^{n}{\lambda_i x_i}\right) \le \sum_{i=1}^{n}{\lambda_i f(x_i)}$**
    - **Condição de Primeira Ordem:** **$f$** é convexa **$\iff$** **$\text{ } f(y) \ge f(x) + \left<\nabla f(x), y - x\right>\text{ }\forall \text{ } x,y\in C$**

    - **Quadrática:** Se **$A$** é simétrica e **$f(x) = x^TAx + 2b^Tx +c$**, então **$f { é }\text{ convexa } \iff A \ge 0 $**
    - **Condição de Segunda Ordem:** **$f \text{ é} \text{ convexa} \iff \nabla^2f(x)\ge 0 \text{ } \forall \text{ }x \in C$**
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
        - **b)** Se **$f$** é convexa, então **$x^*$** é solução global **$\iff$** 
            -  **$\exist \text{ }\lambda_1,.., \lambda_m \ge 0$** e **$\mu_1, \mu_p \in \R$** satisfazendo as condições acima
---
- **Langrangeano e KKT Geral**
    - Um problema geral tem a seguinte forma:
        - **$minimize_x \text{ } f(x)$** sujeito à:
        - **$g_i(x) \le 0, i= [1..m]$**
        -  **$h_j(x) = 0, j=[1..p]$**
    - **Lagrangeano:** **$L(x, \lambda, \mu) := f(x) + \lambda^Tg(x) + \mu^Th(x)$**
    - **$L(x, \lambda, \mu) := f(x) + \sum_{i=1}^m\lambda_ig_i(x) + \sum_{j=1}^p\mu_jh_j(x)$**
    - **Gradiente do Lagrangeano:** **$\nabla_xL(x, \lambda, \mu) := \nabla f(x) + \sum_{i=1}^m\lambda_i\nabla g_i(x) + \sum_{j=1}^p\mu_j\nabla h_j(x)$**
    - **Condição KKT (Geral):** Se **$x^*$** é um mínimo local e **LICQ** é satisfeita em **$x^*$**, então **$\exist \lambda \ge 0, \mu \in \R$** tal que:
        - **1. Estacionariedade:** 
            - **$\nabla_xL(x^*, \lambda, \mu)= 0$**
        - **2. Viabilidade Primal:** 
            - **$g_i(x^*) \le 0$**
            -  **$h_j(x^*) = 0$**
        - **3. Multiplicadores:** 
            - **$\lambda_i \ge 0$**
        - **4. Complementaridade:** 
            - **$\lambda_i g_i(x^*) = 0$**

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
        


