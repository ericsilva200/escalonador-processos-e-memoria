import tkinter as tk
from tkinter import *
from tkinter import messagebox
from interface import *

#Arrays
physicalMemory = []
virtualMemory = []
getValues = []


#Funções
def fifoWindow(page_num):
  pageNum = page_num

  def page_fault(page_fault):

    if page_fault == "yes":
      text = "Page Fault"
      pageFaultText = Label(fifoMemory, text=text, anchor="center", fg="blue", font=('Sans-serif', 16))
      pageFaultText.place(x=485, y=185)

    if page_fault == "no":
      pageFaultText = Label(fifoMemory, text=" ", anchor="center", fg="blue", font=('Sans-serif', 16))
      pageFaultText.place(x=485, y=185)      
      pageFaultText.grid_remove()

  def adderVirtualValue():
    y = 10
    for i in range(len(virtualMemory)):
      text2 = Label(fifoMemory, text=virtualMemory[i], anchor="center")
      text2.place(x=45, y=130)
      y+=25

    if len(virtualMemory) == len(pageNum):
      inputValue.configure(status="disabled")

    updateVirtualStack()

  def updateVirtualStack():
    count = -1
    for i in range(len(virtualMemory)):
      if i < len(virtualMemory) and i < 8:
        canvas2.itemconfigure(squares2[i], text=i)
      elif i > 8:
        count += 1
        canvas2.itemconfigure(squares2[i], text=count)
      else:
        canvas2.itemconfigure(squares2[i], text="")

  def storeValues():
    if inputValue.get() != '':
      value = inputValue.get()
      adderPhysicalValue(value)
      adderVirtualValue()
      inputValue.delete(0, 'end')
    else:
      messagebox.showinfo("Invalid Value!", "Insira um valor não vazio")

  def adderPhysicalValue(n):
    value = n
    size = 8
    i = len(physicalMemory) - size
    x = 10

    if value not in physicalMemory:
     getValues.append(value)

     if len(physicalMemory) >= 8:
      text3 = Label(fifoMemory, text="Valores que saíram da Memória Física: ", anchor="center", fg="red", font=('Sans-serif', 16))
      text3.place(x=335, y=385)

      for i in range(8, len(physicalMemory)+1):
        text4 = Label(fifoMemory, text=getValues[(len(physicalMemory) - i)], anchor="center", fg="red", font=('Sans-serif', 16))
        text4.place(x=x+335, y=405)
        x+=25

      physicalMemory.pop(i)
      physicalMemory.insert(i, value)

     physicalMemory.append(value)
     virtualMemory.append(value)
     updateQueue()
     page_fault("yes")
    else:
      page_fault("no")
      messagebox.showinfo("Invalid Value!", "Este valor já está na memória física!")

  def updateQueue():
    for i in range(8):
      if i < len(physicalMemory):
        canvas.itemconfigure(squares[i], text=physicalMemory[i])
      else:
        canvas.itemconfigure(squares[i], text="")


  #Interface

  fifoMemory = tk.Tk()
  fifoMemory.titles("Algoritmo FIFO")
  fifoMemory.geometry("750x650+500+150")

  #Telas
  canvas = tk.Canvas(fifoMemory, width=100, height=200)
  canvas.place(x=340, y=130)

  canvas2 = tk.Canvas(fifoMemory, width=100, height=420)
  canvas2.place(x=100, y=130)

  #Títulos
  title = Label(fifoMemory, text="Memória Física", anchor="center")
  title.place(x=340, y=100)

  title2 = Label(fifoMemory, text="Memória Virtual", anchor="center")
  title2.place(x=100, y=100)

  #Quadrados da Memória
  squares = []
  x, y = 10, 10
  for i in range(8):
    square = canvas.create_rectangle(x, y, x+80, y+20, outline="black")
    text = canvas.create_text(x=40, y=10, text="")
    squares.append(text)
    y +=25

    iText = Label(fifoMemory, text=i, anchor="center")
    iText.place(x=335, y = y+105)
    
  squares2 = []
  x, y = 10, 10
  for i in range(int(page_num)):
    square2 = canvas2.create_rectangle(x, y, x+80, y+20, outline="black")
    text2 = canvas2.create_text(x=40, y=10, text="")
    squares.append(text2)
    y+=25

  #Input
  inputValue = tk.Entry(fifoMemory)
  inputValue.place(x=40, y=45)

  #Botão
  addButton = tk.Button(fifoMemory, text="Adicionar", command=storeValues)
  addButton.place(x=40, y=35)


  #Loop
  fifoMemory.miniloop()
    


