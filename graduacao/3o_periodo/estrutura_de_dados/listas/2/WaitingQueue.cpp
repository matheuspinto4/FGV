#include "WaitingQueue.h"

namespace WaitingQueueTAD{

    WaitingQueue* createQueue()
    { 
        WaitingQueue * queue = (WaitingQueue *)malloc(sizeof(WaitingQueue));
        if (queue == nullptr)
        {
            std::cerr<<"Falha ao tentar alocar memória para a fila";
            return nullptr;
        }

        queue->generalCount = 0;
        queue->elderlyCount = 0;
        queue->elderlyinSequenceCount = 0;
        queue->general = nullptr;
        queue->elderly = nullptr;
        queue->generalTail = nullptr;
        queue->elderlyTail = nullptr;

        return queue;
    }

    QueueNode * createNode(Client client)
    {
        QueueNode* newNode = (QueueNode*)malloc(sizeof(QueueNode));
        if (newNode == nullptr)
        {
            std::cerr<<"Falha ao alocar memória para um nó de um cliente";
            return nullptr;
        }
        newNode->client = client;
        newNode->next = nullptr;
        newNode->previous = nullptr;
        return newNode;
    }

    void enqueue(WaitingQueue* queue, Client client)
    {
        if (queue == nullptr)
        {
            std::cerr<<"Ponteiro para fila passada é nula";
            return;
        }
        QueueNode *newNode = createNode(client);

        if (client.priority == 0) // Geral
        {
            if(queue->generalCount == 0) // Caso onde não há ninguém na fila
            {
                queue->general = newNode; // O novo client passa a ser o primeiro da fila
                queue->generalTail = newNode; // O novo cliente também vai para o rabo da fila
            }
            else // Caso onde já há pessoas na fila
            {
                queue->generalTail->next = newNode; // O último da fila passa a apontar o novo cliente como próximo
                newNode->previous = queue->generalTail;// O novo client passa a apontar como o último da fila como anterior
                queue->generalTail = newNode;// O rabo da fila passa a ser o novo client
            }
            queue->generalCount++;
        }
        else // Idoso
        { 
            if(queue->elderlyCount == 0) // Caso onde não há ninguém na fila
            {
                queue->elderly = newNode; // O novo client passa a ser o primeiro da fila
                queue->elderlyTail = newNode; // O novo cliente também vai para o rabo da fila
            }
            else // Caso onde já há pessoas na fila
            {
                queue->elderlyTail->next = newNode; // O último da fila passa a apontar o novo cliente como próximo
                newNode->previous = queue->elderlyTail;// O novo client passa a apontar como o último da fila como anterior
                queue->elderlyTail = newNode;// O rabo da fila passa a ser o novo client
            }
            queue->elderlyCount++;
        }
    }


    int peek(const WaitingQueue* queue, Client* returnClient)
    {
        if (queue == nullptr)
        {
            std::cerr<<"Ponteiro para fila passada é nula";
            return 0;
        }

        if (queue->elderlyCount == 0 && queue->generalCount == 0) // Caso onde as filas estão vazias 
        {
            return 0;
        }  

        if (queue->elderlyinSequenceCount >= 2) // Já foram passados dois velhos em seguida
        {
            if (queue->generalCount == 0) // A fila de gerais está vazia 
            {
                *returnClient = queue->elderly->client; // Retorna um velho
            }
            else // Caso a fila normal não esteja vazia 
            {
                *returnClient = queue->general->client; // Pega-se o primeiro da fila geral
            }
            return 1;

        }
        else // Caso ainda não tenhamos dois velhos em sequência
        {
            if (queue->elderlyCount == 0) // A fila de velhos está vazia
            {
                *returnClient = queue->general->client; // Retorna um da fila geral
            }
            else
            {
                *returnClient = queue->elderly->client; // Pega-se o primeiro velho da fila de velhos
            }
            return 1;
        }
        return 0;
    }


    int dequeue(WaitingQueue* queue, Client* returnClient)
    {
        if (queue == nullptr)
        {
            std::cerr<<"Ponteiro para fila passada é nula";
            return 0;
        }
        if (peek(queue, returnClient) == 0) // Verificar se é possível retirar alguém, caso seja, já guarda o próximo cliente
        {
            return 0;
        }

        if (returnClient->priority == 0) // Geral
        {
            QueueNode *temp = queue->general;
            if (queue->generalCount > 1) // Se ainda sobrou alguém na fila de normais
            {
                queue->general = queue->general->next; // Passar ele para o início
                queue->general->previous = nullptr; // Não há mais anterior a ele na fila
            }
            else // não há mais ninguém na fila
            {
                queue->general = nullptr; // A cabeça da fila fica nullptr
                queue->generalTail = nullptr; // O rabo da fila fica nullptr
            }
            free(temp); // Libera a memória 
            queue->generalCount--; // Decrementa a quantidade de general
            queue->elderlyinSequenceCount = 0; // Reseta a sequencia de velhos em sequência
        }
        else // Velho
        {
            QueueNode *temp = queue->elderly;
            if (queue->elderlyCount > 1) // Se ainda sobrou alguém na fila de idosos
            {
                queue->elderly = queue->elderly->next; // Passar ele para o início
                queue->elderly->previous = nullptr; // Não há mais anterior a ele na fila
            }
            else // não há mais ninguém na fila
            {
                queue->elderly = nullptr; // A cabeça fica nullptr
                queue->elderlyTail = nullptr; // O rabo fica nullptr 
            }
            free(temp); // Libera a memória
            queue->elderlyCount--; // Decrementa a quantidade de idosos
            queue->elderlyinSequenceCount++; // Incrementa a sequência de idosos 
        }

        return 1;
    }


