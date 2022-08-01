#! /usr/bin/env python3

from modules.Snap_Tool_Class import SnapTool

"""
Attribute that stores an object of the SnapTool class.
"""
snap_tool = SnapTool()

"""
Main function of the application
"""
if __name__ == "__main__":	
	while True:
		snap_tool.mainMenu()