"""
Second stage of Budget Calc development - ver 0.1
The goal of this build is to give the user the functionality to manage the current expense values for each
category, and allow them to add their own categories with custom labels and allowances. Drop down box
will be avaliable for users to choose whether this custom allowance is per day, week, fortnight, month, or year.

"""

import os
import sys
from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
import arrow
import ast
import configparser

config = configparser.RawConfigParser()

####################################################################
####################################################################


class removeWindow(object):
    def __init__(self, master):
        master = self.master = Toplevel(master)

        F_title = Frame(master)
        F_title.grid(column=0, row=0)
        Label(F_title, text="DELETE A CATEGORY", font=("Castellar", 16, "bold")).grid(
            column=0, row=0
        )

        F_input = Frame(master)
        F_input.grid(column=0, row=1)

        padx = 1
        pady = 5

        def cancelCall():
            mainWindow(self.master)

        def delCall():
            if choice_E.get() != "":
                print("REMOVING PARAM")
                try:
                    index = params.u_Params.index(choice_E.get())
                    print(index)
                    del params.u_Params[index]
                    del params.u_Values[index]
                    del params.u_Rmndr[index]

                except:
                    print("No such category exists, please type an existing category.")
                choice_E.delete(0, 100)

                recalParams()
                write()

        choice_L = Label(F_input, text="Delete: ")
        choice_L.grid(column=0, row=0, padx=padx, pady=pady)

        choice_E = Entry(F_input, bd=5)
        choice_E.grid(column=1, row=0)

        del_B = Button(
            F_input,
            text="DELETE",
            command=lambda: delCall(),
            font=("Arial Black", 14, "bold"),
            bg="dark blue",
            fg="white",
        )
        del_B.grid(column=0, row=1, pady=pady)
        cancel_B = Button(
            F_input,
            text="BACK",
            command=lambda: cancelCall(),
            font=("Arial Black", 14, "bold"),
            bg="red",
            fg="white",
        )
        cancel_B.grid(column=1, row=1, pady=pady)


####################################################################
####################################################################


class addWindow(object):
    def __init__(self, master):
        master = self.master = Toplevel(master)

        F_title = Frame(master)
        F_title.grid(column=0, row=0)
        Label(F_title, text="ADD NEW CATEGORY", font=("Castellar", 16, "bold")).grid(
            column=0, row=0
        )

        F_input = Frame(master)
        F_input.grid(column=0, row=1)

        padx = 1
        pady = 5

        def addCatCall():
            if label_E.get() != "" and allowance_E.get() != "":
                allowance = 0
                if per.get() == "Day":
                    allowance = float(allowance_E.get()) * 7
                elif per.get() == "Week":
                    allowance = float(allowance_E.get())
                elif per.get() == "Fortnight":
                    allowance = float(allowance_E.get()) / 2
                elif per.get() == "Month":
                    allowance = float(allowance_E.get()) / 4
                elif per.get() == "Year":
                    allowance = float(allowance_E.get()) / 52

                params.u_Params.append(str(label_E.get()))
                params.u_Values.append(float(allowance))
                params.u_Rmndr.append(float(allowance))

                label_E.delete(0, 100)
                allowance_E.delete(0, 100)

                recalParams()
                resetWidgets()
                write()

        def cancelCall():
            mainWindow(self.master)

        label_L = Label(F_input, text="Label: ")
        label_L.grid(column=0, row=0)
        allowance_L = Label(F_input, text="Allowance: ")
        allowance_L.grid(column=0, row=1)
        per_L = Label(F_input, text="Per: ")
        per_L.grid(column=0, row=2)

        label_E = Entry(F_input, bd=5)
        label_E.grid(column=1, row=0)
        allowance_E = Entry(F_input, bd=5)
        allowance_E.grid(column=1, row=1)

        per = StringVar()
        per.set("Week")
        per_O = OptionMenu(F_input, per, "Day", "Week", "Fortnight", "Month", "Year")
        per_O.grid(column=1, row=2)

        add_B = Button(
            F_input,
            text="+ADD",
            command=lambda: addCatCall(),
            font=("Arial Black", 14, "bold"),
            bg="dark green",
            fg="white",
        )
        add_B.grid(column=0, row=3, pady=pady)
        cancel_B = Button(
            F_input,
            text="BACK",
            command=lambda: cancelCall(),
            font=("Arial Black", 14, "bold"),
            bg="red",
            fg="white",
        )
        cancel_B.grid(column=1, row=3, pady=pady)


