#!/usr/bin/env python3
#
# aboutdialog.py - About window dialog for jvinventory app.
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

import os

# Contant
__appname__ = "Tarsier Stock"
__description__ = "A simple inventory software for small business."
__version__ = "0.1"
__author__ = "Jesus Vedasto Olazo"
__email__ = "jestoy.olazo@gmail.com"
__web__ = "http://www.jvaolazo.net76.net"
__license__ = "GPL2"
__status__ = "Development"
__maintainer__ = "Jesus Vedasto Olazo"
__copyright__ = "Copyright (c) 2015 - Jesus Vedasto Olazo"


class AboutDialog(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('About')
        self.master.protocol('WM_DELETE_WINDOW', self.appclose)
        self.master.resizable(0, 0)
        self.pack(fill='both', expand=True, padx=5, pady=5)
        self.master.grab_set()
        self.iconlocation = os.getcwd() + "/tsicon.ico"
        self.master.iconbitmap(self.iconlocation)
        # Create style.
        self.style = ttk.Style()
        self.style.configure('appname.TLabel',
                             font=('Curlz MT', 20, 'bold'),
                             foreground='red',
                             anchor='center'
                             )
        self.style.configure('ver.TLabel',
                             font=('Helvetica', 12, 'bold'),
                             foreground='blue',
                             anchor='center'
                             )
        self.style.configure('normal.TLabel',
                             font=('Helvetica', 11),
                             foreground='black',
                             anchor='center'
                             )
        # Add labels for application details.
        self.app_name = ttk.Label(self,
                                  text=__appname__,
                                  style='appname.TLabel'
                                  )
        self.app_name.pack(fill='both')
        self.ver = ttk.Label(self,
                             text="version: "+__version__,
                             style='ver.TLabel'
                             )
        self.ver.pack(fill='both')
        self.desc = ttk.Label(self,
                              text=__description__,
                              style='normal.TLabel'
                              )
        self.desc.pack(fill='both')
        self.author = ttk.Label(self,
                                text='Author: '+__author__,
                                style='normal.TLabel'
                                )
        self.author.pack(fill='both')
        self.email = ttk.Label(self,
                               text='E-mail: '+__email__,
                               style='normal.TLabel'
                               )
        self.email.pack(fill='both')
        self.website = ttk.Label(self,
                                 text='Web: '+__web__,
                                 style='normal.TLabel'
                                 )
        self.website.pack(fill='both')
        self.lic = ttk.Label(self,
                             text='License: '+__license__,
                             style='normal.TLabel'
                             )
        self.lic.pack(fill='both')
        self.close_button = ttk.Button(self,
                                       text='Close',
                                       command=self.appclose
                                       )
        self.close_button.pack(anchor='e', padx=8, pady=8)
        self.app_name.focus_set()

    def appclose(self):
        self.master.grab_release()
        self.master.destroy()


def main():
    app = AboutDialog()
    app.mainloop()

if __name__ == '__main__':
    main()
