import time
import numpy as np
from os import system, name
from time import sleep

import tkinter as tk
from tkinter import *
from tkinter import ttk 

class FIFO:
  def initial(self, Quantum, Overload, Iprocess):
    self.Quantum = Quantum
    self.Overload = Overload
    self.interface = Iprocess[0]
    self.progressTable = Iprocess[2]
    self.var = Iprocess[6]
    self.TurnAroundLabel = Iprocess[7]

  def TurnAround(self, List):
    Turnaround = 0
    for process in List:
      Turnaround += process.WaitTime + process.ExecutionTime

    self.TurnAroundLabel.config(text="TURNROUND - " + str(Turnaround/List.size))
    return Turnaround/List.size
  
  def FIFO(self, Array):
    Copy = np.array([])

    for process in Array:
      Copy = np.append(Copy, process.clone())

    WorkingList = np.array(Copy)
    Total = 0
    Count = Copy.size
    Executing = None
    ReadyList = np.array([])

    while Count != 0:
      for process in WorkingList:
        if process.StartTime <= Total:
          ReadyList = np.append(ReadyList, process)
          WorkingList = np.delete(WorkingList, np.where(WorkingList == process))
          for i in range(Total):
            process.PrintList.append(" ")

      if Executing == None:
        for process in ReadyList:
          if process.StartTime <= None:
            if Executing == None:
              Executing = process  

      Total += 1

      if Executing != None:
        print(f'Tempo Total: {Total}')
        print(f'ID:  {int(Executing.ProcessId)}')
        self.progressTable.loc[int(process.ProcessId), Total-1].configure({"background":'Green'})
        for process in ReadyList:
          if process != Executing:
            self.progressTable.loc[int(process.ProcessId), Total-1].configure({"background":'Green'})
        self.interface.update()

      try:
        Executing.ExecutedTime += 1
        Executing.PrintList.append("x")

        if Executing.Deadline - (Total - Executing.StartTime) < 0:
          self.progressTable.loc[int(Executing.ProcessId), Total-1].configure({"background":'Green'})
          Executing.MetDeadline = False

        if Executing.ExecutedTime == Executing.ExecutionTime:
          ReadyList = np.delete(ReadyList, np.where(ReadyList == Executing))
          Executing = None
          Count -=1

      except:
        pass

      for process in ReadyList:
        if(process == Executing) or (process.StartTime >= Total):
          continue
        process.PrintList.append("0")
        process.WaitTime += 1

      for process in Copy: 
        for i in range(process.WaitTime + process.ExecutedTime + process.StartTime, Total):
          process.PrintList.append(" ")

      self.PrintProcess(Copy, Total)

      if self.var.get() == 0:
        self.interface.wait_variable(self.var)

    print(f"Tempo total: {str(Total)}")
    print(f'TURNAROUND: {str(self.TurnAround(Copy))}')
    return
  
  def PrintProcess(self, Array, Total):
    if name == 'nt':
      _ = system('cls')
    else:
      _ = system('clear')
    
    for process in Array:
      print(process.ProcessId, end="" )
      if process.StartLine < Total:
        for j in range(Total):
          print(process.PrintList[j], end="" )
        if not process.MetDeadline:
          print(" ESTOUROU", end="")

    self.interface.update_idletasks()
    time.sleep(1)
    return