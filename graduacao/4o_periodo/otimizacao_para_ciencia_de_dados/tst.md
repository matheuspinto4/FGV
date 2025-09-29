- **Definições de Matriz**
    - a) **Positiva semi-definida**  
    $A \geq 0 \quad \text{se} \quad x^\top A x \geq 0 \quad \forall x \in \mathbb{R}^n$

    - b) **Positiva definida**  
    $A > 0 \quad \text{se} \quad x^\top A x > 0 \quad \forall x \in \mathbb{R}^n \setminus \{0\}$

    - c) **Negativa semi-definida**  
    $A \leq 0 \quad \text{se} \quad x^\top A x \leq 0 \quad \forall x \in \mathbb{R}^n$

    - d) **Negativa definida**  
    $A < 0 \quad \text{se} \quad x^\top A x < 0 \quad \forall x \in \mathbb{R}^n \setminus \{0\}$

    - e) **Indefinida**  
    $A \text{ é indefinida se } \exists x, y \in \mathbb{R}^n \text{ tais que } x^\top A x > 0 \text{ e } y^\top A y < 0$
---
- **Autovalores (para Matrizes Simétricas)**
    - a) $A \ge  0 \iff \text{autovalores não-negativos} \quad (\lambda_i \ge 0 \quad \forall i)$
    - b) $A \gt  0 \iff \text{autovalores positivos} \quad (\lambda_i > 0 \quad \forall i)$
    - c) $A \le  0 \iff \text{autovalores não-positivos} \quad (\lambda_i \le 0 \quad \forall i)$
    - d) $A <  0 \iff \text{autovalores negativos} \quad (\lambda_i < 0 \quad \forall i)$
    - e) $A \text{ é indefinida}\iff \text{autovalores negativos e positivos} \quad (\exists \lambda_i < 0 \text{ e } \exists \lambda_j > 0)$
---
- **Pontos de Mínimos**
    - **Global:**  **$f(x^*) \le f(x)\text{ }\forall x \in C$**     - **Local Estrito:**         - **$\exist \text{ }r \gt 0 \text{ , } f(x^*) \lt f(x) \text{ , } \forall x \in C \cap B(x^*, r) \setminus \{x^*\}$**
    - **Local:**         - **$\exist \text{ }r \gt 0 \text{ , } f(x^*) \le f(x) \text{ , } \forall x \in C \cap B(x^*, r)$**
        - **$B(x^*, r) = \set{x \in \R^n : \| x - x^*\|_2 \le r}$**
---
- **Derivada Direcional**
    - Derivada direcional de **$f$** em **$x$** na direção **$d$**:
**$
f'(x,d) = \lim_{t \rightarrow 0^+} {\frac{f(x + td) - f(x)}{t}}$**
---
- **Gradiente**
    - **Propriedades**
    **$1. \text{  }f'(x,d) = \langle \nabla f(x), d\rangle = \nabla f(x)^Td \\  \\ 2. \text{ }f(y) \approx f(x) + \nabla f(x)^T(y-x) + O(\|y - x\|)$** ---
- **Hessiana**
    - A função deve ser continuamente duas vezes diferênciável (e simétrica pelo Teorema de Schwarz).
    - **$
\nabla^2 f(x) =
\begin{bmatrix}
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \\
\frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots & \frac{\partial^2 f}{\partial x_2 \partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial^2 f}{\partial x_n \partial x_1} & \frac{\partial^2 f}{\partial x_n \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_n^2}
\end{bmatrix}
$**
    - **Condição de Segunda Ordem para o Mínimo (caso univariado):**
        - $x^*$ é ponto de mínimo local $\Rightarrow f''(x^*) \ge 0$
    - Propriedades:
        - Para todo **$y \in B(x,r), \exist \text{ } \xi \in [x, y]: $** (Fórmula de Taylor de 2ª Ordem com Resto)
            - **$f(y) = f(x) + \nabla f(x)^T (y-x) + \frac{1}{2} (y-x)^T \nabla^ 2 f(\xi )(y-x)$**
        - Para todo **$y \in B(x,r)$** vale (Aproximação Quadrática de Taylor)
            - **$f(y) \approx f(x) + \nabla f(x)^T(y-x) + \frac{1}{2}(y-x)^T\nabla^2f(x)(y-x) + O(\|y-x\|^2)$**
---
- **Condições de Otimalidade de Primeira Ordem:**
    - **Condição Necessária:** $x^*$ é um ótimo local **$\Rightarrow \nabla f(x^*) = 0$** (Ponto Estacionário)
---
- **Condições de Otimalidade de Segunda Ordem:**
    - **Condição Necessária:** $x^*$ é um ponto de mínimo local $\Rightarrow \nabla f(x^*) = 0$ e $\nabla^2 f(x^*) \ge 0$ (Hessiana Positiva Semi-Definida)
    - **Condição Suficiente:** $\nabla f(x^*) = 0$ e $\nabla^2 f(x^*) > 0 \Rightarrow x^*$ é um ponto de mínimo local **estrito** (Hessiana Positiva Definida)