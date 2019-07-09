// Header file for board

#ifndef BOARD_H
#define BOARD_H

typedef struct Tile{
    int row;
    int col;
    char * path_to_img;
}Tile;

typedef struct Board{
    Tile pieces[32];
}Board;

Board * initialize_board();
void initialize_minor_piece(Board *, const char *, const char *, int *);
void initialize_pawns(Board *);
void initialize_rooks(Board *);
void initialize_knights(Board *);
void initialize_bishops(Board *);
void initialize_queens(Board *);
void initialize_kings(Board *);
void delete_board(Board *);
void print_board(Board *);

#endif