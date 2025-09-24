def check_valid_rook(x1,y1,x2,y2):  
    possibleMoves = []
    for iii in range(8):
        possibleMoves.append((iii,y1))
        possibleMoves.append((x1,iii))

    if (x2,y2) in possibleMoves:
        return True
    print("Rook can't move there")
    return False


def get_moves_knight(x1,y1):
    possibleMoves = []
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    for delta in deltas:
        deltaX,deltaY = delta[0], delta[1]
        possibleMoves.append((deltaX+x1,deltaY+y1))
    return possibleMoves

def check_valid_knight(x1,y1,x2,y2):
    possibleMoves = get_moves_knight(x1,y1)
    if (x2,y2) in possibleMoves:
        return True
    print("Knight can't move there")
    return False

def get_moves_bishop(x1,y1):
    possibleMoves = []
    for iii in range(8):
        possibleMoves.append((x1+iii,y1+iii))
        possibleMoves.append((x1-iii,y1-iii))
        possibleMoves.append((x1-iii,y1+iii))
        possibleMoves.append((x1+iii,y1-iii))
    return possibleMoves

def check_valid_bishop(x1,y1,x2,y2):
    possibleMoves = get_moves_bishop(x1,y1)
    if (x2,y2) in possibleMoves:
        return True
    print("Bishop can't move there")
    return False

def get_moves_queen(x1,y1):
    possibleMoves = []
    for iii in range(8):
        possibleMoves.append((iii,y1))
        possibleMoves.append((x1,iii))
        possibleMoves.append((x1+iii,y1+iii))
        possibleMoves.append((x1-iii,y1-iii))
        possibleMoves.append((x1-iii,y1+iii))
        possibleMoves.append((x1+iii,y1-iii))
    return possibleMoves


def check_valid_queen(x1,y1,x2,y2):
    possibleMoves = get_moves_queen(x1,y1)
    if (x2,y2) in possibleMoves:
        return True
    print("Queen can't move there")
    return False
    
def get_moves_king(x1,y1):
    possibleMoves = []
    deltas = [(i, u) for i in range(-1, 2) for u in range(-1, 2)]
    for delta in deltas:
        deltaX,deltaY = delta[0], delta[1]
        possibleMoves.append((deltaX+x1,deltaY+y1))
    return possibleMoves


def check_valid_king(x1,y1,x2,y2):
    possibleMoves = get_moves_king
    if (x2,y2) in possibleMoves:
        return True
    print("King can't move there")
    return False

def get_moves_pawn(x1,y1):
    possibleMoves = []

    # tells us direction of the piece
    if state[y1][x1].Colour == "White":
        direction = 1
    else:
        direction = -1
    
    # adds the move forward 1 or 2 if its the pawns first move
    possibleMoves.append((x1,y1+(1*direction)))
    if (state[y1][x1].FirstMove == True):
        state[y1][x1].FirstMove = False
        possibleMoves.append((x1,y1+(2*direction)))


    #Finds attacking moves
    if state[y2][x2].Type:
        possibleMoves.append((x1+1,y1+(1*direction)))
        possibleMoves.append((x1-1,y1+(1*direction)))

    return possibleMoves

def check_valid_pawn(x1,y1,x2,y2):
    possibleMoves = get_moves_pawn(x1,y1)
    if (x2,y2) in possibleMoves:
        return True
    print("Pawn can't move there")
    return False

def check_valid(userInput):
    x1,y1,x2,y2 = userInput
    if (x1,y1) == (x2,y2):
        print("You can't move a piece to where it already is")
        return False
    
    if state[y1][x1].Colour == state[y2][x2].Colour:
        print("You can't capture your own piece")
        return False
    
    if not (0 <= x1 <= 7 and 0 <= y1 <= 7 and 0 <= x2 <= 7 and 0 <= y2 <= 7):
        print("Your trying to move a piece out of the board")
        return False


    if colourTurn:
        if state[y1][x1].Colour != "White":
            print("That is not your piece")
            return False
    else:
        if state[y1][x1].Colour != "Black":
            print("That is not your piece")
            return False



    typePiece = state[y1][x1].Type


    match typePiece:
        case None:
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