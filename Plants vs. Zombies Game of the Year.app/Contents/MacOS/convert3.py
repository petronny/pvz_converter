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
_bytes=open(filename,'rb').read()
userdata.close()
version=_bytes[0]

if version!=12:
	print('Unsupported userdata version %d' %version)
	print('Please upload "%s" to somewhere (Google Drive, Dropbox, etc.) and issue its link to https://github.com/petronny/pvz_converter/issues' %filename)
	sys.exit(-1)

plants=struct.unpack("<L",_bytes[0x330:0x334])[0]

if format=='mac' and len(_bytes[0x334+plants*0x58:])!=0x44 or format=='windows' and len(_bytes[0x334+plants*0x3c:])!=0x44:
	print('Incorrect input format')
	sys.exit(-1)

def convert(plants):
	if format=='mac':
		return plants[:0x14]+plants[0x18:0x1c]+plants[0x20:0x34]+plants[0x38:0x3c]+plants[0x40:0x4c]
	elif format=='windows':
		zeros=b'\x00\x00\x00\x00'
		return plants[:0x14]+zeros+plants[0x14:0x18]+zeros+plants[0x18:0x2c]+zeros+plants[0x2c:0x30]+zeros+plants[0x30:]+zeros*3

def show(_bytes):
	print()
	for i in range(len(_bytes)):
		print('%02x' %_bytes[i], end='')
		if i%4==3:
			print('|', end='')
		if i%16==15:
			print()
	print()

if format=='mac':
	plants=[_bytes[0x334+i*0x58:0x334+(i+1)*0x58] for i in range(plants)]
else:
	plants=[_bytes[0x334+i*0x3c:0x334+(i+1)*0x3c] for i in range(plants)]
plants=[convert(i) for i in plants]
show(plants[0])
_bytes=_bytes[:0x334]+b''.join(plants)+_bytes[-0x44:]
userdata=open(filename,'wb')
userdata.write(_bytes)
userdata.close()
os.utime(filename,(mtime,mtime))
