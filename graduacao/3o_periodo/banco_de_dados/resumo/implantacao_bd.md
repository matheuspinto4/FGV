# Implantação e Uso de BD


## Referential Integrity Constraint

In each row fo a relation containing a foreign key, the value of the **foreign key** **EITHER matches** one of the vlaues in the **primary key** column o fthe referred relation **OR** the value of **the foreign key is null**

- Regulates the relationship between a table with a foreign key and a able with a primary key to which the foreign key refers. 

## DELETE options

### DELETE RESTRICT

Simplesmente não permite exclusão de registros que possuem "filhos".
### DELETE CASCADE

Sob o ponto de vista da tabela "filha", podemos especificar que, se caso o registro pai seja excluído, excluam-se também os filhos.
### DELETE SET-TO-NULL
Quando deletar o pai, colocar todas as foreign keys das tabelas que referenciam ela como vazias.

### DELETE SET-TO-DEFAULT
Quando deletar na tabela pai, colocar todas as chaves estrangeiras que a referenciam como um "default" definido.

## UPDATE options

### UPDATE RESTRICT

Does not allow the primary key value of a record to be changed if its primary key value is referred to by a foreign key value.
### UPDATE CASCADE

The update cascades from the table that contains the referred-to primary key to the table with the foreign key.

### UPDATE SET-TO-NULL

In all of the records whose foreign key value refers to th eprimary key being changed, the value of the foreign key is set to null.

### UPDATE SET-TO-DEFAULT

In all of the records whose foreign key value refers to the primary key being changed, the values of the foreign key is set to a pre-determined dafault value.

## Implementing User-Defined Constraints 

### CHECK Clause

    CREATE TABLE student
    (
        studentid CHAR(4),
        yearenrolled INT,
        yearofgraduation INT,
        PRIMARY KEY (studentid),
        CHECK (yearenrolled <= yearofgraduation)   

    );

## Indexing

An index is a mechanism for increasing the speed of the data search and data retrival on relations with a large number of records.

Creates an sorted table for the columns indexed with pointers to equivalent lines.

## Database Front End

- **`form`:**  is a databse front-end component whose purpose is to enable data input and retrivial for end user in a way that is straightforward and requires no training. 

- **`report`:** is a database front-end component whose porpose is to present the data and calculations on the data from one or more tables from the database in a formatted way.

- In addition to forms and reports, database front-ends applications can include many other components and functionalities, such as **`menus, charts, graphs, and maps`**.

## Data Quality Issues

The data in a database is considered of high quality if it correctly and nonambiguosly reflects the real world it is designed to represent.

### **Accuracy:** 
- Refers to the extent to which **`data correctly`** **`reflects`** the **`real-world`** instances it is supposed to depict.

### **Uniqueness:**
- requires **`each real-world`** instance to be **`represented only once`** in the data collection. The uniqueness data quality problema is sometimes also referred to as **`data duplication`**

### **Completeness**
- refers to the degree to which all the **`required data is present`** in the data collection.    
    - Exemple: all patients should have an weight on the hospital database.

### **Consistency**

- Refers to the extent to which the data **`properly conforms to and matches up with the other data`**.


### **Timeliness**

- Refers to the degree to which the data is **`aligned with the proper time window`** in its representaion of the real world.

### **Conformity**

- refers to the extent to which the **`data conforms to its specified format`**. Conformity data quality problems occur when an instance of data does not conform to a pre-agreed-upon format for that data.

## Transações

### ACID

- **`Atomicidade:`**
    - Depois que inicia-se uma **`transação`**, **`ou`** ela finaliza com **`sucesso`**, ou ela se **`desfaz completamente`**.

- **`Consistência:`**
    - Conceito em que o SGBD **`sai`** de um estado **`válido`** apenas para **`ir`** para **`outro`** estado **`válido`**.
    - Além dos mecanismos internos, o modelo do banco de dados precisa refletir a visão e as regras de negócio.

- **`Isolamento:`** 
    - Conceito em que cada **`transação ocorre`** de forma **`isolada e independente`** de outras transações, que podem estar ocorrendo ao mesmo tempo e nos mesmos objetos
    - Na prática, o isolamento é obtido através de bloqueios impeditivos.

- **`Durabilidade:`**
    - Conceito referente à durabilidade da transação, mesmo em situações de desastre.
    - Um SGBD possui áreas específicas para o registro de todas as transações, que podem ser reaplicadas durante uma restauração ou aplicadas em um banco de contingência.

### Levels of Consistency in SQL-92

Do menos ao mais restritivo

#### **Read uncommitted:** 
- registros **`não confirmados`** (commited) **`podem ser lidos`**.


#### **Read commited:** 
- **`Apenas registros confirmados`** (commited) **`pode ser lidos`**, é o nível de isolamento **`padrão`** para o SQL Server. **`Impede`** a realização de **`leituras sujas`** especificando que as instruções não podem ler valores de dados que foram modificados, mas ainda não confirmados por outras transações. **`Outras transações`** ainda **`podem modificar, inserir ou excluir`** dados entre execuções de instruções individuais dentro da transação atual, resultando em leituras não repetíveis ou dados fantasmas. **`Simplesmente restringe o leitor de fazer qualquer leitura intermediária, não comprometida e 'suja'`**. Não faz nenhuma promessa de que, se a transação reemitir a leitura, encontrará os mesmos dados, os dados estarão livres para serem alterados depois de lidos.

#### **Repeatable read:**
- além de ler apenas registros confirmados (commites), especifica que **`nenhuma outra transação pode modificar nem excluir dados que tenham sido lidos pela transação atual`**, **`até que a transação atual seja confirmada`**. Os bloqueiros compartilhados nos dados lidos são matidos até o término da transação, em vez de serem liberados ao final de cada instrução. **`No entanto`**, uma transação pode não ser serializável - ela **`pode encontrar alguns registros inseridos por uma transação`**, **`mas não encontrar outros`**.

#### **Serializable:** 
- **`bloqueia intervalos de chaves inteiros até que a transação seja concluída`**. Ele engloba REPEATABLE READ e adiciona a restrição de que **`outras transações não podem inserir`** novas linhas **`em intervalos que foram lidos`** pela transação **`até`** que a **`transação esteja concluída`**.

## Particionamento

### Partition Function
- Cria uma função no banco de dados que mapeia as linhas de uma tabela ou índice em partições com base nos valores de uma coluna especificada. 

### Partition Schema
- Cria um esquema no banco de dados que mapeia as partições de uma tabela particionada ou índice para um ou mais grupos de arquivos 

        CREATE PARTITION FUNCTION myRangePF1 (INT)
        AS RANGE LEFT FOR VALUES (1, 100, 1000);
        GO
        CREATE PARTITION SCHEME myRangePS1
        AS PARTITION myRangePF1
        TO (test1fg, test2fg, test3fg, test4fg);    