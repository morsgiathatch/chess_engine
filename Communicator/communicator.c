#include <unistd.h>
#include <sys/prctl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>


int main(int argc, char ** argv){
    int fds[2];
    int fds2[2];
    pipe(fds2);
    pipe(fds);
    pid_t pid, pid2, wpid;
    int status = 0;

    if ((pid = fork()) == 0)
    {
        // Start gui
        dup2(fds[0], 0);
        dup2(fds2[1], 1);
        close(fds[1]);
        close(fds2[0]);
        char * argv[] = {"../GUI/gui_main", NULL};
        execv("../GUI/gui_main", argv);
    } else if ((pid2 = fork()) == 0){
        //start python script
        dup2(fds2[0], 0);
        dup2(fds[1], 1);
        close(fds[0]);
        close(fds2[1]);
        execlp("python3", "python3", "../run_engine.py", NULL);
    }

    close(fds[0]);
    close(fds[1]);
    close(fds2[0]);
    close(fds2[1]);
    while ((wpid = wait(&status)) > 0){}
    fprintf(stderr, "Exited with status %d\n", WEXITSTATUS(status));
    fflush(stderr);
}