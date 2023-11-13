import tkinter as tk
from tkinter import *
from interface import *
from tkinter import messagebox

#Arrays
physicalMemory = []
virtualMemory = []
getValues = []

#Funções
def LRUWindow():

  def page_fault(page_fault):

    if page_fault == "yes":
      text = "Page Fault"
      pageFaultText = Label(LRUMemory, text=text, anchor="center", fg="blue", font=('Sans-serif', 16))
      pageFaultText.place(x=485, y=185)

    if page_fault == "no":
      pageFaultText = Label(LRUMemory, text=" ", anchor="center", fg="blue", font=('Sans-serif', 16))
      pageFaultText.place(x=485, y=185)      
      pageFaultText.grid_remove()

  def toLeave():
    title = Label(LRUMemory, text="Menos Recentemente Utilizado", anchor="center", fg="black", font=('Sans-serif', 16))
    title.place(x=70, y=130)

    text = Label(LRUMemory, text=physicalMemory[0], anchor="center", fg="red", font=('Sans-serif', 16))
    text.place(x=150, y=160)

    if len(getValues) > len(physicalMemory):
      size = len(getValues) - len(physicalMemory)
      text2 = Label(LRUMemory, text="Retirados da Memória Física: ", anchor="center", font=('Sans-serif', 16))
      text2.place(x=335, y=385)
      x=10
      for i in range(size):
        text3 = Label(LRUMemory, text=getValues[i], anchor="center", font=('Sans-serif', 16))
        text3.place(x=335, y=405)
        x+=25

  def storeValues():
    if inputValue.get() != "":
      adderPhysicalValue(inputValue.get())
      inputValue.delete(0, 'end')
    else:
      messagebox.showinfo("Invalid Value!", "Insira um valor não vazio")

  def adderPhysicalValue(n):
    value = n 
    if value not in physicalMemory:
      getValues.append(value)

      if len(physicalMemory) >= 8:
        physicalMemory.pop(0)

      physicalMemory.append(value)
      updateQueue()
      page_fault("yes")

    else:
      physicalMemory.remove(value)
      physicalMemory.append(value)
      getValues.remove(value)
      getValues.append(value)
      updateQueue()
    
  def updateQueue():

    for i in range(8):
      if i < len(physicalMemory):
        canvas.itemconfigure(squares[i], text=physicalMemory[i])

      else:
        canvas.itemconfigure(squares[i], text="")

    toLeave()

#interface

  
  LRUMemory = tk.Tk()
  LRUMemory.title("Algoritmo LRU(Menos Recentemente Utilizado)")
  LRUMemory.geometry("650x450+500+150")

  #Tela
  canvas = tk.Canvas(LRUMemory, width=100, height=205)
  canvas.place(x=340, y=130)

  #Quadrados da Memória
  squares = []
  x, y = 10, 10
  for i in range(8):
    square = canvas.create_rectangle(x, y, x+80, y+20, outline="black")
    text = canvas.create_text(x=40, y=10, text="")
    squares.append(text)
    y +=25

    iText = Label(LRUMemory, text=i, anchor="center")
    iText.place(x=335, y = y+105)

  #Input
  inputValue = tk.Entry(LRUMemory)
  inputValue.place(x=40, y=45)

  #Botão
  addButton = tk.Button(LRUMemory, text="Adicionar", command=storeValues)
  addButton.place(x=40, y=35)

  #Loop
  LRUMemory.miniloop()

