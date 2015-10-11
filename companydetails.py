#!/usr/bin/env python3
#
# mainwindow.py - Main window of the tarsierstock application.
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
from tkinter import ttk

import sqlite3


class CompanyDetails(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('Company Details')
        self.master.protocol('WM_DELETE_WINDOW', self.appclose)
        self.pack(fill='both', expand=True)
        self.master.grab_set()
        self.master.resizable(0, 0)

        # Create a header label for the company details.
        self.company_details = ttk.Label(self, text='COMPANY DETAILS',
                                         foreground='orange',
                                         font=('Helvetica', 13, 'bold')
                                         )
        self.company_details.pack()

        # Create a main frame for the company details.
        self.mainframe = tk.Frame(self, bd=1, relief='sunken')
        self.mainframe.pack(expand=True, fill='both', padx=5, pady=5)

        # Initialize the database.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

        # Select the details.
        self.data = self.cur.execute("SELECT * FROM company").fetchall()

        name = ['ORGANIZATION NAME: ', 'ADDRESS: ', 'TELEPHONE: ', 'FAX: ', 'E-MAIL: ']
        counter = 0
        for rows in self.data:
            for row in rows:
                if row == '':
                    row = 'None'
                self.label = ttk.Label(self.mainframe, text=name[counter]+row)
                self.label.pack(anchor='w', padx=5, pady=5)
                counter += 1

    def appclose(self):
        # Check whether the database is open or not, if so close it.
        if self.database:
            self.cur.close()
            self.database.close()
        # Finally destroy the window on exit.
        self.master.grab_release()
        self.master.destroy()


def main():
    app = CompanyDetails()
    app.mainloop()

if __name__ == '__main__':
    main()
