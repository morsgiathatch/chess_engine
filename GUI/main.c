#include <gtk/gtk.h>
#include "board.h"

void start_as_white(GtkWidget *white_button, gpointer data){
    GtkWidget * window = (GtkWidget *)data;
    GtkWidget * image = gtk_image_new_from_file (realpath("./imgs/white_board.png", NULL));
    GList * children = gtk_container_get_children(GTK_CONTAINER (window));
    GList * child;

    for (child = children; child != NULL; child = child->next){
        gtk_widget_destroy(GTK_WIDGET(child->data));
    }

    gtk_container_add(GTK_CONTAINER (window), image);
    gtk_widget_show_all(window);

}

void destroy(GtkWidget *widget, gpointer data){
   gtk_main_quit ();
}

int main(int argc,char *argv[]){

    GtkWidget *window;
    GtkWidget *white_button;
    gtk_init (&argc, &argv);

    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    gtk_widget_set_app_paintable(window, TRUE);
    gtk_container_set_border_width(GTK_CONTAINER (window), 20);

    // Add close handler
    g_signal_connect (window, "destroy", G_CALLBACK (destroy), NULL);

    // Add button and button handler
    white_button = gtk_button_new_with_label("Play As White");
    g_signal_connect (white_button, "clicked", G_CALLBACK (start_as_white), window);
    gtk_container_add(GTK_CONTAINER (window), white_button);

    gtk_widget_show_all(window);

    gtk_main ();

    return 0;
}