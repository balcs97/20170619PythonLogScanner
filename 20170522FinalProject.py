'''
Created on 2017/5/22
@author: Vic Huang
'''

from Tkinter import *
import os
import csv


class LogScanner():
    
    def __init__ (self):
        self.root=Tk()
        self.root.title("Log Scanner")
        menubar = Menu(self.root)
        #Variables
        self.var=IntVar()
        self.key1=StringVar()
        self.key2=StringVar()
        self.year=StringVar()
        self.month=StringVar()
        self.date=StringVar()
        self.hour=StringVar()
        #checkbox variable
        self.k2on=IntVar()
        self.xp=IntVar()
        #buffer
        self.buffer=StringVar()
        self.Result = []
        self.output=StringVar()
        self.input=StringVar()
        #Parameter Lists
        self.lastTime=[]
        self.userSaved=[]
        self.SSH=['sshd','','','','','','0','1']
        self.option2=['password','failed','','','','','1','1']
        # create a pulldown menu, and add it to the menu bar  
        filemenu = Menu(menubar, tearoff=0)  
        filemenu.add_command(label="Import", command=self.ImportData)  
        filemenu.add_command(label="Save", command=self.SaveParameter)  
        filemenu.add_separator()  
        filemenu.add_command(label="Exit", command=self.root.quit)  
        menubar.add_cascade(label="File", menu=filemenu)  
          
        # create more pulldown menus  
        editmenu = Menu(menubar, tearoff=0)  
        editmenu.add_command(label="Copy to Clipboard", command=self.Clipboard)  
        menubar.add_cascade(label="Tool", menu=editmenu)  
          
        helpmenu = Menu(menubar, tearoff=0)  
        helpmenu.add_command(label="About", command=self.hello)  
        menubar.add_cascade(label="Help", menu=helpmenu)  
        self.root.config(menu=menubar)  
        #self.label1=Label(text="77777777")
        
        self.labelk1=Label(text="Keyword1:").grid(row=0,column=0,sticky=W)
        self.labelk2=Label(text="Keyword2:").grid(row=1,column=0,sticky=W)
        self.entryk1=Entry(textvariable=self.key1,justify=RIGHT)
        self.entryk1.grid(row=0,column=1)
        self.entryk2=Entry(textvariable=self.key2,justify=RIGHT)
        self.entryk2.grid(row=1,column=1)
        self.labelin=Label(text="Input path:").grid(row=2,column=0,sticky=W)
        self.entryin=Entry(textvariable=self.input,justify=RIGHT)
        self.entryin.grid(row=2,column=1)
        
        
        self.labely=Label(text="Year:").grid(row=0,column=2,sticky=W)
        self.entryy=Entry(textvariable=self.year,justify=RIGHT,state=DISABLED)
        self.entryy.grid(row=0,column=3)
        
        self.labelm=Label(text="Month:").grid(row=1,column=2,sticky=W)
        self.entrym=Entry(textvariable=self.month,justify=RIGHT)
        self.entrym.grid(row=1,column=3)
        self.labeld=Label(text="Date:").grid(row=2,column=2,sticky=W)
        self.entryd=Entry(textvariable=self.date,justify=RIGHT)
        self.entryd.grid(row=2,column=3)
        self.labelh=Label(text="Hour:").grid(row=0,column=4,sticky=W)
        self.entryh=Entry(textvariable=self.hour,justify=RIGHT)
        self.entryh.grid(row=0,column=5)
        
        self.checkbtnk2=Checkbutton(text="Keyword2 ON",variable=self.k2on,onvalue = 1, offvalue = 0)
        self.checkbtnk2.grid(row=1,column=5,sticky=W)
        self.checkbtnxp=Checkbutton(text="Export txt",variable=self.xp,onvalue = 1, offvalue = 0)
        self.checkbtnxp.grid(row=2,column=5,sticky=W)
        
        #Three buttons
        self.btnsv=Button(text="Save Parameters",command=self.SaveParameter).grid(row=3,column=0,sticky=W)
        self.btnip=Button(text="Import Data",command=self.ImportData).grid(row=3,column=1,sticky=W)
        self.btngo=Button(text="Calculate",command=self.Calculate).grid(row=3,column=2,sticky=W,)
        self.btncr=Button(text="Clear",command=self.Clear).grid(row=3,column=4,sticky=W)
        
        #Helpmsg and RadioButtons
        self.helpmsg=Label(self.root,text="")
        self.helpmsg.grid(row=4,column=2,sticky=W,columnspan=3,rowspan=4)
        self.R1=Radiobutton(self.root,text="SSHD Login",variable=self.var,value=1,command=self.sel).grid(row=4,column=0,sticky=W)
        self.R2=Radiobutton(self.root,text="Password check ",variable=self.var,value=2,command=self.sel).grid(row=5,column=0,sticky=W)
        self.R3=Radiobutton(self.root,text="Load Parameters",variable=self.var,value=3,command=self.sel).grid(row=6,column=0,sticky=W)
        self.R4=Radiobutton(self.root,text="Last one",variable=self.var,value=4,command=self.sel).grid(row=7,column=0,sticky=W)
        self.R5=Radiobutton(self.root,text="Self Defined",variable=self.var,value=5,command=self.sel)
        self.R5.grid(row=8,column=0,sticky=W)
        self.R5.select()
        self.buffer.set("Welcome friends!!! I'm Vic Huang!!")
        self.console=Message(self.root,text=self.buffer.get(),width = 600)
        self.console.grid(row=9,column=0,sticky=W,columnspan=4,rowspan=3)
        #self.root.geometry("700x600")
        self.root.resizable(FALSE, FALSE)
        self.root.mainloop()
        
    def hello(self):
        self.console.config(text=str("Yoooooo!\n My Name is Vic Huang"))
    def Clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output)
        self.root.update()
    def sel(self):
        if self.var.get()==1:
            self.helpmsg.config(text="You choose SSHD Login.")
            self.LoadSSH()
        elif  self.var.get()==2:
            self.helpmsg.config(text="You choose Password check .")
            self.LoadOption2()
        elif  self.var.get()==3:
            if not self.userSaved:
                self.helpmsg.config(text="You choose user-saved parameters.System didn't get the record.")
            else:
                self.helpmsg.config(text="You choose to load the parameters you saved")
                self.LoadUserSaved()
        elif  self.var.get()==4:
            if not self.lastTime:
                self.helpmsg.config(text="You choose Last one.System didn't get the record.")
            else:
                self.helpmsg.config(text="You choose Last one.System will insert what you ran last time.")
                self.LoadLastOne()
        elif  self.var.get()==5:
            self.helpmsg.config(text="You choose Self defined.You can insert all parameters yourself.\n Note:Jan Feb...for month")
    def Clear(self):
            self.entryk1.delete(0, END)
            self.entryk2.delete(0, END)
            self.entryy.delete(0, END)
            self.entrym.delete(0, END)
            self.entryd.delete(0, END)
            self.entryh.delete(0, END)
            self.checkbtnk2.deselect()
            self.checkbtnxp.deselect()
    def LoadSSH(self):
            #entry insertion
            self.entryk1.delete(0, END)
            self.entryk1.insert(END,str(self.SSH[0]))
            self.entryk2.delete(0, END)
            self.entryk2.insert(END,str(self.SSH[1]))
            self.entryy.delete(0, END)
            self.entryy.insert(END,str(self.SSH[2]))
            self.entrym.delete(0, END)
            self.entrym.insert(END,str(self.SSH[3]))
            self.entryd.delete(0, END)
            self.entryd.insert(END,str(self.SSH[4]))
            self.entryh.delete(0, END)
            self.entryh.insert(END,str(self.SSH[5]))
            #checkbutton checked 
            if self.SSH[6]==str(1):
                self.checkbtnk2.invoke()
            if self.SSH[7]==str(1):
                self.checkbtnxp.invoke()
    def LoadOption2(self):
            #entry insertion
            self.entryk1.delete(0, END)
            self.entryk1.insert(END,str(self.option2[0]))
            self.entryk2.delete(0, END)
            self.entryk2.insert(END,str(self.option2[1]))
            self.entryy.delete(0, END)
            self.entryy.insert(END,str(self.option2[2]))
            self.entrym.delete(0, END)
            self.entrym.insert(END,str(self.option2[3]))
            self.entryd.delete(0, END)
            self.entryd.insert(END,str(self.option2[4]))
            self.entryh.delete(0, END)
            self.entryh.insert(END,str(self.option2[5]))
            #checkbutton checked 
            if self.option2[6]==str(1):
                self.checkbtnk2.select()
            if self.option2[7]==str(1):
                self.checkbtnxp.select()      
    def SaveParameter(self):
            #remove all elements
            del self.userSaved[:]
            #print self.userSaved
            self.userSaved.append(self.key1.get())
            self.userSaved.append(self.key2.get())
            self.userSaved.append(self.year.get())
            self.userSaved.append(self.month.get())
            self.userSaved.append(self.date.get())
            self.userSaved.append(self.hour.get())
            self.userSaved.append(self.k2on.get())
            self.userSaved.append(self.xp.get())
            print self.userSaved
    def LoadUserSaved(self):
            #entry insertion
            self.entryk1.delete(0, END)
            self.entryk1.insert(END,str(self.userSaved[0]))
            self.entryk2.delete(0, END)
            self.entryk2.insert(END,str(self.userSaved[1]))
            self.entryy.delete(0, END)
            self.entryy.insert(END,str(self.userSaved[2]))
            self.entrym.delete(0, END)
            self.entrym.insert(END,str(self.userSaved[3]))
            self.entryd.delete(0, END)
            self.entryd.insert(END,str(self.userSaved[4]))
            self.entryh.delete(0, END)
            self.entryh.insert(END,str(self.userSaved[5]))
            #checkbutton checked 
            if self.userSaved[6]==1:
                self.checkbtnk2.select()
            if self.userSaved[7]==1:
                self.checkbtnxp.select()
    def SaveLastOne(self):
            #remove all elements
            del self.lastTime[:]
            #print self.lastTime
            self.lastTime.append(self.key1.get())
            self.lastTime.append(self.key2.get())
            self.lastTime.append(self.year.get())
            self.lastTime.append(self.month.get())
            self.lastTime.append(self.date.get())
            self.lastTime.append(self.hour.get())
            self.lastTime.append(self.k2on.get())
            self.lastTime.append(self.xp.get())
            print self.lastTime
    def LoadLastOne(self):
            #entry insertion
            self.entryk1.delete(0, END)
            self.entryk1.insert(END,str(self.lastTime[0]))
            self.entryk2.delete(0, END)
            self.entryk2.insert(END,str(self.lastTime[1]))
            self.entryy.delete(0, END)
            self.entryy.insert(END,str(self.lastTime[2]))
            self.entrym.delete(0, END)
            self.entrym.insert(END,str(self.lastTime[3]))
            self.entryd.delete(0, END)
            self.entryd.insert(END,str(self.lastTime[4]))
            self.entryh.delete(0, END)
            self.entryh.insert(END,str(self.lastTime[5]))
            #checkbutton checked 
            if self.lastTime[6]==1:
                self.checkbtnk2.select()
            if self.lastTime[7]==1:
                self.checkbtnxp.select()
    def testStringVar(self):
        self.buffer.set("777 88888 148456+565+9 987/2616857/86")
        self.console.config(text=str(self.buffer.get()))   
    def ImportData(self):
        if os.path.exists('D:\\test_log.txt'):
            self.buffer.set("Data Imported!!")
            self.console.config(text=str(self.buffer.get()))
        else:
            self.buffer.set("File not exist!!Please Import!!")
            self.console.config(text=str(self.buffer.get()))
    def Calculate(self):
        
        print  os.environ['PYTHONPATH'].split(os.pathsep)
        if os.path.exists('D:\\test_log.txt'):
            infile = r"D:\test_log.txt"
            del self.Result[:]
            if not str(self.key1.get()):
                self.buffer.set("First Keyword can't be null.Please insert again and Run")
                self.console.config(text=str(self.buffer.get()))
            keep_phrases = [str(self.key1.get()),self.year.get(),self.month.get(),self.date.get(),self.hour.get()]
            if str(self.key2.get())   and self.k2on.get()==1:
                keep_phrases.append(self.key2.get())
            keep_phrases = filter(None,keep_phrases)
            if keep_phrases:
                self.SaveLastOne()
                print keep_phrases
                with open(infile) as f:
                    f = f.readlines()
                
                for line in f:
                    for phrase in keep_phrases:
                        if phrase in line:
                            #print self.xp.get()
                            self.Result.append(line)
                            break
                #Format change
                self.output='\n'.join(self.Result)
                if self.xp.get()==1 :
                    fileout = open('D:\\testFinal.txt', 'w')
                    fileout.writelines(self.output)
                    fileout2=open('D:\\testOut.csv','w')
                    fileout2.writelines(self.output)
                else:
                    fileout=open('D:\\testOut.csv','w')
                    fileout.writelines(self.output)
                self.console.config(text=str(self.output))
            else:   
                print "You have to insert Keyword1"
                self.console.config(text=str("You have to insert Keyword1"))
        else:
            self.buffer.set("File not exist!!Please Import Data first!!")
            self.console.config(text=str(self.buffer.get()))
LogScanner()