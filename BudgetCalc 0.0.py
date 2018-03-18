"""
First stage of Budget Calc development - ver 0.0
Establishing basic functionality with the goal to:
    - Allow users to set custom labels/values in a config file
    - Use Tkinter to produce a suitable, working GUI
    - Structure code in such a way that allows expansion for Stage Two (custom labels/values set with GUI)
"""

import tkinter;
from tkinter import *
from tkinter import font
import arrow;
import ast
import configparser;
config = configparser.RawConfigParser()

class mainWindow(object):
    def __init__(self, master):
        self.master = master

        date()

        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(size=14, family="Calibri Light")

        F_title = Frame(master)
        F_title.grid(column = 0, row = 0)
        Label(F_title, text = "BUDGET CALCULATOR", font=('Castellar',16,'bold')).grid(column = 0, row = 0)

        F_input  = Frame(master)
        F_input.grid(column = 0, row = 1)

        padx = 1
        pady = 5

        for i in range(len(params.u_Params)):
            print(params.u_Params[i])
            params.labels[i] = Label(F_input, anchor = E, text = params.u_Params[i])
            params.labels[i].grid(column = 0, row = i, padx = padx, pady = pady)
            params.entries[i] = Entry(F_input, bd = 5)
            params.entries[i].grid(column = 1, row = i, padx = padx, pady = pady)
            params.rmndrs[i] = Label(F_input, text = "$" + str(params.u_Rmndr[i]) + "/" + str(params.u_Values[i]))
            params.rmndrs[i].grid(column = 2, row = i, padx = padx, pady = pady)

            if(i == len(params.u_Params)-1):
                Label(F_input, text = "MONEY LEFT THIS WEEK: ").grid(column = 0, row = i+1, pady = pady, columnspan = 2)
                Label(F_input, text = "$" + str(sum(params.u_Rmndr)) + "/" + str(params.u_Goal)).grid(column = 2, row = i+1, pady = pady)

        def calc():
            print("CALCULATING")

            for i in range(len(params.u_Params)):
                if(params.entries[i].get() != ""):
                    params.u_Rmndr[i] -= round(float(params.entries[i].get()),  2)
                    params.rmndrs[i] = Label(F_input, text ="$" + str(params.u_Rmndr[i]) + "/" + str(params.u_Values[i]))
                    params.rmndrs[i].grid(column = 2, row = i, padx = padx, pady = pady)
                params.entries[i].delete(0, 100)

            write()

        calcB = Button(F_input, text = "CALCUALTE", command = lambda: calc(), font=('Arial Black',14,'bold'), bg = "dark green", fg="white")
        calcB.grid(column = 0, row = 8, pady = 5, columnspan = 3)

class params():
    config.read('config.ini')
    i_wCheck = int(config.get('init', 'i_wCheck'))
    u_Params =  ast.literal_eval(config.get('user', 'u_Params'))
    u_Values =  ast.literal_eval(config.get('user', 'u_Values'))
    u_Rmndr = ast.literal_eval(config.get('user', 'u_Rmndr'))
    u_Inc = config.get('user', 'u_Inc')
    u_Exp = sum(u_Values)
    u_Goal = config.get('user', 'u_Goal')
    labels = [None] * len(u_Params)
    entries = [None] * len(u_Params)
    rmndrs = [None] * len(u_Params)

def write():
    print("WRITING")

    config.set('user', 'u_Rmndr', params.u_Rmndr)
    config.set('user', 'u_Params', params.u_Params)
    config.set('user', 'u_Values', params.u_Values)
    config.set('user', 'u_Inc', params.u_Inc)
    config.set('user', 'u_Goal', params.u_Goal)
    config.set('init', 'i_wCheck', params.i_wCheck)

    outfile = open('config.ini','w')
    config.write(outfile)
    outfile.close

def date():
    print("DATE CONFIG")

    sDate = arrow.get('2018-01-01');
    cDate = arrow.now();
    dateDelta = cDate - sDate;
    modDelta = dateDelta.days % 7;

    if(modDelta == 6 and params.i_wCheck == 0):
        for i in range(len(params.u_Params)):
            params.u_Rmndr[i] += params.u_Values[i]
        params.i_wCheck = 1
        print("VALUES COMPOUNDED")
    elif(modDelta != 6 and params.i_wCheck == 1):
        params.i_wCheck = 0
        print("WEEKLY CHECK RESET")

    write()

if __name__ == "__main__":
    root = Tk()
    m = mainWindow(root)
    root.mainloop()