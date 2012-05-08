import smtplib
import os
from optparse import OptionParser
from HTMLParser import HTMLParser
from traceback import print_exc
from sys import stderr
from re import sub
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

# original source: http://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()

def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text

# original source: http://dzone.com/snippets/send-email-attachments-python
def send_mail(send_from, send_to, subject, text, files=[], html=None, server="localhost"):
  assert type(send_to)==list
  assert type(files)==list

  if html:
    msg = MIMEMultipart('alternative')
    textbody = dehtml(text)
    part1 = MIMEText(textbody, 'plain')
    part2 = MIMEText(text, 'html')
    msg.attach(part1)
    msg.attach(part2)
  else:  
    msg = MIMEMultipart()
    msg.attach( MIMEText(text) )

  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject
  
  for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

  smtp = smtplib.SMTP(server)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()

def main():
  usage = "usage: %prog [options] file1 file2"
  parser = OptionParser(usage=usage)
  parser.add_option("-f", "--from",
      metavar="FROM", help="E-mail From: field", dest="fromx")
  parser.add_option("-t", "--to",
      metavar="TO", help="E-mail To: field (email1@domain1,email2@domain2,...)")
  parser.add_option("-s", "--subject",
      metavar="SUBJECT", help="E-mail Subject: field", default="-")
  parser.add_option("-b", "--body file",
      metavar="BODY", help="E-mail body read from this file", dest="body")
  parser.add_option("--html",
      metavar="HTML", help="Use it in case of HTML encoded body", dest="html", action="store_true", default=False)
  (options, args) = parser.parse_args()

  if options.body is None:
    print "\nA mandatory body option is missing\n"
    parser.print_help()
    exit(-1)

  bodyfile=open(options.body)
  send_mail(options.fromx, options.to.split(','), options.subject , bodyfile.read(), args, options.html)

if __name__ == '__main__':
  main()

