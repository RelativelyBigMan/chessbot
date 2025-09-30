import Move_Validation as M
import King_Safety as K
import sys
colourTurn = True # True is white, black is False
state = None
check = False
# NDEBUG = True


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
        print(row+1, state[row])
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



if __name__=="__main__":
    state = create_board()
    while True:
        if colourTurn == True:
            print("It is white's move\n")
        else:
            print("It is black's move\n")
        if check == True:
            print("Check has been instaniated, either move the king or move a piece into the way")
        print_row(state)
        userInput = get_input()
        if M.check_valid(userInput,colourTurn,state):
            x1,y1,x2,y2 = userInput
            src_piece = state[y1][x1]
            dst_piece = state[y2][x2]
            state[y2][x2] = src_piece
            state[y1][x1] = Piece(None,None,None)
            if K.get_check(colourTurn, state):
                print("Illegal move: your king would be in check")
                # undo
                state[y1][x1] = src_piece
                state[y2][x2] = dst_piece
                continue

            if state[y2][x2] is not None:
                state[y2][x2].FirstMove = False

            opponent = not colourTurn
            if K.get_check(opponent, state):
                if K.get_checkmate(opponent, state):
                    print("Checkmate")
                    sys.exit()
                else:
                    print("Opponent is in check")
            colourTurn = not(colourTurn) # switches the colour Turn





