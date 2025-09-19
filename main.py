# firstMove = True
class Piece:
    def __init__(self, Type, Colour, FirstMove):
        self.Type = Type
        self.Colour = Colour
        self.FirstMove = FirstMove

    def __str__(self):
        if self.Type and self.Colour:
            return f"{self.Type} {self.Colour}"
        return "empty"
    
    def __repr__(self):
        return self.__str__()

def print_row(state):
    for row in state:
        print(row)

def create_board():
    global state
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
    

def check_valid_rook(x1,y1,x2,y2):#    
    possibleMoves = []
    for iii in range(8):
        possibleMoves.append((iii,y1))
        possibleMoves.append((x1,iii))

    if (x2,y2) in possibleMoves:
        return True
    else:
        return False

def check_valid_knight(x1,y1,x2,y2):
    possibleMoves = []
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    for delta in deltas:
        deltaX,deltaY = delta[0], delta[1]
        possibleMoves.append((deltaX+x1,deltaY+y1))

    if (x2,y2) in possibleMoves:
        return True
    return False

def check_valid_bishop(x1,y1,x2,y2):
    possibleMoves = []
    for iii in range(8):
        if (0 <= x1+iii <= 7 and 0 <= y1+iii <= 7):
            possibleMoves.append((x1+iii,y1+iii))
        if (0 <= x1-iii <= 7 and 0 <= y1-iii <= 7):
            possibleMoves.append((x1-iii,y1-iii))
        if (0 <= x1-iii <= 7 and 0 <= y1+iii <= 7):
            possibleMoves.append((x1-iii,y1+iii))
        if (0 <= x1+iii <= 7 and 0 <= y1-iii <= 7):
            possibleMoves.append((x1+iii,y1-iii))

    if (x2,y2) in possibleMoves:
        return True
    return False

def check_valid_queen(x1,y1,x2,y2):
    possibleMoves = []
    for iii in range(8):
        possibleMoves.append((iii,y1))
        possibleMoves.append((x1,iii))
        if (0 <= x1+iii <= 7 and 0 <= y1+iii <= 7):
            possibleMoves.append((x1+iii,y1+iii))
        if (0 <= x1-iii <= 7 and 0 <= y1-iii <= 7):
            possibleMoves.append((x1-iii,y1-iii))
        if (0 <= x1-iii <= 7 and 0 <= y1+iii <= 7):
            possibleMoves.append((x1-iii,y1+iii))
        if (0 <= x1+iii <= 7 and 0 <= y1-iii <= 7):
            possibleMoves.append((x1+iii,y1-iii))

    if (x2,y2) in possibleMoves:
        return True
    return False
    
def check_valid_king(x1,y1,x2,y2):
    possibleMoves = []
    deltas = [(-1,1),(0,1),(1,1),(1,0),(-1,0),(-1,-1),(0,-1),(1,-1)]
    for delta in deltas:
        deltaX,deltaY = delta[0], delta[1]
        possibleMoves.append((deltaX+x1,deltaY+y1))
    if (x2,y2) in possibleMoves:
        return True
    return False


def check_valid_pawn(x1,y1,x2,y2):
    possibleMoves = []

    #tells us direction of the player
    if state[y1][x1].Colour == "White":
        direction = 1
    else:
        direction = -1
    
    possibleMoves.append((x1,y1+(1*direction)))
    if (state[y1][x1].FirstMove == True):
        state[y1][x1].FirstMove = False
        possibleMoves.append((x1,y1+(2*direction)))


    #Finds attacking moves
    if state[y2][x2].Type:
        possibleMoves.append((x1+1,y1+(1*direction)))
        possibleMoves.append((x1-1,y1+(1*direction)))
    
    if (x2,y2) in possibleMoves:
        return True
    return False

def check_valid(userInput):
    x1,y1,x2,y2 = userInput
    if (x1,y1) == (x2,y2):
        return False
    
    if state[y1][x1].Colour == state[y2][x2].Colour:
        return False
    
    if not (0 <= x1 <= 7 and 0 <= y1 <= 7 and 0 <= x2 <= 7 and 0 <= y2 <= 7):
        return False


    typePiece = state[y1][x1].Type


    match typePiece:
        # no fallthrough happening here lol
        case "None":
            return False
        case "rook":
            return check_valid_rook(x1,y1,x2,y2)
        case "knight":
            return check_valid_knight(x1,y1,x2,y2)
        case "bishop":
            return check_valid_bishop(x1,y1,x2,y2)
        case "queen":
            return check_valid_queen(x1,y1,x2,y2)
        case "king":
            return check_valid_king(x1,y1,x2,y2)
        case "pawn":
            return check_valid_pawn(x1,y1,x2,y2)
        
    


if __name__=="__main__":
    state = create_board()
    print_row(state)
    userInput = get_input()
    print(check_valid(userInput))
    # firstMove = False


