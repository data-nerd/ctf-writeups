
# I like to mov it, mov it

This was a reverse engineering challenge in the Codebreaker Challenge Community of Practice Mini-CTF held in April 2022.

It and another challenge in this CTF, *Ida know how they managed that one!*, are based on the work of evil genius Chris Domas. [1]

## tl;dr:
By the title I knew what was coming and when I opened the file in ghidra I had the same reaction as Chris: nope!

https://youtu.be/HlUe0TUHOIc?t=477

It was going to be easier to find the encoded flag and use dynamic analysis to let the binary do all the hard work.

## Finding the encrypted flag

The binary prints the encrypted flag:

```
└─$ ./reverse_me_if_you_dare | xxd
00000000: 5468 6520 666c 6167 2069 733a 2093 9292  The flag is: ...
00000010: 939f a0cb 9d80 a6af 81a3 af87 c5a2 b9be  ................
00000020: 86af 93bf bdc0 bcb5 c4b5 71cd            ..........q.
```

I didn't believe it would be *that* easy so I spent time convincing myself that these bytes were the encrypted flag, untouched by all those `mov`s.

Turns out, those same bytes are the first bytes in the `.data` section of the binary.

```
gef➤  search-pattern 0x93929293                                                                                              
[+] Searching '\x93\x92\x92\x93' in memory                                                                                   
[+] In '/home/test/ctf/cbc/mov/reverse_me_if_you_dare'(0x804c000-0x85f7000), permission=rwx
  0x804d020 - 0x804d030  →   "\x93\x92\x92\x93[...]"                                                                         
gef➤  hexdump b 0x804d020                                                                                                    
0x0804d020     93 92 92 93 9f a0 cb 9d 80 a6 af 81 a3 af 87 c5    ................
0x0804d030     a2 b9 be 86 af 93 bf bd c0 bc b5 c4 b5 71 cd 00    .............q..
```

Still unsure it was that simple, I took the risk that with no input the bytes remain the same from the binary to the output.

I wasn't even sure how to manipulate the bytes since there was no prompt for input nor did it look like command line arguments made any difference. Didn't matter, I had the flag, I just needed it to reveal itself.

## Finding the encryption method

I tried to play the game the "right" way by discovering what the code was doing. I watched the bytes being copied from `.data`. I set breakpoints in the `master_loop` to see how the bytes were changed. I messed with memory at some of the labels (`on` and `toggle_execution` we just *begging* to be changed).

I zeroed out the encrypted flag source bytes to see if it was a simple xor such that xoring with zeroed ciphertext would reveal the key.

None of that worked so I went back to basics: using a crib to break the encryption. This probably wasn't the intended path but 1000 points awaited, so I swallowed my pride and moved on. (Get it!?)

### Basic analysis with a crib 

Flags in this CTF were of the format `CBCCOP{...}`. All those C's and the B right next to a C made it much easier to spot patterns than if the letters had been further apart.

I started with the flag bytes (ciphertext) and asked how they could be manipulated to give a plaintext starting with `CBCCOP`. xor is always popular so I xored the encrypted bytes with my crib:

```
0x93 ^ C => 0xd0
0x92 ^ B => 0xd0
0x92 ^ C => 0xd1
0x93 ^ C => 0xd0
0x9f ^ O => 0xd0
0xa0 ^ P => 0xf0
0xcb ^ { => 0xb0
```

Nice round numbers. That looks promising. Except for that 3rd character. The other C's are decrypted with `0xd0` but it wants `0xd1`. More on that later.

I wasn't sure if the key was a pattern of bytes so I xored the ciphertext with various single-byte keys:

```
0x80: ......K..&/.#/.E"9>./.?=@<5D5.M   (13 unprintable)
0xb0: #""#/.{-0..1..7u...6.#..p..t..}   (15 unprintable)
0xc0: SRRS_`.]@foAcoG.by~FoS.}.|u.u..   (7 unprintable)
0xd0: CBBCOp.MPv.Qs.W.rinV.Com.le.e..   (9 unprintable)
0xd1: BCCBNq.LQw~Pr~V.shoW~Bnl.md.d..   (6 unprintable)
0xf0: cbbcoP;mpV_qS_w5RINv_cOM0LE4E.=   (1 unprintable)
```

Very promising! You can practically read the key when the characters are xored with `0xd0`. And the braces show up where expected when xoring with `0xb0`.

I noticed that the lower nibble was the same in the ciphertext and what I knew of the plaintext, so I created a mapping table for the high nibbles. If it was `0x93` I would map `9` to `4` and get `0x43` or C. After messing with mappings and recovering the full key I noticed that the "mapping" could really just be done with math: subtract 5 from each high nibble.

```
from binascii import unhexlify

# Bytes printed when the binary is run, also the first bytes of the .data section
flag = '93 92 92 93 9f a0 cb 9d 80 a6 af 81 a3 af 87 c5 a2 b9 be 86 af 93 bf bd c0 bc b5 c4 b5 71 cd'
flag_bytes = unhexlify(flag.replace(" ", ""))

plaintext = ''

for b in flag_bytes:
    hi = b & 0xF0
    hi -= 0x50
    ct = hi | (0xF & b)
    plaintext += chr(ct)

print(plaintext)
```

Output:
```
CBBCOP{M0V_1S_7uRin6_Complete!}
```

Oops, that 3rd character is wrong. I honestly don't remember "fixing" it before submitting so I think the actual answer had a different prefix from the other flags. I'm assuming it was some sort of reverse engineering mind games that the challenge authors were playing. If so, well done. You would have thrown me off if I wasn't so stubborn.

Sharp-eyed readers will notice that the bit twiddling isn't necessary. This also works:

```
"".join([chr(b - 0x50) for b in flag_bytes])
```

I left the steps I took in this writeup and the `solve.py` file to show the thought process: from mapping table, to nibble manipulation, to simple subtraction. The end result is clear in hindsight but that's often the case. Learning in in the journey.

## Conclusion

I probably made this way easier than it was supposed to be. I also know I made the basic analysis with a crib way harder than it needed to be.

This writeup is also longer than it needs to be. I didn't want to just post the final solution script. I took a lot of wrong turns and wanted to show what it's like for mere mortals.

In the end, it was a fun challenge and I managed to keep my sanity. Or at least as much as I had when I started.

## References

[1] **Repsych: Psychological Warfare in Reverse Engineering**

https://www.youtube.com/watch?v=HlUe0TUHOIc

https://github.com/xoreaxeaxeax/REpsych
