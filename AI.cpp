typedef uint64_t U64;
#include <string>
#include <iostream>
#include <cstdint>
#include <bitset>
#include <array>


const int NORTH{-8};
const int SOUTH{8};
const int WEST{1};
const int EAST{-1};
const int NORTH_EAST{-7};
const int NORTH_WEST{-9};
const int SOUTH_EAST{9};
const int SOUTH_WEST{7};



struct BoardState
{
    U64 whiteKing{};
    U64 whiteQueen{};
    U64 whiteBishops{};
    U64 whiteKnights{};
    U64 whiteRooks{};
    U64 whitePawns{};

    U64 blackKing{};
    U64 blackQueen{};
    U64 blackBishops{};
    U64 blackKnights{};
    U64 blackRooks{};
    U64 blackPawns{};

    U64 whitePieces{};
    U64 blackPieces{};
    U64 allPieces{};
};

struct PrecomputedMoveTables {
    std::array<U64, 64> kingMoves{};
    std::array<U64, 64> queenMoves{};
    std::array<U64, 64> bishopsMoves{};
    std::array<U64, 64> knightsMoves{};
    std::array<U64, 64> rooksMoves{};
    std::array<U64, 64> pawnsMoves{};
};

struct MoveBitboards {
    U64 king{};
    U64 queen{};
    U64 bishops{};
    U64 knights{};
    U64 rooks{};
    U64 pawns{};
    U64 attackingPawns{};
};

void get_fen(BoardState &P)
{
    P.whiteKing = 1ULL << 4;
    P.whiteQueen = 1ULL << 3;
    P.whiteBishops = (1ULL << 2) | (1ULL << 5);
    P.whiteKnights = (1ULL << 1) | (1ULL << 6);
    P.whiteRooks = (1ULL << 0) | (1ULL << 7);
    P.whitePawns = 65280ULL;

    P.blackKing = 1ULL << 60;
    P.blackQueen = 1ULL << 59;
    P.blackBishops = (1ULL << 58) | (1ULL << 61);
    P.blackKnights = (1ULL << 57) | (1ULL << 62);
    P.blackRooks = (1ULL << 56) | (1ULL << 63);
    P.blackPawns = 71776119061217280ULL;

    P.whitePieces = P.whiteKing | P.whiteBishops | P.whiteKnights | P.whiteRooks | P.whitePawns;
    P.blackPieces = P.blackKing | P.blackBishops | P.blackKnights | P.blackRooks | P.blackPawns;
    P.allPieces = P.blackPieces | P.whitePieces;
};

constexpr U64 get_rook_moves(int index)
{
    U64 moves = 0ULL;

    // Up
    for (int i = index + NORTH; i >= 0; i += NORTH)
        moves |= 1ULL << i;

    // Down
    for (int i = index + SOUTH; i < 64; i += SOUTH)
        moves |= 1ULL << i;


    // Right
    for (int i = index + WEST; i % 8 != 0; i += WEST)
        moves |= 1ULL << i;


    // Left
    for (int i = index + EAST; i % 8 != 7 && i >= 0; i += EAST)
        moves |= 1ULL << i;


    return moves;
}



constexpr U64 get_bishop_moves(int index)
{
    U64 moves = 0ULL;

    // Down-right
    for (int i = index + SOUTH_EAST; i < 64 && (i % 8 != 0); i += SOUTH_EAST)
        moves |= 1ULL << i;


    // Down-left
    for (int i = index + SOUTH_WEST; i < 64 && (i % 8 != 7); i += SOUTH_WEST)
        moves |= 1ULL << i;


    // Up-right
    for (int i = index + NORTH_EAST; i >= 0 && (i % 8 != 0); i += NORTH_EAST)
        moves |= 1ULL << i;


    // Up-left
    for (int i = index + NORTH_WEST; i >= 0 && (i % 8 != 7); i += NORTH_WEST)
        moves |= 1ULL << i;


    return moves;
}



