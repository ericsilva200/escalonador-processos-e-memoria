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
  def clock_exec(self, clock):
    self.exec_check = 0 #sempre resetar essa variável para zero quando o método for acessado
    for x in range(self.process_total):
        if (str(self.process_list.iat[x, 5]) == "finalizando"):
          self.process_list.iat[x, 5] = "finalizado"
          break

    #loop para reduzir o valor do init_time em 1 e, caso chegue em 0, o processo terá ido para a fila.
    print(f"DEBUG - Inicio do clock {clock}\nFila: {self.queue}")
    print(self.process_list)
    
    for x in range(self.process_total):
      currentProcessinit_time = self.process_list.iat[x, 2]
      if (int(currentProcessinit_time) - 1 >= 0):
        self.process_list.iat[x, 2] = int(currentProcessinit_time) - 1
      if (self.process_list.iat[x,2] == 0) and (self.process_list.iat[x,5] == "none"):
        self.process_list.iat[x,5] = "fila"
        self.queue += [self.process_list.iat[x,0]]

    #lógica do FIFO
    if (self.processing == False):
      #se não tiver nada em execução, muda o primeiro processo da fila para em execução
      try:
        self.processing_id = int(self.queue[0]) #garante que a fila não está vazia.
        index_process = 0
        for x in range(self.process_total):
          if (self.processing_id == self.process_list.iat[x, 0]):
            index_process = x
        self.process_list.iat[index_process, 5] = "executando"
        self.queue.pop(0)
        self.processing = True
      except: print("Nada na fila")
    if (self.processing_id != -1):
      for x in range(self.process_total):
          if (self.processing_id == self.process_list.iat[x, 0]):
            index_process = x
      self.process_list.iat[index_process, 1] = int(self.process_list.iloc[index_process,1]) - 1
      if (self.process_list.iloc[index_process,1] == 0):
        self.process_list.iat[index_process, 5] = "finalizando"
        self.processing_id = -1
        self.processing = False
  
    for x in range(self.process_total):
        temp_value = self.process_list.iloc[x,1]
        self.exec_check = self.exec_check + int(temp_value)

    print(f"DEBUG - Fim do clock {clock}\nFila: {self.queue}")
    print(self.process_list)

    return self.process_list
