#include "PatientArray.h"
#include <iostream>

using namespace PatientArrayTAD;

int main()
{
    // Alocando memoria para o ponteiro:
    PatientArray *pa =  initializePatientArray();
    
    Patient p = {"JEANZINHO", 10, "12h10"};
    Patient p1 = {"BIAZINHA", 4, "12h20"};
    Patient p2 = {"MATHEUSINHO", 2, "12h30"};
    Patient p3 = {"BRUNINHO", 10, "12h40"};
    Patient p4 = {"NICOLASINHO", 10, "12h30"};

    insertPatient(pa, p);
    insertPatient(pa, p1);
    insertPatient(pa, p2);
    insertPatient(pa, p3);
    insertPatient(pa, p4);

    printPatients(pa);

    std::cout<<"Paciente mais urgente: "<<findNextPatient(pa)<<std::endl;

    removePatient(pa, 4);
    removePatient(pa, 0);
    
    printPatients(pa);
    try {
        Patient nextPatient = popNextPatient(pa);
        std::cout << "Paciente removido: " << nextPatient.name << ", Gravidade: " << nextPatient.severity << std::endl;
    } catch (const std::runtime_error& e) {
        std::cerr << e.what() << std::endl;
    }
    // Liberando a memória da lista de Patients e PatientArray 
    free(pa->patients);
    free(pa);


    return 0;
}