Script em Python para realizar testes de conectividade (ping) em múltiplos endereços IP de forma prática e organizada.
O programa lê um arquivo lista.csv contendo os IPs, descrições e grupos, realiza os testes de ping e exibe os resultados formatados em tela, destacando:

IP testado

Status da conexão (OK, ERRO ou Sem resposta)

Tempo de resposta em ms

Descrição do equipamento

Também inclui barra de progresso durante a execução e saída colorida para facilitar a identificação de erros ou latência elevada.

O código pode ser convertido em executável para Windows utilizando a biblioteca PyInstaller, permitindo execução sem a necessidade de instalar o Python.

Formato esperado do arquivo lista.csv:

IP;DESCRIÇÃO;GRUPO

192.168.0.1;Servidor;Rede

192.168.0.2;Switch;Rede
