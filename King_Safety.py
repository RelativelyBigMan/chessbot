import Move_Validation as M


def get_check(colourTurn,state):
    all_moves = []
    for yyy in range(8):
        for xxx in range(8):
            if state[yyy][xxx].Colour == None:
                continue
            # print(all_moves)
            typePiece,Colour = state[yyy][xxx].Type, state[yyy][xxx].Colour
            if colourTurn and Colour == "White":
                match typePiece:
                    case None:
                        continue
                    case "rook":
                        all_moves.append(M.get_moves_rook(xxx,yyy,state))
                    case "knight":
                        all_moves.append(M.get_moves_knight(xxx,yyy,state))
                    case "bishop":
                        all_moves.append(M.get_moves_bishop(xxx,yyy,state))
                    case "queen":
                        all_moves.append(M.get_moves_queen(xxx,yyy,state))
                    case "king":
                        all_moves.append(M.get_moves_king(xxx,yyy,state))
                    case "pawn":
                        all_moves.append(M.get_moves_pawn(xxx,yyy,state))

    print(all_moves)