####################################################################
####################################################################


class manageWindow(object):
    def __init__(self, master):
        master = self.master = Toplevel(master)

        F_title = Frame(master)
        F_title.grid(column=0, row=0)
        Label(F_title, text="MANAGE CATEGORIES", font=("Castellar", 16, "bold")).grid(
            column=0, row=0
        )

        F_input = Frame(master)
        F_input.grid(column=0, row=1)

        padx = 1
        pady = 5

        def setCatVal():
            for i in range(len(params.u_Params)):
                if params.entries[i].get() != "":
                    params.u_Values[i] = round(float(params.entries[i].get()), 2)
                params.entries[i].delete(0, 100)

            recalParams()
            write()

        def addCall():
            addWindow(self.master)
            self.master.withdraw()

        def removeCall():
            removeWindow(self.master)
            self.master.withdraw()

        def cancelCall():
            mainWindow(self.master)

        for i in range(len(params.u_Params)):
            params.labels[i] = Label(F_input, anchor=E, text=params.u_Params[i])
            params.labels[i].grid(column=0, row=i, padx=padx, pady=pady)
            params.entries[i] = Entry(F_input, bd=5)
            params.entries[i].grid(column=1, row=i, padx=padx, pady=pady)
            if i == len(params.u_Params) - 1:
                setVal_B = Button(F_input, text="SET", command=lambda: setCatVal())
                setVal_B.grid(column=2, row=0, rowspan=i, padx=padx, pady=pady)
                addCat_B = Button(
                    F_input,
                    text="+ ADD NEW",
                    command=lambda: addCall(),
                    font=("Arial Black", 14, "bold"),
                    bg="dark green",
                    fg="white",
                )
                addCat_B.grid(column=0, row=i + 1, pady=pady)
                dltVal_B = Button(
                    F_input,
                    text="REMOVE",
                    command=lambda: removeCall(),
                    font=("Arial Black", 14, "bold"),
                    bg="dark blue",
                    fg="white",
                )
                dltVal_B.grid(column=1, row=i + 1, pady=pady)
                cancel_B = Button(
                    F_input,
                    text="BACK",
                    command=lambda: cancelCall(),
                    font=("Arial Black", 14, "bold"),
                    bg="red",
                    fg="white",
                )
                cancel_B.grid(column=2, row=i + 1, pady=pady)


####################################################################
####################################################################


