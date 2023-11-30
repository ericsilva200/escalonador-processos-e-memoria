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
    #loop para preencher a fila a cada tique de clock
    self.exec_check = 0
    for x in range(self.process_total):
      print(f"\nDEBUG: Lista no loop {x}, Clock {clock}\nFila: {self.queue}")
      print(self.process_list)
      currentProcessinit_time = self.process_list.iat[x, 2]
      print(f"DEBUG: Current time var: {currentProcessinit_time}, tipo: {type(currentProcessinit_time)}")
      if (int(currentProcessinit_time) - 1 >= 0):
        self.process_list.iat[x, 2] = int(currentProcessinit_time) - 1
      print(f"DEBUG: init time atualizado: {self.process_list.iat[x, 2]}")
      if (self.process_list.iat[x,2] == 0) and (self.process_list.iat[x,5] == "none"):
        self.process_list.iat[x,5] = "fila"
        self.queue += [self.process_list.iat[x,0]]
        print("DEBUG Lista de Processos Atualizada:")
        print(self.process_list)
        print("DEBUG Fila (fim loop):")
        print(self.queue)
    if (self.processing == False):
      #se não tiver nada em execução, muda o primeiro processo da fila para em execução
      try:
        self.processing_id = int(self.queue[0])
        index_process = self.process_list[self.process_list['process_id'] == self.processing_id].index[0]
        print(f"DEBUG index_process do clock {clock}: {index_process} (tipo: {type(index_process)})")
        #self.process_list.iat[index_process, 1] = int(self.process_list.iloc[index_process,1]) - 1 ficará a cargo do IF abaixo
        self.process_list.iat[index_process, 5] = "executando"
        self.queue.pop(0)
        self.processing = True
      except: print("Nada na fila")
    if (self.processing_id != -1):
      index_process = self.process_list[self.process_list['process_id'] == self.processing_id].index[0]
      self.process_list.iat[index_process, 1] = int(self.process_list.iloc[index_process,1]) - 1
      if (self.process_list.iloc[index_process,0] == 0):
        self.process_list.iat[index_process, 5] = "finalizado"
        self.processing_id = -1
        self.processing = False
    print("DEBUG Processos fim código:")
    print(self.process_list)
    print("-----------------------")
  
    for x in range(self.process_total):
        temp_value = self.process_list.iloc[x,1]
        self.exec_check = self.exec_check + int(temp_value)

    return self.process_list
