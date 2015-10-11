#!/usr/bin/env python3
#
# mainwindow.py - Main window of the jvinventory application.
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


from createdatabase import *
from aboutdialog import *
from itemmaster import *
from companydetails import *
from itemin import *
from itemout import *
from reports import *
from licensewindow import *

# Constant
__appname__ = "Tarsier Stock"
__version__ = "0.1"


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        """
        Initialize the graphics user interface for the main window of
        the application. It consist of menubar and 4 buttons for item
        master, incoming and outgoing transaction, and stock report.
        """
        tk.Frame.__init__(self, master)
        # Set the title of the window.
        self.master.title(__appname__ + " " + __version__)
        # Set the protocol.
        self.master.protocol('WM_DELETE_WINDOW', self.appclose)
        # Disable maximize window.
        self.master.resizable(0, 0)
        self.pack(fill='both', expand=True, padx=5, pady=5)
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        self.master.iconbitmap(self.iconlocation)

        # Create menu bar of the main window.
        self.menubar = tk.Menu(self)
        self.master.config(menu=self.menubar)
        self.filemenu = tk.Menu(self.menubar)
        self.helpmenu = tk.Menu(self.menubar)
        self.optionmenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='Option', menu=self.optionmenu)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        self.filemenu.add_command(label='Quit', command=self.appclose)
        self.helpmenu.add_command(label='License', command=self.licensewindow)
        self.helpmenu.add_command(label='Company', command=self.companydetails)
        self.helpmenu.add_command(label='About', command=self.aboutdialog)
        self.optionmenu.add_command(label='Edit Company', command=self.updatedetails)

        # Create 4 buttons for item master, incoming, outgoing, and reports.
        self.item_master_btn = ttk.Button(self, text='Item Master',
                                          command=self.itemmaster
                                          )
        self.item_master_btn.grid(row=0, column=0)
        self.incoming_btn = ttk.Button(self, text='Incoming',
                                       command=self.incoming)
        self.incoming_btn.grid(row=0, column=1)
        self.outgoing_btn = ttk.Button(self, text='Outgoing',
                                       command=self.outgoing)
        self.outgoing_btn.grid(row=0, column=2)
        self.report_btn = ttk.Button(self, text='Reports',
                                     command=self.showreport)
        self.report_btn.grid(row=0, column=3)

        # Check whether database is available
        # if not create database and tables.
        if os.path.isfile('inv_database.db') is False:
            self.setcompanydetails()

    def updatedetails(self):
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

    def setcompanydetails(self):
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
        self.save_button.bind('<Button-1>', self.insertcomdetails)
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

    def insertcomdetails(self, event):
        """
        This method is a bind event to a tkinter button widget so that
        if the save button has been pressed it will insert the details
        into the database and create the initial database of the program.
        """
        print(event)
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

    def aboutdialog(self):
        """
        This is where you can find the details of the application
        including the name of the app, version, author, email of
        the author, website and license.
        """
        self.about_dialog = tk.Toplevel(self.master)
        AboutDialog(self.about_dialog)

    def itemmaster(self):
        """
        This method is for adding new items into the database to use
        in the application.
        """
        self.item_master_tp = tk.Toplevel(self.master)
        ItemMaster(self.item_master_tp)

    def incoming(self):
        """
        This method is for incoming transactions like deliveries or even
        stock adjustments.
        """
        self.incoming_tp = tk.Toplevel(self.master)
        ItemIn(self.incoming_tp)

    def licensewindow(self):
        """
        This method is for incoming transactions like deliveries or even
        stock adjustments.
        """
        self.license_tp = tk.Toplevel(self.master)
        LicenseWindow(self.license_tp)

    def outgoing(self):
        """
        This method is for outgoing transactions like issues/sales or even
        stock adjustments.
        """
        self.outgoing_tp = tk.Toplevel(self.master)
        ItemOut(self.outgoing_tp)

    def companydetails(self):
        """
        This is where the details for your company can be found including
        the name of the company, address, telephone and fax number, and
        e-mail provided at the start of the application.
        """
        self.com_details_tp = tk.Toplevel(self.master)
        CompanyDetails(self.com_details_tp)

    def showreport(self):
        """
        This method is for showing the user the stock reports for monitoring
        purposes.
        """
        self.showreport_tp = tk.Toplevel(self.master)
        Reports(self.showreport_tp)

    def appclose(self):
        """
        This method is for quitting your application gracefully.
        """
        self.master.destroy()


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
