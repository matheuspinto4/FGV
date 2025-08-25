# Bases de dados em grafos

- Linguagem para banco de dados orientados a grafos
- É composta por três componentes: G (dados), $\Psi$ (instruções), e um conjunto de caminhos T.
- Respeita a linguagem nativa dos ambientes OLTP e OLAP


## GREMILIN:
Gremilin é uma linguagem universal aplicada para percorre grafos.

A linguagem funciona a partir de três componentes básicos:

1. Um grafo
    - O grafo precisa ser direcionado, consistindo um conjunto não vazio de vértices e de arestas direcionadas.


2. Um conjunto de "transversers"
    - "transverser" é o processo de percorrer o grafo em si. Na falta de um termo equivalente, mantivemos transverser.

3. Um conjunto de instruções de travessia
    - Conceitualmente, uma coleção de "transversers" ***T*** move-se sobre o grafo ***G*** de acordo com as instruções **$\Psi$**.
    - A computação é finalizada quando:
        1. Não há *transverser* em ***T***, ou
        2. Tdoso os *transverser* ***T*** não são mais referenciados por instruções em ***$\Psi$*** (i.e., foram até as terminações).
    - No caso a), o resultado é um conjunto vazio
    - No caso b), o resultado é o conjunto uniãp das localizações sobre ***G*** percorridas pelos traversers ***T***.