#include <stdio.h>
#include <unistd.h>

int main() {
    printf("HPID = %d, Parent PID = %d\n", getpid(), getppid());
    return 0;
}