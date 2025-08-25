#include <iostream>

using namespace std;

int* createArray(int n)
{
    int *p = new int(n);
    for (int i = 0; i < n; i++)
    {
        p[i] = i+1;
    }
    return p;
}


int main()
{
    int *p = createArray(10);
    for (int i = 0; i < 10; i++)
    {
        std::cout<<p[i]<<" ";
    } 

    delete p;
    return 0;
}