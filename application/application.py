#!/usr/bin/env python3
#
# application.py - Module of the tarsierstock application.
#
# Copyright (c) 2015 - Jesus Vedasto Olazo <jessie@jestoy.frihost.net>
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
from tkinter import messagebox
from tkinter import scrolledtext
import os
import csv
import sqlite3
from datetime import date
from datetime import date

__appname__ = "Tarsier Stock"
__description__ = "A simple inventory software for small business."
__version__ = "0.2"
__author__ = "Jesus Vedasto Olazo"
__email__ = "jestoy.olazo@gmail.com"
__web__ = "http://jestoy.frihost.net"
__license__ = "GPLV2"
__status__ = "Development"
__maintainer__ = "Jesus Vedasto Olazo"
__copyright__ = "Copyright (c) 2015 - Jesus Vedasto Olazo"


class ItemOut(tk.Toplevel):

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        # Set the window title.
        self.title('Outgoing')

        # This protocol is used to call the method self.quitApp
        # for exiting the application in proper way and to make
        # sure that the database has been closed.
        self.protocol('WM_DELETE_WINDOW', self.quitApp)

        # Set the window icon.
        try:
            icon = tk.PhotoImage(file='tsicon.gif')
            self.tk.call('wm', 'iconphoto', self._w, icon)
        except:
            print('Sorry an error occured setting the icon.')

        # Initialize the database and the cursor.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

        # Add to labelframe for select item and insert item.
        self.selectframe = ttk.LabelFrame(self, text='Select Item')
        self.selectframe.pack(side='left', anchor='n', fill='both')
        self.insertframe = ttk.LabelFrame(self, text='Outgoing Item')
        self.insertframe.pack(anchor='n',
                              fill='both'
                              )
        self.displayframe = ttk.LabelFrame(self, text='Details')
        self.displayframe.pack(side='bottom', expand=True, fill='both')

        # Add a ttk treeview for the display of transaction.
        self.display_tree = ttk.Treeview(self.displayframe)
        self.display_tree.pack(side='left', expand=True, fill='both')
        self.disyscroll = tk.Scrollbar(self.displayframe,
                                       command=self.display_tree.yview)
        self.disyscroll.pack(side='left', fill='y')
        self.display_tree.config(yscrollcommand=self.disyscroll.set)
        self.column = ('date',
                       'itemcode',
                       'description',
                       'unit', 'rate',
                       'quantity',
                       'amount',
                       'remarks')
        self.heading = ('Date',
                        'Item Code',
                        'Description',
                        'Unit',
                        'Rate',
                        'Quantity',
                        'Amount',
                        'Remarks')
        self.display_tree['columns'] = self.column
        for elem in self.column:
            if elem == 'date':
                col_width = 75
            elif elem == 'itemcode':
                col_width = 85
            elif elem == 'description':
                col_width = 250
            elif elem == 'unit':
                col_width = 35
            elif elem == 'remarks':
                col_width = 175
            else:
                col_width = 100

            if elem == 'remarks':
                self.display_tree.column(elem, width=col_width)
            else:
                self.display_tree.column(elem, width=col_width, stretch=False)

        counter = 0
        self.display_tree.heading('#0', text='S. No.')
        self.display_tree.column('#0', width=50, stretch=False)
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
        self.yscroll = tk.Scrollbar(self.selectframe,
                                    command=self.itemlistbox.yview)
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
                                     command=self.quitApp
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
        quantity = float(self.quantity_entry.get()) * -1
        sdate = datetime.strptime(self.date_entry.get(), '%Y-%m-%d')
        remarks = str(self.remarks_entry.get())
        self.cur.execute("""
                         INSERT INTO outgoing VALUES(null, ?, ?, ?, ?, ?, ?, ?)""",
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

    def insertitemlist(self):
        # Insert item list into the listbox.
        dataquery = self.cur.execute("Select * FROM item")
        rows = dataquery.fetchall()
        for row in rows:
            self.itemlistbox.insert('end', row[1])

    def insertdetails(self):
        # Check if there is any data in the treeview
        # if so delete and load the list again.
        if len(self.display_tree.get_children()) != 0:
            child = self.display_tree.get_children()
            for item in child:
                self.display_tree.delete(item)

        # Initialize the database.
        data = self.cur.execute("""SELECT * FROM outgoing""")
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
            self.display_tree.set(str(row[0]), self.column[6], str(row[4]*row[5]))
            self.display_tree.set(str(row[0]), self.column[7], str(row[7]))
            counter += 1

    def quitApp(self):
        # Check first if the database is open, if so close it.
        if self.database:
            try:
                self.database.commit()
            except sqlite3.Error:
                self.database.rollback()
            self.cur.close()
            self.database.close()
        self.destroy()


class ItemIn(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        # Set the window title.
        self.title('Incoming')

        # This protocol is used to call the method self.quitApp
        # for exiting the application in proper way and to make
        # sure that the database has been closed.
        self.protocol('WM_DELETE_WINDOW', self.quitApp)

        # Set the window icon.
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        try:
            self.iconbitmap(self.iconlocation)
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
                                     command=self.quitApp
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

    def quitApp(self):
        # Check first if the database is open, if so close it.
        if self.database:
            try:
                self.database.commit()
            except sqlite3.Error:
                self.database.rollback()
            self.cur.close()
            self.database.close()
        self.destroy()


class ItemMaster(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title('Item Master')
        self.protocol('WM_DELETE_WINDOW', self.quitApp)
        self.grab_set()

        # Set the icon of the window.
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        try:
            self.iconbitmap(self.iconlocation)
        except:
            pass

        # Initialize the database.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

        # Create 3 main container of the window.
        self.upperframe = tk.Frame(self)
        self.upperframe.pack(fill='both')
        self.lowerframe = tk.Frame(self)
        self.lowerframe.pack(fill='both', expand=True)
        self.buttonframe = tk.Frame(self)
        self.buttonframe.pack(fill='both')

        # Create 3 container for labels, buttons, and entries.
        self.upframe1 = tk.Frame(self.upperframe)
        self.upframe1.pack(side='left')
        self.upframe2 = tk.Frame(self.upperframe)
        self.upframe2.pack(side='left')
        self.upframe3 = tk.Frame(self.upperframe)
        self.upframe3.pack(side='left')

        # Add labels for self.upframe1.
        self.item_code = ttk.Label(self.upframe1, text='Item Code:')
        self.item_code.pack(anchor='w', padx=5, pady=5)
        self.item_desc = ttk.Label(self.upframe1, text='Description:')
        self.item_desc.pack(anchor='w', padx=5, pady=5)
        self.item_unit = ttk.Label(self.upframe1, text='Unit:')
        self.item_unit.pack(anchor='w', padx=5, pady=5)

        # Add entries for self.upframe2
        self.item_code_entry = ttk.Entry(self.upframe2)
        self.item_code_entry.pack(anchor='w', padx=5, pady=5)
        self.item_desc_entry = ttk.Entry(self.upframe2, width=40)
        self.item_desc_entry.pack(anchor='w', padx=5, pady=5)
        self.item_unit_entry = ttk.Entry(self.upframe2, width=10)
        self.item_unit_entry.pack(anchor='w', padx=5, pady=5)
        self.item_unit_entry.bind('<KeyPress>', self.additem_event)

        # Add buttons to self.upframe3
        self.add_btn = ttk.Button(self.upframe3, text='Add')
        self.add_btn.pack(anchor='center', padx=5, pady=5)
        self.add_btn.config(command=self.additem)
        self.delete_btn = ttk.Button(self.upframe3, text='Delete')
        self.delete_btn.pack(anchor='center', padx=5, pady=5)
        self.delete_btn.config(command=self.deleteitem)
        self.search_btn = ttk.Button(self.upframe3, text='Search')
        self.search_btn.pack(anchor='center', padx=5, pady=5)
        self.search_btn.config(command=self.searchitem)

        # Add the tree inside self.lowerframe.
        self.item_display = ttk.Treeview(self.lowerframe)
        self.item_display.pack(side='left',
                               expand=True,
                               fill='both'
                               )
        self.tyscroll = tk.Scrollbar(self.lowerframe,
                                     orient='vertical',
                                     command=self.item_display.yview)
        self.tyscroll.pack(side='left', fill='both')
        self.item_display.config(yscrollcommand=self.tyscroll.set)

        # Add close button to the self.buttonframe
        self.close_btn = ttk.Button(self.buttonframe,
                                    text='Close',
                                    command=self.quitApp
                                    )
        self.close_btn.pack(anchor='e', pady=5)

        # Create the heading of the treeview.
        column = ('itemcode', 'description', 'unit')
        heading = ('Item Code', 'Description', 'Unit')
        self.item_display['columns'] = column
        self.item_display.heading('#0', text='S. No.')
        self.item_display.column('#0', width=35)
        counter = 0
        for hlabel in heading:
            if counter == 0:
                self.item_display.column(column[counter], width=85)
            elif counter == 1:
                self.item_display.column(column[counter], width=175)
            else:
                self.item_display.column(column[counter], width=35)
            self.item_display.heading(column[counter], text=hlabel)
            counter += 1

        # Create tags for the treeview.
        self.item_display.tag_configure('evenrow', background='#FFB586')
        self.item_display.tag_configure('oddrow', background='#FDA46A')

        # Display the items in the treeview.
        self.displayitem()

    def additem(self):
        self.cur.execute("INSERT INTO item VALUES(null, ?, ?, ?)",
                         (self.item_code_entry.get(),
                          self.item_desc_entry.get(),
                          self.item_unit_entry.get())
                         )
        try:
            self.database.commit()
            tk.messagebox.showinfo('Save', 'Saving complete.', parent=self.master)
        except sqlite3.Error:
            self.database.rollback()
            tk.messagebox.showwarning('Save', 'An Error Occured.', parent=self.master)

        # Clear the entries.
        self.item_code_entry.delete(0, 'end')
        self.item_code_entry.insert(0, '')
        self.item_desc_entry.delete(0, 'end')
        self.item_desc_entry.insert(0, '')
        self.item_unit_entry.delete(0, 'end')
        self.item_unit_entry.insert(0, '')

        # Refresh the list of items.
        self.displayitem()
        self.item_code_entry.focus_set()

    def additem_event(self, event):
        if event.keysym == 'Return':
            print('item added')
            self.cur.execute("INSERT INTO item VALUES(null, ?, ?, ?)",
                             (self.item_code_entry.get(),
                              self.item_desc_entry.get(),
                              self.item_unit_entry.get())
                             )
            try:
                self.database.commit()
                tk.messagebox.showinfo('Save', 'Saving complete.', parent=self.master)
            except sqlite3.Error:
                self.database.rollback()

            # Clear the entries.
            self.item_code_entry.delete(0, 'end')
            self.item_code_entry.insert(0, '')
            self.item_desc_entry.delete(0, 'end')
            self.item_desc_entry.insert(0, '')
            self.item_unit_entry.delete(0, 'end')
            self.item_unit_entry.insert(0, '')

            # Refresh the list of items.
            self.displayitem()
            self.item_code_entry.focus_set()

    def deleteitem(self):
        try:
            # Ask if you really want to delete the item.
            askifsure = tk.messagebox.askokcancel('Warning',
                                                  "Delete the item?",
                                                  parent=self.master
                                                  )

            # If answer from askifsure variable is True, delete the item.
            if askifsure is True:
                self.cur.execute("DELETE FROM item WHERE rowid = ?",
                                 (self.item_display.selection()[0]))
                try:
                    self.database.commit()
                except sqlite3.Error:
                    self.database.rollback()
                # Show if the item has been remove from the database.
                tk.messagebox.showinfo('Information',
                                       "Item deleted from the database.",
                                       parent=self.master
                                       )
            # Else do nothing and prompt an info that no item was deleted.
            else:
                tk.messagebox.showinfo('Information',
                                       'No changes has been applied.',
                                       parent=self.master
                                       )
        # If there nothing is selected from the table prompt a warning.
        except IndexError:
            tk.messagebox.showwarning('Warning',
                                      'Please select the item first.',
                                      parent=self.master
                                      )

        # Refresh the table and set the focus to item code entry.
        self.displayitem()
        self.item_code_entry.focus_set()

    def searchitem(self):
        print('item search')
        hello = tk.messagebox.askokcancel('Warning',
                                          'This is a test.',
                                          parent=self.master
                                          )
        print(hello)

    def displayitem(self):
        # Check if there is any data in the treeview
        # if so delete and load the list again.
        if len(self.item_display.get_children()) != 0:
            child = self.item_display.get_children()
            for item in child:
                self.item_display.delete(item)

        # Initialize the database.
        data = self.cur.execute("SELECT * FROM item")
        data_list = data.fetchall()
        column = ('itemcode', 'description', 'unit')
        counter = 1
        if len(data_list) > 0:
            for num in data_list:
                if counter % 2 == 0:
                    self.item_display.insert('',
                                             'end',
                                             str(num[0]),
                                             text=str(num[0]),
                                             tag='evenrow'
                                             )
                else:
                    self.item_display.insert('',
                                             'end',
                                             str(num[0]),
                                             text=str(num[0]),
                                             tag='oddrow'
                                             )
                self.item_display.set(str(num[0]), column[0], str(num[1]))
                self.item_display.set(str(num[0]), column[1], str(num[2]))
                self.item_display.set(str(num[0]), column[2], str(num[3]))
                counter += 1
        self.item_code_entry.focus_set()

    def quitApp(self):
        # Check whether the database is open, if so close it.
        if self.database:
            self.cur.close()
            self.database.close()
            print('Database successfully closed.')
        self.grab_release()
        self.destroy()


class CompanyDetails(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title('Company Details')
        self.protocol('WM_DELETE_WINDOW', self.quitApp)
        self.grab_set()
        self.resizable(0, 0)
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        try:
            self.master.iconbitmap(self.iconlocation)
        except:
            pass

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
                ttk.Label(self.mainframe, text=name[counter]+row).pack(anchor='w', padx=5, pady=5)
                counter += 1

    def quitApp(self):
        # Check whether the database is open or not, if so close it.
        if self.database:
            self.cur.close()
            self.database.close()
        # Finally destroy the window on exit.
        self.grab_release()
        self.destroy()


class CreateDatabase:

    def __init__(self, com_name,
                 com_address,
                 com_telephone,
                 com_fax,
                 com_email
                 ):
        self.com_name = com_name
        self.com_address = com_address
        self.com_telephone = com_telephone
        self.com_fax = com_fax
        self.com_email = com_email
        # Create the database.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

    def create(self):
        # Create item table.
        self.cur.execute("""
            CREATE TABLE item(rowid INTEGER PRIMARY KEY,
                itemcode TEXT,
                description TEXT,
                unit TEXT)
            """)
        # Create incoming transaction table.
        self.cur.execute("""
            CREATE TABLE incoming(rowid INTEGER PRIMARY KEY,
                itemcode TEXT,
                description TEXT,
                unit TEXT,
                quantity REAL,
                rate REAL,
                date DATE,
                remarks TEXT)
            """)
        # Create outgoing transaction table.
        self.cur.execute("""
            CREATE TABLE outgoing(rowid INTEGER PRIMARY KEY,
                itemcode TEXT,
                description TEXT,
                unit TEXT,
                quantity REAL,
                rate REAL,
                date DATE,
                remarks TEXT)
            """)
        # Create company details.
        self.cur.execute("""
            CREATE TABLE company(com_name TEXT,
                com_address TEXT,
                com_telephone TEXT,
                com_fax TEXT,
                com_email TEXT)
            """)
        # Insert company details.
        self.cur.execute("INSERT INTO company VALUES(?, ?, ?, ?, ?)",
                         (self.com_name,
                          self.com_address,
                          self.com_telephone,
                          self.com_fax,
                          self.com_email))
        # Apply the changes.
        try:
            self.database.commit()
        except sqlite3.Error:
            self.database.rollback()
        # Close the database.
        if self.database:
            self.cur.close()
            self.database.close()


class Reports(tk.Toplevel):

    def __init__(self, master):
        """
        Initialize the graphics user interface for stock reporting.
        """
        tk.Toplevel.__init__(self, master)
        self.title('Stock Report')
        self.protocol('WM_DELETE_WINDOW', self.quitApp)
        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        # Set the window icon.
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        try:
            self.iconbitmap(self.iconlocation)
        except:
            pass

        # Initialize the database.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

        # Create a label for the window.
        report_label = ttk.Label(container, text='Stock Report')
        report_label.pack(padx=7, pady=7)
        report_label.config(font=('Helvetica', 15, 'bold'))

        # Create container for the treeview and scrollbar.
        display_frame = tk.Frame(container)
        display_frame.pack(expand=True, fill='both')

        # Create a tkinter.ttk treeview.
        self.display_tree = ttk.Treeview(display_frame)
        self.display_tree.pack(side='left', expand=True, fill='both')

        # Create a scrollbar for the treeview.
        yscrollbar = tk.Scrollbar(display_frame)
        yscrollbar.pack(side='left', fill='y')
        yscrollbar.config(command=self.display_tree.yview)
        self.display_tree.config(yscrollcommand=yscrollbar.set)

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
        self.insertDetails()

        # Create a button below the treeview for exporting
        # the report to a csv file.
        self.export_btn = ttk.Button(self, text='Export',
                                     command=self.exportFile
                                     )
        self.export_btn.pack()

    def insertDetails(self):
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

    def exportFile(self):
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
        messagebox.showinfo('Information', location)

    def quitApp(self):
        """
        This method was created for properly shutting down
        the application. And for the database to close properly.
        """
        if self.database:
            self.cur.close()
            self.database.close()
            print('Database has been closed.')
        self.destroy()


class LicenseWindow(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title("License")
        self.protocol("WM_DELETE_WINDOW", self.quitApp)

        # Create the rest of the widget here.
        mainframe = tk.Frame(self)
        mainframe.pack(expand=True, fill='both')

        self.lic_text = scrolledtext.ScrolledText(mainframe)
        self.lic_text.pack(expand=True, fill='both')

        # Insert details.
        self.insertDetails()

        close_btn = ttk.Button(self, text='Close', command=self.quitApp)
        close_btn.pack(padx=5, pady=5)

    def insertDetails(self):
        lic_file = open("LICENSE", 'r')
        data = lic_file.read()
        lic_file.close()

        self.lic_text.insert('end', data)
        self.lic_text.config(state='disabled')

    def quitApp(self):
        self.destroy()


class AboutDialog(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title('About')
        self.protocol('WM_DELETE_WINDOW', self.quitApp)
        self.resizable(0, 0)
        container = tk.Frame(self)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.grab_set()
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        print(self.iconlocation)
        try:
            self.master.iconbitmap(self.iconlocation)
        except:
            pass
        # Create style.
        style = ttk.Style()
        style.configure('appname.TLabel',
                        font=('Curlz MT', 20, 'bold'),
                        foreground='red',
                        anchor='center'
                        )
        style.configure('ver.TLabel',
                        font=('Helvetica', 12, 'bold'),
                        foreground='blue',
                        anchor='center'
                        )
        style.configure('normal.TLabel',
                        font=('Helvetica', 11),
                        foreground='black',
                        anchor='center'
                        )
        # Add labels for application details.
        app_name = ttk.Label(container,
                             text=__appname__,
                             style='appname.TLabel'
                             )
        app_name.pack(fill='both')
        ver = ttk.Label(container,
                        text="version: "+__version__,
                        style='ver.TLabel'
                        )
        ver.pack(fill='both')
        desc = ttk.Label(container,
                         text=__description__,
                         style='normal.TLabel'
                         )
        desc.pack(fill='both')
        author = ttk.Label(container,
                           text='Author: '+__author__,
                           style='normal.TLabel'
                           )
        author.pack(fill='both')
        email = ttk.Label(container,
                          text='E-mail: '+__email__,
                          style='normal.TLabel'
                          )
        email.pack(fill='both')
        website = ttk.Label(container,
                            text='Web: '+__web__,
                            style='normal.TLabel'
                            )
        website.pack(fill='both')
        lic = ttk.Label(container,
                        text='License: '+__license__,
                        style='normal.TLabel'
                        )
        lic.pack(fill='both')
        close_button = ttk.Button(container,
                                  text='Close',
                                  command=self.quitApp
                                  )
        close_button.pack(anchor='e', padx=8, pady=8)
        close_button.focus_set()

    def quitApp(self):
        self.grab_release()
        self.destroy()


class MainWindow(tk.Frame):

    def __init__(self, master):
        """
        Initialize the graphics user interface for the main window of
        the application. It consist of menubar and 4 buttons for item
        master, incoming and outgoing transaction, and stock report.
        """
        tk.Frame.__init__(self, master)
        # Set the title and position of the window.
        self.master.title(" ".join([__appname__, __version__]))
        self.master.geometry("+100+100")
        self.master.protocol('WM_DELETE_WINDOW', self.quitApp)
        # Disable maximize window.
        self.master.resizable(0, 0)
        self.pack(fill='both', expand=True, padx=5, pady=5)
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        try:
            self.master.iconbitmap(self.iconlocation)
        except:
            pass

        # Create menu bar of the main window.
        self.menubar = tk.Menu(self)
        self.master.config(menu=self.menubar)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.optionmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='Option', menu=self.optionmenu)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        self.filemenu.add_command(label='Quit', command=self.quitApp)
        self.helpmenu.add_command(label='License', command=self.licenseWindow)
        self.helpmenu.add_command(label='Company', command=self.companyDetails)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label='About', command=self.aboutDialog)
        self.optionmenu.add_command(label='Edit Company', command=self.updateDetails)

        # Create 4 buttons for item master, incoming, outgoing, and reports.
        self.item_master_btn = ttk.Button(self, text='Item Master',
                                          command=self.itemMaster
                                          )
        self.item_master_btn.grid(row=0, column=0)
        self.incoming_btn = ttk.Button(self, text='Incoming',
                                       command=self.incoming)
        self.incoming_btn.grid(row=0, column=1)
        self.outgoing_btn = ttk.Button(self, text='Outgoing',
                                       command=self.outgoing)
        self.outgoing_btn.grid(row=0, column=2)
        self.report_btn = ttk.Button(self, text='Reports',
                                     command=self.showReport)
        self.report_btn.grid(row=0, column=3)

        # Check whether database is available
        # if not create database and tables.
        if not os.path.isfile('inv_database.db'):
            self.setCompanyDetails()

    def updateDetails(self):
        """
        This method is for updating the company details if there is a
        some changes needed to done for information puporses and make
        sure that the existing table has been deleted before creating
        a new table for company.
        """
        # Initialize the database and delete company table
        database = sqlite3.connect('inv_database.db')
        cur = database.cursor()
        cur.execute("DROP TABLE IF EXISTS company")
        cur.execute("""
            CREATE TABLE company(com_name TEXT,
                com_address TEXT,
                com_telephone TEXT,
                com_fax TEXT,
                com_email TEXT)
            """)
        self.setcompanydetails()
        self.save_button.grid_forget()
        self.update_button = ttk.Button(self.setcom_frame, text='Update')
        self.update_button.bind('<Button-1>', self.updatecomdetails)
        self.update_button.grid(row=5, column=1, sticky='e')
        if database:
            database.commit()
            cur.close()
            database.close()

    def setCompanyDetails(self):
        """
        This is a toplevel tkinter window for adding or updating
        the company details.
        """
        self.setcom_tp = tk.Toplevel(self.master)
        self.setcom_tp.title('Enter Details')
        self.setcom_tp.protocol('WM_DELETE_WINDOW', self.cancelprogram)
        self.setcom_tp.tkraise(aboveThis=self.master)
        self.setcom_tp.grab_set()
        self.setcom_frame = ttk.LabelFrame(self.setcom_tp,
                                           text='Set Company Details'
                                           )
        self.setcom_frame.pack()
        self.com_name = ttk.Label(self.setcom_frame, text='Company Name:')
        self.com_name.grid(row=0, column=0)
        self.com_addr = ttk.Label(self.setcom_frame, text='Address:')
        self.com_addr.grid(row=1, column=0)
        self.com_tel = ttk.Label(self.setcom_frame, text='Telephone:')
        self.com_tel.grid(row=2, column=0)
        self.com_fax = ttk.Label(self.setcom_frame, text='Fax:')
        self.com_fax.grid(row=3, column=0)
        self.com_email = ttk.Label(self.setcom_frame, text='E-mail:')
        self.com_email.grid(row=4, column=0)

        # Add company details entry.
        self.com_name_entry = ttk.Entry(self.setcom_frame)
        self.com_name_entry.grid(row=0, column=1)
        self.com_addr_entry = ttk.Entry(self.setcom_frame)
        self.com_addr_entry.grid(row=1, column=1)
        self.com_tel_entry = ttk.Entry(self.setcom_frame)
        self.com_tel_entry.grid(row=2, column=1)
        self.com_fax_entry = ttk.Entry(self.setcom_frame)
        self.com_fax_entry.grid(row=3, column=1)
        self.com_email_entry = ttk.Entry(self.setcom_frame)
        self.com_email_entry.grid(row=4, column=1)

        # Create save button.
        self.save_button = ttk.Button(self.setcom_frame, text='Save')
        self.save_button.bind('<Button-1>', self.insertComDetails)
        self.save_button.grid(row=5, column=1, sticky='e')

        # Set the focus to company name entry widget.
        self.com_name_entry.focus_set()

    def cancelprogram(self):
        """
        This method is for checking if company name
        is available. If not these will not create the
        database and instead exit from the application
        gracefully.
        """
        if self.com_name_entry.get() == '':
            self.setcom_tp.grab_release()
            self.setcom_tp.destroy()
            self.master.destroy()
        else:
            self.insert_name = self.com_name_entry.get()
            self.insert_addr = self.com_addr_entry.get()
            self.insert_tel = self.com_tel_entry.get()
            self.insert_fax = self.com_fax_entry.get()
            self.insert_email = self.com_email_entry.get()

            dbase = CreateDatabase(self.insert_name,
                                   self.insert_addr,
                                   self.insert_tel,
                                   self.insert_fax,
                                   self.insert_email
                                   )
            dbase.create()
            self.setcom_tp.grab_release()
            self.setcom_tp.destroy()

    def insertComDetails(self, event):
        """
        This method is a bind event to a tkinter button widget so that
        if the save button has been pressed it will insert the details
        into the database and create the initial database of the program.
        """
        if self.com_name_entry.get() == '':
            self.setcom_tp.grab_release()
            self.setcom_tp.destroy()
            self.master.destroy()
        else:
            self.insert_name = self.com_name_entry.get()
            self.insert_addr = self.com_addr_entry.get()
            self.insert_tel = self.com_tel_entry.get()
            self.insert_fax = self.com_fax_entry.get()
            self.insert_email = self.com_email_entry.get()

            dbase = CreateDatabase(self.insert_name,
                                   self.insert_addr,
                                   self.insert_tel,
                                   self.insert_fax,
                                   self.insert_email
                                   )
            dbase.create()
            self.setcom_tp.grab_release()
            self.setcom_tp.destroy()

    def updatecomdetails(self, event):
        """
        This method will insert the new details for the company
        into the newly created table and close the user interface.
        """
        print(event)
        database = sqlite3.connect('inv_database.db')
        cur = database.cursor()
        cur.execute("INSERT INTO company VALUES(?, ?, ?, ?, ?)",
                    (self.com_name_entry.get(),
                     self.com_addr_entry.get(),
                     self.com_tel_entry.get(),
                     self.com_fax_entry.get(),
                     self.com_email_entry.get()))
        try:
            database.commit()
        except sqlite3.Error:
            database.rollback()

        if database:
            cur.close()
            database.close()

        self.setcom_tp.grab_release()
        self.setcom_tp.destroy()

    def aboutDialog(self):
        """
        This is where you can find the details of the application
        including the name of the app, version, author, email of
        the author, website and license.
        """
        AboutDialog(self)

    def itemMaster(self):
        """
        This method is for adding new items into the database to use
        in the application.
        """
        ItemMaster(self)

    def incoming(self):
        """
        This method is for incoming transactions like deliveries or even
        stock adjustments.
        """
        ItemIn(self)

    def licenseWindow(self):
        """
        This method is for incoming transactions like deliveries or even
        stock adjustments.
        """
        LicenseWindow(self)

    def outgoing(self):
        """
        This method is for outgoing transactions like issues/sales or even
        stock adjustments.
        """
        ItemOut(self)

    def companyDetails(self):
        """
        This is where the details for your company can be found including
        the name of the company, address, telephone and fax number, and
        e-mail provided at the start of the application.
        """
        CompanyDetails(self)

    def showReport(self):
        """
        This method is for showing the user the stock reports for monitoring
        purposes.
        """
        Reports(self)

    def quitApp(self):
        """
        This method is for quitting your application gracefully.
        """
        self.master.destroy()


def main():
    app = tk.Tk()
    MainWindow(app)
    app.mainloop()


if __name__ == '__main__':
    main()
