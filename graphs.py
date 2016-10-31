import numpy as n
import pandas as pd
import os
import csv
from tkinter import *
import matplotlib.pyplot as plt

symbolsFile = 'simboli.txt'

def getSymbols(file_name):
    list = []
    with open(file_name, encoding='cp1252') as file:
        for line in file:
            if line[1:5].lstrip().rstrip() == '0020':
                list.append(line[16:24].rstrip().lstrip())
    return list

symbols = getSymbols(symbolsFile)

class GUI():

    def __init__(self, master):
        self.izbrani = None
        self.scrollbar = Scrollbar(master)
        self.listbox = Listbox(master, selectmode=BROWSE, activestyle='underline', yscrollcommand=self.scrollbar.set)
        for symbol in symbols:
            self.listbox.insert(END, symbol)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky=N+S, rowspan=7)
        self.listbox.grid(row=1, column=0, sticky=N+S, rowspan=7)
        self.vnosCena = StringVar(master)
        self.vnosKolicina = StringVar(master)
        self.curval = StringVar(master)
        self.purval = StringVar(master)
        self.quant = StringVar(master)
        self.pr = StringVar(master)
        self.total = StringVar(master)

        Label(master, text='Izberi:', font='Verdana 12 bold').grid(row=0, column=0, columnspan=2)

        Label(master, text='Vnos novega nakupa:', font='Verdana 12 bold').grid(row=0, column=2, columnspan=2)
        Label(master, text='Cena delnice ob nakupu').grid(row=1, column=2)
        Label(master, text='Količina').grid(row=2, column=2)
        self.cena = Entry(master, textvariable=self.vnosCena)
        self.kolicina = Entry(master, textvariable=self.vnosKolicina)
        self.cena.grid(row=1, column=3)
        self.kolicina.grid(row=2, column=3)

        Label(master, text='Trenutno stanje:', font='Verdana 12 bold').grid(row=4, column=2, columnspan=2)
        Label(master, text='Trenutna vrednost delnice:').grid(row=5, column=2)
        Label(master, text='Povprečna vrednost delnice ob nakupu:').grid(row=6, column=2)
        Label(master, text='Količina:').grid(row=7, column=2)
        Label(master, text='Skupna vrednost delnic ob nakupu:').grid(row=8, column=2)
        Label(master, text='Profit:').grid(row=9, column=2)
        self.curValue = Entry(master, textvariable=self.curval)
        self.purValue = Entry(master, textvariable=self.purval)
        self.quantity = Entry(master, textvariable=self.quant)
        self.profit = Entry(master, textvariable=self.pr)
        self.totalval = Entry(master, textvariable=self.total)
        self.curValue.grid(row=5, column=3)
        self.purValue.grid(row=6, column=3)
        self.quantity.grid(row=7, column=3)
        self.totalval.grid(row=8, column=3)
        self.profit.grid(row=9, column=3)

        b0 = Button(master, text='Vnesi', command=self.vnesi)
        b0.grid(row=3, column=2, columnspan=2)

        b1 = Button(master, text='Nariši graf', command=self.narisi)
        b1.grid(row=8, column=0, columnspan=2)

        b2 = Button(master, text='Prikaži podatke', command=self.prikazi)
        b2.grid(row=9, column=0, columnspan=2)

    def narisi(self):
        self.izbrani = self.listbox.curselection()
        symbol = self.listbox.get(self.izbrani)
        if len(self.izbrani) == 0:
            print('Ne rišem')
        else:
            plt.close()
            data = pd.read_csv('{}.csv'.format(symbol))['Uradni tecaj']
            plt.plot(range(len(data)), data)
            plt.show()

    def vnesi(self):
        value =  self.vnosCena.get()
        quantity = self.vnosKolicina.get()
        self.izbrani = self.listbox.curselection()
        symbol = self.listbox.get(self.izbrani)
        curdict = {'Cena':value, 'Kolicina':quantity}
        if not os.path.isfile('{}bought.csv'.format(symbol)):
            with open('{}bought.csv'.format(symbol), 'w', newline='', encoding='cp1252') as csv_file:
                writer = csv.DictWriter(csv_file,['Cena', 'Kolicina'])
                writer.writeheader()
                writer.writerow(curdict)
            csv_file.close()
        else:
            with open('{}bought.csv'.format(symbol), 'a', newline='', encoding='cp1252') as csv_file:
                writer = csv.DictWriter(csv_file,['Cena', 'Kolicina'])
                writer.writerow(curdict)
            csv_file.close()


    def prikazi(self):
        curval = 0
        purval = 0
        quant = 0
        profit = 0
        total = 0

        self.izbrani = self.listbox.curselection()
        symbol = self.listbox.get(self.izbrani)
        data = pd.read_csv('{}.csv'.format(symbol))['Uradni tecaj']
        curval = data[len(data)-1]

        if not os.path.isfile('{}bought.csv'.format(symbol)):
            pass
        else:
            data = pd.read_csv('{}bought.csv'.format(symbol))
            kolicina = 0
            vrednost = 0
            for i in range(len(data)):
                kolicina += data.iloc(0)[i]['Kolicina']
                vrednost += data.iloc(0)[i]['Cena']*kolicina

            if kolicina != 0:
                purval = vrednost/kolicina
            quant = kolicina
            total = vrednost

        profit = curval*quant - purval*quant

        self.curval.set(curval)
        self.purval.set(purval)
        self.quant.set(quant)
        self.pr.set(profit)
        self.totalval.set(total)
root = Tk()
aplikacija = GUI(root)
root.mainloop()