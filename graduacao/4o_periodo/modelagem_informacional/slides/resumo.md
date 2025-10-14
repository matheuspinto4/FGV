# Modelagem Informacional

## Casos de Uso

### Diagrama de Casos de Uso

Expressa as expectativas dos stakeholders. Pode ser usado durante todo o processo de análise e clarificação de requisitos.

Responde as seguintes perguntas:

- O que está sendo descrito? 
    - Que sistema está sendo modelado?

- Quem interage com o sistema?
    - Quem são os atores (papéis) que interagem com que sistemas?

- O que os atores (papéis) podem fazer?
    - Através da diagramação, os casos de uso revelam onde cada ator pode interagir.


#### O Caso de Uso

Descreve as funcionalidades esperadas de um sistema em desenvolvimento.

O conjunto de todos os casos de uso descreve, em alto nível, todas as funcionalidades que os sistema deve prover.

#### Os Atores

Os atores interagem com o sistema quando:

1. Usam dos casos;
2. São usados pelos casos.

Atores não fazem parte do sistema, por isso ficam fora dos limites do sistema

Atores podem ser humanos ou não-humanos.

#### Tipos de Atores

- **Humano:** estudante, professor,...
- **Não-humano:** Servidor de e-mail.
- **Primário:** Principal beneficiário da execução do caso de uso
- **Secundário:** Não recebe nenhum benefício direto.
- **Ativo:** Inicia a execução do caso de uso. 
- **Passivo:** Propicia funcionalidades para a execução do caso de uso.

#### Associação entre Caso de Uso e Ator

##### Caso de Uso Base: 

###### A ---> B
- (A) Necessita que seja feita a execução de (B) antes que a própria (A) seja executada.

###### A <--- B
- (A) decide se vai ou não executar (B)


#### Dicas

##### Identificação de Atores

Quem usa os principais casos de uso?

##### Identificação de Casos de Uso
 
Quais são as principais tarefas que um ator precisa executar? 


---

## MIR Modelagem Informacional de Requisitos

Foi proposta como uma especialização do modelo de Casos de Uso.

Em especial, o conceito de objetivo informacional substitui o de Caso de Uso, associando um nível de abstração específica aos objetivos considerados na modelagem.


### Princípios da solução

- **Focar nos Objetivos:** O objetivo é o nível mais alto de abstração de um processo. Logo é o mais adequado para uma primeira representação.

- **Atribuir níveis de abstração aos objetivos:** Corresponde a uma estratégia de aprticionamento funcional do sistema com base no conhecimento do problema.

- **Focar no detalhamento da informação:** Cada objetivo exprime uma mudança de estado que é concretizada pela execução do seu processo subjacente. O fluxo de informação que entra e sai do sistema é o foco do detalhe.

### Objetivos Informacionais

Quais eventos originados pelos atores externos levam o sistema a intervir atomicamentemente?

#### Passos Necessários:

1. **Definir** os **atores e objetivos informacioanis** numa tabela.
2. Fazer a **interface do sistema informacional** com:
    - **Descrição**;
    - **Propósito**;
    - **Frequência**;
3. **Dicionário** de itens elementares;
4. **Objetivos organizacionais**.
    - **Linhas temporais** com a sequência de objetivos informacionais. 

Sempre tentar ser o mais **simples e claro** o possível.

---

## DW 

### Informação Transacional vs Analítica

- **Transacional / Operacional:** Armazenamento num banco de dados para o uso cotidiano.

- **Analítico:** Armazenamento feito para análise de dados e tomadas de decisões.


### Conceitos de um DW

O DW é um repositório estruturado de informação. O propósito é a extração de informações analíticas. O DW pode guardar informações detalhadas e temporais.

#### Repositório Estruturados
- O DW é um banco de dados contendo informações analíticas.

#### Integrado
- Se refere ao processo de juntar informações de vários bancos de dados diferentes em um único DW.

#### Orientado por Objetivo
- O DW é desenvolvido para um objetivo de negócio específico.

#### Visão Ampla Empresarial
- Refere-se ao fato de dar uma grande visão analítica da empresa como um todo.

#### Histórico
- Grande horizonte temporal de informações quando comparado com um banco de dados operacional.

#### Coleta de Informações Analíticas
- Somente para leitura dos usuários.

### Componentes de um DW:

#### Sistemas de origem
- São bases de dados operacionais e outros repositórios de dados.
- Pode-se incluir fontes internas e externas.

#### Data Warehouse
- Destino dos dados de origem
- Sempre lê os dados com uma certa frequência, oferecendo dados atualizados.

#### Infraestrutura de ETL

- A infraestrutura de ETL facilita a leitura de dados das bases oepracionais para os DW.

#### Aplicações Front-End

- Permitem o acesso indireto dos usuários aos dados.

### Data Marts

- Segue o mesmo princípio de um DW. Porém possui um escopo mais limitado.
















