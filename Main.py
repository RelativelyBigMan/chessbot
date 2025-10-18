import Move_Validation as M
import King_Safety as K
import sys
import subprocess
import os


colourTurn = True # True is white, black is False
state = None
isCheck = False



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

def get_input():
    print("Example input: '1 2' These are x and y respectively")
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


def board_to_fen(state,colourTurn):
    string = ""
    noneValue = Piece(None,None,None)
    index = 0
    for yyy in range(8):
        if index != 0:
            string += str(index)  
            index = 0
        string += "/"
        for xxx in range(8):
            cur = state[yyy][xxx]
            if cur.Type is not None:

                if cur.Colour == "Black":

                    match cur.Type:
                        case "rook":
                            string += "R"
                        case "knight":
                            string += "N"
                        case "bishop":
                            string += "B"
                        case "queen":
                            string += "Q"
                        case "king":
                            string += "K"
                        case "pawn":
                            string += "P"
                else:
                    match cur.Type:
                        case "rook":
                            string += "r"
                        case "knight":
                            string += "n"
                        case "bishop":
                            string += "b"
                        case "queen":
                            string += "q"
                        case "king":
                            string += "k"
                        case "pawn":
                            string += "p"
            else:
                index += 1

    if colourTurn == "White":
        string += " w"
    else:
        string += " b"
    return string


# https://stackoverflow.com/questions/41171791/how-to-suppress-or-capture-the-output-of-subprocess-run
def get_AI_move(state,colourTurn):

    if "chess_engine" not in os.listdir():
        subprocess.run(["g++", "-O2", "-std=c++20", "AI.cpp", "-o", "chess_engine"])
        print("Compiled C++ program")
    pieceFrom, pieceTo = subprocess.run(["./chess_engine", board_to_fen(state,colourTurn)], capture_output = True, text=True).stdout.split(" ")
    print(pieceFrom,pieceTo)
    pieceFrom, pieceTo = int(pieceFrom), int(pieceTo)

    indexFrom = (pieceFrom%8,pieceFrom//8)
    indexTo = (pieceTo%8,pieceTo//8)
    return indexFrom,indexTo

if __name__=="__main__":
    state = create_board()
    while True:
        if colourTurn == True:
            print("It is white's move\n")
        else:
            print("It is black's move\n")

        if isCheck == True:
            print("Check has been instaniated, either move the king or move a piece into the way\n")
        print_row(state)
        userInput = get_input()

        if M.check_valid(userInput,colourTurn,state):

            x1,y1,x2,y2 = userInput
            org = state[y1][x1]
            trg = state[y2][x2]
            state[y2][x2] = org
            state[y1][x1] = Piece(None,None,None)

            if isCheck and K.get_check(colourTurn,state):
                print("ERROR: king in check")
                state[y1][x1] = org
                state[y2][x2] = trg
                continue

            if state[y2][x2]:
                state[y2][x2].FirstMove = False

            if K.get_check(colourTurn, state):
                isCheck = True
                if K.get_checkmate(colourTurn, state):
                    print("Checkmate")
                    sys.exit("\n")
                else:
                    print("Opponent is in check")

            colourTurn = not(colourTurn) # switches the colour Turn





