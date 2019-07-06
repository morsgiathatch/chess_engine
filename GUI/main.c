#include <gtk/gtk.h>
#include "board.h"


static int counter = 0;

static gboolean expose(GtkWidget *widget, GdkEventExpose *event, gpointer userdata){

}

void destroy(GtkWidget *widget, gpointer data){
   gtk_main_quit ();
}

int main(int argc,char *argv[]){

    GtkWidget *window;
    gtk_init (&argc, &argv);

    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    gtk_widget_set_app_paintable(window, TRUE);

    g_signal_connect (window, "destroy", G_CALLBACK (destroy), NULL);
    /* Let's set the border width of the window to 20.
    * You may play with the value and see the
    * difference. */
    gtk_container_set_border_width(GTK_CONTAINER (window), 600);
    gtk_container_set_border_height(GTK_CONTAINER (window), 600);
    g_signal_connect(G_OBJECT(window), "expose-event", G_CALLBACK(expose), NULL);

    gtk_widget_show_all(window);

    gtk_main ();

    return 0;
}