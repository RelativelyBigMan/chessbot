# DROPPED EN PASSANT, CASTLING AND PAWN PROMOTION
# King can move into check, not implemented to stop this, its pretty late right now so I dont think I will bother

def get_index(x,y,state):
    if 0 <= x < 8 and 0 <= y < 8:
        return state[y][x]
    return None

def get_moves_rook(x1,y1,state):
    possibleMoves = []
    org = get_index(x1,y1,state)
    for iii in range(x1+1,8):
        trg = get_index(iii,y1,state)
        if trg is None:
            break
        if trg.Type is None:
            possibleMoves.append((iii,y1))
        elif trg.Colour != org.Colour:
            possibleMoves.append((iii,y1))
            break
        else:
            break
    
    for iii in range(x1-1,-1,-1):
        trg = get_index(iii,y1,state)
        if trg is None:
            break
        if trg.Type is None:
            possibleMoves.append((iii,y1))
        elif trg.Colour != org.Colour:
            possibleMoves.append((iii,y1))
            break
        else:
            break

    for iii in range(y1+1,8):
        trg = get_index(x1,iii,state)
        if trg is None:
            break
        if trg.Type is None:
            possibleMoves.append((x1,iii))
        elif trg.Colour != org.Colour:
            possibleMoves.append((x1,iii))
            break
        else:
            break
    
    for iii in range(y1-1,-1,-1):
        trg = get_index(x1,iii,state)
        if trg is None:
            break
        if trg.Type is None:
            possibleMoves.append((x1,iii))
        elif trg.Colour != org.Colour:
            possibleMoves.append((x1,iii))
            break
        else:
            break

    return possibleMoves


def check_valid_rook(x1,y1,x2,y2,state):  
    possibleMoves = get_moves_rook(x1,y1,state)
    if (x2,y2) in possibleMoves:
        return True
    print("Rook can't move there")
    return False


def get_moves_knight(x1,y1,state):
    possibleMoves = []
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]    
    for delta in deltas:
        trg = get_index(delta[0]+x1,delta[1]+y1,state)
        if trg is None:
            continue
        if trg.Type is None or trg.Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((delta[0]+x1,delta[1]+y1))
    return possibleMoves

def check_valid_knight(x1,y1,x2,y2,state):
    possibleMoves = get_moves_knight(x1,y1,state)
    if (x2,y2) in possibleMoves:
        return True
    print("Knight can't move there")
    return False


def get_moves_bishop(x1,y1,state):
    possibleMoves = []
    org = get_index(x1,y1,state)
    # min() gets distance to the edge of the board, somewhat annoying to read/write as coordinates are flipped on the x axis but thats just how the matrix works
    for iii in range(1,min(7-x1,7-y1)+1): 
        trg = get_index(x1+iii,y1+iii,state)
        if trg is None:
            break
        if trg.Type is None:
            possibleMoves.append((x1+iii,y1+iii))
        elif trg.Colour != org.Colour:
            possibleMoves.append((x1+iii,y1+iii))
            break
        else:
            break
        
    
    for iii in range(1,min(x1,y1)+1):
        trg = get_index(x1-iii,y1-iii,state)
        if trg is None:
            break
        if trg.Type is None:
            possibleMoves.append((x1-iii,y1-iii))
        elif trg.Colour != org.Colour:
            possibleMoves.append((x1-iii,y1-iii))
            break
        else:
            break
        

    for iii in range(1,min(x1,7-y1)+1):
        trg = get_index(x1-iii,y1+iii,state)
        if trg is None:
            break

        if trg.Type is None:
            possibleMoves.append((x1-iii,y1+iii))
        elif trg.Colour != org.Colour:
            possibleMoves.append((x1-iii,y1+iii))
            break
        else:
            break
        

    for iii in range(1,min(7-x1,y1)+1):
        trg = get_index(x1+iii,y1-iii,state)
        if trg is None:
            break

        if trg.Type is None:
            possibleMoves.append((x1+iii,y1-iii))
        elif trg.Colour != org.Colour:
            possibleMoves.append((x1+iii,y1-iii))
            break
        else:
            break
        
    return possibleMoves


