from flask import Flask, request
import led_matrix_vis_test_all as t
from twilio.twiml.messaging_response import Message, MessagingResponse
import webbrowser

# webbrowser.open("https://www.twilio.com/console/phone-numbers/PNc2480db697222fd47d47b60eb6465898#")

"""Last login: Tue Jul 30 14:42:38 on ttys001
/Users/martingleave/Downloads/ngrok ; exit;
(base) dhcp-10-32-82-110:~ martingleave$ /Users/martingleave/Downloads/ngrok ; exit;
NAME:
   ngrok - tunnel local ports to public URLs and inspect traffic

DESCRIPTION:
    ngrok exposes local networked services behinds NATs and firewalls to the
    public internet over a secure tunnel. Share local websites, build/test
    webhook consumers and self-host personal services.
    Detailed help for each command is available with 'ngrok help <command>'.
    Open http://localhost:4040 for ngrok's web interface to inspect traffic.

EXAMPLES:
    ngrok http 80                    # secure public URL for port 80 web server
    ngrok http -subdomain=baz 8080   # port 8080 available at baz.ngrok.io
    ngrok http foo.dev:80            # tunnel to host:port instead of localhost
    ngrok http https://localhost     # expose a local https server
    ngrok tcp 22                     # tunnel arbitrary TCP traffic to port 22
    ngrok tls -hostname=foo.com 443  # TLS traffic for foo.com to port 443
    ngrok start foo bar baz          # start tunnels from the configuration file

VERSION:
   2.3.34

AUTHOR:
  inconshreveable - <alan@ngrok.com>

COMMANDS:
   authtoken	save authtoken to configuration file
   credits	prints author and licensing information
   http		start an HTTP tunnel
   start	start tunnels by name from the configuration file
   tcp		start a TCP tunnel
   tls		start a TLS tunnel
   update	update ngrok to the latest version
   version	print the version string
   help		Shows a list of commands or help for one command
logout
Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.

[Process completed]

To run:

sudo python /Users/martingleave/Documents/GitHub/JG_rasp-1/app.py
/Users/martingleave/Documents/GitHub/JG_rasp-1/ngrok http 8080
https://www.twilio.com/console/phone-numbers/PNc2480db697222fd47d47b60eb6465898#
"""


app = Flask(__name__)
resp = MessagingResponse()


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    message = message_body.split(" -")
    parse_sms(message)
    # t.composite_test()

    return str(resp)


def parse_sms(m: str):
    print(m)

    for command in m:
        if "-help" in command:
            resp.message("-\n\n*****************\n"
                         "Enter any of these commands!\n"
                         "-")

        if "-spectrogram" in command:
            print("spectrogram")

        if "-text" in command:
            text = command[5]
            print(text)


if __name__ == '__main__':
    app.run(port=8080)




