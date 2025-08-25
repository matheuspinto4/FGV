#include "WaitingQueue.h"

using namespace WaitingQueueTAD;

int main()
{
    
    WaitingQueue* qu = createQueue(); // 1 1 1 0 0 0 1 1 
    enqueue(qu, Client{"Biazinha", 1});
    enqueue(qu, Client{"Jeanzinho", 1});
    enqueue(qu, Client{"Nicolazinho", 1});
    enqueue(qu, Client{"Matheuzinho", 0});
    enqueue(qu, Client{"Bruninho", 0});
    enqueue(qu, Client{"Luquinhas", 0});
    enqueue(qu, Client{"Joaozinho", 1});
    enqueue(qu, Client{"thalizinho", 1});
    int r = removeClient(qu,(char *)"Joaozinho");
    
    int numClients;
    Client *order = getQueueOrder(qu, &numClients);
    for (int i = 0; i < numClients; i++)
    {
        std::cout<<order[i].priority<<std::endl;
    }

    deleteQueue(qu);

    return 0;
}