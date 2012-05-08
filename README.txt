This program is created for mail sending from command-line. It uses the local SMTP facility to deliver emails.
It is able to handle file attachments and HTML encoded body. It is not complete now but capable to handle my tasks (daily reports with HTML body and attachments).

Usage:
---------------------
Usage: mailsender.py [options] file1 file2

Options:
  -h, --help            show this help message and exit
  -f FROM, --from=FROM  E-mail From: field
  -t TO, --to=TO        E-mail To: field (email1@domain1,email2@domain2,...)
  -s SUBJECT, --subject=SUBJECT
                        E-mail Subject: field
  -b BODY, --body file=BODY
                        E-mail body read from this file
  --html                Use it in case of HTML encoded body

This is my first Python program - it is noticable in its quality. Its parts are grabbed from different sources accross the Internet (Google was my friend), you can see the credits in the comments.

László Kurta E-mail:qrtalaci@qrtalaci.com
