#include <iostream>

#include "modulo2.h"

using namespace std;


struct Node
{
    Node* next;
    int value;
};

struct Queue
{
    Node* next;
    int size;
};


Queue * init()
{
    Queue *q = new Queue;
    q->next = nullptr;
    q->size = 0;
    return q;
}

void push(Queue *q, int value)
{
    Node *n = new Node;
    n->value = value;
    n->next = nullptr;
    if(q->size == 0)
    {
        q->next = n;
    }
    else
    {
        Node *temp = new Node;
        temp = q->next;
        for (int i = 0; i < q->size - 1; i++)
        {
            temp = temp->next;
        }
        temp->next = n;
    }
    q->size++;
}

void printQueue(Queue *q)
{
    Node *temp = new Node;
    temp = q->next;
    while(temp != nullptr)
    {
        std::cout<<temp->value<<" ";
        temp = temp->next;
    }
    std::cout<<std::endl;
}


int peek(Queue *q, int *value)
{
   if (q->size == 0)
   {
        return 0;
   } 
   *value = q->next->value;
   return 1;
}


int dequeue(Queue *q, int *value)
{
    if (peek(q, value) == 0)
    {
        return 0;
    }
    Node *temp = new Node;
    temp = q->next;
    q->next = q->next->next;
    delete temp;
    q->size--;
    return 1;
}



int main()
{
    Queue *q = init();
    push(q, 10);
    push(q, 1234);
    push(q, 12343);
    printQueue(q);

    int a;
    dequeue(q,&a);
    std::cout<<a<<"\n";
    printQueue(q);
UVgq5606
    return 0;
}