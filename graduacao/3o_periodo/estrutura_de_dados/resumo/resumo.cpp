#include <iostream>

using namespace std;


int somaArray(int array[], int tamanho);
int somaArray(int array[], int tamanho)
{
    int soma = 0;
    int index = 0;
    do 
    {
        soma += array[index];
        index++;
    }while(index < tamanho);
    return soma;
}

void inverterArray(char* array, int size)
{
    for(int i = 0; i < size / 2; i++)
    {
        char temp = array[i];
        array[i] = array[size - i - 1];
        array[size - i - 1] = temp;
    }
}

void exibirArray(char* array, int size)
{
    for (int i = 0; i < size; i++)
    {
        std::cout<<array[i]<<" ";
    }
    cout<<"\n\n";
}

void exibirMatriz(int (*mtrz)[3], int linha)
{
    for (int i = 0; i < linha; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            cout<<mtrz[i][j];
        }
    }
}

int main()
{

    int a = 0;
    //cin.ignore(); // Evita buffers como \n

    //cin>>a;

    switch(a)
    {
        case 1:
            cout<<"Escolheu 1\n";
            break;
        case 2:
            cout<<"Escolheu 2\n";
            break;
        default:
            cout<<"no\n";
    }

    do 
    {
        cout<<"Vai executar ao menos uma vez\n";
    }
    while(false);
    
    int arr[5]; // declara um array com 5 elementos
    int arr2[5] = {1,2,3,4,5}; // declara um array com 5 elementos
    
    //cout<<somaArray(arr2, 5);
    char array[6] = {'a', 'b', 'c', 'd', 'e', 'f'};
    int size = 6;
    exibirArray(array,size);
    inverterArray(array, size);
    exibirArray(array,size);
    
    int mat[2][3] = {{1, 2, 3}, {4, 5, 6}};
    exibirMatriz(mat, 2);
    return 0;
}