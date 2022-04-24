from binascii import unhexlify

# Bytes printed when the binary is run, also the first bytes of the .data section
flag = '93 92 92 93 9f a0 cb 9d 80 a6 af 81 a3 af 87 c5 a2 b9 be 86 af 93 bf bd c0 bc b5 c4 b5 71 cd'
flag_bytes = unhexlify(flag.replace(" ", ""))

# Short, but expanded for clarity
plaintext = ''

for b in flag_bytes:
    hi = b & 0xF0
    hi -= 0x50
    ct = hi | (0xF & b)
    plaintext += chr(ct)

print(plaintext)

# Even shorter
plaintext = ''

for b in flag_bytes:
    plaintext += chr(b - 0x50)

print(plaintext)
