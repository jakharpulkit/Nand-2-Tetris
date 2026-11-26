# Capstone: Make the Computer Draw a Box
Pulkit Jakhar | Roll no. 2601732501 | **K = 01**

| Item | Value |
|---|---|
| Box start row | 1 |
| Box height | 20 rows (rows 1-20) |
| Box width | 16 x ((1 mod 4)+1) = 32 pixels (2 words) |
| Extra assembler feature (K mod 3 = 1) | Clear error messages with line numbers |

Files: `assembler.py`, `Box.asm`, `Box.hack`, `tests/`, and the HDL chips (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`).

Run: `python assembler.py Box.asm`
