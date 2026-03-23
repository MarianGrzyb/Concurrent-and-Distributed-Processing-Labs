#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(1);
    } else if (pid == 0) {
        printf("Child PID %d exiting...\n", getpid());
        exit(0);
    } else {
        printf("Parent PID %d sleeping. Child PID %d should become zombie.\n", getpid(), pid);
        sleep(10);
        printf("Parent now calling wait() to clean up child.\n");
        wait(NULL);
        printf("Parent finished.\n");
    }

    return 0;
}