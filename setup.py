import sys
from cx_Freeze import setup,Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python36-32\\tcl\\tk8.6"

includefiles 		= ['.git/*', 'font/*', 'css.css', 'html.html', 'jquery.min.js', 'script.js']
include 			= ['control.py', 'start.py', 'sysVar.py', 'usb.py', 'utils.py', 'webUser.py']
packages 			= ['os', 'sys', 'time', 'get', 'serial']
exclude 			= ['tkinter']

if sys.platform == "win32":
    base = "Win32GUI"

setup(
	name 			= 'egg Force One',
	version 		= '0.0',
	description 	= 'controller for all fdm printer',
	author 			= 'Casal Guillaume',
	author_email 	= '',
	option 			= {'build_exe': {'includes':include, 'packages':packages, 'exclude':exclude, 'include_files':includefiles}},
	executables 	= [Executable("main.py")]
	)
