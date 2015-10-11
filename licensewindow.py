#!/usr/bin/env python3
#
# licensewindow.py - The license window of tarsier application.
#
# Copyright (c) 2015 - Jesus Vedasto Olazo <jestoy.olazo@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.


import tkinter as tk
from tkinter import ttk, scrolledtext


class LicenseWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("License")
        self.master.protocol("WM_DELETE_WINDOW", self.appclose)
        self.pack(expand=True, fill='both', padx=5, pady=5)

        # Create the rest of the widget here.
        self.mainframe = tk.Frame(self)
        self.mainframe.pack(expand=True, fill='both')

        self.lic_text = scrolledtext.ScrolledText(self.mainframe)
        self.lic_text.pack(expand=True, fill='both')

        # Insert details.
        self.insertdetails()

        self.close_btn = ttk.Button(self, text='Close', command=self.appclose)
        self.close_btn.pack()

    def insertdetails(self):
        lic_file = open("LICENSE", 'r')
        data = lic_file.read()

        self.lic_text.insert('end', data)
        self.lic_text.config(state='disabled')

        lic_file.close()

    def appclose(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    LicenseWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
