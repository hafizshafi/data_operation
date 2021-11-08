from data_op import data_op
from data_endoscope import data_op_endo
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os

win = tk.Tk()
win.title("Deparment of Surgical Logbook")

namelabel = ttk.Label(win, text="NAME")
namelabel.grid(column=0, row =0)
name=tk.StringVar()
name_entry = ttk.Entry(win, width=12, textvariable=name)
name_entry.grid(column=3, row=0)


yearlabel=ttk.Label(win,text="YEAR")
yearlabel.grid(column=0, row = 1)
year= tk.StringVar()
year_entry=ttk.Entry(win,width=12,textvariable=year)
year_entry.grid(column=3, row =1)

##############################OT_DATA################################################-

def generate_LB_OT():
    surgeonyear = str(year.get())
    surgeon_name = str(name.get())
    read = data_op(surgeonyear)
    logbook=read.logbook_ot_surgeon(surgeon_name)
    _path = Path.cwd()
    os.chdir(_path)
    pathlogbook = surgeon_name+"_OT_"+surgeonyear
    os.mkdir(pathlogbook)
    logbook.to_csv(str(_path)+"/"+pathlogbook+"/"+pathlogbook+".csv")
   

generate_ot_button = ttk.Button(win, text="GENERATE_OT_LOGBOOK",command=generate_LB_OT)
generate_ot_button.grid(column=2, row=3)

def generate_LB_assist_OT():
    surgeonyear = str(year.get())
    surgeon_name = str(name.get())
    read = data_op(surgeonyear)
    logbook=read.logbook_ot_assistant(surgeon_name)
    _path = Path.cwd()
    os.chdir(_path)
    pathlogbook = surgeon_name+"_OTassis_"+surgeonyear
    os.mkdir(pathlogbook)
    logbook.to_csv(str(_path)+"/"+pathlogbook+"/"+pathlogbook+".csv")


generate_ot_button = ttk.Button(win, text="GENERATE_OT_assist_LOGBOOK",command=generate_LB_assist_OT)
generate_ot_button.grid(column=2, row=4)

###############################ENDOSCOPY DATA######################################
    
def generate_LB_ENDO():
    surgeonyear = str(year.get())
    surgeon_name = str(name.get())
    read = data_op(surgeonyear)
    logbook=read.logbook_scope_surgeon(surgeon_name)
    _path = Path.cwd()
    os.chdir(_path)
    pathlogbook = surgeon_name+"_scope_"+surgeonyear
    os.mkdir(pathlogbook)
    logbook.to_csv(str(_path)+"/"+pathlogbook+"/"+pathlogbook+".csv")
    
generate_endo_button = ttk.Button(win, text="GENERATE_ENDOSCOPE_LOGBOOK",command=generate_LB_ENDO)
generate_endo_button.grid(column=2, row=5)



def generate_LB_assist_ENDO():
    surgeonyear = str(year.get())
    surgeon_name = str(name.get())
    read = data_op(surgeonyear)
    logbook=read.logbook_scope_assist(surgeon_name)
    _path = Path.cwd()
    os.chdir(_path)
    pathlogbook = surgeon_name+"_scopeassist_"+surgeonyear
    os.mkdir(pathlogbook)
    logbook.to_csv(str(_path)+"/"+pathlogbook+"/"+pathlogbook+".csv")

generate_endo_button = ttk.Button(win, text="GENERATE_ENDOSCOPE_assistant_LOGBOOK",command=generate_LB_assist_ENDO)
generate_endo_button.grid(column=2, row=6)

win.mainloop()

