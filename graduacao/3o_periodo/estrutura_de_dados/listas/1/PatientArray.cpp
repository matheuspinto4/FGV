#include "PatientArray.h"


namespace PatientArrayTAD
{

    PatientArray * initializePatientArray()
    {   // Esta função irá inicializar o PatientArray e retornar um ponteiro que aponta para ele.
        
        // inicializando o ponteiro e alocando a memória
        PatientArray *pa = (PatientArray *)malloc(sizeof(PatientArray));

        // verificando se o ponteiro pode ser criado
        if (pa == nullptr)
        {
            std::cerr<< "Falha ao alocar a memória para PatientArray"<<std::endl;
            free(pa);
            throw std::bad_alloc();
        }
        
        pa->size = 0; // definindo o tamanho inicial como zero 
        pa->capacity = 4; // definindo a capacidade para 4
        pa->patients = (Patient *)malloc(pa->capacity*sizeof(Patient)); // alocando memória do tamanho de capacity * sizeof(Patient)
        
        // verificando se o ponteiro para a lista de Patients pode ser criado
        if (pa->patients == nullptr)
        {
            std::cerr<< "Falha ao alocar a memória para a lista de Patients"<<std::endl;
            throw std::bad_alloc();
        }

        return pa; // retornando o ponteiro
    }

    
    void printPatients(PatientArray *pa)
    {// Esta função irá mostrar os pacientes na tela
        // checando se o ponteiro passado não é nulo
        if (pa == nullptr)
        {
            std::cerr<<"O ponteiro passado é considerado NULO"<<std::endl;  
            return;
        }

        // mostrando a capacidade do array e o tamanho
        std::cout << "Capacity: "<< pa->capacity << std::endl; 
        std::cout << "Current size: "<< pa->size << std::endl<<std::endl;

        std::cout<<"Patients:\n";
        for (int i = 0; i < pa->size; i++)
        { // acessando a lista do ponteiro e mostrando os valores de cada paciente
            std::cout<<"* " << pa->patients[i].arrival_time<<" | "<< pa->patients[i].severity<<" | "<<pa->patients[i].name<<std::endl;   
        }
    }
 
    
    void insertPatient(PatientArray *pa, Patient p)
    {// Esta função irá inserir um paciente novo na lista
        //checando 
        if(pa == NULL || pa->patients == NULL)
        {
            std::cerr<<"Operação inválida: Array NULL presente"<<std::endl;
            return;
        }

        if (pa->size >= 3 * pa->capacity / 4) // Se o tamanho exceder três quartos da capacidade dobrar de tamanho
        {
            pa->capacity *= 2; // dobrando o tamanho do array

            Patient *novo_pacientes = (Patient *)realloc(pa->patients, pa->capacity * sizeof(Patient)); // cria um ponteiro novo para evitar vazamento de memória
            if (novo_pacientes == nullptr)
            {
                free(pa->patients);
                pa->patients = nullptr;
                pa->size = 0;
                pa->capacity = 0;
                throw std::bad_alloc();
            }

            pa->patients = novo_pacientes; // copiando o novo_pacientes para o ponteiro original    
        }
        pa->patients[pa->size] = p; // adicionando o paciente no final da lista
        pa->size++; // aumentando o tamanho da lista em 1
    }

    int findNextPatient(PatientArray *pa)
    {// Esta função irá procurar o próximo paciente de maior urgência
        //checando
        if(pa == NULL || pa->patients == NULL)
        {
            std::cerr<<"Operação inválida: Array NULL presente. Retornando -1"<<std::endl;
            return -1;
        }

        int severityAtual = -1;
        int indiceEscolhido = -1;

        for (int i = 0; i < pa->size; i++)
        {
            int severity_i = pa->patients[i].severity; // Severidade do paciente de indice i
            
            //std::cout<<severity_i<<" "<<severityAtual<<std::endl;
            if (severity_i > severityAtual) // se a severidade do paciente i for maior que a severidade atual
            {
                indiceEscolhido = i; // o indice principal passa a ser i
                severityAtual = severity_i; // a severidade atual passa a ser a severidade de indice i 

            }else if (severity_i == severityAtual) // se a severidade i for igual a severidade atual
            {
                if (strcmp(pa->patients[i].arrival_time, pa->patients[indiceEscolhido].arrival_time) < 0) // comparando os tempos
                {
                    indiceEscolhido = i; // caso o tempo de indice i for menor, então trocar o indice escolhido para i
                    severityAtual = severity_i; // e passar a severiade para o de indice i (apenas para entender melhor o código, elas já são iguais)  
                } 
            }
        }
        return indiceEscolhido; // retornar o indice escolhido
    }


    void removePatient(PatientArray *pa, int index)
    {// Função que irá remover o paciente de indice especificado 
        if(pa == NULL || pa->patients == NULL || index < 0 || index >= pa->size)
        {
            std::cerr<<"Operacao Invalida: Ponteiro nulo ou indice fora de limite permitido pelo array"<<std::endl;
            return ;
        }

        // Passando todos os elementos depois do indice para a esquerda
        for (int i = index; i < pa->size - 1; i++)
        {
            pa->patients[i] = pa->patients[i+1]; // todo elemento será igual ao seu sucessor
        } 

        pa->size--; // diminuindo o tamnanho do array em 1

        if (pa->size < pa->capacity/4)// caso o tamanho do array seja menor que um quarto de sua capacidade, realizar o seguinte:
        { // dividir por 2 a capacidade do array
            if (pa->capacity/2 < 4) // caso a capacidade/2 seja menor que 4:
            {
                pa->capacity = 4; // transformar a capacidade em 4
            }else
            {
                pa->capacity /= 2; // caso o contrário, apenas dividir a capacidade por 2
            }

            pa->patients = (Patient *)realloc(pa->patients, pa->capacity * sizeof(Patient)); // realocando a memória para o Array
            // verificando se foi possível realocar o array
            if(pa->patients == nullptr)
            {
                std::cerr << "Falha ao redimensionar o array" << std::endl;
                pa->size = 0;
                pa->capacity = 0;
                throw std::bad_alloc();                
            }
        }
    }

    Patient popNextPatient(PatientArray *pa)
    { // esta função irá encontrar o paciente mais urgente e o remover da lista, retornando ele como referência 
        if (pa == nullptr)
        {
            std::cerr<<"O ponteiro é nulo, não e possivel continuar a operacao"<<std::endl;
            throw std::runtime_error("Erro: Ponteiro nulo fornecido.");
        }

        // encontrando o indice do proximo paciente
        int proximoPaciente = findNextPatient(pa);
        if (proximoPaciente == -1)
        {
            std::cerr << "Nenhum paciente disponível no array" << std::endl;
            throw std::runtime_error("Erro: Nenhum paciente disponível.");
        }
        
        // armazenando o proximo paciente
        Patient p = pa->patients[proximoPaciente];

        //removendo o paciente do array
        removePatient(pa, proximoPaciente);

        return p; 
    }
};


