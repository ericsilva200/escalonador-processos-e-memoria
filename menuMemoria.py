import pandas as pd
import tkinter as tk
from tkinter import *
from memoriaLRU import *
from memoriaFifo import *
from memoriaFifo import janelaFifo

def menuMemoria():
  window = Tk()
  window.title("Simulador de Memória")
  window.configure(bg='#d1d1d1')

  pages_label = Label(window, text="Quantidade de Páginas", anchor="center")
  pages_label.grid(row=0, column=0)
  pages_input = Entry(window, justify="center")
  pages_input.grid(row=0, column=1, columnspan=2)

  def next_window_lru():
      memoriaLRU = janelaLRU()
      memoriaLRU.janelaLRU()

  def next_window_fifo():
      num_pag = int(pages_input.get())
      memoriaFifo = janelaFifo(num_pag)
      memoriaFifo.janelaFifo(num_pag)
  
  algorithm_label = Label(window, text="Algoritmo: ", anchor="center")
  algorithm_label .grid(row=1, column=0)

  fifo_button = Button(window, text="FIFO", command=next_window_fifo)
  fifo_button.grid(row=1, column=1, padx=5, pady=10)

  lru_button = Button(window, text="LRU", command=next_window_lru)
  lru_button.grid(row=1, column=2, padx=5, pady=10)

  window.mainloop()

 
