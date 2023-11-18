import pandas as pd
import tkinter as tk
from tkinter import *
from memoriaLRU import *
from memoriaFifo import *
from memoriaFifo import janelaFifo

def menuMemoria():
  window = Tk()
  window.geometry("400x400")
  window.resizable(False, False)
  window.configure(bg='#cf9416') 

  pages_label = Label(window, text="Quantidade de Páginas", anchor="center")
  pages_label.place(x=70, y=120)
  pages_input = Entry(justify="center")
  pages_input.place(x=200, y=120)

  num_pag = int(pages_input.get())

  def next_window():
      
      memoriaFifo = janelaFifo(num_pag)
      memoriaLRU = janelaLRU()

      print(pages_algorithm)
      if pages_algorithm == "FIFO":
           memoriaFifo.janelaFifo(num_pag)
      elif pages_algorithm == "LRU":
            memoriaLRU.janelaLRU()

  conffirm_button = Button(window, text="Avançar", command=next_window)
  conffirm_button.place(x=260, y=260)

  pages = StringVar()
  pages.set('FIFO')
  page_menu = OptionMenu(window, pages, "FIFO", "LRU")
  page_menu.place(x=120+180, y=70+230)
  pages_algorithm = pages.get()

  window.mainloop()

 
