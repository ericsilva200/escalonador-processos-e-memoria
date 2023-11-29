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

  def next_window_lru():
      memoriaLRU = janelaLRU()
      memoriaLRU.janelaLRU()

  def next_window_fifo():
      num_pag = int(pages_input.get())
      memoriaFifo = janelaFifo(num_pag)
      memoriaFifo.janelaFifo(num_pag)
            

  fifo_button = Button(window, text="FIFO", command=next_window_fifo)
  fifo_button.place(x=260, y=260)

  lru_button = Button(window, text="LRU", command=next_window_lru)
  lru_button.place(x=230, y=260)
  

  window.mainloop()

 