def check_valid_bishop(x1,y1,x2,y2,state):
    possibleMoves = get_moves_bishop(x1,y1,state)
    if (x2,y2) in possibleMoves:
        return True
    print("Bishop can't move there")
    return False

def get_moves_queen(x1,y1,state):
    possibleMoves = get_moves_bishop(x1,y1,state) + get_moves_rook(x1,y1,state)
    return possibleMoves


def check_valid_queen(x1,y1,x2,y2,state):
    possibleMoves = get_moves_queen(x1,y1,state)
    if (x2,y2) in possibleMoves:
        return True
    print("Queen can't move there")
    return False
    
def get_moves_king(x1,y1,state):
    possibleMoves = []
    #[(i, u) for i in range(-1, 2) for u in range(-1, 2) if not (i==0 and u==0)]
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] 

    for delta in deltas:
        trg = get_index(delta[0]+x1,delta[1]+y1,state)
        if trg is None:
            continue

        if trg.Type is None or trg.Colour != get_index(x1,y1,state).Colour:
            possibleMoves.append((delta[0]+x1,delta[1]+y1))
    return possibleMoves


def check_valid_king(x1,y1,x2,y2,state):
    possibleMoves = get_moves_king(x1,y1,state)
    if (x2,y2) in possibleMoves:
        return True
    print("King can't move there")
    return False

def get_moves_pawn(x1,y1,state):
    possibleMoves = []

    org = get_index(x1,y1,state)
    if org is None:
        return possibleMoves

    # tells us direction of the piece
    if org.Colour == "White":
        direction = 1
    else:
        direction = -1
    
    # move forward 1
    forward1 = get_index(x1, y1+direction, state)
    if forward1 and forward1.Type is None:
        possibleMoves.append((x1,y1+direction))


    forward2 = get_index(x1, y1+2*direction, state)
    if org.FirstMove and forward1 and forward1.Type is None and forward2 and forward2.Type is None:
        possibleMoves.append((x1,y1+2*direction))

    for xxx in (1,-1):
        trg = get_index(x1+xxx,y1+direction,state)
        if trg and trg.Type is not None and trg.Colour != org.Colour:
            possibleMoves.append((x1+xxx,y1+direction))

    return possibleMoves

def get_attack_moves_pawn(x1,y1,state):
    possibleMoves = []

    org = get_index(x1,y1,state)
    if org is None:
        return possibleMoves

    # tells us direction of the piece
    if org.Colour == "White":
        direction = 1
    else:
        direction = -1
    
    for xxx in (1,-1):
        trg = get_index(x1+xxx,y1+direction,state)
        if trg and trg.Type is not None and trg.Colour != org.Colour:
            possibleMoves.append((x1+xxx,y1+direction))

    return possibleMoves


def check_valid_pawn(x1,y1,x2,y2,state):
    possibleMoves = get_moves_pawn(x1,y1,state)
    if (x2,y2) in possibleMoves:
        return True
    print("Pawn can't move there")
    return False



def check_valid(userInput,colourTurn,state):
    x1,y1,x2,y2 = userInput
    # bounds check first
    if not (0 <= x1 <= 7 and 0 <= y1 <= 7 and 0 <= x2 <= 7 and 0 <= y2 <= 7):
        print("Your trying to move a piece out of the board")
        return False

    if (x1,y1) == (x2,y2):
        print("You can't move a piece to where it already is")
        return False
    
    src = get_index(x1,y1,state)
    dst = get_index(x2,y2,state)
    if src is None:
        print("No piece at source")
        return False
    if dst is None:
        print("Destination out of bounds")
        return False

    if src.Colour == dst.Colour and src.Colour is not None:
        print("You can't capture your own piece")
        return False


    if colourTurn:
        if src.Colour != "White":
            print("That is not your piece")
            return False
    else:
        if src.Colour != "Black":
            print("That is not your piece")
            return False



    typePiece = src.Type

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