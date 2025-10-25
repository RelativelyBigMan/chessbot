import Move_Validation as M
import King_Safety as K
import sys
import subprocess
import os
import random
import time
import functools
import json
from statistics import mean
import psutil




# 90061043
# 50586168
# 17152963
# 25707880
# 43176964

seed = random.randint(0,99999999)
random.seed(seed)
AITurn = False
colourTurn = True # True is white, black is False
state = None
isCheck = False
prevMoves = [(0,0,0,0)] * 10
timesUser1 = []
timesUser2 = []

def trackcalls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.has_been_called = True
        return func(*args, **kwargs)
    wrapper.has_been_called = False
    return wrapper

def piece_to_letter(Type,Colour):
    if not(Type and Colour):
        return "."
    if Type != "knight":
        letter = Type[0]
    else:
        letter = "n"
    if Colour == "Black":
        return letter.lower()
    else:
        return letter.upper()

def print_row(state):
    string = "   1  2  3  4  5  6  7  8   X"
    print(string)
    for row in range(len(state)):
        print(row+1,state[row])
    print("\nY\n")

class Piece:
    def __init__(self, Type, Colour, FirstMove):
        self.Type = Type
        self.Colour = Colour
        self.FirstMove = FirstMove

    def __repr__(self):
        return piece_to_letter(self.Type,self.Colour)

def create_board():
    pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    pawns = ["pawn" for _ in range(8)]
    state = [[Piece(None,None,None) for _ in range(8)] for _ in range(8)]
    state[0] = [Piece(Type, "White",True) for Type in pieces]
    state[1] = [Piece(Type, "White",True) for Type in pawns]
    state[6] = [Piece(Type, "Black",True) for Type in pawns]
    state[7] = [Piece(Type, "Black",True) for Type in pieces]
    return state



def get_first_move(state):
    bin_str = ""
    for yyy in range(8):
        for xxx in range(8):
            if state[yyy][xxx].FirstMove == True:
                bin_str += "1"
            else:
                bin_str += "0"
    return str(int(bin_str,2))

def get_input():
    print("Example input: '1 2' These are x and y respectively:")
    while True:
        try:
            x1,y1 = input("What would you like to move: ").split()
            x2,y2 = input("Where would you like to move it to: ").split()
            x1,y1,x2,y2 = int(x1)-1, int(y1)-1, int(x2)-1, int(y2)-1
            return (x1,y1,x2,y2)
        except KeyboardInterrupt:
            print("\n")
            sys.exit()
        except (ValueError, IndexError):
            print("Invalid input, go again")


# maybe the bug is with the c++?
def board_to_fen(state,colourTurn):
    mat = []
    index = 0
    for yyy in range(8):
        string = ""
        for xxx in range(8):
            cur = state[yyy][xxx]
            if cur.Type is not None:
                if index != 0:
                    string += str(index)  
                    index = 0
                string += piece_to_letter(cur.Type, cur.Colour)

            else:
                index += 1

        if index != 0:
            string += str(index)  
            index = 0
        mat.append(string)
    string = "/".join(mat)
    if colourTurn == True:
        string += " w"
    else:
        string += " b"
    return string


def get_random_move(colourTurn,state):
    all_moves = []

    if colourTurn:
        curColour = "White"
    else:
        curColour = "Black"
    for yyy in range(8):
        for xxx in range(8):
            piece = state[yyy][xxx]
            if piece.Colour == None:
                continue
            typePiece,Colour = piece.Type, piece.Colour

            if Colour == curColour:
                match typePiece:
                    case None:
                        continue
                    case "rook":
                        moves = (M.get_moves_rook(xxx,yyy,state))
                    case "knight":
                        moves = (M.get_moves_knight(xxx,yyy,state))
                    case "bishop":
                        moves = (M.get_moves_bishop(xxx,yyy,state))
                    case "queen":
                        moves = (M.get_moves_queen(xxx,yyy,state))
                    case "king":
                        moves = (M.get_moves_king(xxx,yyy,state))
                    case "pawn":
                        moves = (M.get_moves_pawn(xxx,yyy,state))

                for move in moves:
                    all_moves.append((xxx,yyy,move[0], move[1]))
    return all_moves

def check_insuffiececnt_pieces(state):
    for yyy in range(8):
        for xxx in range(8):
            cur = state[yyy][xxx]
            if cur.Type not in ["pawn", "king","bishop",None]:
                return False
    return True

def get_unchecked(state,colourTurn):
    colour = "Black"
    if colourTurn:
        colour = "White"
    for xxx in range(8):
        for yyy in range(8):
            if state[yyy][xxx].Type == "king" and state[yyy][xxx] == colour:
                move = random.choice(M.get_moves_king(xxx,yyy,state))
                return (xxx,yyy,move[0],move[1])