class mainWindow(object):
    def __init__(self, master):
        self.master = master

        date()

        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(size=14, family="Calibri Light")
        F_title = Frame(master)
        F_title.grid(column=0, row=0)
        img = Image.open(getAsset("banner.gif"))
        imgtk = ImageTk.PhotoImage(img)
        x = Label(F_title, image=imgtk, font=("Castellar", 16, "bold"))
        x.image = imgtk
        x.grid(column=0, row=0)

        F_input = Frame(
            master,
        )
        F_input.grid(column=0, row=1)

        padx = 1
        pady = 4

        for i in range(len(params.u_Params)):
            params.labels[i] = Label(F_input, anchor=E, text=params.u_Params[i])
            params.labels[i].grid(column=0, row=i, padx=padx, pady=pady)
            params.entries[i] = Entry(F_input, bd=5)
            params.entries[i].grid(column=1, row=i, padx=padx, pady=pady)
            params.rmndrs[i] = Label(
                F_input,
                text="$" + str(params.u_Rmndr[i]) + "/" + str(params.u_Values[i]),
            )
            params.rmndrs[i].grid(column=2, row=i, padx=padx, pady=pady)

            if i == len(params.u_Params) - 1:
                Label(F_input, text="MONEY LEFT THIS WEEK: ").grid(
                    column=0, row=i + 1, pady=pady, columnspan=2
                )
                Label(
                    F_input,
                    text="$"
                    + str(round(sum(params.u_Rmndr), 2))
                    + "/"
                    + str(round(params.u_Goal, 2)),
                ).grid(column=2, row=i + 1, pady=pady)

        def calcCall():
            for i in range(len(params.u_Params)):
                if params.entries[i].get() != "":
                    params.u_Rmndr[i] -= round(float(params.entries[i].get()), 2)
                    params.rmndrs[i] = Label(
                        F_input,
                        text="$"
                        + str(params.u_Rmndr[i])
                        + "/"
                        + str(params.u_Values[i]),
                    )
                    params.rmndrs[i].grid(column=2, row=i, padx=padx, pady=pady)
                if i == len(params.u_Params) - 1:
                    Label(
                        F_input,
                        text="$"
                        + str(round(sum(params.u_Rmndr), 2))
                        + "/"
                        + str(params.u_Goal),
                    ).grid(column=2, row=i + 1, pady=pady)
                params.entries[i].delete(0, 100)

            write()

        calc_B = Button(
            F_input,
            text="CALCUALTE",
            command=lambda: calcCall(),
            font=("Arial Black", 14, "bold"),
            bg="dark green",
            fg="white",
        )
        calc_B.grid(column=0, row=len(params.u_Params) + 1, pady=5, columnspan=2)

        manage_B = Button(
            F_input,
            text="MANAGE",
            command=lambda: self.manageCall(),
            font=("Arial Black", 14, "bold"),
            bg="dark red",
            fg="white",
        )
        manage_B.grid(column=2, row=len(params.u_Params) + 1, pady=5)

    def manageCall(self):
        manageWindow(self.master)
        self.master.withdraw()


####################################################################
####################################################################


class params:
    config.read("config.ini")
    i_wCheck = int(config.get("init", "i_wCheck"))
    u_Params = ast.literal_eval(config.get("user", "u_Params"))
    u_Values = ast.literal_eval(config.get("user", "u_Values"))
    u_Rmndr = ast.literal_eval((config.get("user", "u_Rmndr")))
    u_Rmndr = [round(float(i), 2) for i in u_Rmndr]
    u_Inc = float(config.get("user", "u_Inc"))
    u_Exp = round(sum(u_Values), 2)
    u_Goal = round(float(config.get("user", "u_Goal")), 2)
    labels = [None] * len(u_Params)
    entries = [None] * len(u_Params)
    rmndrs = [None] * len(u_Params)


def recalParams():
    params.u_Exp = sum(params.u_Values)
    params.u_Goal = params.u_Inc - params.u_Exp


def resetWidgets():
    params.labels = [None] * len(params.u_Params)
    params.entries = [None] * len(params.u_Params)
    params.rmndrs = [None] * len(params.u_Params)


def write():
    print("WRITING")

    config.set("user", "u_Rmndr", params.u_Rmndr)
    config.set("user", "u_Params", params.u_Params)
    config.set("user", "u_Values", params.u_Values)
    config.set("user", "u_Inc", params.u_Inc)
    config.set("user", "u_Goal", params.u_Goal)
    config.set("init", "i_wCheck", params.i_wCheck)

    outfile = open("config.ini", "w")
    config.write(outfile)
    outfile.close


def date():
    print("DATE CONFIG")

    sDate = arrow.get("2018-01-01")
    cDate = arrow.now()
    dateDelta = cDate - sDate
    modDelta = dateDelta.days % 7

    if modDelta == 6 and params.i_wCheck == 0:
        for i in range(len(params.u_Params)):
            params.u_Rmndr[i] += params.u_Values[i]
        params.i_wCheck = 1
    elif modDelta != 6 and params.i_wCheck == 1:
        params.i_wCheck = 0

    write()


def getAsset(assetName):
    return f"{sys.path[0]}/assets/{assetName}"


####################################################################
####################################################################
if __name__ == "__main__":
    root = Tk()
    root.tk.call("wm", "iconphoto", root._w, PhotoImage(file=getAsset("icon.png")))
    # root.iconbitmap(getAsset("icon.ico"))
    root.title("Budget Calc.")
    root.tk_setPalette(background="white")
    m = mainWindow(root)
    root.mainloop()
