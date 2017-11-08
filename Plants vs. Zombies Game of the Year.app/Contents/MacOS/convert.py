#!/bin/python
import os
import sys

if len(sys.argv) == 3 and sys.argv[1] in ['windows', 'mac']:
	format=sys.argv[1]
	filename=sys.argv[2]
else:
	print('Usage:\tpython '+os.path.basename(sys.argv[0])+' <windows|mac> user1.dat')
	sys.exit(-1)

import struct
mtime = os.path.getmtime(filename)
userdata=open(filename,'rb')
bytes=open(filename,'rb').read()
userdata.close()
plants=struct.unpack("<L",''.join([bytes[0x330:0x334]]))[0]

if format=='mac' and len(bytes[0x334+plants*0x58:])!=0x44 or format=='windows' and len(bytes[0x334+plants*0x3c:])!=0x44:
	print('Incorrect input format')
	sys.exit(-1)

def convert(plants):
	if format=='mac':
		return plants[:0x14]+plants[0x18:0x1c]+plants[0x20:0x34]+plants[0x38:0x3c]+plants[0x40:0x4c]
	elif format=='windows':
		zeros=''.join([chr(0x00) for i in range(4)])
		return plants[:0x14]+zeros+plants[0x14:0x18]+zeros+plants[0x18:0x2c]+zeros+plants[0x2c:0x30]+zeros+plants[0x30:]+zeros*3

def show(bytes):
	print
	for i in range(len(bytes)):
		print '%02x' %ord(bytes[i]),
		if i%4==3:
			print '|',
		if i%16==15:
			print
	print
		
if format=='mac':
	plants=[bytes[0x334+i*0x58:0x334+(i+1)*0x58] for i in range(plants)]
else:
	plants=[bytes[0x334+i*0x3c:0x334+(i+1)*0x3c] for i in range(plants)]
plants=[convert(i) for i in plants]
show(plants[0])
bytes=bytes[:0x334]+''.join(plants)+bytes[-68:]
userdata=open(filename,'wb')
userdata.write(bytes)
userdata.close()
os.utime(filename,(mtime,mtime))
