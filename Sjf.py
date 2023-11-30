from os import system, name
import pandas as pd
import time

class SJF:
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

    #lógica do SJF
    if (self.processing == False):
      #se não tiver nada em execução, verifica na fila quem tem o menor tempo de execução
      try:
        minor = 100
        index_process = -1
        temp=-1
        for i in range(len(self.queue)):
          #acha o índice do processo na posição i da fila no DataFrame
          for x in range(self.process_total):
            if (self.queue[i] == self.process_list.iat[x, 0]):
                temp = x
          #se o valor do processo na posição i da fila for o com menor exec_time, atualiza o index_process
          if (minor > int(self.process_list.iat[temp, 1])):
            minor = int(self.process_list.iat[temp, 1])
            index_process = temp
        self.process_list.iat[index_process, 5] = "executando"
        self.processing_id = self.process_list.iat[index_process, 0]
        self.processing = True

        #self.queue.remove(self.processing_id)
        for i in range(len(self.queue)):
          if (self.queue[i] == self.processing_id):
            self.queue.pop(i)
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

    