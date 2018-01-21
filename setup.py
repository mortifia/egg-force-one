import sys
from cx_Freeze import setup,Executable

includefiles 		= ['.git/*', 'font/*', 'css.css', 'html.html', 'jquery.min.js', 'script.js']
include 			= ['cam.py', 'control.py', 'start.py', 'sysVar.py', 'usb.py', 'utils.py', 'webUser.py']
packages 			= ['os', 'sys', ]

if sys.platform == "win32":
	base = "Win32GUI"

setup(
	name 			= 'egg Force One',
	version 		= '0.0',
	description 	= 'controller for all fdm printer',
	author 			= 'Casal Guillaume',
	author_email 	= '',
	option 			= {'build_exe': {'includes':include, 'packages':packages, 'include_files':includefiles}},
	#executables 	= [Executable("main.py", base = base)]
	executables 	= [Executable("main.py")]
	)
