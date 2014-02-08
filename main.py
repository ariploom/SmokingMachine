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
      
        self.parent.title("File dialog")
        self.pack(fill=BOTH, expand=1)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)        
        
        self.txt = Text(self,height=1,width=50,bg="yellow")
        self.txt.place(x=0, y=0)
        
        self.select_button = Button(self, text='Select', command=self.onOpen)
        self.select_button.place(x=0,y=30)

        self.analyze_button = Button(self, text='Analyze')
        self.analyze_button.place(x=0,y=60)


    def onOpen(self):
      
        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        
        self.txt.insert(END, fl)
            

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text

    def centerWindow(self):
    	
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        w = sw
        h = sh
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def analyze(self):
    	filename = self.txt.get()
         

def main():
  
    root = Tk()
    ex = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  