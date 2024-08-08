from ping3 import ping
import pandas as pd
import time
from pathlib import Path
from os import system
import sys
import threading

system('cls')
arquivo = Path('lista.csv')

print("\n===== TESTE DE CONEXÃO =====\n")
time.sleep(1)
print("O arquivo CSV deve estar no mesmo local com o nome 'lista.csv',") 
print("os dados devem estar separados por ; na seguinte sequencia 'IP;DESCRIÇÃO;GRUPO'.\n")

time.sleep(5)

input()
system('cls')

if arquivo.exists():
    df = pd.read_csv(arquivo, header=None, delimiter=";", encoding="latin1")
    df = pd.DataFrame(df)
    df = df.sort_values(by=df.columns[1])
    print("Arquivo carregado com sucesso.")
    time.sleep(2)
else:
    print(f"O arquivo '{arquivo}' não foi encontrado.")
    exit()

def teste_ip(ip):
    try:
        response_time = ping(ip, unit='ms', ttl=50)
        if response_time is None:
            return {'ip': ip, 'status': 'No response', 'response_time': None}
        elif response_time is False:
            return {'ip': ip.ljust(12), 'status': 'ERRO'.ljust(6) , 'response_time': response_time}
        else:
            return {'ip': ip.ljust(12), 'status': 'OK'.ljust(6), 'response_time': int(max(1, response_time))}
    except Exception as e:
        return {'ip': ip, 'status': 'Error', 'response_time': None, 'error': str(e)}

def mostrar_progresso(iterador, total):
    progress_chars = ['|', '/', '-', '\\']
    while not iterador.done:
        sys.stdout.write(f"\rProcessando... {progress_chars[iterador.count % len(progress_chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        iterador.count += 1

print('Iniciando teste....\n')

system('cls')

class Iterador:
    def __init__(self):
        self.done = False
        self.count = 0

iterador = Iterador()

thread_progresso = threading.Thread(target=mostrar_progresso, args=(iterador, len(df)))
thread_progresso.start()

results = [teste_ip(ip) for ip in df.iloc[:, 0]]

iterador.done = True
thread_progresso.join()

system('cls')
print("===== TESTE DE CONEXÃO =====\n")
print("IP           |STATUS  | PING   | DESCRIÇÃO")
print("----------------------------------------------")

erros = [result for result in results if result['status'].strip() == 'ERRO']
outros = [result for result in results if result['status'].strip() != 'ERRO']

for i, result in enumerate(erros):
    ip = result['ip'].strip()
    descricao = df.iloc[i, 1]
    status = result['status']
    response_time = result['response_time']
    
    print(f"{ip.ljust(12)} | \033[31m{status}\033[0m | {'--'.ljust(3)} ms | {descricao.ljust(25)}")
    df.loc[i, 'STATUS'] = status

for i, result in enumerate(outros, start=len(erros)):
    ip = result['ip'].strip()
    descricao = df.iloc[i, 1]
    status = result['status']
    response_time = result['response_time']
    
    print(f"{ip.ljust(12)} | \033[{'33m' if response_time > 50 else '32m'}{status}\033[0m | {str(response_time).ljust(3)} ms | {descricao.ljust(25)}")
    df.loc[i, 'STATUS'] = status

print("----------------------------------------------\n")
print("Enter para finalizar!")
input()
system('cls')
