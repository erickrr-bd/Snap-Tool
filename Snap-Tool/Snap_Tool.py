#! /usr/bin/env python3.12

"""
Main function.
"""
from modules.Snap_Tool_Class import SnapTool

if __name__ == "__main__":
	snap_tool = SnapTool()
	while True:
		snap_tool.main_menu()
		