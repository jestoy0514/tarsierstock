#!/usr/bin/env python3
#
# itemin.py - The incoming delivery window.
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
from datetime import date, datetime
import os


class ItemIn(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Set the window title.
        self.master.title('Incoming')

        # This protocol is used to call the method self.appclose
        # for exiting the application in proper way and to make
        # sure that the database has been closed.
        self.master.protocol('WM_DELETE_WINDOW', self.appclose)

        # Set the geometry placement manager for the window.
        self.pack(fill='both', expand=True, padx=5, pady=5)

        # Set the window icon.
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        try:
            self.master.iconbitmap(self.iconlocation)
        except:
            pass

        # Initialize the database and the cursor.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

        # Add to labelframe for select item and insert item.
        self.selectframe = ttk.LabelFrame(self, text='Select Item')
        self.selectframe.pack(side='left', anchor='n', fill='both')
        self.insertframe = ttk.LabelFrame(self, text='Incoming Item')
        self.insertframe.pack(anchor='n',
                              fill='both'
                              )
        self.displayframe = ttk.LabelFrame(self, text='Details')
        self.displayframe.pack(side='bottom', expand=True, fill='both')

        # Add a ttk treeview for the display of transaction.
        self.display_tree = ttk.Treeview(self.displayframe)
        self.display_tree.pack(side='left', expand=True, fill='both')
        self.disyscroll = tk.Scrollbar(self.displayframe, command=self.display_tree.yview)
        self.disyscroll.pack(side='left', fill='y')
        self.display_tree.config(yscrollcommand=self.disyscroll.set)
        self.column = ('date', 'itemcode', 'description', 'unit', 'rate', 'quantity', 'amount', 'remarks')
        self.heading = ('Date',
                        'Item Code',
                        'Description',
                        'Unit',
                        'Rate',
                        'Quantity',
                        'Amount',
                        'Remarks'
                        )
        self.display_tree['columns'] = self.column
        for elem in self.column:
            if elem == 'date':
                col_width = 75
            elif elem == 'itemcode':
                col_width = 85
            elif elem == 'description':
                col_width = 200
            elif elem == 'unit':
                col_width = 35
            elif elem == 'remarks':
                col_width = 175
            else:
                col_width = 100
            self.display_tree.column(elem, width=col_width)

        counter = 0
        self.display_tree.heading('#0', text='S. No.')
        self.display_tree.column('#0', width=35)
        for elem in self.column:
            self.display_tree.heading(elem, text=self.heading[counter])
            counter += 1
        # Create tags for treeview.
        self.display_tree.tag_configure('evenrow', background='#FFB586')
        self.display_tree.tag_configure('oddrow', background='#FDA46A')

        # Add a delete and edit button for under tree view for
        # database manipulation and editing.
        self.delete_btn = ttk.Button(self.displayframe, text='Delete')
        self.delete_btn.pack(padx=5, pady=5)
        self.edit_btn = ttk.Button(self.displayframe, text='Edit')
        self.edit_btn.pack(padx=5, pady=5)

        # Create and add a list box and a entry inside selectframe.
        self.searchitem_entry = ttk.Entry(self.selectframe)
        self.searchitem_entry.pack(fill='x')
        self.searchitem_entry.bind('<KeyPress>', self.refreshlist)
        self.itemlistbox = tk.Listbox(self.selectframe)
        self.itemlistbox.pack(side='left', fill='both')
        self.yscroll = tk.Scrollbar(self.selectframe, command=self.itemlistbox.yview)
        self.yscroll.pack(side='left', fill='y')
        self.itemlistbox.config(yscrollcommand=self.yscroll.set)
        self.itemlistbox.bind('<Double-Button-1>', self.selectitem)

        # Insert item list into the listbox.
        self.insertitemlist()

        # Create labels inside the insert frame.
        self.date_label = ttk.Label(self.insertframe, text='Date:')
        self.date_label.grid(row=0, column=0, sticky='w')
        self.itemcode_label = ttk.Label(self.insertframe, text='Item Code:')
        self.itemcode_label.grid(row=1, column=0, sticky='w')
        self.descp_label = ttk.Label(self.insertframe, text='Description:')
        self.descp_label.grid(row=2, column=0, sticky='w')
        self.unit_label = ttk.Label(self.insertframe, text='Unit:')
        self.unit_label.grid(row=3, column=0, sticky='w')
        self.rate_label = ttk.Label(self.insertframe, text='Rate:')
        self.rate_label.grid(row=4, column=0, sticky='w')
        self.quantity_label = ttk.Label(self.insertframe, text='Quantity:')
        self.quantity_label.grid(row=5, column=0, sticky='w')
        self.remarks_label = ttk.Label(self.insertframe, text='Remarks')
        self.remarks_label.grid(row=6, column=0, sticky='w')

        # Create entries inside the insert frame.
        self.date_entry = ttk.Entry(self.insertframe)
        self.date_entry.grid(row=0, column=1, sticky='w')
        self.itemcode_entry = ttk.Entry(self.insertframe)
        self.itemcode_entry.grid(row=1, column=1, sticky='w')
        self.descp_entry = ttk.Entry(self.insertframe, width=40)
        self.descp_entry.grid(row=2, column=1, sticky='w')
        self.unit_entry = ttk.Entry(self.insertframe, width=10)
        self.unit_entry.grid(row=3, column=1, sticky='w')
        self.rate_entry = ttk.Entry(self.insertframe, width=20)
        self.rate_entry.grid(row=4, column=1, sticky='w')
        self.quantity_entry = ttk.Entry(self.insertframe, width=20)
        self.quantity_entry.grid(row=5, column=1, sticky='w')
        self.remarks_entry = ttk.Entry(self.insertframe, width=40)
        self.remarks_entry.grid(row=6, column=1, sticky='w')

        # Create cancel save button
        self.cancel_btn = ttk.Button(self.insertframe,
                                     text='Cancel',
                                     command=self.appclose
                                     )
        self.cancel_btn.grid(row=7, column=1, sticky='e')
        self.save_btn = ttk.Button(self.insertframe,
                                   text='Save',
                                   command=self.saveentry
                                   )
        self.save_btn.grid(row=8, column=1, sticky='e')
        self.insertdetails()

        # Insert today's date.
        today = date.strftime(date.today(), '%Y-%m-%d')
        self.date_entry.insert(0, today)
        self.itemcode_entry.focus_set()

    def insertitemlist(self):
        # Insert item list into the listbox.
        dataquery = self.cur.execute("Select * FROM item")
        rows = dataquery.fetchall()
        for row in rows:
            self.itemlistbox.insert('end', row[1])

    def selectitem(self, event):
        print(event)
        self.itemcode_entry.delete(0, 'end')
        self.descp_entry.delete(0, 'end')
        self.unit_entry.delete(0, 'end')
        searchvalue = self.itemlistbox.get('active')
        forquery = "SELECT description, unit FROM item WHERE itemcode='" + str(searchvalue) + "'"
        descpquery = self.cur.execute(forquery)
        insertvalue = descpquery.fetchone()
        dvalue = insertvalue[0]
        uvalue = insertvalue[1]
        print(dvalue)
        print(uvalue)
        self.itemcode_entry.insert('end', str(searchvalue))
        self.descp_entry.insert('end', str(dvalue))
        self.unit_entry.insert('end', str(uvalue))

    def saveentry(self):
        itemcode = str(self.itemcode_entry.get())
        description = str(self.descp_entry.get())
        unit = str(self.unit_entry.get())
        rate = float(self.rate_entry.get())
        quantity = float(self.quantity_entry.get())
        sdate = datetime.strptime(self.date_entry.get(), '%Y-%m-%d')
        remarks = str(self.remarks_entry.get())
        self.cur.execute("""
            INSERT INTO incoming VALUES(null, ?, ?, ?, ?, ?, ?, ?)""",
                         (itemcode, description, unit, quantity, rate, sdate, remarks)
                         )
        self.insertdetails()

        # Clear the entries on save except date.
        self.itemcode_entry.delete('0', 'end')
        self.descp_entry.delete('0', 'end')
        self.unit_entry.delete('0', 'end')
        self.rate_entry.delete('0', 'end')
        self.quantity_entry.delete('0', 'end')
        self.remarks_entry.delete('0', 'end')

    def refreshlist(self, event):
        print(event.char)
        if event.keysym == 'Return':
            if self.searchitem_entry.get() == '':
                self.insertitemlist()
            else:
                item = self.searchitem_entry.get()
                # test = "SELECT itemcode FROM item WHERE itemcode MATCH :?", (item)
                model = "SELECT itemcode FROM item WHERE itemcode=" + item
                dataquery = self.cur.execute(model)
                datafetch = dataquery.fetchall()
                for data in datafetch:
                    print(data[0])
                    self.itemlistbox.delete('0', 'end')
                    self.itemlistbox.insert('end', data[0])

    def insertdetails(self):
        # Check if there is any data in the treeview
        # if so delete and load the list again.
        if len(self.display_tree.get_children()) != 0:
            child = self.display_tree.get_children()
            for item in child:
                self.display_tree.delete(item)

        # Initialize the database.
        data = self.cur.execute("""SELECT * FROM incoming""")
        rows = data.fetchall()

        # insert the report into the tree.
        counter = 1
        for row in rows:
            if counter % 2 == 0:
                self.display_tree.insert('', 'end', str(row[0]), text=str(row[0]), tag=('evenrow',))
            else:
                self.display_tree.insert('', 'end', str(row[0]), text=str(row[0]), tag=('oddrow',))
            self.display_tree.set(str(row[0]), self.column[0], str(row[6]))
            self.display_tree.set(str(row[0]), self.column[1], str(row[1]))
            self.display_tree.set(str(row[0]), self.column[2], str(row[2]))
            self.display_tree.set(str(row[0]), self.column[3], str(row[3]))
            self.display_tree.set(str(row[0]), self.column[4], str(row[5]))
            self.display_tree.set(str(row[0]), self.column[5], str(row[4]))
            self.display_tree.set(str(row[0]), self.column[6], str(row[4] * row[5]))
            self.display_tree.set(str(row[0]), self.column[7], str(row[7]))
            counter += 1

    def appclose(self):
        # Check first if the database is open, if so close it.
        if self.database:
            try:
                self.database.commit()
            except sqlite3.Error:
                self.database.rollback()
            self.cur.close()
            self.database.close()
        self.master.destroy()


def main():
    root = tk.Tk()
    ItemIn(root)
    root.mainloop()


if __name__ == '__main__':
    main()
