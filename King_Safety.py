import Move_Validation as M
import Main


def get_all_moves(colourTurn,state):
    all_moves = []
    king_pos = None

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
            if typePiece == "king" and Colour == curColour:
                king_pos = (xxx,yyy)
            if Colour == curColour:
                match typePiece:
                    case None:
                        continue
                    case "rook":
                        all_moves.extend(M.get_moves_rook(xxx,yyy,state))
                    case "knight":
                        all_moves.extend(M.get_moves_knight(xxx,yyy,state))
                    case "bishop":
                        all_moves.extend(M.get_moves_bishop(xxx,yyy,state))
                    case "queen":
                        all_moves.extend(M.get_moves_queen(xxx,yyy,state))
                    case "king":
                        all_moves.extend(M.get_moves_king(xxx,yyy,state))
                    case "pawn":
                        all_moves.extend(M.get_moves_pawn(xxx,yyy,state))
    return all_moves,king_pos


def get_pawn_attacks(x1,y1,state):
    attacks = []
    org = state[y1][x1]
    if org is None or org.Colour is None:
        return attacks
    
    direction = 1 if org.Colour == "White" else -1
    for x in (-1,1):
        nx,ny = x1+x, y1+direction
        if 0 <= nx < 8 and 0 <= ny < 8:
            attacks.append((nx,ny))
    return attacks


def get_check(colourTurn,state):
    # check if the side colourTurn is in check
    opponent = not colourTurn
    opponent_moves, _ = get_all_moves(opponent, state)
    # add pawn attack squares for opponent pawns
    for y in range(8):
        for x in range(8):
            p = state[y][x]
            if p.Colour is None:
                continue
            if p.Colour == ("White" if opponent else "Black") and p.Type == "pawn":
                opponent_moves.extend(get_pawn_attacks(x,y,state))

    _, king_pos = get_all_moves(colourTurn, state)
    if king_pos is None:
        return False
    return king_pos in opponent_moves


def undo_move(x1,y1,x2,y2,state,prev_piece):
    state[y1][x1] = state[y2][x2]
    state[y2][x2] = prev_piece


def get_checkmate(colourTurn,state):
    curColour = "White" if colourTurn else "Black"

    for y in range(8):
        for x in range(8):
            piece = state[y][x]
            if piece.Colour != curColour:
                continue
            moves = []
            match piece.Type:
                case "rook":
                    moves = M.get_moves_rook(x,y,state)
                case "knight":
                    moves = M.get_moves_knight(x,y,state)
                case "bishop":
                    moves = M.get_moves_bishop(x,y,state)
                case "queen":
                    moves = M.get_moves_queen(x,y,state)
                case "king":
                    moves = M.get_moves_king(x,y,state)
                case "pawn":
                    moves = M.get_moves_pawn(x,y,state)
            for (x2,y2) in moves:
                src_piece = state[y][x]
                dst_piece = state[y2][x2]
                state[y2][x2] = src_piece
                state[y][x] = Main.Piece(None,None,None)
                if not get_check(colourTurn, state):
                    state[y][x] = src_piece
                    state[y2][x2] = dst_piece
                    return False
                state[y][x] = src_piece
                state[y2][x2] = dst_piece
    return True

