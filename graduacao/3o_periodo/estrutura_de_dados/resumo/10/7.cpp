#include <iostream>


struct CircularQueue
{
    int *data;
    int maxSize;
    int size;
    int head;
    int tail;
};

CircularQueue * initialization(int maxSize)
{
    CircularQueue *q = new CircularQueue;
    q->data = new int[maxSize];
    q->head = 0;
    q->tail = -1;
    q->size = 0;
    return q;
}

int enqueue(CircularQueue *q, int value)
{
    if (q->size == q->maxSize)
    {
        return 0;
    }
    q->tail = (q->tail + 1) % q->maxSize;
    q->data[q->tail] = value;
    q->size++;
    return 1;
}

int dequeue(CircularQueue *q, int *value)
{
    if (q->size == 0)
    {
        return 0;
    }
    *value = q->data[q->head];
    q->head = (q->head + 1) % q->maxSize;
    q->size--;
    return 1;
}


int buscar(CircularQueue *c, int value)
{
    
}


int main()
{

    
    return 0;
}



