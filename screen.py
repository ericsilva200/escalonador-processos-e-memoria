from tkinter import messagebox
from Fifo import *
from Sjf import *
from RoundRobin import *
from Edf import *
import pandas as pd
import tkinter as tk
from tkinter import *
from menuMemoria import *
import Process 

#Classe Process: Usada para criar um objeto, o qual será adicionado ao DataFrame de lista de processos (process_list) através da janela "Criar Processo"
class Process:
  def __init__(self, process_id, exec_time, init_time, deadline, priority):
    self.process_id = process_id
    self.exec_time = exec_time
    self.init_time = init_time
    self.deadline = deadline
    self.priority = priority
    self.status = "none"

  def returnData(self):
    return {'process_id': self.process_id, 'exec_time' : self.exec_time, 'init_time': self.init_time, 'deadline': self.deadline, 'priority' : self.priority, 'status' : self.status}
  

def root():
  #id de processo
  global process_id
  process_id=0

  #janela principal da aplicação
  root = Tk()
  root.title("Escalonador de Processos")
  scnwidth = root.winfo_screenwidth()
  scnheight = root.winfo_screenheight()
  root.geometry(f"{scnwidth}x{scnheight}+0+0")
  root.configure(bg='#d1d1d1')

  #Declarando DataFrame de processos
  global process_list
  process_list = pd.DataFrame(columns=['process_id', 'exec_time', 'init_time', 'deadline', 'priority', 'status'])

  def submitProcessData():
    #num_process = int(process_input.get())
    quantum = int(quantum_input.get())
    overload = int(overload_input.get())
    #process_window(num_process, quantum, overload)

  #frame p/ gerenciar aplicação
  manage_frame = Frame(root, width=400, height=200)
  manage_frame.grid(row=0, column=0, padx=5, pady=5)

  #input para atualizar quantum
  quantum_label = Label(manage_frame, text="Quantum")
  quantum_label.grid(row=2, column=0)
  quantum_input = Entry(manage_frame)
  quantum_input.grid(row=2, column=1)

  #input para atualizar sobrecarga
  overload_label = Label(manage_frame, text="Sobrecarga")
  overload_label.grid(row=2, column=3)
  overload_input = Entry(manage_frame)
  overload_input.grid(row=2, column=4)

  #frame para lista de processos
  process_frame = Frame(root, width=800, height=200)
  process_frame.grid(row=0, column=1, padx=5, pady=5)

  #frame para gráfico dos processos
  gantt_frame = Frame(root, width=1200, height=400)
  gantt_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

  #botão e método para abrir simulador de memoria
  def memButton():
    menuMemoria()
    root.destroy()
  memoria_button = Button(root, text="Simulador de Memória", command=memButton)
  memoria_button.grid(row=2, column=2)

  #botão e método para criar processo e eliminar processo
  def newProcess():
    newprocess = Tk()
    newprocess.title("Criar novo processo")
    newprocess.geometry("400x400")
    newprocess.configure(bg='#d1d1d1')

    init_label = Label(newprocess, text='Tempo de Entrada:')
    init_label.grid(row=0, column=0, padx=5, pady=10)
    exec_label = Label(newprocess, text='Tempo de Execução:')
    exec_label.grid(row=1, column=0, padx=5, pady=10)
    deadline_label = Label(newprocess, text='Deadline:')
    deadline_label.grid(row=2, column=0, padx=5, pady=10)
    priority_label = Label(newprocess, text='Prioridade:')
    priority_label.grid(row=3, column=0, padx=5, pady=10)

    init_entry = Entry(newprocess, text="Tempo de Entrada")
    init_entry.grid(row=0, column=1, padx=5, pady=10)
    exec_entry = Entry(newprocess, text="Tempo de Execução")
    exec_entry.grid(row=1, column=1, padx=5, pady=10)
    deadline_entry = Entry(newprocess, text="Deadline")
    deadline_entry.grid(row=2, column=1, padx=5, pady=10)
    priority_entry = Entry(newprocess, text="Prioridade")
    priority_entry.grid(row=3, column=1, padx=5, pady=10)

    #método para submeter os dados do processo novo
    def submitNewProcess():
      global process_list
      global process_id
      init_time = init_entry.get()
      exec_time = exec_entry.get()
      deadline = deadline_entry.get()
      priority = priority_entry.get()
      process_temp = Process(process_id, exec_time, init_time, deadline, priority)
      #abaixo: DataFrame temporário com os dados do processo a ser criado
      process_tempDataFrame = pd.DataFrame([process_temp.returnData()])
      #abaixo: Array de DataFrames, contendo a lista de processos e o novo processo
      process_array = [process_list, process_tempDataFrame]
      #abaixo: Concatena os dois dataframes em process_list
      process_list = pd.concat(process_array)
      process_id = process_id+1
      newprocess.destroy()

    submit_button = Button(newprocess, text="Criar Processo", command=submitNewProcess)
    submit_button.grid(row=4, column=0, columnspan=2)

  newprocess_button = Button(manage_frame, text="Criar Processo", command=newProcess)
  newprocess_button.grid(row=3, column=0, padx=10, pady=10)

  def killProcess():
    endprocess = Tk()
    endprocess.tittle("Eliminar processo")
    endprocess.geometry("400x100")
    endprocess.configure(bg='#d1d1d1')

  endprocess_button = Button(manage_frame, text="Eliminar Processo", command=killProcess)
  endprocess_button.grid(row=3, column=1, padx=10, pady=10)

  #botão para executar o simulador de processos
  start_button = Button(manage_frame, text="Iniciar simulação", command=submitProcessData)
  start_button.grid(row=3, column=4, padx=10, pady=10)

  root.mainloop()

  