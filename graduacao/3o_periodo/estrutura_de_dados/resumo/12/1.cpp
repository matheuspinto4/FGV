#include <iostream>

struct Node
{
    Node* next;
    int value;
};


struct Stack
{
    Node* next;
    int size;
};


Stack * initialize(int maxSize)
{
    Stack *s = new Stack;
    s->next = nullptr;
    s->size = 0;
    return s;    
}

void push(Stack *s, int value)
{
    Node *n = new Node;
    n->value = value;
    n->next = nullptr;
    s->size++;
    if (s->size == 0)
    {
        s->next = n;
    }
    else
    {
        n->next = s->next;
        s->next = n;
    }
}

void printStack(Stack *s)
{
    Node *temp = new Node;
    temp = s->next;
    while(temp != nullptr)
    {
        std::cout<<temp->value<<" ";
        temp = temp->next;
    }
    std::cout<<std::endl;
}


int main()
{
    Stack *s = initialize(10);
    push(s, 10);
    push(s,2);
    push(s,12);
    printStack(s);
    delete s;
    std::cout<<s->next->value;
    
    return 0;
}