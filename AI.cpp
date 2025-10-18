#include <iostream>
#include <cstdint>
#include <string>
#include <string_view>
#include <vector>
#include <algorithm>

const int NORTH{-8};
const int SOUTH{8};
const int WEST{-1};
const int EAST{1};
const int NORTH_EAST{-7};
const int EAST_SOUTH{9};
const int SOUTH_WEST{7};
const int WEST_NORTH{-9};

// deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]  
constexpr int KNIGHT_DELTA[8] = {
    NORTH*2 + WEST,   
    NORTH*2 + EAST,   
    SOUTH*2 + WEST,   
    SOUTH*2 + EAST,   
    NORTH + WEST*2,   
    NORTH + EAST*2,   
    SOUTH + WEST*2,   
    SOUTH + EAST*2    
};

// deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] 
constexpr int KING_DELTA[8] = {
    NORTH + WEST,  // up-left      (-1, -1)
    NORTH,         // up           (-1, 0)
    NORTH + EAST,  // up-right     (-1, 1)
    WEST,          // left         (0, -1)
    EAST,          // right        (0, 1)
    SOUTH + WEST,  // down-left    (1, -1)
    SOUTH,         // down         (1, 0)
    SOUTH + EAST   // down-right   (1, 1)
};




enum Colours
{
    WHITE,
    BLACK
};
enum type_of_piece
{
    NOPIECE,
    PAWN,
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN,
    KING
};


struct Move {
    int from;
    int to;
};


struct allMoves {
    std::vector<Move> pawn{}; // 16
    std::vector<Move> knight{}; // 16
    std::vector<Move> bishop{}; // 28
    std::vector<Move> rook{}; // 28
    std::vector<Move> queen{}; // 28
    std::vector<Move> king{}; // 8

    allMoves() {
        pawn.reserve(32);
        knight.reserve(16);
        bishop.reserve(28);
        rook.reserve(28);
        queen.reserve(28);
        king.reserve(8);
    }
};



struct Piece
{
    int type{};
    bool Colour{};
    bool firstMove{};
};


bool inBounds(int x) {
    return x >= 0 && x < 64;
}

// switch statement taken from somewhere, not much to steal though because it was using 
// could pass by refernence but compiler is smart enough to know to use pass by refernce
bool setFEN(std::string_view aFEN, std::vector<Piece>& allPieces)
{
    size_t j{0};
    int square_index{0};
    bool stop{false};
    while (j < aFEN.length()){
        if (stop == true){
            break;
        }
        switch (aFEN.at(j))
            {
                case 'p': allPieces[square_index] = Piece{PAWN,BLACK,true};  square_index++; break;
                case 'r': allPieces[square_index] = Piece{ROOK,BLACK,true};  square_index++; break;
                case 'n': allPieces[square_index] = Piece{KNIGHT,BLACK,true};square_index++; break;
                case 'b': allPieces[square_index] = Piece{BISHOP,BLACK,true};square_index++; break;
                case 'q': allPieces[square_index] = Piece{QUEEN,BLACK,true}; square_index++; break;
                case 'k': allPieces[square_index] = Piece{KING,BLACK,true};  square_index++; break;
                case 'P': allPieces[square_index] = Piece{PAWN,WHITE,true};  square_index++; break;
                case 'R': allPieces[square_index] = Piece{ROOK,WHITE,true};  square_index++; break;
                case 'N': allPieces[square_index] = Piece{KNIGHT,WHITE,true};square_index++; break;
                case 'B': allPieces[square_index] = Piece{BISHOP,WHITE,true};square_index++; break;
                case 'Q': allPieces[square_index] = Piece{QUEEN,WHITE,true}; square_index++; break;
                case 'K': allPieces[square_index] = Piece{KING,WHITE,true};  square_index++; break;
                case '/':                                                      break;
                case '1':                                                      break;
                case '2': square_index++;                                      break;
                case '3': square_index += 2;                                   break;
                case '4': square_index += 3;                                   break;
                case '5': square_index += 4;                                   break;
                case '6': square_index += 5;                                   break;
                case '7': square_index += 6;                                   break;
                case '8': square_index += 7;                                   break;
                case ' ': stop = true;                                         break;
                
            }
        ++j;
    }
    if (aFEN.at(j) == 'w'){
        return false;
    } else{
        return true;
    }
}

