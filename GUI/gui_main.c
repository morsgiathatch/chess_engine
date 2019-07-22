#include <gtk/gtk.h>
#include <gtk/gtkfixed.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "board.h"

#define BORDER_WIDTH 20.0
#define PIECE_WIDTH 60.0
#define MAX_BUFF 1024
// Macros for converting coordinates based on black or white based game to be used in window
#define white_row_to_img_coords(i) (478 - ((int)PIECE_WIDTH * (i)))
#define white_col_to_img_coords(i) (59 + ((int)PIECE_WIDTH * (i)))
#define black_row_to_img_coords(i) (58 + ((int)PIECE_WIDTH * (i)))
#define black_col_to_img_coords(i) (479 - ((int)PIECE_WIDTH * (i)))
#define y_img_coord_to_white_row(i) (int)((478.0 - (double)(i) + BORDER_WIDTH + PIECE_WIDTH) / PIECE_WIDTH)
#define x_img_coord_to_white_col(i) (int)(((double)(i) - 59.0 - BORDER_WIDTH) / PIECE_WIDTH)
#define y_img_coord_to_black_row(i) (int)(((double)(i) - 58.0 - BORDER_WIDTH) / PIECE_WIDTH)
#define x_img_coord_to_black_col(i) (int)((479.0 - (double)(i) + BORDER_WIDTH + PIECE_WIDTH) / PIECE_WIDTH)
// Macros for use within GtkFixed board_background (i.e., ignore border width)
#define y_img_coord_to_white_row_in_board(i) (int)((478.0 - (double)(i) + PIECE_WIDTH) / PIECE_WIDTH)
#define x_img_coord_to_white_col_in_board(i) (int)(((double)(i) - 59.0) / PIECE_WIDTH)
#define y_img_coord_to_black_row_in_board(i) (int)(((double)(i) - 58.0) / PIECE_WIDTH)
#define x_img_coord_to_black_col_in_board(i) (int)((479.0 - (double)(i) + PIECE_WIDTH) / PIECE_WIDTH)
#define pink_square_i(i) ((i) - 2)
#define pink_square_j(j) (j)

static bool PLAYER_IS_WHITE = false;
static bool PIECE_PREVIOUSLY_CLICKED = false;
static int  PIECE_PREVIOUSLY_CLICKED_I = 0;
static int  PIECE_PREVIOUSLY_CLICKED_J = 0;
static GtkWidget * BOARD_IMAGE_PTR = NULL;



typedef struct BoardGUI{
    Board * board;
    GtkWidget * window;
    GtkWidget * board_background;
    GList * pieces;
    GList * pink_squares;
} BoardGUI;

void get_window_coords(int * i, int * j, int row, int col){
    if (PLAYER_IS_WHITE){
        *i = white_row_to_img_coords(row);
        *j = white_col_to_img_coords(col);
    }
    else{
        *i = black_row_to_img_coords(row);
        *j = black_col_to_img_coords(col);
    }
}

void get_board_coords(int * row, int * col, int x, int y){
    if (PLAYER_IS_WHITE){
        *row = y_img_coord_to_white_row_in_board(y);
        *col = x_img_coord_to_white_col_in_board(x);
    }
    else{
        *row = y_img_coord_to_black_row_in_board(y);
        *col = x_img_coord_to_black_col_in_board(x);
    }
}


Tile * get_piece_at(int row, int col, Board * board){
    int i;
    for (i = 0; i < 32; i++){
        Tile * piece;
        piece = &(board->pieces[i]);
        if (piece->row == row && piece->col == col)
            return piece;
    }
    return NULL;
}

void add_widget_at(int row, int col, GtkWidget * widget, BoardGUI * board_gui){
    int x_coord, y_coord;
    get_window_coords(&x_coord, &y_coord, row, col);
    gtk_fixed_put(GTK_FIXED(board_gui->board_background), GTK_WIDGET(widget), x_coord, y_coord);
    board_gui->pieces = g_list_append(board_gui->pieces, widget);
}

