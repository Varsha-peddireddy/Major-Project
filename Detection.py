#! /usr/bin/env python
#  -*- coding: utf-8 -*-

from re import S
import sys
import os
import glob
import csv
from datetime import datetime
from email_service import send_challan

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from tkinter import messagebox

try:
    import ttk
except ImportError:
    import tkinter.ttk as ttk

import Detection_support


def vp_start_gui():
    global root
    root = tk.Tk()
    Detection_support.set_Tk_var()
    top = Detection(root)
    Detection_support.init(root, top)
    root.mainloop()


class Detection:
    def __init__(self, top=None):

        self.index = 0
        self.ChallanImg = -1
        self.listFiles = glob.glob('output/*.txt')

        # ---------------- SEND CHALLAN ---------------- #
        def sendChalan(event):
            try:
                helmet = self.cmbHelmetStatus.get()
                plateNumber = self.txtPlateNumber.get().strip()
                noOfPassengers = self.txtPassengers.get()

                amount = 0

                if helmet == "Not Wearing":
                    amount += 500

                if noOfPassengers != "":
                    if int(noOfPassengers) >= 3:
                        amount += 1000

                if plateNumber == "":
                    messagebox.showerror("Error", "Plate Number is empty!")
                    return

                print("Sending Challan ->", plateNumber, "Amount:", amount)

                send_challan(plateNumber, amount)

                messagebox.showinfo('Success', 'Challan mail sent Successfully')

            except Exception as e:
                messagebox.showerror('Error', str(e))

        # ---------------- SHOW IMAGE DATA ---------------- #
        def showOutput(event):
            try:
                data = open(self.listFiles[self.index]).read().split('\n')

                self.img = tk.PhotoImage(file=data[0])
                self.lblRider.configure(image=self.img)

                # Helmet
                if data[1] == "True":
                    self.cmbHelmetStatus.set('Wearing')
                elif data[1] == "False":
                    self.cmbHelmetStatus.set('Not Wearing')
                else:
                    self.cmbHelmetStatus.set('Not Found')

                # Plate
                if data[3] != "None":
                    self.txtPlateNumber.delete(0, "end")
                    self.txtPlateNumber.insert(0, data[3])

                self.txtPassengers.delete(0, "end")
                self.txtPassengers.insert(0, data[4])

                if data[2] == "True":
                    self.cmbPlateStatus.set('Visible')
                elif data[2] == "False":
                    self.cmbPlateStatus.set('Not Visible')
                else:
                    self.cmbPlateStatus.set('Not Found')

                self.index += 1
                self.ChallanImg += 1

            except:
                messagebox.showinfo('Info', 'No More Images')

        # ---------------- WINDOW ---------------- #
        top.geometry("1469x907+249+68")
        top.title("Smart Traffic Violation Detection System")
        top.state("zoomed")

        # Title
        self.Label1 = tk.Label(top, text="Smart Traffic Violation Detection System",
                               font=("Segoe UI", 28))
        self.Label1.place(relx=0.05, rely=0.02)

        # Image Label
        self.lblRider = tk.Label(top, bg="#d2d2d2", width=80, height=30)
        self.lblRider.place(relx=0.05, rely=0.1)

        # Right Frame
        self.Frame1 = tk.Frame(top, relief='groove', borderwidth=2)
        self.Frame1.place(relx=0.55, rely=0.1, relheight=0.8, relwidth=0.4)

        # Helmet
        tk.Label(self.Frame1, text="Helmet Status:",
                 font=("Segoe UI", 18)).place(relx=0.1, rely=0.05)
        self.cmbHelmetStatus = ttk.Combobox(self.Frame1,
                                            values=['Wearing', 'Not Wearing', 'Not Found'])
        self.cmbHelmetStatus.place(relx=0.55, rely=0.05, relwidth=0.35)

        # Plate Status
        tk.Label(self.Frame1, text="Number Plate:",
                 font=("Segoe UI", 18)).place(relx=0.1, rely=0.18)
        self.cmbPlateStatus = ttk.Combobox(self.Frame1,
                                           values=['Visible', 'Not Visible', 'Not Found'])
        self.cmbPlateStatus.place(relx=0.55, rely=0.18, relwidth=0.35)

        # Plate Number
        tk.Label(self.Frame1, text="Plate Number:",
                 font=("Segoe UI", 18)).place(relx=0.1, rely=0.32)
        self.txtPlateNumber = tk.Entry(self.Frame1)
        self.txtPlateNumber.place(relx=0.55, rely=0.32, relwidth=0.35)

        # Passengers
        tk.Label(self.Frame1, text="No. Passengers:",
                 font=("Segoe UI", 18)).place(relx=0.1, rely=0.46)
        self.txtPassengers = tk.Entry(self.Frame1)
        self.txtPassengers.place(relx=0.55, rely=0.46, relwidth=0.35)

        # Buttons
        self.btnSendChallan = tk.Button(self.Frame1, text="Send Challan",
                                        command=lambda: sendChalan(None))
        self.btnSendChallan.place(relx=0.1, rely=0.65, width=200)

        self.btnNextImage = tk.Button(self.Frame1, text="Next Image",
                                      command=lambda: showOutput(None))
        self.btnNextImage.place(relx=0.55, rely=0.65, width=200)

        self.btnExit = tk.Button(self.Frame1, text="EXIT", bg="#d8368c",
                                 fg="white", command=top.destroy)
        self.btnExit.place(relx=0.3, rely=0.82, width=200)

        showOutput(None)


#vp_start_gui()