// https://www.learncpp.com/cpp-tutorial/introduction-to-overloading-the-i-o-operators/
std::ostream& operator<<(std::ostream& os, const Piece& P){
    std::string type{};
    switch (P.type)
        {
            case PAWN:   type = "PAWN";   break;
            case KNIGHT: type = "KNIGHT"; break;
            case BISHOP: type = "BISHOP"; break;
            case ROOK:   type = "ROOK";   break;
            case QUEEN:  type = "QUEEN";  break;
            case KING:   type = "KING";   break;
            default: std::cout << "No type value"; break;
        }
    os << type << " " << (P.Colour ? "White" : "Black") << " " << (P.firstMove ? "True" : "False") << "\n";
    return os;
};

std::ostream& operator<<(std::ostream& os, const std::vector<Move>& moveArray){
    int8_t iii{0};
    while  (iii < moveArray.size()){
        os << static_cast<int>(moveArray[iii].from) << " " << static_cast<int>(moveArray[iii].to) << " ";
        ++iii;
    };
    return os;
}


void get_moves_rook(int index, const std::vector<Piece>& allPieces, allMoves& M) {
    Piece org = allPieces[index];
    for (int i = index + WEST; inBounds(i) && i / 8 == index / 8; i += WEST) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.rook.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.rook.push_back({index,i});
            break;
        }
    }

    for (int i = index + EAST; inBounds(i) && i / 8 == index / 8; i += EAST) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.rook.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.rook.push_back({index,i});
            break;
        }
    }

    for (int i = index + NORTH; inBounds(i); i += NORTH) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.rook.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.rook.push_back({index,i});
            break;
        }
    }
    for (int i = index + SOUTH; inBounds(i);i += SOUTH) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.rook.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.rook.push_back({index,i});
            break;
        }
    }
};



//seems somewhat buggy might change to the same implementation as my python
void get_bishop_moves(int index, const std::vector<Piece>& allPieces, allMoves& M) {

    Piece org = allPieces[index];
    int movesToNorth{7 - (index / 8)};
    int movesToSouth{index / 8};
    int movesToEast{7 - (index % 8)};
    int movesToWest{index % 8};


    int movesToNE{std::min(movesToNorth,movesToEast)};
    int movesToES{std::min(movesToEast,movesToSouth)};
    int movesToSW{std::min(movesToSouth,movesToWest)};
    int movesToWN{std::min(movesToWest,movesToNorth)};


    int i{0};
    for (int iii{1}; iii <= movesToNE; ++iii) {
        i = index + iii*NORTH_EAST;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.bishop.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.bishop.push_back({index,i});
                break;
            }
        }
    }

    for (int iii{1}; iii <= movesToES; ++iii) {
        i = index + iii*EAST_SOUTH;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.bishop.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.bishop.push_back({index,i});
                break;
            }
        }

    }
        for (int iii{1}; iii <= movesToSW; ++iii) {
        i = index + iii*SOUTH_WEST;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.bishop.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.bishop.push_back({index,i});
                break;
            }
        }

    }
        for (int iii{1}; iii <= movesToWN; ++iii) {
        i = index + iii*WEST_NORTH;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.bishop.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.bishop.push_back({index,i});
                break;
            }
        }
    }
    
}

// deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)] 
void get_king_moves(int index, const std::vector<Piece>& allPieces, allMoves& M){
    Piece org{allPieces[index]};
    for (int i:KING_DELTA){
        int newIndex = index+i;
        // checks if its out of bounds
        if (!inBounds(newIndex)){
            continue;
        }
        // gets the diff between the two cols and rows and sees if its more than 1
        if (abs((newIndex / 8) - (index / 8)) > 1 || abs((newIndex % 8) - (index % 8)) > 1){
            continue;
        }
        Piece trg = allPieces[newIndex];
        
        if (trg.type == NOPIECE || trg.Colour != org.Colour){
            M.king.push_back({index,newIndex});
        }
    }
};

// deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]  
void get_knight_moves(int index, const std::vector<Piece>& allPieces, allMoves& M){
    Piece org{allPieces[index]};
    for (int i:KNIGHT_DELTA){
        int newIndex = index+i;
        if (!inBounds(newIndex)){
            continue;
        }
        // gets the diff between the two cols and rows and sees if its more than 2, could probaly check if one dimensio nchanegs by 1 and the other by 2 but I think this works
        if (abs((newIndex / 8) - (index / 8)) > 2 || abs((newIndex % 8) - (index % 8)) > 2){
            continue;
        }
        Piece trg = allPieces[newIndex];
        
        if (trg.type == NOPIECE || trg.Colour != org.Colour){
            M.knight.push_back({index,newIndex});
        }
    }
};

