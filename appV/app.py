from tkBuilder import *
import tkinter as tk
import xml.dom.minidom
import cssutils

APP_PATH 	= 'app.xml'

class myApp(Builder):
	def __init__(self, appPath, style=None):
		super().__init__(appPath)
		self.build()

app = myApp(APP_PATH)
app.mainloop()