import psutil
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

class MonitoramentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoramento de Software")
        
        # Configurações da janela
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")
        
        # Título
        self.title_label = tk.Label(root, text="Monitoramento de Software", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20)
        
        # Frame para entrada de dados
        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)
        
        # Nome do processo
        self.label_process = tk.Label(self.input_frame, text="Nome do Processo:", font=("Arial", 12), bg="#f0f0f0")
        self.label_process.grid(row=0, column=0, padx=10, pady=5)
        self.entry_process = tk.Entry(self.input_frame, font=("Arial", 12))
        self.entry_process.grid(row=0, column=1, padx=10, pady=5)
        
        # Tempo de monitoramento
        self.label_time = tk.Label(self.input_frame, text="Tempo (segundos):", font=("Arial", 12), bg="#f0f0f0")
        self.label_time.grid(row=1, column=0, padx=10, pady=5)
        self.entry_time = tk.Entry(self.input_frame, font=("Arial", 12))
        self.entry_time.grid(row=1, column=1, padx=10, pady=5)
        self.entry_time.insert(0, "30")  # Valor padrão
        
        # Botão para iniciar
        self.button_start = tk.Button(root, text="Iniciar Monitoramento", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.iniciar_monitoramento)
        self.button_start.pack(pady=20)
        
        # Área para exibir o gráfico
        self.fig, self.ax = plt.subplots(2, 1, figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=20)
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress_bar.pack(pady=10)
        
        # Variáveis para guardar os dados
        self.cpu_data = []
        self.memory_data = []
        self.monitorando = False

    def iniciar_monitoramento(self):
        nome_processo = self.entry_process.get()
        tempo = self.entry_time.get()
        
        if tempo.isdigit():
            tempo = int(tempo)
        else:
            tempo = 30
        
        # Verificar se o processo existe
        proc = self.encontrar_processo(nome_processo)
        if not proc:
            messagebox.showerror("Erro", f"Processo '{nome_processo}' não encontrado.")
            return
        
        self.monitorando = True
        self.cpu_data = []
        self.memory_data = []
        
        self.button_start.config(state=tk.DISABLED)  # Desabilitar o botão enquanto monitora
        self.progress_bar["value"] = 0  # Resetar a barra de progresso
        self.progress_bar["maximum"] = tempo  # Definir o tempo máximo

        # Começar o monitoramento em uma thread separada
        threading.Thread(target=self.monitorar, args=(nome_processo, tempo)).start()

    def monitorar(self, nome_processo, duracao):
        proc = self.encontrar_processo(nome_processo)
        
        for i in range(duracao):
            if not self.monitorando:
                break

            try:
                cpu = proc.cpu_percent(interval=1)
                memoria = proc.memory_info().rss / (1024 * 1024)  # MB
                self.cpu_data.append(cpu)
                self.memory_data.append(memoria)
                
                # Atualizando gráfico
                self.atualizar_grafico()
                
                # Atualizando barra d]]e progresso
                self.progress_bar["value"] = i + 1

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                messagebox.showwarning("Aviso", "O processo foi finalizado ou está inacessível.")
                break

        self.finalizar_monitoramento()

    def finalizar_monitoramento(self):
        self.monitorando = False
        self.button_start.config(state=tk.NORMAL)  # Habilitar o botão novamente
        messagebox.showinfo("Monitoramento Finalizado", "O monitoramento foi concluído com sucesso!")

    def encontrar_processo(self, nome_processo):
        for proc in psutil.process_iter(['pid', 'name']):
            if nome_processo.lower() in proc.info['name'].lower():
                return proc
        return None

    def atualizar_grafico(self):
        # Limpar gráficos
        self.ax[0].cla()
        self.ax[1].cla()
        
        # Plot CPU
        self.ax[0].plot(self.cpu_data, label="Uso de CPU (%)")
        self.ax[0].set_title("Uso de CPU")
        self.ax[0].legend()

        # Plot Memória
        self.ax[1].plot(self.memory_data, label="Uso de Memória (MB)", color="r")
        self.ax[1].set_title("Uso de Memória")
        self.ax[1].legend()

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitoramentoApp(root)
    root.mainloop()
