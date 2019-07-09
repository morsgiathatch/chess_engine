#include <gtk/gtk.h>
#include "board.h"

#define row_to_img_coords(i) (480 - (60 * (i)))
#define col_to_img_coords(i) (58 + (60 * (i)))

typedef struct WindowBoard{
    Board * board;
    GtkWidget * window;
} WindowBoard;


void draw_initial_pieces(GtkFixed * window, Board * board){
//    print_board(board);
    int i;
    for (i = 0; i < 32; i++){
        Tile piece = board->pieces[i];
        int i_ = row_to_img_coords(piece.row);
        int j_ = col_to_img_coords(piece.col);
        GtkWidget * piece_img = gtk_image_new_from_file(realpath(piece.path_to_img, NULL));
        gtk_fixed_put(window, piece_img, j_, i_);
//        gtk_widget_show_all(window);

    }

}

void start_as_white(GtkWidget *white_button, gpointer data){
    WindowBoard * window_board = (WindowBoard *)data;
    GtkWidget * window = window_board->window;
    GtkWidget * board_background = gtk_fixed_new();
    GtkWidget * image = gtk_image_new_from_file (realpath("./imgs/white_board.png", NULL));
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

}

void destroy(GtkWidget *widget, gpointer data){
    delete_board((Board *)data);
    gtk_main_quit ();
}

int main(int argc,char *argv[]){

    GtkWidget *window;
    GtkWidget *white_button;
    gtk_init (&argc, &argv);

    // Initialize Board
    Board * board = initialize_board();


    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    gtk_widget_set_app_paintable(window, TRUE);
    gtk_container_set_border_width(GTK_CONTAINER (window), 20);

    // Add close handler
    g_signal_connect (window, "destroy", G_CALLBACK (destroy), board);

    // Add button and button handler
    white_button = gtk_button_new_with_label("Play As White");
    // Make dumb struct to pass multiple types
    WindowBoard window_board;
    window_board.window = window;
    window_board.board = board;

    g_signal_connect (white_button, "clicked", G_CALLBACK (start_as_white), &window_board);
    gtk_container_add(GTK_CONTAINER (window), white_button);

    gtk_widget_show_all(window);

    gtk_main();

    return 0;
}