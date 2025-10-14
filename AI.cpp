#include <iostream>
#include <cstdint>
#include <string>
#include <vector>

const int NORTH{-8};
const int SOUTH{8};
const int WEST{1};
const int EAST{-1};
const int NORTH_EAST{-7};
const int NORTH_WEST{-9};
const int SOUTH_EAST{9};
const int SOUTH_WEST{7};

enum Colours
{
    WHITE,
    BLACK
};
enum type_of_piece
{
    PAWN,
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN,
    KING
};

struct Piece
{
    int type{};
    bool Colour{};
    bool firstMove{};
};

// switch statement taken from somewhere, not much to steal though because it was using 
// could pass by refernence but compiler is smart enough to know to use pass by refernce
void setFEN(std::string aFEN, std::vector<Piece> allPieces)
{
    size_t j{0};
    int square_index{0};
    while (j < aFEN.length()){
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
                default:  return;
            }
        ++j;
    }
    return;
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

int main()
{
    std::string aFEN{"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"};
    std::vector<Piece> allPieces(64);
    setFEN(aFEN, allPieces);
    std::cout << allPieces[0];
};
