#include <string>
#include <iostream>
#include <cstdint>
#include <bitset>
#include <vector>

const int up{-8};
const int down{8};
const int right{1};
const int left{-1};
const int upRight{-7};
const int upLeft{-9};
const int downRight{9};
const int downLeft{7};



struct piece
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

struct allMoves
{
    std::vector<std::bitset<64>> kingMoves{};
    std::vector<std::bitset<64>> queenMoves{};
    std::vector<std::bitset<64>> bishopsMoves{};
    std::vector<std::bitset<64>> knightsMoves{};
    std::vector<std::bitset<64>> rooksMoves{};
    std::vector<std::bitset<64>> pawnsMoves{};
};

void get_fen(piece &P)
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

    P.whitePieces = P.whiteKing | P.whiteKing | P.whiteBishops | P.whiteKnights | P.whiteRooks | P.whitePawns;
    P.blackPieces = P.blackKing | P.blackKing | P.blackBishops | P.blackKnights | P.blackRooks | P.blackPawns;
    P.allPieces = P.blackPieces | P.whitePieces;
};

std::bitset<64> get_rook_moves(int index)
{
    std::bitset<64> moves = 0ULL;

    // Up
    for (int i = index + up; i >= 0; i += up)
        moves.set(i);

    // Down
    for (int i = index + down; i < 64; i += down)
        moves.set(i);

    // Right
    for (int i = index + right; i % 8 != 0; i += right)
        moves.set(i);

    // Left
    for (int i = index + left; i % 8 != 7 && i >= 0; i += left)
        moves.set(i);

    return moves;
}


// ------------------ BISHOP ------------------
std::bitset<64> get_bishop_moves(int index)
{
    std::bitset<64> moves = 0ULL;

    // Down-right
    for (int i = index + downRight; i < 64 && (i % 8 != 0); i += downRight)
        moves.set(i);

    // Down-left
    for (int i = index + downLeft; i < 64 && (i % 8 != 7); i += downLeft)
        moves.set(i);

    // Up-right
    for (int i = index + upRight; i >= 0 && (i % 8 != 0); i += upRight)
        moves.set(i);

    // Up-left
    for (int i = index + upLeft; i >= 0 && (i % 8 != 7); i += upLeft)
        moves.set(i);

    return moves;
}


// ------------------ KING ------------------
std::bitset<64> get_king_moves(int index)
{
    std::bitset<64> moves = 0ULL;
    const int directions[8] = {up, down, left, right, upLeft, upRight, downLeft, downRight};

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

// ------------------ KNIGHT ------------------
std::bitset<64> get_knight_moves(int index)
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

// ------------------ QUEEN ------------------
std::bitset<64> get_queen_moves(int index)
{
    return get_rook_moves(index) | get_bishop_moves(index);
}

// ------------------ PAWN ------------------
std::bitset<64> get_pawn_moves(int index, bool isWhite = true)
{
    std::bitset<64> moves = 0ULL;
    int dir = isWhite ? up : down;
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

allMoves createAllMoves(){

    allMoves bitMaskMoves{};
    auto& m = bitMaskMoves;
    m.kingMoves.reserve(64);
    m.queenMoves.reserve(64);
    m.bishopsMoves.reserve(64);
    m.knightsMoves.reserve(64);
    m.rooksMoves.reserve(64);
    m.pawnsMoves.reserve(64);
    
    for (int iii{};iii < 64; ++iii){
        m.kingMoves.push_back(get_king_moves(iii));
        m.queenMoves.push_back(get_queen_moves(iii));
        m.bishopsMoves.push_back(get_bishop_moves(iii));
        m.knightsMoves.push_back(get_knight_moves(iii));
        m.rooksMoves.push_back(get_rook_moves(iii));
        m.pawnsMoves.push_back(get_pawn_moves(iii));
    };
    return m;
}

int main()
{
    piece P{};
    get_fen(P);
    allMoves bitMaskMoves{createAllMoves()};
    return 0;
};
