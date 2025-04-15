import psutil
import time

def encontrar_processo(nome_processo):
    for proc in psutil.process_iter(['pid', 'name']):
        if nome_processo.lower() in proc.info['name'].lower():
            return proc
    return None

def monitorar_processo(nome_processo, duracao=30):
    proc = encontrar_processo(nome_processo)
    
    if not proc:
        print(f"Processo '{nome_processo}' não encontrado.")
        return

    print(f"Monitorando '{nome_processo}' (PID {proc.pid}) por {duracao} segundos...\n")
    with open("monitoramento_saida.txt", "w") as arquivo:
        arquivo.write("Tempo;CPU (%);Memória (MB)\n")

        for i in range(duracao):
            try:
                cpu = proc.cpu_percent(interval=1)
                memoria = proc.memory_info().rss / (1024 * 1024)
                timestamp = time.strftime("%H:%M:%S")

                saida = f"{timestamp};{cpu};{memoria:.2f}"
                print(saida)
                arquivo.write(saida + "\n")

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print("Processo finalizado ou inacessível.")
                break

if __name__ == "__main__":
    nome = input("Digite o nome do processo/software para monitorar: ")
    tempo = input("Quantos segundos deseja monitorar? (padrão 15): ")

    if tempo.strip().isdigit():
        tempo = int(tempo)
    else:
        tempo = 30

    monitorar_processo(nome, tempo)