void delete_widget_at(int row, int col, BoardGUI * board_gui, bool pink_squares){
    GList * children;
    GList * child_;
    if (pink_squares)
        children = board_gui->pink_squares;
    else
        children = board_gui->pieces;

    GtkWidget * child;

    for (child_ = children; child_ != NULL; child_ = child_->next){
        int x, y;
        child = (GtkWidget *)(child_->data);
        if (GTK_IS_WIDGET(child)){
            GtkAllocation allocation;
            GtkAllocation * alloc_ptr = &allocation;

            gtk_widget_get_allocation(child, alloc_ptr);

            x = ((GdkRectangle *)alloc_ptr)->x;
            y = ((GdkRectangle *)alloc_ptr)->y;

            int row_, col_;
            get_board_coords(&row_, &col_, x, y);
            if (col_ == col && row_ == row){
                if (pink_squares)
                    board_gui->pink_squares = g_list_remove(board_gui->pink_squares, child);
                else
                    board_gui->pieces = g_list_remove(board_gui->pieces, child);
                // remove child from board background
                // TODO FIX BELOW. IT IS THE INCORRECT METHOD TO DELETE WIDGETS
                gtk_container_remove(GTK_CONTAINER(board_gui->board_background), GTK_WIDGET(child));
            }
        }
    }
}

GtkWidget * get_widget_at(int row, int col, BoardGUI * board_gui, bool pink_squares){
    GList * children;
    GList * child_;
    if (pink_squares)
        children = board_gui->pink_squares;
    else
        children = board_gui->pieces;

    GtkWidget * child;
//    fprintf(stderr, "address of board image: %p\n", BOARD_IMAGE_PTR);

    for (child_ = children; child_ != NULL; child_ = child_->next){
        int x, y;
        child = (GtkWidget *)(child_->data);
//        fprintf(stderr, "address of child: %p\n", child);
//        fflush(stderr);
        if (GTK_IS_WIDGET(child) && child != BOARD_IMAGE_PTR){
            GtkAllocation allocation;
            GtkAllocation * alloc_ptr = &allocation;

            gtk_widget_get_allocation(child, alloc_ptr);

            x = ((GdkRectangle *)alloc_ptr)->x;
            y = ((GdkRectangle *)alloc_ptr)->y;

            int row_, col_;
            get_board_coords(&row_, &col_, x, y);
            if (col_ == col && row_ == row){
                return child;
            }
        }
    }
    return NULL;
}

void update_opponent_move(BoardGUI * board_gui, char * buffer, int buffer_len){
    // if buffer len is 4, then a standard move was made, if buffer len is 5, then a pawn promotion occured
    if (buffer_len == 4 || buffer_len == 5){
        int start_row, start_col, end_row, end_col;
        start_row = buffer[0] - '0';
        start_col = buffer[1] - '0';
        end_row = buffer[2] - '0';
        end_col = buffer[3] - '0';

        GtkWidget * piece;
        piece = get_widget_at(start_row, start_col, board_gui, false);
        // delete opponent piece if exists
        delete_widget_at(end_row, end_col, board_gui, false);
        int x_coord, y_coord;
        get_window_coords(&y_coord, &x_coord, end_row, end_col);
        if (buffer_len == 5){
            delete_widget_at(start_row, start_col, board_gui, false);
            char color[10];
            char piece[20];
            if (PLAYER_IS_WHITE)
                strcpy(color, "white");
            else
                strcpy(color, "black");
            if (buffer[4] == 'Q')
                strcpy(piece, "queen");
            else if (buffer[4] == 'R')
                strcpy(piece, "rook");
            else if (buffer[4] == 'N')
                strcpy(piece, "knight");
            else
                strcpy(piece, "bishop");
            char piece_img_path[128];
            snprintf(piece_img_path, sizeof(piece_img_path), "../GUI/imgs/%s_%s.png", color, piece);
            GtkWidget * new_piece;
            new_piece = gtk_image_new_from_file (realpath(piece_img_path, NULL));
            add_widget_at(end_row, end_col, new_piece, board_gui);
        }
        else
            gtk_fixed_move(GTK_FIXED(board_gui->board_background), piece, x_coord, y_coord);

    }
    // if buffer len is 6, then en passant occured
    else if (buffer_len == 6){
        int start_row, start_col, end_row, end_col, opponent_row, opponent_col;
        start_row = buffer[0] - '0';
        start_col = buffer[1] - '0';
        end_row = buffer[2] - '0';
        end_col = buffer[3] - '0';
        opponent_row = buffer[4] - '0';
        opponent_col = buffer[5] - '0';

        GtkWidget * piece;
        piece = get_widget_at(start_row, start_col, board_gui, false);
        // delete opponent piece if exists
        delete_widget_at(opponent_row, opponent_col, board_gui, false);
        int x_coord, y_coord;
        get_window_coords(&y_coord, &x_coord, end_row, end_col);
        gtk_fixed_move(GTK_FIXED(board_gui->board_background), piece, x_coord, y_coord);
    }
    // if buffer len is 8, then castling occured
    else if (buffer_len == 8){
        int i;
        for (i = 0; i < 8; i += 4){
            int start_row, start_col, end_row, end_col;
            start_row = buffer[0 + i] - '0';
            start_col = buffer[1 + i] - '0';
            end_row = buffer[2 + i] - '0';
            end_col = buffer[3 + i] - '0';
            GtkWidget * piece;
            piece = get_widget_at(start_row, start_col, board_gui, false);
            // delete opponent piece if exists
            int x_coord, y_coord;
            get_window_coords(&y_coord, &x_coord, end_row, end_col);
            gtk_fixed_move(GTK_FIXED(board_gui->board_background), piece, x_coord, y_coord);
        }
    }

    // Need to handle piece promotion now

    gtk_widget_show_all(GTK_WIDGET(board_gui->board_background));
}


