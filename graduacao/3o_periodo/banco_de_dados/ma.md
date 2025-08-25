Em um Sistema Gerenciador de Banco de Dados (SGBD) configurado com o nível de isolamento **`SERIALIZABLE`**, considere o seguinte cenário com duas transações concorrentes:

1.  A Transação A executa uma consulta que conta o número de registros em uma tabela que satisfazem uma determinada condição (por exemplo, `SELECT COUNT(*) FROM Tabela WHERE Condição`).
2.  Enquanto a Transação A ainda está ativa (não finalizada com `COMMIT` ou `ROLLBACK`), a Transação B insere um ou mais novos registros na *mesma* tabela, e esses novos registros *satisfazem* a condição utilizada pela Transação A. A Transação B, então, realiza um `COMMIT`.
3.  A Transação A executa a *mesma* consulta de contagem novamente.

Neste cenário, com a Transação A operando sob o nível de isolamento `SERIALIZABLE`, qual fenômeno de leitura **será evitado** em comparação com níveis de isolamento mais baixos?