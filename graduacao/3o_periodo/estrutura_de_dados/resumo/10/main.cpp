#include <iostream>


struct Stack
{
    char * data;
    int maxSize;
    int top;
};

Stack* initialize(int maxSize)
{
    Stack *s = new Stack;
    s->data = new char[maxSize];
    s->maxSize = maxSize;
    s->top = -1;
    
    return s;
}

int push(Stack* s, char value)
{
    if (s->top == s->maxSize - 1)
    {
        return 0;
    }
    s->top++;
    s->data[s->top] = value;
    return 1; 
}

void printStack(Stack* s)
{
    for(int i = s->top; i >= 0; i--)
    {
        std::cout<<s->data[i]<<" ";
    }
    std::cout<<std::endl;
}

Stack* invertStack(Stack *s)
{
    Stack *s2 = initialize(s->maxSize);
    for(int i = s->top; i >= 0; i--)
    {
        push(s2, s->data[i]);
    }
    return s2;
}

int main()
{
    Stack *s = initialize(3);
    push(s,'a');
    push(s,'b');
    push(s,'c');
    printStack(s);
    Stack *s2 = invertStack(s);
    printStack(s2);

    return 0;
}