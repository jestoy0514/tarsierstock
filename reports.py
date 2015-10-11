#!/usr/bin/env python3
#
# reports.py - The reports window.
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
from tkinter import ttk, messagebox

import sqlite3
import csv
import os


class Reports(tk.Frame):

    def __init__(self, master):
        """
        Initialize the graphics user interface for stock reporting.
        """
        tk.Frame.__init__(self, master)
        self.master.title('Stock Report')
        self.master.protocol('WM_DELETE_WINDOW', self.appclose)
        self.pack(fill='both', expand=True)

        # Set the window icon.
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        self.master.iconbitmap(self.iconlocation)

        # Initialize the database.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

        # Create a label for the window.
        self.report_label = ttk.Label(self, text='Stock Report')
        self.report_label.pack(padx=7, pady=7)
        self.report_label.config(font=('Helvetica', 15, 'bold'))

        # Create container for the treeview and scrollbar.
        self.display_frame = tk.Frame(self)
        self.display_frame.pack(expand=True, fill='both')

        # Create a tkinter.ttk treeview.
        self.display_tree = ttk.Treeview(self.display_frame)
        self.display_tree.pack(side='left', expand=True, fill='both')

        # Create a scrollbar for the treeview.
        self.yscrollbar = tk.Scrollbar(self.display_frame)
        self.yscrollbar.pack(side='left', fill='y')
        self.yscrollbar.config(command=self.display_tree.yview)
        self.display_tree.config(yscrollcommand=self.yscrollbar.set)

        # Initialize column and heading variable.
        self.headers = ('Item Code',
                        'Description',
                        'Unit',
                        'In',
                        'Out',
                        'Balance'
                        )
        
        self.column = ('itemcode',
                       'description',
                       'unit',
                       'incoming',
                       'outgoing',
                       'balance'
                       )

        # Set the column of the tree.
        self.display_tree['columns'] = self.column

        # Set the heading of the tree and the width of each column.
        counter = 0
        self.display_tree.heading('#0', text='S. No.')
        self.display_tree.column('#0', width=40)
        for head in self.column:
            if head == 'itemcode':
                setwidth = 85
            elif head == 'description':
                setwidth = 180
            else:
                setwidth = 50
            self.display_tree.heading(head, text=self.headers[counter])
            self.display_tree.column(head, width=setwidth)
            counter += 1
        # Create tags for treeview.
        self.display_tree.tag_configure('evenrow', background='#FFB586')
        self.display_tree.tag_configure('oddrow', background='#FDA46A')

        # Insert the details to the tree.
        self.insertdetails()

        # Create a button below the treeview for exporting
        # the report to a csv file.
        self.export_btn = ttk.Button(self, text='Export',
                                     command=self.exportfile
                                     )
        self.export_btn.pack()

    def insertdetails(self):
        """
        This method is for inserting all the details from the database
        to the treeview so that it can be shown to the user the total
        incoming and outgoing items and the balance for each items in the
        item master listing.
        """
        # Combine incoming and outgoing material
        item_table = self.cur.execute("SELECT * FROM item")
        item_table_fetch = item_table.fetchall()
        in_table = self.cur.execute("SELECT itemcode, quantity FROM incoming")
        in_table_fetch = in_table.fetchall()
        out_table = self.cur.execute("SELECT itemcode, quantity FROM outgoing")
        out_table_fetch = out_table.fetchall()

        counter = 1
        for elem in item_table_fetch:
            if counter % 2 == 0:
                self.display_tree.insert('', 'end', str(elem[0]), text=str(elem[0]), tag=('evenrow',))
            else:
                self.display_tree.insert('', 'end', str(elem[0]), text=str(elem[0]), tag=('oddrow',))
            self.display_tree.set(str(elem[0]), self.column[0], str(elem[1]))
            self.display_tree.set(str(elem[0]), self.column[1], str(elem[2]))
            self.display_tree.set(str(elem[0]), self.column[2], str(elem[3]))
            itotal = 0
            for inqty in in_table_fetch:
                if inqty[0] == elem[1]:
                    itotal += inqty[1]
            self.display_tree.set(str(elem[0]), self.column[3], str(itotal))
            ototal = 0
            for outqty in out_table_fetch:
                if outqty[0] == elem[1]:
                    ototal += outqty[1]
            self.display_tree.set(str(elem[0]), self.column[4], str(ototal))
            self.display_tree.set(str(elem[0]), self.column[5], str(itotal + ototal))
            counter += 1

    def exportfile(self):
        """
        This method is for exporting the stock report into a csv file
        for further editing due to lack of printing support from tkinter
        module. From the csv file they can manipulate easily the details
        so that it can be print into the printer with ease and report can
        be easily forwarded via e-mail.
        """
        # Initialize the data to be shown
        item_table = self.cur.execute("SELECT * FROM item")
        item_table_fetch = item_table.fetchall()
        in_table = self.cur.execute("SELECT itemcode, quantity FROM incoming")
        in_table_fetch = in_table.fetchall()
        out_table = self.cur.execute("SELECT itemcode, quantity FROM outgoing")
        out_table_fetch = out_table.fetchall()

        # Start saving it into a csv file.
        with open('exportfile.csv', 'w', newline='') as csvfile:
            cwriter = csv.writer(csvfile, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # Write the title of the report.
            cwriter.writerow(['Stock Report - Al Hamra Maintenance'])
            # Then write the header of the report.
            cwriter.writerow(['S. No.',
                              'Item Code',
                              'Description',
                              'Unit',
                              'In',
                              'Out',
                              'Balance'
                              ])
            # Start writing the details into the csv file.
            for row in item_table_fetch:
                
                # Check the itemcode if there is any in transaction.
                # if so, sum the quantity of that transaction.
                itotal = 0
                for inqty in in_table_fetch:
                    if inqty[0] == row[1]:
                        itotal += inqty[1]

                ototal = 0
                
                # Check the itemcode if there is any out transaction.
                # if so, sum the quantity of that transaction.
                for outqty in out_table_fetch:
                    if outqty[0] == row[1]:
                        ototal += outqty[1]
                # Start writing the details in the csv file.  
                cwriter.writerow([row[0],
                                  row[1],
                                  row[2],
                                  row[3],
                                  itotal,
                                  ototal,
                                  itotal+ototal
                                  ])
        # Once all the details has been saved to the excel.
        # Show some confirmation.
        # Declare also a location variable so that it can be
        # shown to the user where the file has been saved.
        location = "Report has been exported to csv file.\n\n" + "Location: " + os.getcwd()
        tk.messagebox.showinfo('Information', location)

    def appclose(self):
        """
        This method was created for properly shutting down
        the application. And for the database to close properly.
        """
        if self.database:
            self.cur.close()
            self.database.close()
            print('Database has been closed.')
        self.master.destroy()


def main():
    root = tk.Tk()
    Reports(root)
    root.mainloop()


if __name__ == '__main__':
    main()
