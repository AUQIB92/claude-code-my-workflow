// Fill.asm — CS401 Lab 4 reference solution
// Continuously polls the keyboard; blackens the entire screen while any
// key is pressed, whitens it otherwise. The screen is 8192 memory-mapped
// 16-bit words (256 rows x 512 columns / 16 bits-per-word = 32 words/row
// x 256 rows = 8192 words), starting at address 16384 (SCREEN).

(LOOP)
  @KBD
  D=M
  @BLACK
  D;JGT        // if a key is pressed (KBD != 0), go set color = black
  @color
  M=0          // else color = white (0)
  @FILL
  0;JMP
(BLACK)
  @color
  M=-1         // color = black (all 16 bits set, i.e. -1 in two's complement)
(FILL)
  @i
  M=0          // i = 0 (word index into the screen, 0..8191)
(FILLLOOP)
  @i
  D=M
  @8192
  D=D-A
  @LOOP
  D;JGE        // if i >= 8192, the whole screen is filled -- restart polling
  @i
  D=M
  @SCREEN
  D=D+A        // D = SCREEN + i  (this word's absolute address)
  @addr
  M=D
  @color
  D=M
  @addr
  A=M
  M=D          // RAM[SCREEN + i] = color
  @i
  M=M+1
  @FILLLOOP
  0;JMP