void color_possible_moves(BoardGUI * board_gui, char * buffer, int buffer_len){
    GtkFixed * board_background = GTK_FIXED(board_gui->board_background);
    int i;
    GtkWidget * child;

    for (i = 0; i < buffer_len; i += 2){
        // Get row/col and convert to int
        int row, col;
        row = buffer[i] - '0';
        col = buffer[i + 1] - '0';
        GtkWidget * piece;
        piece = get_widget_at(row, col, board_gui, false);

        int i_, j_;
        get_window_coords(&i_, &j_, row, col);
        GtkWidget * pink_square;
        pink_square = gtk_image_new_from_file (realpath("../GUI/imgs/pink_square.png", NULL));

        if (piece == NULL){
            board_gui->pink_squares = g_list_append(board_gui->pink_squares, pink_square);
            gtk_fixed_put(board_background, pink_square, pink_square_j(j_), pink_square_i(i_));
        }
        else {
            GtkWidget * overlay;
            overlay = gtk_fixed_new();
            gtk_fixed_put(GTK_FIXED(overlay), GTK_WIDGET(pink_square), 0, 0);

            Tile * tile = get_piece_at(row, col, board_gui->board);
            GtkWidget * piece_img;
            piece_img = gtk_image_new_from_file(realpath(tile->path_to_img, NULL));
            gtk_fixed_put(GTK_FIXED(overlay), piece_img, 0, 2);
            gtk_fixed_put(board_background, GTK_WIDGET(overlay), pink_square_j(j_), pink_square_i(i_));
            board_gui->pink_squares = g_list_append(board_gui->pink_squares, overlay);
        }
    }
    gtk_widget_show_all(GTK_WIDGET(board_background));
}