constexpr U64 get_king_moves(int index)
{
    U64 moves = 0ULL;
    const int directions[8] = {NORTH, SOUTH, EAST, WEST, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST};

    for (int dir : directions)
    {
        int target = index + dir;
        if (target < 0 || target >= 64)
            continue;
        if (abs((target % 8) - (index % 8)) > 1)
            continue; // avoid wrapping
        moves |= 1ULL << target;
    }

    return moves;
}


constexpr U64 get_knight_moves(int index)
{
    U64 moves = 0ULL;
    const int offsets[8] = {17, 15, 10, 6, -17, -15, -10, -6};

    for (int off : offsets)
    {
        int target = index + off;
        if (target < 0 || target >= 64)
            continue;
        int dx = abs((target % 8) - (index % 8));
        int dy = abs((target / 8) - (index / 8));
        if (dx + dy == 3 && dx != 0 && dy != 0)
            moves |= 1ULL << target;
    }

    return moves;
}


constexpr U64 get_queen_moves(int index)
{
    return get_rook_moves(index) | get_bishop_moves(index);
}


constexpr U64 get_pawn_moves(int index, bool isWhite = true)
{
    U64 moves = 0ULL;
    int dir = isWhite ? NORTH : SOUTH;
    int startRank = isWhite ? 1 : 6;
    int rank = index / 8;

    // One step
    int one = index + dir;
    if (one >= 0 && one < 64)
        moves |= 1ULL << one;

    // Two-step from starting rank
    if (rank == startRank)
    {
        int two = index + 2 * dir;
        if (two >= 0 && two < 64)
            moves |= 1ULL << two;
    }

    return moves;
}

constexpr PrecomputedMoveTables createAllMoves(){

    PrecomputedMoveTables bitMaskMoves{};
    auto& m = bitMaskMoves;
    
    for (int iii{};iii < 64; ++iii){
        m.kingMoves[iii] = (get_king_moves(iii));
        m.queenMoves[iii] = (get_queen_moves(iii));
        m.bishopsMoves[iii] = (get_bishop_moves(iii));
        m.knightsMoves[iii] = (get_knight_moves(iii));
        m.rooksMoves[iii] = (get_rook_moves(iii));
        m.pawnsMoves[iii] = (get_pawn_moves(iii));
    };
    return bitMaskMoves;
}

int pop_highest_bit(U64 &x) {
    if (x == 0) return 0;
    int pos = 63 - __builtin_clzll(x); // 63 since its index by 1 insted of 0
    x ^= (1u << pos);
    return pos;
}


void get_all_moves(PrecomputedMoveTables m, BoardState P, int colour){
    MoveBitboards workingState{};
    auto& W{workingState};

    MoveBitboards allPossibleMoves{};
    auto& moves{allPossibleMoves};
    enum colours{white,black};

    int iii{};
    if (colour == white){
        W.attackingPawns = P.whitePawns;
        W.queen = P.whiteQueen;
        W.bishops = P.whiteBishops;
        W.knights = P.whiteKnights;
        W.rooks = P.whiteRooks;
        W.pawns = P.whitePawns;

        while (W.queen){
            int iii = pop_highest_bit(W.queen);
            moves.queen |= (m.queenMoves[iii] & ~P.whitePieces); // doesent deal with oppsite side pieces
        };
    }
    else if (colour == black)
    {
        W.attackingPawns = P.blackPawns;
        W.queen = P.blackQueen;
        W.bishops = P.blackBishops;
        W.knights = P.blackKnights;
        W.rooks = P.blackRooks;
        W.pawns = P.blackPawns;
    }
    else{
        std::cout << "invalid colour";
    };


    


}

int main()
{
    int colour{0}; // probaly could make it 1 bit but not much of a improvement in efficency
    BoardState P{};
    get_fen(P);
    constexpr PrecomputedMoveTables bitMaskMoves{createAllMoves()};

    get_all_moves(bitMaskMoves, P, colour);
    return 0;
};



