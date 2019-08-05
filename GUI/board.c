#include <stdlib.h>
#include <stdio.h>
#include "board.h"


static int piece_counter = 0;

Board * initialize_board(){
    Board * board = (Board *) malloc(sizeof(Board));
    initialize_pawns(board);
    initialize_rooks(board);
    initialize_knights(board);
    initialize_bishops(board);
    initialize_queens(board);
    initialize_kings(board);
    return board;
}

void initialize_pawns(Board * board){
    int i;
    for(i = 0; i < 8; i++){
        Tile w_pawn_tile, b_pawn_tile;
        w_pawn_tile.row = 1;
        w_pawn_tile.col = i;
        w_pawn_tile.path_to_img = realpath("../GUI/imgs/white_pawn.png", NULL);
        w_pawn_tile.piece_type = 'p';

        b_pawn_tile.row = 6;
        b_pawn_tile.col = i;
        b_pawn_tile.path_to_img = realpath("../GUI/imgs/black_pawn.png", NULL);
        b_pawn_tile.piece_type = 'p';

        board->pieces[piece_counter] = w_pawn_tile;
        board->pieces[piece_counter + 1] = b_pawn_tile;
        piece_counter += 2;
    }
}

void initialize_rooks(Board * board){
    const char * white_path = "../GUI/imgs/white_rook.png";
    const char * black_path = "../GUI/imgs/black_rook.png";
    int indices[8] = {0, 0, 0, 7, 7, 0, 7, 7};
    initialize_minor_piece(board, white_path, black_path, indices, 'R');
}

void initialize_knights(Board * board){
    const char * white_path = "../GUI/imgs/white_knight.png";
    const char * black_path = "../GUI/imgs/black_knight.png";
    int indices[8] = {0, 1, 0, 6, 7, 1, 7, 6};
    initialize_minor_piece(board, white_path, black_path, indices, 'N');
}

void initialize_bishops(Board * board){
    const char * white_path = "../GUI/imgs/white_bishop.png";
    const char * black_path = "../GUI/imgs/black_bishop.png";
    int indices[8] = {0, 2, 0, 5, 7, 2, 7, 5};
    initialize_minor_piece(board, white_path, black_path, indices, 'B');
}

void initialize_queens(Board * board){
    Tile white_queen, black_queen;
    white_queen.path_to_img = realpath("../GUI/imgs/white_queen.png", NULL);
    black_queen.path_to_img = realpath("../GUI/imgs/black_queen.png", NULL);
    white_queen.row = 0;
    white_queen.col = 3;
    black_queen.row = 7;
    black_queen.col = 3;
    black_queen.piece_type = 'Q';
    white_queen.piece_type = 'Q';
    board->pieces[piece_counter] = white_queen;
    board->pieces[piece_counter + 1] = black_queen;
    piece_counter += 2;
}

void initialize_kings(Board * board){
    Tile white_king, black_king;
    white_king.path_to_img = realpath("../GUI/imgs/white_king.png", NULL);
    black_king.path_to_img = realpath("../GUI/imgs/black_king.png", NULL);
    white_king.row = 0;
    white_king.col = 4;
    black_king.row = 7;
    black_king.col = 4;
    white_king.piece_type = 'K';
    black_king.piece_type = 'K';
    board->pieces[piece_counter] = white_king;
    board->pieces[piece_counter + 1] = black_king;
    piece_counter += 2;
}

void initialize_minor_piece(Board * board, const char * img_path_white, const char * img_path_black, int * indices, char piece_type){
    int i;
    int j = 0;
    for (i = 0; i < 4; i++){
        Tile piece;
        if (i < 2)
            piece.path_to_img = realpath(img_path_white, NULL);
        else
            piece.path_to_img = realpath(img_path_black, NULL);

        piece.row = indices[j];
        piece.col = indices[j + 1];
        piece.piece_type = piece_type;
        board->pieces[piece_counter] = piece;
        piece_counter += 1;
        j += 2;
    }
}

void delete_board(Board * board){
    free(board);
}

void print_board(Board * board){
    int i;
    for (i = 0; i < 32; i++){
    Tile piece = (board->pieces)[i];
    printf("piece %d\n:  i = %d\nj_=%d\n", i + 1, piece.row, piece.col);
    }
}