gboolean piece_clicked(GtkWidget *window, GdkEvent * event, gpointer data){
    BoardGUI * board_gui = (BoardGUI *)data;
    Board * board = board_gui->board;
    bool queue_print = false;

    gdouble x;
    gdouble y;
    gdk_event_get_coords(event, &x, &y);
    // find x_, y_ coords in board
    int row, col;
    if (PLAYER_IS_WHITE){
        row = y_img_coord_to_white_row(y);
        col = x_img_coord_to_white_col(x);
    }
    else{
        row = y_img_coord_to_black_row(y);
        col = x_img_coord_to_black_col(x);
    }

    if (PIECE_PREVIOUSLY_CLICKED){
        GtkWidget * clicked_square;
        bool clicked_flag = false;
        clicked_square = get_widget_at(row, col, board_gui, true);
        // If user clicked on a pink square
        if (clicked_square != NULL){
            clicked_flag = true;
            GtkWidget * originally_clicked_piece, * target_tile;
            originally_clicked_piece = get_widget_at(PIECE_PREVIOUSLY_CLICKED_I, PIECE_PREVIOUSLY_CLICKED_J, board_gui, false);
            target_tile = get_widget_at(row, col, board_gui, false);
            // delete existing piece at target tile, if existent
            if (target_tile != NULL){
                delete_widget_at(row, col, board_gui, false);
                fprintf(stderr, "Deleting piece due to capture\n");
                fflush(stderr);
            }
            else{
                if (originally_clicked_piece == NULL)
                    fprintf(stderr, "Error in finding previously clicked piece!\n");
                fprintf(stderr, "pink square clicked!\n");
                fflush(stderr);
            }
            int x_coord, y_coord;
            get_window_coords(&y_coord, &x_coord, row, col);
            gtk_fixed_move(GTK_FIXED(board_gui->board_background), originally_clicked_piece, x_coord, y_coord);
            queue_print = true;
            // Update board state internals, but I don't think I need these anymore
//            board_gui->board->pieces[PIECE_PREVIOUSLY_CLICKED_I]
            // TODO WILL NEED TO UPDATE THESE INTERNALS FOR TRACKING WHICH PIECE WAS CLICKED.
        }

        // Remove all pink squares
        GList * l;
        GList * children;
        children = gtk_container_get_children(board_gui->board_background);
        fprintf(stderr, "number of children before deletion is %d\n", (int)g_list_length(children));
//        fprintf(stderr, "address of image is %p\n", BOARD_IMAGE_PTR);
        int g_list_len;
        for (l = board_gui->pink_squares; l != NULL; l = l->next){
            if ((g_list_len = g_list_index(children, l->data)) == -1)
                fprintf(stderr, "FAILED TO FIND PINK SQUARE\n");
//            fprintf(stderr, "address of pink_square: %p\n", l->data);
//            fflush(stderr);

            if(GTK_IS_WIDGET(l->data)){
                GList * pink_square;
                pink_square = g_list_find(children, l->data);
                if (pink_square->data != BOARD_IMAGE_PTR){
                    gtk_widget_destroy(pink_square->data);
                    g_list_remove(children, l->data);
                }
            }
        }
        g_list_free(board_gui->pink_squares);
        board_gui->pink_squares = NULL;
        fprintf(stderr, "number of children after deletion is %d\n", (int)g_list_length(children));
        fprintf(stderr, "number of pink squares remaining is %d\n", (int)g_list_length(board_gui->pink_squares));
        fflush(stderr);
        gtk_widget_hide(GTK_WIDGET(board_gui->board_background));
        gtk_widget_show_all(GTK_WIDGET(board_gui->board_background));
        PIECE_PREVIOUSLY_CLICKED = false;
        if (queue_print){
            printf("%d,%d!!\n", row, col);
            fflush(stdout);
        }
        // Now wait for python to make opponent move and then return true, if user clicked valid button
        if (clicked_flag){
            char buffer[MAX_BUFF];
            fgets(buffer, MAX_BUFF, stdin);
            int buffer_len;
            buffer_len = strlen(buffer);
            update_opponent_move(board_gui, buffer, buffer_len);
        }
        return true;

    } else{
        // Find piece at click
        Tile * piece;
        piece = NULL;
        int i;
        for (i = 0; i < 32; i++){
            if ((board->pieces)[i].row == row && (board->pieces)[i].col == col){
                printf("%d,%d\n", row, col);
                fflush(stdout);
                piece = &(board->pieces[i]);
                break;
            }
        }
        if (piece == NULL)
            return true;

        // Now need to wait for python part to get possible moves at (row, col) entry
        char buffer[MAX_BUFF];
        fgets(buffer, MAX_BUFF, stdin);
        int buffer_len;
        buffer_len = strlen(buffer);
        fprintf(stderr, buffer);
        // read each move and update color of board.
        color_possible_moves(board_gui, buffer, buffer_len - 1);
        PIECE_PREVIOUSLY_CLICKED = true;
        PIECE_PREVIOUSLY_CLICKED_I = row;
        PIECE_PREVIOUSLY_CLICKED_J = col;
        // return true to stop propagating event signal
        return true;
    }
}