void get_queen_moves(int index, const std::vector<Piece>& allPieces, allMoves& M){
    Piece org = allPieces[index];
    int movesToNorth{7 - (index / 8)};
    int movesToSouth{index / 8};
    int movesToEast{7 - (index % 8)};
    int movesToWest{index % 8};


    int movesToNE{std::min(movesToNorth,movesToEast)};
    int movesToES{std::min(movesToEast,movesToSouth)};
    int movesToSW{std::min(movesToSouth,movesToWest)};
    int movesToWN{std::min(movesToWest,movesToNorth)};

    int i{0};
    for (int iii{1}; iii <= movesToNE; ++iii) {
        i = index + iii*NORTH_EAST;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.queen.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.queen.push_back({index,i});
                break;
            }
        }
    }

    for (int iii{1}; iii <= movesToES; ++iii) {
        i = index + iii*EAST_SOUTH;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.queen.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.queen.push_back({index,i});
                break;
            }
        }
    }
        for (int iii{1}; iii <= movesToSW; ++iii) {
        i = index + iii*SOUTH_WEST;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.queen.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.queen.push_back({index,i});
                break;
            }
        }
    }
        for (int iii{1}; iii <= movesToWN; ++iii) {
        i = index + iii*WEST_NORTH;
        if (inBounds(i)){
            Piece trg = allPieces[i];
            if (trg.type == NOPIECE){
                M.queen.push_back({index,i});
            }
            else if(trg.Colour == org.Colour){
                break;
            }
            else if (trg.Colour != org.Colour){
                M.queen.push_back({index,i});
                break;
            }
        }
    }

    for (int i = index + WEST; inBounds(i) && i / 8 == index / 8; i += WEST) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.queen.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.queen.push_back({index,i});
            break;
        }
    }

    for (int i = index + EAST; inBounds(i) && i / 8 == index / 8; i += EAST) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.queen.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.queen.push_back({index,i});
            break;
        }
    }

    for (int i = index + NORTH; inBounds(i); i += NORTH) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.queen.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.queen.push_back({index,i});
            break;
        }
    }
    for (int i = index + SOUTH; inBounds(i);i += SOUTH) {
        Piece trg = allPieces[i];
        if (trg.type == NOPIECE) {
            M.queen.push_back({index,i});
        } else {
            if (trg.Colour != org.Colour) M.queen.push_back({index,i});
            break;
        }
    }
    
};


void get_pawn_moves(int index, const std::vector<Piece>& allPieces, allMoves& M){
    Piece org{allPieces[index]};
    int direction{(org.Colour == WHITE) ? NORTH : SOUTH};
    // uses int instead of Piece directly because of out of bounds issues
    int forward1{index + direction};
    int forward2{index + 2*direction};
    int trg1{index + direction + EAST};
    int trg2{index + direction + WEST};
    
    if (inBounds(forward1) && allPieces[forward1].type == NOPIECE){
        M.pawn.push_back({index,forward1});
        if (org.firstMove && inBounds(forward2) && allPieces[forward2].type == NOPIECE){
            M.pawn.push_back({index,forward2});
        }
    }

    if (inBounds(trg1)) {
        Piece target1 = allPieces[trg1];
        if (target1.type != NOPIECE && target1.Colour != org.Colour && (!(abs((trg1 / 8) - (index / 8)) > 1 || abs((trg1 % 8) - (index % 8)) > 1))) {
            M.pawn.push_back({index,trg1});
        }
    }
    if (inBounds(trg2)) {
        Piece target2 = allPieces[trg2];
        if (target2.type != NOPIECE && target2.Colour != org.Colour && (!(abs((trg2 / 8) - (index / 8)) > 1 || abs((trg2 % 8) - (index % 8)) > 1))) {
            M.pawn.push_back({index,trg2});
        }
    }
}

int eval(const std::vector<Piece>& allPieces,bool colour){
    int score{0};
    int value{0};
    for (int i{0}; i<64; ++i){

        Piece cur = allPieces[i];
        if (cur.type == NOPIECE){
            continue;
        }
        switch(cur.type){
            case PAWN:   value = 100; break;
            case KNIGHT: value = 320; break;
            case BISHOP: value = 330; break;
            case ROOK:   value = 500; break;
            case QUEEN:  value = 900; break;
            case KING:   value = 20000; break;
        }
        score += (cur.Colour == static_cast<int>(colour)) ? value : -value;
    }
    return score;
}

