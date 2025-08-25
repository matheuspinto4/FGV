#pragma once

#include <iostream>
#include <cstdlib>
#include <string.h>

namespace WaitingQueueTAD
{
    // Estrutura para representar um cliente na fila
    struct Client {
        char name[50];    // Nome do cliente (máximo de 49 caracteres + '\0')
        int priority;     // Prioridade do cliente: 0 = Geral, 1 = Idoso
    };
    
    // Estrutura para representar um nó da fila duplamente encadeada
    struct QueueNode {
        Client client;        // Dados do cliente armazenados no nó
        QueueNode* next;      // Ponteiro para o próximo nó da fila
        QueueNode* previous;  // Ponteiro para o nó anterior da fila
    };
    
    // Estrutura para representar a fila de espera com duas subfilas (geral e idosos)
    struct WaitingQueue {
        int generalCount;         // Número de clientes na fila geral
        int elderlyCount;         // Número de clientes na fila de idosos
        QueueNode *general;       // Ponteiro para o início da fila geral
        QueueNode *generalTail;   // Ponteiro para o final da fila geral
        QueueNode *elderly;       // Ponteiro para o início da fila de idosos
        QueueNode *elderlyTail;   // Ponteiro para o final da fila de idosos
        int elderlyinSequenceCount; // Contador de idosos atendidos consecutivamente
        //<Demais variáveis a serem definidas>
    };

    /**
     * @brief Cria e inicializa uma nova fila de espera alocada dinamicamente.
     * @return Ponteiro para a nova WaitingQueue, ou nullptr se a alocação falhar.
     */
    WaitingQueue* createQueue();

    /**
     * @brief Cria um novo nó para a fila contendo os dados de um cliente.
     * @param client Cliente a ser armazenado no nó.
     * @return Ponteiro para o novo QueueNode, ou nullptr se a alocação falhar.
     */
    QueueNode* createNode(Client client);

    /**
     * @brief Insere um cliente no final da fila apropriada (geral ou idosos).
     * @param queue Ponteiro para a WaitingQueue onde o cliente será inserido.
     * @param client Cliente a ser adicionado (prioridade 0 = geral, 1 = idoso).
     */
    void enqueue(WaitingQueue* queue, Client client);

    /**
     * @brief Consulta o próximo cliente a ser atendido sem removê-lo da fila.
     * @param queue Ponteiro para a WaitingQueue (não modificada).
     * @param returnClient Ponteiro onde o próximo cliente será armazenado.
     * @return 1 se um cliente foi encontrado, 0 se a fila está vazia.
     * @note Segue a política de prioridade: idosos têm preferência, mas após dois
     *       idosos consecutivos, um cliente geral é priorizado se disponível.
     */
    int peek(const WaitingQueue* queue, Client* returnClient);

    /**
     * @brief Remove e retorna o próximo cliente da fila.
     * @param queue Ponteiro para a WaitingQueue onde o cliente será removido.
     * @param returnClient Ponteiro onde o cliente removido será armazenado.
     * @return 1 se a remoção foi bem-sucedida, 0 se a fila está vazia.
     * @note Atualiza elderlyinSequenceCount: incrementa para idosos, reseta para gerais.
     */
    int dequeue(WaitingQueue* queue, Client* returnClient);

    /**
     * @brief Remove um cliente específico da fila pelo nome.
     * @param queue Ponteiro para a WaitingQueue onde o cliente será removido.
     * @param name Nome do cliente a ser removido (string não constante).
     * @return 1 se o cliente foi encontrado e removido, 0 se não foi encontrado.
     * @note Busca nas filas geral e de idosos; ajusta ponteiros e contadores adequadamente.
     */
    int removeClient(WaitingQueue* queue, char* name);

    /**
     * @brief Retorna um array com a ordem de atendimento dos clientes na fila.
     * @param queue Ponteiro para a WaitingQueue (não modificada).
     * @param numClients Ponteiro onde o número total de clientes será armazenado.
     * @return Ponteiro para o array de Clients alocado dinamicamente, ou nullptr se a fila
     *         está vazia ou a alocação falhar. O chamador deve liberar o array com free().
     * @note Segue a mesma política de prioridade do peek.
     */
    Client* getQueueOrder(const WaitingQueue* queue, int* numClients);

    /**
     * @brief Libera toda a memória alocada para a WaitingQueue e seus nós.
     * @param queue Ponteiro para a WaitingQueue a ser deletada.
     * @note Após a chamada, o ponteiro queue se torna inválido (dangling pointer).
     */
    void deleteQueue(WaitingQueue* queue);

}; // namespace WaitingQueueTAD
