from RR import *
from SJF import *
from EDF import *
from FIFO import *
from tkinter import messagebox
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import *
from memoryMenu import *
import Process 

def interface():
  interface = Tk()
  interface.title("Escalonador de Processos e de Memória")
  interface.geometry("400x400")
  interface.resizable(False, False)
  interface.configure(bg='#0effcf')

  def recallMemory():
    interface.destroy()
    memoryMenu()

  button1 = Button(interface, text="Memória", command=recallMemory)
  button1.place(x=70, y=70)

  label1 = Label(interface, text="Quantidade de Processos", anchor="center")
  label1.place(x=70, y=120)
  input1 = Entry(justify="center")
  input1.place(x=200, y=120)

  label2 = Label(interface, text="Quantum", anchor="center")
  label2.place(x=70, y=150)
  input2 = Entry(justify="center")
  input2.place(x=200, y=150)

  label3 = Label(interface, text="Sobrecarga", anchor="center")
  label3.place(x=70, y=180)
  input3 = Entry(justify="center")
  input3.place(x=200, y=180)

  def nextInterface():
    numberProcess = int(input1.get())
    quantum = int(input2.get())
    overload = int(input3.get())
    interface.destroy()
    processInterface(numberProcess, quantum, overload)

  button2 = Button(interface, text="Confirmar", command=nextInterface)
  button2.place(x=260, y=260)
  interface.mainloop()

def processInterface(numberProcess, quantum, overload):
  root= Tk()
  root.geometry('600x600')
  root.resizable(False, False)
  
  root.configure(bg='#0effcf')

  dataProcess = ()
  currentProcess = 0
  y = 70
  x = 120

  label1 = Label(root, text=f'ID: {currentProcess}')
  label1.place(x=x, y=y)

  label2 = Label(root, text=f'Tempo Inicial: ')
  label2.place(x=x, y=y+25)
  init = Entry(root, text="Tempo Inicial: ")
  init.place(x=x+150, y=y+25)

  label3 = Label(root, text=f'Tempo de Execução: ')
  label3.place(x=x, y=y+50)
  execution = Entry(root, text="Tempo de Execução: ")
  execution.place(x=x+150, y=y+50)
  
  label4 = Label(root, text=f'Deadline: ')
  label4.place(x=x, y=y+75)
  deadline = Entry(root, text="Deadline: ")
  deadline.place(x=x+150, y=y+75)

  label5 = Label(root, text=f'Prioridade: ')
  label5.place(x=x, y=y+100)
  priority = Entry(root, text="Prioridade: ")
  priority.place(x=x+150, y=y+100)

  def checkOccupation():
    completed = False
    values = [  init.get(),
                execution.get(),
                deadline.get(),
                priority.get(),
                "1"]
    if "" not in values:
      print("Completed")
      completed = True
    return completed
  
  def clean():
    init.delete(0, END)
    execution.delete(0, END)
    deadline.delete(0, END)
    priority.delete(0, END)

  def nextProcess():
    nonlocal currentProcess
    init.focus()
    if checkOccupation():
      if currentProcess < numberProcess:

        dataProcess[str(currentProcess)] = [  init.get(),
                execution.get(),
                deadline.get(),
                priority.get(),
                "1"]
        currentProcess += 1
        if currentProcess < numberProcess:
          label1.configure(text=f'ID: {currentProcess}')
          clean()   
    else:
      messagebox.showinfo(message="Você não preencheu todos os campos!")

  button3 = Button(root, text="Próximo", command=nextProcess)
  button3.place(x=x+225, y=y+175)

  label6 = Label(root, text="Escalonador de Processos")
  label6.place(x=x, y=y+230)

  process = StringVar()
  process.set('FIFO')
  menu = OptionMenu(root, process, "FIFO", "SJF", "RR", "EDF")
  menu.place(x=x+180, y=y+230)

  def transfer():
    if len(dataProcess) == numberProcess - 1 and checkOccupation():
      nonlocal currentProcess
      dataProcess[str(currentProcess)] = [  init.get(),
                execution.get(),
                deadline.get(),
                priority.get(),
                "1"]
      currentProcess += 1
    elif len(dataProcess) != numberProcess:
      messagebox.showinfo(message="Falta Processos!")
      return
    
    algorithm = process.get()
    root.destroy()
    scheduler(numberProcess, quantum, overload, dataProcess, algorithm)

  button4 = Button(root, text="Simular", command=transfer)
  button4.place(x=x+100, y=y+330)

