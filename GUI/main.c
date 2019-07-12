#include <gtk/gtk.h>
#include <gtk/gtkfixed.h>
#include <stdbool.h>
#include <stdio.h>
#include "board.h"

#define BORDER_WIDTH 20.0
#define PIECE_WIDTH 60.0
#define MAX_BUFF 1000
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


static bool player_is_white = false;

typedef struct WindowBoard{
    Board * board;
    GtkWidget * window;
} WindowBoard;

typedef struct FixedBoard{
    Board * board;
    GtkFixed * board_background;
} FixedBoard;

void get_window_coords(int * i, int * j, int row, int col){
    if (player_is_white){
        *i = white_row_to_img_coords(row);
        *j = white_col_to_img_coords(col);
    }
    else{
        *i = black_row_to_img_coords(row);
        *j = black_col_to_img_coords(col);
    }
}

void get_board_coords(int * row, int * col, int x, int y){
    if (player_is_white){
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


GtkWidget * get_widget_at(int row, int col, GtkFixed * board_background){
    GList * children;
    GList * child_;
    children = gtk_container_get_children(GTK_CONTAINER(board_background));

    GtkFixedChild * child;
    GtkWidget * child_widget;

    for (child_ = children; child_ != NULL; child_ = child_->next){
        int x, y;
        child = (GtkFixedChild *)(child_->data);
        child_widget = child->widget;
        GtkAllocation * allocation;
        gtk_widget_get_allocation(child, allocation);
        GdkRectangle * rect;
        rect = (GdkRectangle *)allocation;

        x = rect->x;
        y = rect->y;

        int * _row = (int *)malloc(sizeof(int));
        int * _col = (int *)malloc(sizeof(int));
        get_board_coords(_row, _col, x, y);

        if (*_col == col && *_row == row){
//                printf("found widget at %d,%d\n", *_row, *_col);
            return GTK_WIDGET(child);
        }
    }
//    printf("found %d widgets\n", counter);
    return NULL;
}


void color_possible_moves(FixedBoard * fixed_board, char * buffer){
    Board * board = fixed_board->board;
    GtkFixed * board_background = fixed_board->board_background;

    int i = 0;
    while (1){
        if (buffer[i + 1] == 0)
            break;

        // Get row/col and convert to int
        int row, col;
        row = buffer[i] - '0';
        col = buffer[i + 1] - '0';
        GtkWidget * piece;
        piece = get_widget_at(row, col, board_background);
        int i_, j_;
        get_window_coords(&i_, &j_, row, col);
        GtkWidget * pink_square;
        pink_square = gtk_image_new_from_file (realpath("./imgs/pink_square.png", NULL));
        gtk_fixed_put(board_background, pink_square, j_, i_);

        if (piece != NULL){
            gtk_fixed_move(board_background, piece, j_, i_);
        }
        i += 2;
    }
    gtk_widget_show_all(GTK_WIDGET(board_background));


}


gboolean piece_clicked(GtkWidget *window, GdkEvent * event, gpointer data){
    FixedBoard * fixed_board = (FixedBoard *)data;
    Board * board = fixed_board->board;

    gdouble x;
    gdouble y;
    gdk_event_get_coords(event, &x, &y);
    // find x_, y_ coords in board
    int row, col;
    if (player_is_white){
        row = y_img_coord_to_white_row(y);
        col = x_img_coord_to_white_col(x);
    }
    else{
        row = y_img_coord_to_black_row(y);
        col = x_img_coord_to_black_col(x);
    }

    // Find piece at click
    Tile * piece;
    int i;
    for (i = 0; i < 32; i++){
        if ((board->pieces)[i].row == row && (board->pieces)[i].col == col){
            printf("%d,%d\n", row, col);
            piece = &(board->pieces[i]);
            break;
        }
    }
    // Now need to wait for python part to get possible moves at (row, col) entry
    char buffer[MAX_BUFF];
    for (i = 0; i < MAX_BUFF; i++)
        buffer[i] = 0;
    fgets(buffer, MAX_BUFF, stdin);
    // read each move and update color of board
    color_possible_moves(fixed_board, buffer);
    // return true to stop propagating event signal
    return true;
}

void draw_initial_pieces(GtkFixed * window, Board * board){
    int i;
    for (i = 0; i < 32; i++){
        int i_, j_;
        Tile piece = board->pieces[i];
        if (player_is_white){
            i_ = white_row_to_img_coords(piece.row);
            j_ = white_col_to_img_coords(piece.col);
        }
        else{
            i_ = black_row_to_img_coords(piece.row);
            j_ = black_col_to_img_coords(piece.col);
        }

        GtkWidget * piece_img = gtk_image_new_from_file(realpath(piece.path_to_img, NULL));
        gtk_fixed_put(window, piece_img, j_, i_);
        gtk_widget_show_all(GTK_WIDGET(window));
    }
}

void start_game(GtkWidget *button, gpointer data){
    GtkWidget * board_background;
    board_background = gtk_fixed_new();

    WindowBoard * window_board = (WindowBoard *)data;
    GtkWidget * window = window_board->window;
    GtkWidget * image;

    // Get correct board
    if (player_is_white)
        image = gtk_image_new_from_file (realpath("./imgs/white_board.png", NULL));
    else
        image = gtk_image_new_from_file (realpath("./imgs/black_board.png", NULL));

    // Destroy all existing children, i.e. remake window
    GList * children = gtk_container_get_children(GTK_CONTAINER (window));
    GList * child;

    for (child = children; child != NULL; child = child->next){
        gtk_widget_destroy(GTK_WIDGET(child->data));
    }

    gtk_container_add(GTK_CONTAINER (window), board_background);
    gtk_fixed_put(GTK_FIXED(board_background), image, 0, 0);

    Board * board = window_board->board;
    draw_initial_pieces(GTK_FIXED(board_background), board);
    gtk_widget_show_all(window);

    FixedBoard * fixed_board = (FixedBoard *)malloc(sizeof(FixedBoard));
    fixed_board->board = board;
    fixed_board->board_background = board_background;

    // Add handler for click
     g_signal_connect (window, "button-press-event", G_CALLBACK(piece_clicked), fixed_board);


}

void start_as_white(GtkWidget *white_button, gpointer data){
    player_is_white = true;
    printf("w\n");
    start_game(white_button, data);
}

void start_as_black(GtkWidget *black_button, gpointer data){
    player_is_white = false;
    printf("b\n");
    start_game(black_button, data);
}

void destroy(GtkWidget *widget, gpointer data){
    delete_board((Board *)data);
    gtk_main_quit ();
}

int main(int argc,char *argv[]){
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
    WindowBoard window_board;
    window_board.window = window;
    window_board.board = board;

    g_signal_connect (white_button, "clicked", G_CALLBACK (start_as_white), &window_board);
    g_signal_connect (black_button, "clicked", G_CALLBACK (start_as_black), &window_board);

    gtk_box_pack_start(GTK_BOX(button_panel), white_button, true, true, 20);
    gtk_box_pack_end(GTK_BOX(button_panel), black_button, true, true, 20);
    gtk_container_add(GTK_CONTAINER (window), button_panel);

    gtk_widget_show_all(window);

    gtk_main();

    return 0;
}