- **Definições de Matriz**
    - a) **Positiva semi-definida:**  $A \geq 0  \text{ se } x^\top A x \geq 0 \quad \forall x \in \mathbb{R}^n$ **$\iff tr(A) \ge 0$** e **$det(A) \ge 0$**
    - b) **Positiva definida:**  $A > 0  \text{ se } x^\top A x > 0 \quad \forall x \in \mathbb{R}^n \setminus \{0\}$ **$\iff tr(A) \gt 0$** e **$det(A) \gt 0$**

    - c) **Negativa semi-definida:**  $A \leq 0 \text{ se } x^\top A x \leq 0 \quad \forall x \in \mathbb{R}^n$

    - d) **Negativa definida:**  $A < 0 \text{ se } x^\top A x < 0 \quad \forall x \in \mathbb{R}^n \setminus \{0\}$

    - e) **Indefinida:**  $A \text{ é indefinida se } \exists \text{ }x, y \in \mathbb{R}^n \text{ tais que } x^\top A x > 0 \text{ e } y^\top A y < 0$
- **Autovalores**
    - a) $A \ge  0 \iff \text{autovalores não-negativos}$
    - b) $A \gt  0 \iff \text{autovalores positivos}$
    - b) $A \text{ é indefinida}\iff \text{autovalores negativos e positivos}$

- **Pontos de Mínimos**
    - **Global:**  **$f(x^*) \le f(x)\text{ }\forall x \in C$** 
    - **Local:** 
        - **$\exist \text{ }r \gt 0 \text{ , } f(x^*) \lt f(x) \text{ , } \forall x \in C \cap B(x^*, r)$**
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
    - **Condição Necessária:** **$x^*$** é um ponto de mínimo local **$\Rightarrow \nabla f(x^*) = 0$** e **$\nabla^2 f(x^*) \ge 0$** (Hessiana Positiva Semi-Definida)
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

    - **Desigualdade de Jensen:** Seja **$f$** convexa num conjunto **$C$** convexo. **$\iff$**
        - Para quaisquer **$x_1, \dots, x_n \in C$** e quaisquer pesos **$\lambda_1, \dots, \lambda_n$** tais que **$\lambda_i \ge 0$** e **$\sum_{i=1}^{n}{\lambda_i} = 1$**, vale: **$f\left(\sum_{i=1}^{n}{\lambda_i x_i}\right) \le \sum_{i=1}^{n}{\lambda_i f(x_i)}$**
    
    - Somas de **$f_s$** convexas é convexa
    - **$f(Ax + b)$** é convexa se **$f$** é convexa
    - Se **$f$** é convexa e **$g$** é convexa **não decresente**, então **$g(f(x))$** é convexa
    - O "máximo" de funções convexas é convexa: **$f(x) = \max_i f_i(x)$** é convexo