def scheduler(numberProcess, quantum, overload, dataProcess, algorithm):
  y = 40
  x = 200

  interface2 = Tk()
  interfaceWidth = interface2.winfo_screenwidth()
  interfaceHeight = interface2.winfo_screenheight()
  interface2.title("Escalonador de Processos")
  interface2.geometry(f'{interfaceWidth}x{interfaceHeight}')
  interface2.configure(bg="#0effcf")

  box = 2
  rows = numberProcess
  columns = 6
  table = pd.DataFrame(index=np.arange(rows), columns=np.arange(columns))

  YProgress = y + 150
  rowsProgress = numberProcess
  columnsProgress = 50
  tableProgress = pd.DataFrame(index=np.arange(rowsProgress), columns=np.arange(columnsProgress))

  for i in range(rowsProgress):
    for i in range(columnsProgress):
      tableProgress.loc[i, j] = Entry(interface2, width=1, fg='black', font=('Sans-serif', 16, 'bold'))
      if j == 0:
        tableProgress.loc[i, j].grid(row=i, column=j, padx=[x,0])
      else:
        tableProgress.loc[i, j].grid(row=i, column=j)
      
      if i == 0:
        tableProgress.loc[i, j].grid(row=i, column=j, pady=(YProgress, 0))

  y2 = YProgress + 5
  for k in range(numberProcess):
    label = Label(interface2, text=str[k], font=("Sans-serif", 8))
    label.place(x=x-30, y=y2)
    y2 = y2 + 28
    label.configure(bg="#0effcf")

  execution = Entry(interface2, width=box, fg="black", font=('Sans-serif', 8))
  execution.grid(row=0, column= 0, padx=[x-100])
  execution.configure(bg="Green")
  label2 = Label(interface2, text="Executando", font=('Sans-serif', 8))
  label2.place(x=x - 80, y=95)
  label2.configure(bg='#0effcf')

  execution = Entry(interface2, width=box, fg="black", font=('Sans-serif', 8))
  execution.grid(row=0, column= 0, padx=[x-100], pady=[30,0])
  execution.configure(bg="Gray")
  label2 = Label(interface2, text="Espera", font=('Sans-serif', 8))
  label2.place(x=x - 80, y=113)
  label2.configure(bg='#0effcf')

  execution = Entry(interface2, width=box, fg="black", font=('Sans-serif', 8))
  execution.grid(row=0, column= 0, padx=[x-100], pady=[60,0])
  execution.configure(bg="Red")
  label2 = Label(interface2, text="Overload", font=('Sans-serif', 8))
  label2.place(x=x - 80, y=129)
  label2.configure(bg='#0effcf')

  execution = Entry(interface2, width=box, fg="black", font=('Sans-serif', 8))
  execution.grid(row=0, column= 0, padx=[x-100], pady=[90,0])
  execution.configure(bg="Blue")
  label2 = Label(interface2, text="Estouro", font=('Sans-serif', 8))
  label2.place(x=x - 80, y=143)
  label2.configure(bg='#0effcf')

  x2 = x
  for k in range(columnsProgress+1):
    label3 = Label(interface2, text=str[k], font=('Sans-serif', 8))
    label3.place(x=x2, y=YProgress-22)
    if k<10:
      x+=15
    else:
      x+=16
    label3.configure(bg='#0effcf')

  var = tk.IntVar()
  var.set(0)

  def Step():
    var.set(0)
    return
  def Auto():
    var.set(1)
    return
  def callOpen2():
    interface2.destroy()
    interface()

  button5 = Button(interface2, text=" passo-a-passo ", command=Step)
  button5.place(x=x, y=YProgress - 90)

  button6 = Button(interface2, text=" Pause ", command=Step)
  button6.place(x=x + 120, y=YProgress - 90)

  button7 = Button(interface2, text=" total ", command=Auto)
  button7.place(x=x+190, y=YProgress - 90)

  label4 = Label(interface2, text='', font=('Sans-serif', 13))
  label4.place(x=x+290, y=YProgress - 90)
  label4.configure(bg='#0effcf')

  button8 = Button(interface2, text=' Voltar ', command=callOpen2)
  button8.place(x=x, y=YProgress-55)

  ProcessArray = [Process.process[dataProcess[str(i)][0],dataProcess[str(i)][1],dataProcess[str(i)][2]]]
  processInterfacePackpage = [interface2, table, tableProgress, button5, button6, button7]

  fifo = FIFO(quantum, overload, processInterfacePackpage)
  sjf = SJF(quantum, overload, processInterfacePackpage)
  rr = RR(quantum, overload, processInterfacePackpage)
  edf = EDF(quantum, overload, processInterfacePackpage)

  print(algorithm)
  if algorithm == "FIFO":
    fifo.FIFO(ProcessArray)
  elif algorithm == "SJF":
    sjf.Sjf(ProcessArray)
  elif algorithm == "Round Robin":
    rr.RoundRobin(ProcessArray)
  elif algorithm == "EDF":
    edf.Edf(ProcessArray)
  