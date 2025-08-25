#include <iostream>

using namespace std;


struct Aluno
{
    std::string name;
    float nota;
};

Aluno* criarAluno()
{
    Aluno* estudante = new Aluno;
    estudante->name = "";
    estudante->nota = 0;
    return estudante;
} 

int main()
{
    Aluno *estudante = criarAluno();
    std::cout<<estudante->name<<" "<<estudante->nota;
    delete estudante;

    return 0;
}