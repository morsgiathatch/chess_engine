#include <stdlib.h>
#include <stdio.h>
#include "board.h"


Board * initialize_board(){
    Board * board = (Board *) malloc(sizeof(Board));
    // Initialize to NULL to keep track of blank spaces
    int i, j;
    for (i = 0; i < 8; i++)
        for(j = 0; j < 8; j++)
            board->tiles[i][j] = NULL;

    initialize_pawns(board);
    initialize_rooks(board);
    initialize_knights(board);
    initialize_bishops(board);
    initialize_queens(board);
    initialize_kings(board);

}

void initialize_pawns(Board * board){
    int i;
    for(i = 0; i < 8; i++){
        Tile * w_pawn_tile = (Tile *) malloc(sizeof(Tile));
        Tile * b_pawn_tile = (Tile *) malloc(sizeof(Tile));
        w_pawn_tile->row = 1;
        w_pawn_tile->col = i;
        w_pawn_tile->path_to_img = realpath("./imgs/white_pawn.png", NULL);

        b_pawn_tile->row = 6;
        b_pawn_tile->col = i;
        b_pawn_tile->path_to_img = realpath("./imgs/white_pawn.png", NULL);

        board->tiles[1][i] = w_pawn_tile;
        board->tiles[6][i] = w_pawn_tile;
    }
}

void initialize_rooks(Board * board){
    const char * white_path = "./imgs/white_rook.png";
    const char * black_path = "./imgs/black_rook.png";
    int indices[8] = {0, 0, 0, 7, 7, 0, 7, 7};
    initialize_minor_piece(board, white_path, black_path, indices);
}

void initialize_knights(Board * board){
    const char * white_path = "./imgs/white_knight.png";
    const char * black_path = "./imgs/black_knight.png";
    int indices[8] = {0, 1, 0, 6, 7, 1, 7, 6};
    initialize_minor_piece(board, white_path, black_path, indices);
}

void initialize_bishops(Board * board){
    const char * white_path = "./imgs/white_bishop.png";
    const char * black_path = "./imgs/black_bishop.png";
    int indices[8] = {0, 2, 0, 5, 7, 2, 7, 5};
    initialize_minor_piece(board, white_path, black_path, indices);
}

void initialize_queens(Board * board){
    Tile * white_queen = (Tile *) malloc(sizeof(Tile));
    Tile * black_queen = (Tile *) malloc(sizeof(Tile));
    white_queen->path_to_img = realpath("./imgs/white_queen.png", NULL);
    black_queen->path_to_img = realpath("./imgs/black_queen.png", NULL);
    white_queen->row = 0;
    white_queen->col = 3;
    black_queen->row = 7;
    black_queen->col = 3;
    board->tiles[0][3] = white_queen;
    board->tiles[7][3] = black_queen;

}
void initialize_kings(Board * board){
    Tile * white_king = (Tile *) malloc(sizeof(Tile));
    Tile * black_king = (Tile *) malloc(sizeof(Tile));
    white_king->path_to_img = realpath("./imgs/white_king.png", NULL);
    black_king->path_to_img = realpath("./imgs/black_king.png", NULL);
    white_king->row = 0;
    black_king->col = 4;
    white_king->row = 7;
    black_king->col = 4;
    board->tiles[0][4] = white_king;
    board->tiles[7][4] = black_king;
}

void initialize_minor_piece(Board * board, const char * img_path_white, const char * img_path_black, int * indices){
    int i;
    int j = 0;
    for (i = 0; i < 4; i++){
        Tile * piece = (Tile *) malloc(sizeof(Tile));
        if (i < 2)
            piece->path_to_img = realpath(img_path_white, NULL);
        else
            piece->path_to_img = realpath(img_path_black, NULL);

        piece->row = indices[j];
        piece->col = indices[j + 1];
        board->tiles[indices[j]][indices[j + 1]] = piece;
        j += 2;
    }
}

void delete_board(Board * board){
    int i, j;
    for (i = 0; i < 8; i++)
        for (j = 0; j < 8; j++)
            free(board->tiles[i][j]);

    free(board);
}