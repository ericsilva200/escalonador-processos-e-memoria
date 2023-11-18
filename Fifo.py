import time
import numpy as np
from os import system, name
from time import sleep

import tkinter as tk
from tkinter import *
from tkinter import ttk 

class Fifo:
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
  
  def FIFO(self, ProcessArray):
    CopyArray = np.array([])

    for process in ProcessArray:
      CopyArray = np.append(CopyArray, process.clone())

    WorkingList = np.array(CopyArray)
    TotalTime = 0
    ProcessCount = CopyArray.size
    ExecutingProcess = None
    ReadyList = np.array([])

    #Execução dos Processos
    while ProcessCount != 0:
      for process in WorkingList:
        if process.StartTime <= TotalTime:
          ReadyList = np.append(ReadyList, process)
          WorkingList = np.delete(WorkingList, np.where(WorkingList == process))
          for i in range(TotalTime):
            process.PrintList.append(" ")

      if ExecutingProcess == None: #Se nenhum estiver sendo executado, escolhe o primeiro do pronto
        for process in ReadyList:
            ExecutingProcess = process   
            break 

      TotalTime += 1

      if ExecutingProcess != None:
        print(f'Tempo Total: {TotalTime}')
        print(f'ID:  {int(ExecutingProcess.ProcessId)}')
        self.progress_table.loc[int(process.ProcessId), TotalTime-1].configure({"background":'Green'})
        for process in ReadyList:
          if process != ExecutingProcess:
            self.progress_table.loc[int(process.ProcessId), TotalTime-1].configure({"background":'Grey'})
        self.process_window.update()

      try:
        ExecutingProcess.ExecutedTime += 1
        ExecutingProcess.PrintList.append("x")

        if ExecutingProcess.Deadline - (TotalTime - ExecutingProcess.StartTime) < 0:
          self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Green'})
          ExecutingProcess.MetDeadline = False

        if ExecutingProcess.ExecutedTime == ExecutingProcess.ExecutionTime:
          ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
          ExecutingProcess = None
          ProcessCount -=1

      except:
        pass

      #Tempo de Espera para calculo de turnaround
      for process in ReadyList:
        if(process == ExecutingProcess) or (process.StartTime >= TotalTime):
          continue
        process.PrintList.append("0")
        process.WaitTime += 1

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
    if name == 'nt':
      _ = system('cls')
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