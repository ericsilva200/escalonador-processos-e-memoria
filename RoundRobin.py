import time
import numpy as np
from os import system, name
from time import sleep

import tkinter as tk
from tkinter import *
from tkinter import ttk 

class RoundRobin:
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
  
  def RoundRobin(self, ProcessArray):
    WorkingArray = np.array([])

    for process in ProcessArray:
      WorkingArray = np.append(WorkingArray, process.clone())

    CopyArray = np.array(WorkingArray)
    TotalTime = 0
    ProcessCount = WorkingArray.size
    ExecutingProcess = None
    ReadyList = np.array([])
    Overloading = False
    OverloadTime = self.Overload

    #Execução
    while ProcessCount != 0:
      for process in WorkingArray: #Colocar na lista de pronto
        if process.StartTime <= TotalTime:
          ReadyList = np.append(ReadyList, process)
          WorkingArray = np.delete(WorkingArray, np.where(WorkingArray == process))
          for i in range(TotalTime):
            process.PrintList.append(" ")

      if ExecutingProcess == None: #Se nenhum estiver sendo executado, escolhe o primeiro do pronto
        for process in ReadyList:
            ExecutingProcess = process   
            break

      TotalTime += 1

      if not Overloading:
        if ExecutingProcess != None:
          self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Green'})
          for process in ReadyList:
            if process != ExecutingProcess:
              self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Grey'})
            self.process_window.update()
        
        try:
          ExecutingProcess.ExecutedTime += 1
          ExecutingProcess.ExecutionTimePerQuantum += 1
          ExecutingProcess.PrintList.append("X")


          if ExecutingProcess.ExecutedTime == ExecutingProcess.ExecutionTime:
            ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
            ExecutingProcess = None
            ProcessCount -=1

          elif ExecutingProcess.ExecutionTimePerQuantum == self.Quantum and self.Overload > 0:
            ExecutingProcess.ExecutionTimePerQuantum = 0
            Overloading = True
            
        except:
          pass

        for process in ReadyList:
          if(process == ExecutingProcess) or (process.StartLine >= TotalTime):
            continue
          process.PrintList.append("0")
          process.WaitTime += 1

      else:
        self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Red'})
        for process in ReadyList:
          if process != ExecutingProcess:
            self.progress_table.loc[int(ExecutingProcess.ProcessId), TotalTime-1].configure({"background":'Grey'})
        self.process_window.update()

        ReadyList = np.delete(ReadyList, np.where(ReadyList == ExecutingProcess))
        ReadyList = np.append(ReadyList, ExecutingProcess)

        for process in ReadyList:
          if process.StartLine > TotalTime:
            continue
          process.PrintList.append("#")
          process.WaitTime += 1
        OverloadTime -= 1

        if OverloadTime <= 0:
          OverloadTime = self.Overload
          ExecutingProcess = None
          Overloading = False

      for process in CopyArray:
        for i in range(process.WaitTime + process.ExecutedTime + process.StartLine , TotalTime):
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

      