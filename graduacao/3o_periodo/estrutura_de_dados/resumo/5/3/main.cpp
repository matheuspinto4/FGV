#include <iostream>

using namespace std;


enum Cargo
{
    Estagiario,
    Junior,
    Pleno,
    Senior
};


struct Funcionario
{
    std::string nome;
    Cargo cargo;
};


Funcionario* criarVetor(int n)
{
    Funcionario *vetor = new Funcionario[n];

    return vetor;
}

int main()
{
    Funcionario f;
    f.cargo = Estagiario;
    f.nome = "ASD";
    
    Funcionario *vetor = criarVetor(10);
    
    Funcionario f2 {"AS", Junior};
    vetor[0] = f2;
    std::cout<<vetor[0].nome;
    delete[] vetor;
    


    return 0;
}