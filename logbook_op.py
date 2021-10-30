from data_op import data_op
from data_endoscope import data_op_endo
import tkinter as tk
from tkinter import ttk
from pathlib import Path

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
    read.generate_logbook(logbook,surgeon_name)
    print(Path.cwd())

generate_ot_button = ttk.Button(win, text="GENERATE_OT_LOGBOOK",command=generate_LB_OT)
generate_ot_button.grid(column=2, row=3)

def generate_LB_assist_OT():
    surgeonyear = str(year.get())
    surgeon_name = str(name.get())
    read = data_op(surgeonyear)
    logbook=read.logbook_ot_assistant(surgeon_name)
    read.generate_logbook(logbook,surgeon_name)
    print(Path.cwd())

generate_ot_button = ttk.Button(win, text="GENERATE_OT_assist_LOGBOOK",command=generate_LB_assist_OT)
generate_ot_button.grid(column=2, row=4)

###############################ENDOSCOPY DATA######################################
    
def generate_LB_ENDO():
    surgeonyear = str(year.get())
    surgeon_name = str(name.get())
    read = data_op_endo(surgeonyear)
    logbook=read.logbook_scope_surgeon(surgeon_name)
    read.generate_logbook(logbook,surgeon_name)
    print(Path.cwd())

generate_endo_button = ttk.Button(win, text="GENERATE_ENDOSCOPE_LOGBOOK",command=generate_LB_ENDO)
generate_endo_button.grid(column=2, row=5)



def generate_LB_assist_ENDO():
    surgeonyear = str(year.get())
    surgeon_name = str(name.get())
    read = data_op_endo(surgeonyear)
    logbook=read.logbook_scope_assist(surgeon_name)
    read.generate_logbook(logbook,surgeon_name)
    print(Path.cwd())

generate_endo_button = ttk.Button(win, text="GENERATE_ENDOSCOPE_assistant_LOGBOOK",command=generate_LB_assist_ENDO)
generate_endo_button.grid(column=2, row=6)

win.mainloop()
