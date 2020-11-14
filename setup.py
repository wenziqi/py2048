#-*-coding: UTF-8-*-

from distutils.core import setup
import py2exe

INCLUDES = ["sip"]
options = {
	"py2exe" :  
	{	"compressed" : 1,  
		"optimize" : 2,  
		"bundle_files" : 1,  
		"includes" : INCLUDES,  
		"dll_excludes": ["w9xpopen.exe"],
	}
}


info={
	"script": "main.py",
	"icon_resources": [(1, "2048.ico")] ,
}
setup(
	options = options, 
	description = "2048 game",
	name="2048",
	zipfile=None,
	windows=[info,],
)