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
            if typePiece == "king" and Colour != curColour:
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




def get_check(colourTurn,state):
    opponent_moves, king_pos = get_all_moves(not colourTurn, state)
    return king_pos in opponent_moves




def get_checkmate(colourTurn,state):
    curColour = "White" if colourTurn else "Black"

    for yyy in range(8):
        for xxx in range(8):
            piece = state[yyy][xxx]
            if piece.Colour != curColour:
                continue
            moves = []
            match piece.Type:
                case "rook":
                    moves = M.get_moves_rook(xxx,yyy,state)
                case "knight":
                    moves = M.get_moves_knight(xxx,yyy,state)
                case "bishop":
                    moves = M.get_moves_bishop(xxx,yyy,state)
                case "queen":
                    moves = M.get_moves_queen(xxx,yyy,state)
                case "king":
                    moves = M.get_moves_king(xxx,yyy,state)
                case "pawn":
                    moves = M.get_attack_moves_pawn(xxx,yyy,state)
            for (x2,y2) in moves:
                org = state[yyy][xxx]
                trg = state[y2][x2]
                # make the move
                state[y2][x2] = org
                state[yyy][xxx] = Main.Piece(None,None,None)
                if not get_check(colourTurn, state):
                    
                    # undo the move
                    state[yyy][xxx] = org
                    state[y2][x2] = trg
                    return False
                state[yyy][xxx] = org
                state[y2][x2] = trg
    return True

