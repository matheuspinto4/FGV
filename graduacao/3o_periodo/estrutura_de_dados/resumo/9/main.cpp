#include <iostream>

struct Stack 
{
    int * data; // Array com os elementos
    int maxSize; // Tamanho máximo da pilha
    int top; // Indice do topo atual na pilha
};


Stack* initialization(int maxSize)
{
    Stack *s = new Stack;
    s->maxSize = maxSize;
    s->data = new int[s->maxSize];
    s->top = -1;
    return s;
}

void destroy(Stack* s)
{
    delete[] s->data;
    delete s;
}

int push(Stack *s, int value)
{
    if (s->top == s->maxSize -1)
    {
        return 0; // Full stack
    }
    s->top += 1;
    s->data[s->top] = value;
    return 1;
}

int peek(Stack *s, int *value)
{
    if (s->top == -1)
    {
        return 0; // Não há elementos na fila
    }
    *value = s->data[s->top];
    return 1;
}

int main()
{
    Stack *s = initialization(5);
    
    push(s, 3);
    int v;

    if (peek(s, &v) == 0)
    {
        std::cout<<"Fila vazia\n";
    }
    else
    {
        std::cout<<v<<"\n";
    }

    return 0;
}