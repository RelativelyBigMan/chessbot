import Check as C
colourTurn = True # True is white, black is False
state = None
# NDUG = True

# TODO: MAKE THE check_valid() functions not check any further values if there is a piece in the way
# when get_pawn_moves() is called make another parameter to make sure pawn movign forward isnt included whne checking for check

def piece_to_letter(Type,Colour):
    if not(Type and Colour):
        return "."
    letter = Type[0]
    if Colour == "Black":
        return letter.lower()
    else:
        return letter.upper()

def print_row(state):
    string = "   0  1  2  3  4  5  6  7   X"
    print(string)
    for row in range(len(state)):
        print(row, state[row])
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
    print("Example input:(1 2) These are x and y respectively and have zero based indexing")
    x1,y1 = input("What would you like to move: ").split(" ")
    x2,y2 = input("Where would you like to move it to: ").split(" ")
    x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
    return ((x1,y1,x2,y2))

if __name__=="__main__":
    state = create_board()

    while True:
        if colourTurn == True:
            print("It is white's move\n")
        else:
            print("It is black's move\n")
        print(C.get_moves_bishop(2,0,0,2,state))
        print_row(state)
        userInput = get_input()
        if (C.check_valid(userInput,colourTurn,state)):
            x1,y1,x2,y2 = userInput
            state[y2][x2] = state[y1][x1]
            state[y1][x1] = Piece(None,None,None)
            colourTurn = True ^ colourTurn # switches the colour Turn

    