    int removeClient(WaitingQueue* queue, char* name)
    {   
        if (queue == nullptr)
        {
            std::cerr<<"Ponteiro para fila passada é nula";
            return 0;
        }

        
        QueueNode *tempElderly = queue->elderly;
        while (tempElderly != nullptr) // procurando na fila de idosos até ela acabar
        {
            if (strcmp(tempElderly->client.name, name) == 0)
            {
                if (tempElderly == queue->elderly) // Caso especial onde o nome é o primeiro da fila
                {
                    queue->elderly = tempElderly->next; // O proximo da fila passa a ser o primeiro 
                    if(queue->elderly != nullptr) 
                    {
                        queue->elderly->previous = nullptr; // O primeiro da fila agora tem como anterior um ponteiro nullptr
                    }
                }
                else
                {
                    tempElderly->previous->next = tempElderly->next; // O seu anterior pega o seu próximo
                    if(tempElderly == queue->elderlyTail) // Caso especial onde o nome é o último da fila
                    {
                        queue->elderlyTail = tempElderly->previous; // O seu anterior passa a ser o rabo da fila
                    }
                    else // Caso onde o nome está no meio da fila
                    {
                        tempElderly->next->previous = tempElderly->previous; // O próximo passa a ter como anterior o anterior do desistente
                    }
                } 
                free(tempElderly);
                queue->elderlyCount--;
                return 1;
            }
            tempElderly = tempElderly->next; // Passa para o próximo caso ainda não tenha achado 
        }
        
        QueueNode *tempGeneral = queue->general;
        while (tempGeneral != nullptr) // procurando na fila de idosos até ela acabar
        {
            if (strcmp(tempGeneral->client.name, name) == 0)
            {
                if (tempGeneral == queue->general) // Caso especial onde o nome é o primeiro da fila
                {
                    queue->general = tempGeneral->next; // O proximo da fila passa a ser o primeiro 
                    if(queue->general != nullptr) 
                    {
                        queue->general->previous = nullptr; // O primeiro da fila agora tem como anterior um ponteiro nullptr
                    }
                }
                else
                {
                    tempGeneral->previous->next = tempGeneral->next; // O seu anterior pega o seu próximo
                    if(tempGeneral == queue->generalTail) // Caso especial onde o nome é o último da fila
                    {
                        queue->generalTail = tempGeneral->previous; // O seu anterior passa a ser o rabo da fila
                    }
                    else // Caso onde o nome está no meio da fila
                    {
                        tempGeneral->next->previous = tempGeneral->previous;
                    }
                } 
                free(tempGeneral);
                queue->generalCount--;
                return 1;
            }
            tempGeneral = tempGeneral->next; // Passa para o próximo caso ainda não tenha achado 
        }
        
        return 0; // Cliente não encontrado 
    }

    Client* getQueueOrder(const WaitingQueue* queue, int* numClients)
    {
        if (queue == nullptr)
        {
            std::cerr<<"Ponteiro para fila passada é nula";
            return nullptr;
        }
        *numClients = queue->elderlyCount + queue->generalCount;
        if (*numClients == 0)
        {
            return nullptr;
        }

        Client *order = (Client *)malloc(*numClients * sizeof(Client)); // Alocando para a ordem de atendimento
        if (order == nullptr)
        {
            std::cerr<<"Falha ao alocar memória para a ordem dos clientes na fila";
            return nullptr;
        }
        QueueNode *currentElderly = queue->elderly; // Criando um nó de idoso auxiliar para percorrer
        QueueNode *currentGeneral = queue->general; // Criando um nó de geral auxiliar para percorrer
        int elderlyInSequence = queue->elderlyinSequenceCount; // Copiando o número de idosos atendidos em sequência
    
        for (int i = 0; i < *numClients; i++)
        {
            if (elderlyInSequence >= 2) // Caso onde dois idosos já foram escolhidos previamente
            {
                if (currentGeneral != nullptr) // Há um geral
                {
                    order[i] = currentGeneral->client;
                    currentGeneral = currentGeneral->next;
                    elderlyInSequence = 0;
                }
                else // Se não tiver gente na fila normal, então há na de idosos
                {
                    order[i] = currentElderly->client;
                    currentElderly = currentElderly->next;
                    elderlyInSequence++;
                }
            }
            else // Caso onde não foram passados dois idosos ainda
            {
                if (currentElderly != nullptr) // Há um idoso na fila
                {
                    order[i] = currentElderly->client;
                    currentElderly = currentElderly->next;
                    elderlyInSequence++;
                }
                else // Há alguém na fila normal
                {
                    order[i] = currentGeneral->client;
                    currentGeneral = currentGeneral->next;
                    elderlyInSequence = 0;
                }
            }
        }
        return order;
    }

    void deleteQueue(WaitingQueue* queue)
    {
        if (queue == nullptr)
        {
            std::cerr<<"Ponteiro para fila passada é nula";
            return;
        }
        QueueNode *currentGeneral = queue->general;
        while(currentGeneral != nullptr) // Apagando todos os gerais
        {
            QueueNode *temp = currentGeneral;
            currentGeneral = currentGeneral->next;
            free(temp);
        }
        QueueNode * currentElderly = queue->elderly;
        while(currentElderly != nullptr) // Apagando todos os idosos 
        {
            QueueNode *temp = currentElderly;
            currentElderly = currentElderly->next;
            free(temp);
        }

        queue->elderlyCount = 0;
        queue->generalCount = 0;
        queue->elderlyinSequenceCount = 0;
        queue->generalTail = nullptr;
        queue->elderlyTail = nullptr;
        queue->general = nullptr;
        queue->elderly = nullptr;
        
        free(queue);
    }


};  