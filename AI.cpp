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
    std::bitset<64> whiteKing{};
    std::bitset<64> whiteQueen{};
    std::bitset<64> whiteBishops{};
    std::bitset<64> whiteKnights{};
    std::bitset<64> whiteRooks{};
    std::bitset<64> whitePawns{};

    std::bitset<64> blackKing{};
    std::bitset<64> blackQueen{};
    std::bitset<64> blackBishops{};
    std::bitset<64> blackKnights{};
    std::bitset<64> blackRooks{};
    std::bitset<64> blackPawns{};

    std::bitset<64> whitePieces{};
    std::bitset<64> blackPieces{};
    std::bitset<64> allPieces{};
};

struct PrecomputedMoveTables {
    std::array<std::bitset<64>, 64> kingMoves{};
    std::array<std::bitset<64>, 64> queenMoves{};
    std::array<std::bitset<64>, 64> bishopsMoves{};
    std::array<std::bitset<64>, 64> knightsMoves{};
    std::array<std::bitset<64>, 64> rooksMoves{};
    std::array<std::bitset<64>, 64> pawnsMoves{};
};

struct MoveBitboards {
    std::bitset<64> king{};
    std::bitset<64> queen{};
    std::bitset<64> bishops{};
    std::bitset<64> knights{};
    std::bitset<64> rooks{};
    std::bitset<64> pawns{};
    std::bitset<64> attackingPawns{};
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

constexpr std::bitset<64> get_rook_moves(int index)
{
    std::bitset<64> moves = 0ULL;

    // Up
    for (int i = index + NORTH; i >= 0; i += NORTH)
        moves.set(i);

    // Down
    for (int i = index + SOUTH; i < 64; i += SOUTH)
        moves.set(i);

    // Right
    for (int i = index + WEST; i % 8 != 0; i += WEST)
        moves.set(i);

    // Left
    for (int i = index + EAST; i % 8 != 7 && i >= 0; i += EAST)
        moves.set(i);

    return moves;
}



constexpr std::bitset<64> get_bishop_moves(int index)
{
    std::bitset<64> moves = 0ULL;

    // Down-right
    for (int i = index + SOUTH_EAST; i < 64 && (i % 8 != 0); i += SOUTH_EAST)
        moves.set(i);

    // Down-left
    for (int i = index + SOUTH_WEST; i < 64 && (i % 8 != 7); i += SOUTH_WEST)
        moves.set(i);

    // Up-right
    for (int i = index + NORTH_EAST; i >= 0 && (i % 8 != 0); i += NORTH_EAST)
        moves.set(i);

    // Up-left
    for (int i = index + NORTH_WEST; i >= 0 && (i % 8 != 7); i += NORTH_WEST)
        moves.set(i);

    return moves;
}



constexpr std::bitset<64> get_king_moves(int index)
{
    std::bitset<64> moves = 0ULL;
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


constexpr std::bitset<64> get_knight_moves(int index)
{
    std::bitset<64> moves = 0ULL;
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


constexpr std::bitset<64> get_queen_moves(int index)
{
    return get_rook_moves(index) | get_bishop_moves(index);
}


constexpr std::bitset<64> get_pawn_moves(int index, bool isWhite = true)
{
    std::bitset<64> moves = 0ULL;
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

void getAllMoves(PrecomputedMoveTables m, BoardState P, colour){
    MoveBitboards {};


}

int main()
{
    int colour{2}; // probaly could make it 1 bit but not much of a improvement in efficency
    BoardState P{};
    get_fen(P);
    constexpr PrecomputedMoveTables bitMaskMoves{createAllMoves()};

    getAllMoves(bitMaskMoves, P,colour);
    return 0;
};



