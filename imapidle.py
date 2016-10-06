# Copyright (c) 2012 Mathieu Lecarme
# This code is licensed under the MIT license (see LICENSE for details)

import imaplib


def idle(connection):
    tag = connection._new_tag()
    connection.send("%s IDLE\r\n" % tag)
    response = connection.readline()
    connection.loop = True
    if response == '+ idling\r\n':
        while connection.loop:
            resp = connection.readline()
            yield resp
           # uid, message = resp[2:-2].split(' ')
           # yield uid, message
    else:
        raise Exception("IDLE not handled? : %s" % response)


def done(connection):
    connection.send("DONE\r\n")
    connection.loop = False

imaplib.IMAP4.idle = idle
imaplib.IMAP4.done = done
