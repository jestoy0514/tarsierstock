#!/usr/bin/env python3
#
# itemmaster.py - Item master window.
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
from tkinter import messagebox

import sqlite3
import os


class ItemMaster(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title('Item Master')
        self.master.protocol('WM_DELETE_WINDOW', self.appclose)
        self.pack(fill='both', expand=True, padx=5, pady=5)
        self.master.grab_set()

        # Set the icon of the window.
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        self.master.iconbitmap(self.iconlocation)

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
                                    command=self.appclose
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

    def appclose(self):
        # Check whether the database is open, if so close it.
        if self.database:
            self.cur.close()
            self.database.close()
            print('Database successfully closed.')
        self.master.grab_release()
        self.master.destroy()


def main():
    root = tk.Tk()
    ItemMaster(root)
    root.mainloop()

if __name__ == '__main__':
    main()
