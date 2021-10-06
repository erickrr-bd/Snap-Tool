#! /usr/bin/env python3

from modules.FormClass import FormDialog

"""
FormDialogs type object.
"""
forms = FormDialog()

"""
Main function of the application
"""
if __name__ == "__main__":	
	while True:
		forms.mainMenu()