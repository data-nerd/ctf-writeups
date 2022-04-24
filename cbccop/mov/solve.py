import string
from binascii import hexlify, unhexlify

flag =         '93 92 92 93 9f a0 cb 9d 80 a6 af 81 a3 af 87 c5 a2 b9 be 86 af 93 bf bd c0 bc b5 c4 b5 71 cd'

#               C  B  C  C  O  P  {  mM 0  vV _  1  sS _  7  u  rR iI nN 6  _  cC oO mM p  lL eE t  eE    }
final_keys = [ 'D0 D0 D1 D0 D0 F0 B0 D0 B0 D0 F0 B0 D0 F0 B0 B0 D0 D0 D0 B0 F0 D0 D0 D0 B0 D0 D0 B0 D0    B0',
               'D0 D0 D1 D0 D0 F0 B0 F0 B0 F0 F0 B0 F0 F0 B0 B0 F0 F0 F0 B0 F0 F0 F0 F0 B0 F0 F0 B0 F0    B0'
]

flag_bytes = unhexlify(flag.replace(" ", ""))

def solve_with_mapping():
    mapping = {
        0x7: 0x2,
        0x8: 0x3,
        0x9: 0x4,
        0xA: 0x5,
        0xB: 0x6,   # ?? 0xD ??
        0xC: 0x7,
    }

    plaintext = ''

    for b in flag_bytes:
        nibble = b >> 4
        new_nibble = mapping[nibble]
        ct = (new_nibble << 4) | (0xF & b)
        plaintext += chr(ct)

    print(f"flag = {plaintext}")

def solve_with_math():
    plaintext = ''

    for b in flag_bytes:
        plaintext += chr(b - 0x50)

    print(f"flag = {plaintext}")

def solve_with_pythonic_math():
    print(f'flag = {"".join([chr(b - 0x50) for b in flag_bytes])}')

def find_key_with_crib():
    crib = 'CBCCOP{'

    for i in range(len(crib)):
        print(f'{hex(flag_bytes[i])} ^ {crib[i]} => {hex(flag_bytes[i] ^ ord(crib[i]))}')

def test_keys():
    keys = [0x80, 0xb0, 0xc0, 0xd0, 0xd1, 0xf0]

    for key in keys:
        plaintext = ''
        unprintable = 0

        for b in flag_bytes:
            ch = chr(b ^ key)

            if ch in string.printable and ch not in string.whitespace:
                plaintext += ch
            else:
                plaintext += '.'
                unprintable += 1
        
        print(f"{hex(key)}: {plaintext}   ({unprintable} unprintable)")
        #print(f"{hexlify(plaintext.encode())}")
        print()


if __name__ == "__main__":
    find_key_with_crib()
    test_keys()
    solve_with_mapping()
    solve_with_math()
    solve_with_pythonic_math()
