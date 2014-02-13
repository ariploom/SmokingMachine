#!/usr/bin/python

from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from compare_samples import *

class MainWindow(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        self.centerWindow()
        

    def initUI(self):
      
        self.parent.title("Smoking Machine Analysis")
        self.pack(fill=BOTH, expand=1)


    def centerWindow(self):
    	
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        w = sw
        h = sh
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
  
    root = Tk()
    main_window = MainWindow(root)

    figures = compare_samples('A0001A', 'A0001B', 'A0001C',supress_plots=True)
    canvas = FigureCanvasTkAgg(figures[1], master=root)
    canvas.show()

    root.mainloop()


if __name__ == '__main__':
    main()  