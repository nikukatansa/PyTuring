# PyTuring
A programmable Turing machine implemented in Python

## Usage
*python turing.py Program Tape [Bits]*

* Program should be a plain text file where each line has the form [value at head, current state] => [new value at head, new state, tape movement].  Tape movement can be any integer value, and can use the variable n which will be replaced by the value of Bits when the program is run.
* Tape should be an array representing the tape that will be used with the Turing machine.  The first cell of the tape will be position 0, and this will be where the head of the Turing machine will begin when the program is run.  The head will be in state 0 when the program is run.
* Bits is an optional integer representing the word size for this Turing machine.

A true Turing machine only allows rules that move the tape by at most one cell left or right.  PyTuring allows slightly higher-level programs to be written, where the tape can be moved by any integer number of cells.  When a program is run, however, a new low-level Turing machine program is created, where the movement value is -1, 0 or 1.  This is saved in a new program file, *adjusted_Program*.

## Example
The program fulladder.tur represents a full adder in an n bit processor.  The input tape for this program should be of the form [ P (n bits), Q (n bits), Carry Out (1 bit, 0), Sum (n bits, 0s), Calculation area (n bits, 0s), Looping area (n bits, 100...0) ].

To calculate 5 + 6 on a 4 bit machine, call the program as follows:

python turing.py fulladder.py "[0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0]" 4

The output will be stored in the five cells of the tape beginning at index 8.
