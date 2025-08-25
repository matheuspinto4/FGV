#include <iostream>




struct CircularQueue
{
    int *data;
    int maxSize;
    int size;
    int head;
    int tail;
};


CircularQueue * initi(int maxSize)
{
    CircularQueue *c = new CircularQueue;
    c->data = new int[maxSize];
    c->maxSize = maxSize;
    c->head = 0;
    c->tail = -1;
    c->size = 0;
    return c;
}

int enqueue(CircularQueue *c, int e)
{
    if (c->size == c->maxSize)
    {
        return 0;
    }
    c->tail = (c->tail + 1) % c->maxSize;
    c->data[c->tail] = value;
    c->size++;
    return 1;
}


int dequeue(CircularQueue *c, int *value)
{
    if (c->size == 0)
    {
        return 0;
    }
    *value = c->data[c->head];
    c->head = (c->head + 1) % c->maxSize;
    c->size--;
    return 1;
}


int buscar(CircularQueue *c, int value)
{
    if (c->size == 0)
    {
        return 0;
    }
    for (int i = c->head;i != c->tail; i = (i + 1)%c->maxSize)
    {
        if (c->data[i] == value) return 1;
    }
    return 0;
    
}



int main()
{
    CircularQueue *c = initi(5);
    enqueue(c, 10);
    enqueue(c, 3);
    enqueue(c, 5);
    if (buscar(c, 7) == 1)
    {
        std::cout<<" achou"<<std::endl;
    }
    else
    {
        std::cout<<"nao achou\n";
    }

    return 0;
}