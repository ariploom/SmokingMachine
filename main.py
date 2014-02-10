#!/usr/bin/python

from Tkinter import *
import tkFileDialog 

class Example(Frame):
  
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
    ex = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  