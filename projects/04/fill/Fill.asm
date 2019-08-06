// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

  // Put your code here.
  (CHOOSE)
  @SCREEN
  D = A // D = @SCREEN 
  @addr
  M = D // @addr = @SCREEN 
  @KBD
  D = M // D = M[@KBD] 
  @WHITE
  D;JEQ // M[@KBD] == 0 => @WHITE
  @BLACK
  0;JEQ // ELSE => @BLACK
  
  (WHITE)
  @color
  M = 0 // @color = 0
  @SHOW
  0;JMP // Jump @SHOW
  
  (BLACK)
  @color
  M = -1 // @color = -1
  @SHOW
  0;JMP // Jump @SHOW

  (SHOW)
  @addr
  D = M // D = @addr
  @KBD
  D = D - A // D = @addr - @KBD
  @CHOOSE
  D;JEQ // (@addr - @KBD) == 0 => @CHOOSE
  @color
  D = M // D = @color
  @addr
  A = M // A = @addr
  
  M = D // M[@addr] = @color
  @addr
  M = M + 1 // @addr = @addr + 1

  @SHOW
  0;JMP
