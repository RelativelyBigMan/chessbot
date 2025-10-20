# taken from binary exploitation template, I am using this for tests, seems the easiest way of doing it
# without completly redoing how my project works from cryptocat series


#!/usr/bin/env python3
import sys
from pwn import *
exe = '/home/ubuntu/chessbot/Main.py'

PY = sys.executable

def start(argv=[], *a, **kw):
    return process([PY, exe] + argv, *a, **kw)

# gdbscript = '''
# break main
# '''.format(**locals())

# taken from chatgpt I couldnt be bothered finding a valid set of moves for checkmate
test_moves = [
    (5, 2, 5, 4),  # White: e2 -> e4
    (6, 7, 6, 5),  # Black: f7 -> f5
    (5, 4, 6, 5),  # White: e4 -> f5 
    (7, 7, 7, 5),  # Black: g7 -> g5
    (4, 1, 8, 5),  # White: Qd1 -> h5
    (1, 7, 1, 6),  # Black: a7 -> a6
]

io = start()
for move in test_moves:
    print(io.recvuntil("What would you like to move: ").decode())
    io.sendline(f"{move[0]} {move[1]}")
    io.recvuntil("Where would you like to move it to: ")
    io.sendline(f"{move[2]} {move[3]}")
data = io.recvall(timeout=2) # I was being left hanging so added timeout
print(data.decode())