# def check_stalemate(state,colourTurn):
#     allMoves,king_pos = K.get_all_moves(colourTurn,state)
#     moves = M.get_moves_king(king_pos[0],king_pos[1],state)
#     for move in moves:
#         if (move not in K.get_all_moves(not(colourTurn,state))) and allMoves == []:
#             return False
#     return True
    
def save_data(data, filename="alpha-beta-tuning-depth5.json"):
    try:
        with open(filename, "r") as file:
            allPrevGames = json.load(file)
    except FileNotFoundError:
        allPrevGames = []
    
    allPrevGames.append(data)

    with open(filename, "w", encoding='utf-8') as file:
        json.dump(allPrevGames, file, indent=2) 

    




@trackcalls
def get_AI_move(state,colourTurn,prevMoves, isCheck):

    if "chess_engine" not in os.listdir():
        subprocess.run(["g++", "-O2", "-std=c++20", "AI.cpp", "-o", "chess_engine"])
        print("Compiled C++ program")
    if isCheck:
        move = (get_unchecked(state,colourTurn))



    if not get_AI_move.has_been_called:
        allMoves = get_random_move(colourTurn,state)
        return random.choice(allMoves)
    for move in prevMoves:
        if move in prevMoves:
            allMoves = get_random_move(colourTurn,state)
            return random.choice(allMoves)

    board_to_fen(state,colourTurn)
    pieceFrom, pieceTo = subprocess.run(["./chess_engine", board_to_fen(state,colourTurn), get_first_move(state)], capture_output = True, text=True).stdout.split(" ")
    pieceFrom, pieceTo = int(pieceFrom), int(pieceTo)

    return (pieceFrom%8, pieceFrom//8, pieceTo%8, pieceTo//8)


if __name__=="__main__":
    for iii in range(1000):
        print(f"there has been {iii} iterations")
        temps = psutil.sensors_temperatures()

        coreTemps = []
        for core in temps.get("coretemp", []):
            if core.label.startswith("Core"):
                coreTemps.append(core.current)

        temp = (sum(coreTemps) / len(coreTemps))
        seed = random.randint(0,99999999)
        random.seed(seed)
        StartTime = time.time()
        state = create_board()
        colourTurn = True
        prevMoves = []
        timesUser1 = []
        timesUser2 = []
                
        U1Name = "AI 1"
        U2Name = "AI 2"
        randomNum = random.randint(0,100)
        guessU1 = random.randint(0,100)
        guessU2 = random.randint(0,100)
        diffU1 = abs(randomNum - guessU1)
        diffU2 = abs(randomNum - guessU2)

        game_over = False
        move_count = 0
        max_moves = 500  

        while not game_over and move_count < max_moves:
            move_count += 1
            

            if check_insuffiececnt_pieces(state):
                data = {
                    "seed": seed,
                    "mode": 3,
                    "winner": "Draw",
                    "ending": "insufficient_pieces",
                    "duration": time.time() - StartTime,
                    "moves": move_count,
                    "final_pos": board_to_fen(state, colourTurn),
                    "core_temp":temp
                }
                save_data(data)
                game_over = True
                break

            initialTime = time.time()
            userInput = get_AI_move(state, colourTurn, prevMoves, isCheck)
            timeTook = time.time() - initialTime
            
            if colourTurn == True:
                timesUser1.append(timeTook)
            else:
                timesUser2.append(timeTook)
            
            if M.check_valid(userInput, colourTurn, state):
                x1, y1, x2, y2 = userInput
                org = state[y1][x1]
                trg = state[y2][x2]
                state[y2][x2] = org
                state[y1][x1] = Piece(None, None, None)
                prevMoves.append((x1, y1, x2, y2))

                if state[y2][x2]:
                    state[y2][x2].FirstMove = False

                if K.get_check(colourTurn, state):
                    state[y1][x1] = org
                    state[y2][x2] = trg
                    prevMoves.pop()
                    continue
                
                colourTurn = not(colourTurn)
                
                if K.get_check(colourTurn, state):
                    if K.get_checkmate(colourTurn, state):

                        data = {
                            "seed": seed,
                            "mode": 3,
                            "winner": "White" if not colourTurn else "Black",
                            "ending": "checkmate",
                            "duration": time.time() - StartTime,
                            "moves": move_count,
                            "final_pos": board_to_fen(state, colourTurn),
                            "core_temp":temp
                        }
                        save_data(data)
                        game_over = True
                        break
        
        if move_count >= max_moves:
            data = {
                "seed": seed,
                "mode": 3,
                "winner": "Draw",
                "ending": "max_moves_reached",
                "duration": time.time() - StartTime,
                "moves": move_count,
                "final_pos": board_to_fen(state, colourTurn),
                "core_temp":temp
            }
            save_data(data)
        

                





