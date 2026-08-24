// Mult.asm — CS401 Lab 4 reference solution
// Computes RAM[2] = RAM[0] * RAM[1] via repeated addition (Hack has no
// multiply instruction). Precondition, matching the supplied Mult.tst:
// RAM[0] >= 0, RAM[1] >= 0.

  @2
  M=0          // RAM[2] = 0 (running product)
  @0
  D=M
  @END
  D;JEQ        // if RAM[0] == 0, product is 0 -- done
  @1
  D=M
  @END
  D;JEQ        // if RAM[1] == 0, product is 0 -- done
  @i
  M=0          // i = 0 (loop counter, counts up to RAM[1])
(LOOP)
  @i
  D=M
  @1
  D=D-M
  @END
  D;JEQ        // if i == RAM[1], done
  @0
  D=M
  @2
  M=D+M        // RAM[2] += RAM[0]
  @i
  M=M+1        // i++
  @LOOP
  0;JMP
(END)
  @END
  0;JMP        // Nand2Tetris convention: halt via a tight infinite loop
