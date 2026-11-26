// Box.asm  --  Pulkit Jakhar, Roll 2601732501, K = 01
// While any key is pressed, draw a black box; when released, clear it.
// Box: starts at row K = 1, 20 rows tall,
//      width = 16 * ((K mod 4) + 1) = 32 pixels = 2 words, from the left edge.
// Row r starts at SCREEN + 32*r, so row 1 starts at SCREEN + 32.

(LOOP)
    @KBD
    D=M
    @BLACK
    D;JNE           // key pressed -> use black
    @color
    M=0             // no key -> white (erase)
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1            // all 16 bits = 1 -> black
(DRAW)
    @SCREEN
    D=A
    @32
    D=D+A           // D = SCREEN + 32*1 (first row of the box)
    @addr
    M=D
    @20
    D=A
    @rows
    M=D             // rows left to draw = 20
(ROWLOOP)
    @color
    D=M
    @addr
    A=M
    M=D             // word 0 of this row (pixels 0-15)
    A=A+1
    M=D             // word 1 of this row (pixels 16-31)
    @32
    D=A
    @addr
    M=D+M           // addr = addr + 32 (next row)
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT           // more rows left?
    @LOOP
    0;JMP
