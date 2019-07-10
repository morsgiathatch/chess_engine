#include <gtk/gtk.h>
#include "board.h"
#include <stdbool.h>

// Macros for converting coordinates based on black or white based game
#define white_row_to_img_coords(i) (478 - (60 * (i)))
#define white_col_to_img_coords(i) (59 + (60 * (i)))
#define black_row_to_img_coords(i) (58 + (60 * (i)))
#define black_col_to_img_coords(i) (479 - (60 * (i)))

static bool player_is_white = false;

typedef struct WindowBoard{
    Board * board;
    GtkWidget * window;
} WindowBoard;


void piece_clicked(GtkWidget *board_background, gpointer data){


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
    }

}

void start_game(GtkWidget *button, gpointer data){
    WindowBoard * window_board = (WindowBoard *)data;
    GtkWidget * window = window_board->window;
    GtkWidget * board_background = gtk_fixed_new();
    GtkWidget * image;
    if (player_is_white)
        image = gtk_image_new_from_file (realpath("./imgs/white_board.png", NULL));
    else
        image = gtk_image_new_from_file (realpath("./imgs/black_board.png", NULL));

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

    // Add handler for click
    // Probably won't work. need to wrap board_background in eventbox
     g_signal_connect (board_background, "clicked", G_CALLBACK(piece_clicked), NULL);

}


void start_as_white(GtkWidget *white_button, gpointer data){
    player_is_white = true;
    start_game(white_button, data);
}

void start_as_black(GtkWidget *black_button, gpointer data){
    player_is_white = false;
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
    gtk_container_set_border_width(GTK_CONTAINER (window), 20);

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