void draw_initial_pieces(BoardGUI * board_gui){
    int i;
    for (i = 0; i < 32; i++){
        int i_, j_;
        Tile piece = (board_gui->board)->pieces[i];
        get_window_coords(&i_, &j_, piece.row, piece.col);

        GtkWidget * piece_img = gtk_image_new_from_file(realpath(piece.path_to_img, NULL));
        gtk_fixed_put(GTK_FIXED(board_gui->board_background), piece_img, j_, i_);

        // Add image widget to pieces
        board_gui->pieces = g_list_append(board_gui->pieces, piece_img);
        gtk_widget_show_all(GTK_WIDGET(piece_img));
    }

}

void start_game(GtkWidget *button, gpointer data){
    GtkWidget * board_background;
    board_background = gtk_fixed_new();
    BoardGUI * board_gui = (BoardGUI *)data;
    GtkWidget * window = board_gui->window;
    GtkWidget * image;

    // Get correct board
    if (PLAYER_IS_WHITE)
        image = gtk_image_new_from_file (realpath("../GUI/imgs/white_board.png", NULL));
    else
        image = gtk_image_new_from_file (realpath("../GUI/imgs/black_board.png", NULL));

    // Destroy all existing children, i.e. remake window
    GList * children = gtk_container_get_children(GTK_CONTAINER (window));
    GList * child;

    for (child = children; child != NULL; child = child->next){
        gtk_widget_destroy(GTK_WIDGET(child->data));
    }

    gtk_container_add(GTK_CONTAINER (window), board_background);
    gtk_fixed_put(GTK_FIXED(board_background), image, 0, 0);
    board_gui->board_background = board_background;
    BOARD_IMAGE_PTR = image;

    draw_initial_pieces(board_gui);
    gtk_widget_show_all(window);

    // Add handler for click
     g_signal_connect (window, "button-press-event", G_CALLBACK(piece_clicked), board_gui);
}

void start_as_white(GtkWidget *white_button, gpointer data){
    PLAYER_IS_WHITE = true;
    printf("w\n");
    fflush(stdout);
    fprintf(stderr, "w\n");
    start_game(white_button, data);
}

void start_as_black(GtkWidget *black_button, gpointer data){
    PLAYER_IS_WHITE = false;
    printf("b\n");
    fflush(stdout);
    fprintf(stderr, "b\n");
    start_game(black_button, data);
}

void delete_board_gui(BoardGUI * board_gui){
    return;
}

void destroy(GtkWidget *widget, gpointer data){
    delete_board_gui((BoardGUI *)data);
    gtk_main_quit ();
}

int main(int argc,char *argv[]){
    sleep(1);
//    char buffer[MAX_BUFF];
//    fgets(buffer, MAX_BUFF, stdin);
//    fprintf(stderr, buffer);
    GtkWidget *window;
    GtkWidget *button_panel;
    GtkWidget *white_button;
    GtkWidget *black_button;
    gtk_init (&argc, &argv);

    // Initialize Board
    Board * board = initialize_board();

    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    button_panel = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 20);
    gtk_widget_set_app_paintable(window, TRUE);
    gtk_container_set_border_width(GTK_CONTAINER (window), (int)BORDER_WIDTH);

    // Add close handler
    g_signal_connect (window, "destroy", G_CALLBACK (destroy), board);

    // Add button and button handler
    white_button = gtk_button_new_with_label("Play As White");
    black_button = gtk_button_new_with_label("Play as Black");
    // Make dumb struct to pass multiple types
    BoardGUI * board_gui = (BoardGUI *)malloc(sizeof(BoardGUI));
    board_gui->window = window;
    board_gui->board = board;
    board_gui->board_background = NULL;
    // GList must be initialized to null
    board_gui->pieces = NULL;
    board_gui->pink_squares = NULL;

    g_signal_connect (white_button, "clicked", G_CALLBACK (start_as_white), board_gui);
    g_signal_connect (black_button, "clicked", G_CALLBACK (start_as_black), board_gui);
    gtk_box_pack_start(GTK_BOX(button_panel), white_button, true, true, 20);
    gtk_box_pack_end(GTK_BOX(button_panel), black_button, true, true, 20);
    gtk_container_add(GTK_CONTAINER (window), button_panel);

    gtk_widget_show_all(window);

    gtk_main();
    free(board_gui);

    return 0;
}