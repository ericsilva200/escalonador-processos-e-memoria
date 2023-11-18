import time
import numpy as np
from os import system, name
from time import sleep

import tkinter as tk
from tkinter import *
from tkinter import ttk 

class Edf:
  def __init__(self, Quantum, Overload, process_interface):
    self.Quantum = Quantum
    self.Overload = Overload
    self.process_window = process_interface[0]
    self.progress_table = process_interface[2]
    self.var = process_interface[6]
    self.TurnAroundLabel = process_interface[7]

  def TurnAround(self, ProcessList):
    Turnaround = 0
    for process in ProcessList:
      Turnaround += process.WaitTime + process.ExecutionTime

    self.TurnAroundLabel.config(text="TURNROUND - " + str(Turnaround/ProcessList.size))
    return Turnaround/ProcessList.size
  
  def Edf(self, ProcessArray):
    CopyArray = np.array([])

    for process in ProcessArray:
      CopyArray = np.append(CopyArray, process.clone())

    WorkingList = np.array(CopyArray)
    TotalTime = 0
    ProcessCount = CopyArray.size
    ExecutingProcess = None
    ReadyList = np.array([])

    Overloading = False
    OverloadTime = self.Overload

    #Execução do Escalonamento
    while ProcessCount != 0:
      for process in WorkingList: #Adiciona a lista de prontos os processos que já chegaram
        if process.StartTime <= TotalTime:
          ReadyList = np.append(ReadyList, process)
          WorkingList = np.delete(WorkingList, np.where(WorkingList == process))
          for i in range(TotalTime):
            process.PrintList.append(" ")

      #Escolhe o processo que será executado
      if ExecutingProcess == None:
        for process in ReadyList:
          if process.StartTime <= None:
            if ExecutingProcess == None:
              ExecutingProcess = process
            else:
              if process.Deadline - (TotalTime - process.StartTime) < ExecutingProcess.Deadline - (TotalTime - process.StartTime):
                ExecutingProcess = process   

      TotalTime += 1

      #Executando um processo
      if not Overloading:
        try:
          ExecutingProcess.ExecutedTime += 1
          ExecutingProcess.ExecutionTimePerQuantum += 1
          ExecutingProcess.PrintList.append("X")

          #Atualiza a interface durante a execução de um processo
          if ExecutingProcess != None:
            self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Green'})
            for process in ReadyList:
              if process != ExecutingProcess:
                self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Grey'})
            self.process_window.update()

          if ExecutingProcess.Deadline - (TotalTime - ExecutingProcess.StartTime) < 0:
              self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Blue'})
              self.process_window.update()

          #Remove o processo da lista de prontos caso tenha terminado
          if ExecutingProcess.ExecutedTime == ExecutingProcess.ExecutionTime:
            ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
            ExecutingProcess = None
            ProcessCount -=1

          #Controle do quantum
          elif ExecutingProcess.ExecutionTimePerQuantum == self.Quantum and self.Overload > 0:
            ExecutingProcess.ExecutionTimePerQuantum = 0
            Overloading = True
            
        except:
          pass

        #Cálculo do tempo de espera
        for process in ReadyList:
          if(process == ExecutingProcess) or (process.StartTime >= TotalTime):
            continue
          process.PrintList.append("0")
          process.WaitTime += 1
      else:
        #Atualiza a interface durante a execução de um processo
        if ExecutingProcess != None:
          print(f'Tempo Total: {TotalTime}')
          print(f'ID: {int(ExecutingProcess.ProcessId)}')
          self.process_window.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Red'})
          for process in ReadyList:
            if process != ExecutingProcess:
              self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Grey'})
          self.process_window.update()
        ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
        ReadyList = np.append(ReadyList, ExecutingProcess)

        for process in ReadyList:
          if process.StartTime > TotalTime:
            continue
          process.PrintList.append("#")
          process.WaitTime += 1
        OverloadTime -= 1
        if OverloadTime <= 0: #Terminando Overload
          OverloadTime = self.Overload
          ExecutingProcess = None
          Overloading = False
      for process in CopyArray: 
        for i in range(process.WaitTime + process.ExecutedTime + process.StartTime, TotalTime):
          process.PrintList.append(" ")

      self.PrintProcess(CopyArray, TotalTime)

      if self.var.get() == 0:
        self.process_window.wait_variable(self.var)


    print(f"Tempo total: {str(TotalTime)}")
    print(f'TURNAROUND: {str(self.TurnAround(CopyArray))}')
    return
  
  def PrintProcess(self, ProcessArray, TotalTime):
    #Windows
    if name == 'nt':
      _ = system('cls')
    #MAC LINUX
    else:
      _ = system('clear')
    
    for process in ProcessArray:
      print(process.ProcessId, end="" )
      if process.StartLine < TotalTime:
        for j in range(TotalTime):
          print(process.PrintList[j], end="" )
        if not process.MetDeadline:
          print(" ESTOUROU", end="")

    self.process_window.update_idletasks()
    time.sleep(1)
    return