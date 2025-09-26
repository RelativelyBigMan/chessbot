

# Stops out of range errors
def get_index(x,y,state):
    if 0 <= x < 8 and 0 <= y < 8:
        return state[y][x]
    return None

def get_moves_rook(x1,y1,state):
    possibleMoves = []
    for iii in range(x1+1,8):
        if not(get_index(iii,y1,state).Type):
            possibleMoves.append((iii,y1))
        elif get_index(iii,y1,state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((iii,y1))
            break
        else:
            break
    
    for iii in range(x1-1,-1,-1):
        if not(get_index(iii,y1,state).Type):
            possibleMoves.append((iii,y1))
        elif get_index(iii,y1,state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((iii,y1))
            break
        else:
            break


    for iii in range(y1+1,8):
        if not(get_index(x1,iii,state).Type):
            possibleMoves.append((x1,iii))
        elif get_index(x1,iii,state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((x1,iii))
            break
        else:
            break
    
    for iii in range(y1-1,-1,-1):
        if not(get_index(x1,iii,state).Type):
            possibleMoves.append((x1,iii))
        elif get_index(x1,iii,state).Colour != get_index(x1,iii,state).Colour:
            possibleMoves.append((x1,iii))
            break
        else:
            break

    return possibleMoves


def check_valid_rook(x1,y1,x2,y2,state):  
    possibleMoves = get_moves_rook(x1,y1,state)
    if (x2,y2) in possibleMoves:
        get_index(x1,y1,state).FirstMove = False
        return True
    print("Rook can't move there")
    return False


def get_moves_knight(x1,y1,state):
    possibleMoves = []
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    for delta in deltas:
        deltaX,deltaY = delta[0], delta[1]
        possibleMoves.append((deltaX+x1,deltaY+y1))
    return possibleMoves

def check_valid_knight(x1,y1,x2,y2,state):
    possibleMoves = get_moves_knight(x1,y1,state)
    if (x2,y2) in possibleMoves:
        get_index(x1,y1,state).FirstMove = False
        return True
    print("Knight can't move there")
    return False

def get_moves_bishop(x1,y1,state):
    possibleMoves = []
    for iii in range(1,min(7-x1,7-y1)+1):
        if (get_index(x1+iii,y1+iii,state).Type) is None:
            possibleMoves.append((x1+iii,y1+iii))
        elif get_index(x1+iii,y1+iii,state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((x1+iii,y1+iii))
            break
        else:
            break
        
    
    for iii in range(1,min(x1,y1)+1):
        if (get_index(x1-iii,y1-iii,state).Type) is None:
            possibleMoves.append((x1-iii,y1-iii))
        elif get_index(x1-iii,y1-iii,state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((x1-iii,y1-iii))
            break
        else:
            break
        

    for iii in range(1,min(x1,7-y1)+1):

        if (get_index(x1-iii,y1+iii,state).Type) is None:
            possibleMoves.append((x1-iii,y1+iii))
        elif get_index(x1-iii,y1+iii,state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((x1-iii,y1+iii))
            break
        else:
            break
        

    for iii in range(1,min(7-x1,y1)+1):

        if (get_index(x1+iii,y1-iii,state).Type) is None:
            possibleMoves.append((x1+iii,y1-iii))
        elif get_index(x1+iii,y1-iii,state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((x1+iii,y1-iii))
            break
        else:
            break
        
    return possibleMoves


def check_valid_bishop(x1,y1,x2,y2,state):
    possibleMoves = get_moves_bishop(x1,y1,state)
    if (x2,y2) in possibleMoves:
        state[y1][x1].FirstMove = False
        return True
    print("Bishop can't move there")
    return False

def get_moves_queen(x1,y1,state):
    possibleMoves = get_moves_bishop(x1,y1,state) + get_moves_rook(x1,y1,state)
    return possibleMoves


def check_valid_queen(x1,y1,x2,y2,state):
    possibleMoves = get_moves_queen(x1,y1,state)
    if (x2,y2) in possibleMoves:
        state[y1][x1].FirstMove = False
        return True
    print("Queen can't move there")
    return False
    
def get_moves_king(x1,y1,state):
    possibleMoves = []
    deltas = [(i, u) for i in range(-1, 2) for u in range(-1, 2)]
    for delta in deltas:
        deltaX,deltaY = delta[0], delta[1]
        possibleMoves.append((deltaX+x1,deltaY+y1))
    return possibleMoves


def check_valid_king(x1,y1,x2,y2,state):
    possibleMoves = get_moves_king(x1,y1,state)
    if (x2,y2) in possibleMoves:
        state[y1][x1].FirstMove = False
        return True
    print("King can't move there")
    return False

def get_moves_pawn(x1,y1,state):
    possibleMoves = []

    # tells us direction of the piece
    if state[y1][x1].Colour == "White":
        direction = 1
    else:
        direction = -1
    
    # move forward 1 or 2 if its the pawns first move checks for pieces in the way checks if theres anythign there first
    if get_index(x1, y1+(1*direction), state):
        if get_index(x1, y1+(1*direction), state).Type is None:
            possibleMoves.append((x1,y1+(1*direction)))

    if get_index(x1,y1,state) and get_index(x1,y1+(1*direction),state) and get_index(x1,y1+(2*direction),state):
        if (get_index(x1,y1,state).FirstMove == True) and (get_index(x1,y1+(1*direction),state).Type is None) and (get_index(x1,y1+(2*direction),state).Type is None):
            possibleMoves.append((x1,y1+(2*direction)))

    #Finds attacking moves
    if get_index(x1+1,y1+(1*direction),state) and get_index(x1,y1,state):
        if get_index(x1+1,y1+(1*direction),state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((x1+1,y1+(1*direction)))

    if get_index(x1-1,y1+(1*direction),state) and get_index(x1,y1,state):
        if get_index(x1-1,y1+(1*direction),state).Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((x1-1,y1+(1*direction)))

    return possibleMoves

def check_valid_pawn(x1,y1,x2,y2,state):
    possibleMoves = get_moves_pawn(x1,y1,state)
    if (x2,y2) in possibleMoves:
        state[y1][x1].FirstMove = False
        return True
    print("Pawn can't move there")
    return False



def check_valid(userInput,colourTurn,state):
    x1,y1,x2,y2 = userInput
    if (x1,y1) == (x2,y2):
        print("You can't move a piece to where it already is")
        return False
    
    if get_index(x1,y1,state).Colour == get_index(x2,y2,state).Colour:
        print("You can't capture your own piece")
        return False
    
    if not (0 <= x1 <= 7 and 0 <= y1 <= 7 and 0 <= x2 <= 7 and 0 <= y2 <= 7):
        print("Your trying to move a piece out of the board")
        return False


    if colourTurn:
        if get_index(x1,y1,state).Colour != "White":
            print("That is not your piece")
            return False
    elif not(colourTurn):
        if get_index(x1,y1,state).Colour != "Black":
            print("That is not your piece")
            return False



    typePiece = state[y1][x1].Type

    match typePiece:
        case None:
            return False
        case "rook":
            return check_valid_rook(x1,y1,x2,y2,state)
        case "knight":
            return check_valid_knight(x1,y1,x2,y2,state)
        case "bishop":
            return check_valid_bishop(x1,y1,x2,y2,state)
        case "queen":
            return check_valid_queen(x1,y1,x2,y2,state)
        case "king":
            return check_valid_king(x1,y1,x2,y2,state)
        case "pawn":
            return check_valid_pawn(x1,y1,x2,y2,state)