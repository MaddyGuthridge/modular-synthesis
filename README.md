# Modular Synthesis

A simple program for generating and manipulating waveforms.

This project isn't intended to be performant. It's just a little demo I made
for fun.

## Example usage

```txt
Enter a command: gen sine 220 1 a
Enter a command: gen sine 330 1 e
Enter a command: op append a e seq
Enter a command: gen sine 220 0.166667 as
Enter a command: gen sine 165 0.166667 els
Enter a command: op append seq as seq
Enter a command: op append seq els seq
Enter a command: op append seq as seq
Enter a command: gen sine 330 0.1 evs
Enter a command: gen sine 330 0.066667 silence
Enter a command: op scale silence 0 silence
Enter a command: op append seq evs seq
Enter a command: op append seq silence seq
Enter a command: op append seq e seq
Enter a command: save seq test.wav
Enter a command: quit
Goodbye!
```