void get_all_moves(const std::vector<Piece>& allPieces, allMoves& M, bool colour){
    for (int i{0}; i<64; ++i){
        Piece cur = allPieces[i];
        if (!(cur.type == NOPIECE) && (colour == cur.Colour)){
            switch(cur.type){
                case(PAWN): get_pawn_moves(i, allPieces, M); break;
                case(ROOK): get_moves_rook(i, allPieces, M); break;
                case(BISHOP): get_bishop_moves(i, allPieces, M); break;
                case(KING): get_king_moves(i,allPieces,M); break;
                case(QUEEN): get_queen_moves(i,allPieces,M); break;
                case(KNIGHT): get_knight_moves(i,allPieces,M); break;
            }
        }
        
    }
};




//well aware that this makes a copy every time I will redo this later more efficently
std::vector<Piece> make_move(const std::vector<Piece>& allPieces, const Move& move){
    std::vector<Piece> copyBoard = allPieces;
    copyBoard[move.to] = copyBoard[move.from];
    copyBoard[move.from] = Piece{NOPIECE, false, false};
    copyBoard[move.to].firstMove = false;
    return copyBoard;
};




// def min_max2(BOARD):
//     moves = list(BOARD.legal_moves)
//     scores = []

//     for move in moves:
//         temp = deepcopy(BOARD)
//         temp.push(move)
//         temp_best_move = most_value_agent(temp)
//         temp.push(temp_best_move)
//         scores.append(eval_board(temp))

//     if BOARD.turn == True:
        
//         best_move = moves[scores.index(max(scores))]

//     else:
//         best_move = moves[scores.index(min(scores))]

//     return best_move




int minimax(int depth, bool colour, const std::vector<Piece>& allPieces){
    if (depth == 0){
        return eval(allPieces,colour);
    }
    allMoves M{};
    get_all_moves(allPieces, M, colour);
    std::vector<Move> allPossibleMoves{};
    allPossibleMoves.insert(allPossibleMoves.end(), M.pawn.begin(), M.pawn.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.queen.begin(), M.queen.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.bishop.begin(), M.bishop.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.king.begin(), M.king.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.knight.begin(), M.knight.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.rook.begin(), M.rook.end());

    int bestEval = colour ? -999999 : 999999;
    for (Move move: allPossibleMoves){
        auto newAllPieces = make_move(allPieces, move);
        int evalValue = minimax(depth - 1, !colour, newAllPieces);

        if (colour)
            bestEval = std::max(bestEval, evalValue);
        else
            bestEval = std::min(bestEval, evalValue);
    }

    return bestEval;

};

struct MinimaxRes{
    int eval;
    Move bestMove;
};

// does minimax recursion on all moves after the intital moves so that it dosent need to return MinimaxRes struct on every return
MinimaxRes find_best_move(int depth, bool colour, const std::vector<Piece>& allPieces){
    allMoves M{};
    get_all_moves(allPieces, M, colour);
    std::vector<Move> allPossibleMoves{};

    allPossibleMoves.insert(allPossibleMoves.end(), M.pawn.begin(), M.pawn.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.queen.begin(), M.queen.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.bishop.begin(), M.bishop.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.king.begin(), M.king.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.knight.begin(), M.knight.end());
    allPossibleMoves.insert(allPossibleMoves.end(), M.rook.begin(), M.rook.end());

    int bestEval = colour ? -999999 : 999999;
    Move bestMove;
    for (Move move: allPossibleMoves){
        auto newAllPieces = make_move(allPieces, move);
        int evalValue = minimax(depth - 1, !colour, newAllPieces);

        if (colour) {
            if (evalValue > bestEval) {
                bestEval = evalValue;
                bestMove = move;
            }
        } else {
            if (evalValue < bestEval) {
                bestEval = evalValue;
                bestMove = move;
            }
        }
    }
    return {bestEval,bestMove};

};




// https://www.geeksforgeeks.org/cpp/command-line-arguments-in-cpp/

int main(int argc, char* argv[])
{
    std::string aFEN{argv[1]};
    // std::string aFEN{"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b"};
    std::vector<Piece> allPieces(64);
    bool colour{setFEN(aFEN, allPieces)};
    MinimaxRes res {find_best_move(4,colour,allPieces)};
    std::cout << res.bestMove.from << " " << res.bestMove.to << "\n";
};
