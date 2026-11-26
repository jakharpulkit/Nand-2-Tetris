#!/usr/bin/env python3
"""
Hack Assembler (Nand to Tetris, Capstone Project)
Student : Pulkit Jakhar   Roll no: 2601732501   K = 01

Usage:  python assembler.py Prog.asm        -> writes Prog.hack

Extra feature for K mod 3 = 1:
  Wrong lines do not crash the assembler. Every bad line is reported as
      Line 7: invalid instruction
  (line number = line in the original .asm file). If any error is found,
  no .hack file is written.
"""
import sys

# ---------- translation tables ----------
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
for i in range(16):
    PREDEFINED["R%d" % i] = i

SYMBOL_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.$:")


def valid_symbol(s):
    return s != "" and not s[0].isdigit() and all(c in SYMBOL_CHARS for c in s)


def clean(line):
    """Remove comments and all whitespace."""
    if "//" in line:
        line = line[:line.index("//")]
    return "".join(line.split())


def assemble(lines):
    """Returns (list_of_binary_strings, list_of_error_messages)."""
    errors = []
    symbols = dict(PREDEFINED)

    # ---------- FIRST READING: remove comments/blank lines, record labels ----------
    code = []              # (original line number, cleaned text)
    for num, raw in enumerate(lines, start=1):
        text = clean(raw)
        if text == "":
            continue
        if text.startswith("("):
            if not text.endswith(")") or text.count("(") != 1 or text.count(")") != 1:
                errors.append("Line %d: invalid label definition '%s'" % (num, text))
                continue
            label = text[1:-1]
            if not valid_symbol(label):
                errors.append("Line %d: invalid label name '%s'" % (num, label))
                continue
            symbols[label] = len(code)      # label points to next instruction
            continue
        code.append((num, text))

    # ---------- SECOND READING: translate to 16 bits ----------
    next_var = 16
    out = []
    for num, text in code:
        if text.startswith("@"):                       # A-instruction
            sym = text[1:]
            if sym == "":
                errors.append("Line %d: invalid instruction, '@' has no address" % num)
                continue
            if sym.isdigit():
                value = int(sym)
                if value > 32767:
                    errors.append("Line %d: address %d is too large (max 32767)" % (num, value))
                    continue
            elif valid_symbol(sym):
                if sym not in symbols:                 # new variable
                    symbols[sym] = next_var
                    next_var += 1
                value = symbols[sym]
            else:
                errors.append("Line %d: invalid instruction, bad symbol '%s'" % (num, sym))
                continue
            out.append(format(value, "016b"))
        else:                                          # C-instruction: dest=comp;jump
            dest, comp, jump = "", text, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)
            if dest not in DEST:
                errors.append("Line %d: invalid destination '%s'" % (num, dest))
            elif comp not in COMP:
                errors.append("Line %d: invalid instruction, unknown computation '%s'" % (num, comp))
            elif jump not in JUMP:
                errors.append("Line %d: invalid jump '%s'" % (num, jump))
            else:
                out.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
    return out, errors


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        print("Usage: python assembler.py File.asm")
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path) as f:
            lines = f.read().splitlines()
    except OSError as e:
        print("Cannot open file:", e)
        sys.exit(1)

    out, errors = assemble(lines)
    if errors:
        for e in errors:
            print(e)
        print("%d error(s). No .hack file written." % len(errors))
        sys.exit(1)

    hack = path[:-4] + ".hack"
    with open(hack, "w") as f:
        f.write("\n".join(out) + "\n")
    print("Wrote %s (%d instructions)" % (hack, len(out)))


if __name__ == "__main__":
    main()
