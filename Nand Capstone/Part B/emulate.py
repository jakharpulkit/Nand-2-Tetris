"""Tiny Hack CPU emulator, only to check Box.hack without the GUI. Usage: python emulate.py Box.hack"""
import sys
def run(rom, key, steps=5000):
    ram = [0]*32768; ram[24576] = key; A = D = pc = 0
    for _ in range(steps):
        i = rom[pc]
        if i[0] == "0":
            A = int(i, 2); pc += 1; continue
        a = i[3]; c = i[4:10]; d = i[10:13]; j = i[13:]
        y = ram[A] if a == "1" else A
        x = D
        f = {"101010":0,"111111":1,"111010":-1,"001100":x,"110000":y,"001101":~x,"110001":~y,
             "001111":-x,"110011":-y,"011111":x+1,"110111":y+1,"001110":x-1,"110010":y-1,
             "000010":x+y,"010011":x-y,"000111":y-x,"000000":x&y,"010101":x|y}[c]
        f = ((f + 32768) & 0xFFFF) - 32768
        oldA = A
        if d[2] == "1": ram[oldA] = f
        if d[1] == "1": D = f
        if d[0] == "1": A = f
        jump = (j[0]=="1" and f<0) or (j[1]=="1" and f==0) or (j[2]=="1" and f>0)
        pc = oldA if jump else pc + 1
    return ram
rom = open(sys.argv[1]).read().split()
for key, name in ((0, "no key"), (75, "key pressed")):
    ram = run(rom, key)
    rows = {r for r in range(256) for w in range(32) if ram[16384+32*r+w] != 0}
    words = {w for r in range(256) for w in range(32) if ram[16384+32*r+w] != 0}
    print(name, "-> black rows:", (min(rows), max(rows)) if rows else None,
          "| black words per row:", sorted(words) if words else None)
