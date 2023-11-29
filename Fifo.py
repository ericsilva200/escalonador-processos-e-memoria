from os import system, name
import pandas as pd

class Fifo:
  def __init__(self, quantum, overload, process_list):
    self.quantum = quantum
    self.overload = overload
    self.process_list = process_list
    self.process_total = process_list.shape[0] #quantidade de processos
    self.process_index = process_list.shape[1] #quantidade de atributos do processo
    self.processing = False #checa para garantir que não tem nada executando
    self.processing_id = -1 #id do processo em execução. -1 significa que o processador tá livre
    self.queue = []
    self.exec_check = 0
  #process_list = pd.DataFrame(columns=['process_id', 'exec_time', 'init_time', 'deadline', 'priority', 'status'])
  def clock_exec(self):
    #loop para preencher a fila a cada tique de clock
    self.exec_check = 0
    for x in range(self.process_total):
      self.process_list.at[x, 'init_time'] = int(self.process_list.iloc[x,2]) - 1
      if (self.process_list.iloc[x,2] == 0) and (self.process_list.iloc[x,5] == "none"):
        self.process_list.at[x, 'status'] = "fila"
        self.queue.append(self.process_list.iloc[x,0])
    if (self.processing == False):
      #se não tiver nada em execução, muda o primeiro processo da fila para em execução
      self.processing_id = int(self.queue[0])
      index_process = self.process_list[self.process_list['process_id'] == self.processing_id].index[0]
      self.process_list.at[index_process, 'exec_time'] = int(self.process_list.iloc[index_process,1]) - 1
      self.process_list.at[index_process, 'status'] = "executando"
      self.queue.pop(0)
      self.processing = True
    if (self.processing_id != -1):
      index_process = self.process_list[self.process_list['process_id'] == self.processing_id].index[0]
      if (self.process_list.iloc[index_process,0] == 0):
        self.process_list.at[index_process, 'status'] = "finalizado"
        self.processing_id = -1
        self.processing = False
  
    for x in range(self.process_total):
        temp_value = self.process_list.iloc[x,1]
        self.exec_check = self.exec_check + int(temp_value)
    return self.process_list
