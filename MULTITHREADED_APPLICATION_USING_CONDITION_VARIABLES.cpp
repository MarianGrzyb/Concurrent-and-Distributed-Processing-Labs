#include <iostream>
#include <vector>
#include <string>
#include <pthread.h>
#include <unistd.h>
#include <chrono>

#define INITIAL_NUMBER_OF_TICKETS 200
#define MINIMAL_NUMBER_OF_TICKETS 0
#define NUMBER_OF_THREADS 5
#define SLEEP_TIME 1

using namespace std;

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t condition = PTHREAD_COND_INITIALIZER;
int numberOfTickets = INITIAL_NUMBER_OF_TICKETS;
bool resourceReady = true;

struct Input {
    pthread_t thread;
    int id;
    string movieTitle;
};

void* sellMutex(void* arg) {
    Input* data = (Input*)arg;

    // run until the loop breaks
    while (true) {
        // changing global variable, therefore the section needs to be locked
        pthread_mutex_lock(&mutex);

        // if number of tickets is greater than minimal
        if (numberOfTickets > MINIMAL_NUMBER_OF_TICKETS)
        {
            // decrease number of tickets
            numberOfTickets = numberOfTickets - 1;

            cout << "Thread [" << data->id << "] for " << data->movieTitle << ". Tickets left: " << numberOfTickets << endl;
            
            // unlock
            pthread_mutex_unlock(&mutex);
            // simulate using sleep
            sleep(SLEEP_TIME);
        }
        else
        {
            // unlock and break if the number of tickets is minimal
            pthread_mutex_unlock(&mutex);
            break;
        }
    }

    return nullptr;
}

void mutexExecution() {
    vector<Input> workers(NUMBER_OF_THREADS);

    // initialize threads, giving their id and movie title
    for (int i = 0; i < NUMBER_OF_THREADS; i++) {
        workers[i].id = i + 1;
        workers[i].movieTitle = "Movie";

        pthread_create(&workers[i].thread, nullptr, sellMutex, &workers[i]);
    }

    // Join all the threads
    for(int i = 0; i < NUMBER_OF_THREADS; i++)
    {
        pthread_join(workers[i].thread, nullptr);
    }
}

void* sellCondition(void* arg) {
    Input* data = (Input*)arg;

    // run until the loop breaks
    while (true) {
        pthread_mutex_lock(&mutex);
        
        while(!resourceReady && numberOfTickets > 0) {
            pthread_cond_wait(&condition, &mutex);
        }

        resourceReady = false;

        // if number of tickets is greater than minimal
        if (numberOfTickets > MINIMAL_NUMBER_OF_TICKETS)
        {
            // decrease number of tickets
            numberOfTickets = numberOfTickets - 1;

            cout << "Thread [" << data->id << "] for " << data->movieTitle << ". Tickets left: " << numberOfTickets << endl;
            
            resourceReady = true;
            pthread_cond_signal(&condition);

            // unlock
            pthread_mutex_unlock(&mutex);
            // simulate using sleep
            sleep(SLEEP_TIME);
        }
        else
        {
            // unlock and break if the number of tickets is minimal
            pthread_mutex_unlock(&mutex);
            break;
        }
    }

    return nullptr;
}

void conditionExecution() {
    numberOfTickets = INITIAL_NUMBER_OF_TICKETS;
    vector<Input> workers(NUMBER_OF_THREADS);

    // initialize threads, giving their id and movie title
    for (int i = 0; i < NUMBER_OF_THREADS; i++) {
        workers[i].id = i + 1;
        workers[i].movieTitle = "Movie";

        pthread_create(&workers[i].thread, nullptr, sellCondition, &workers[i]);
    }

    // Join all the threads
    for(int i = 0; i < NUMBER_OF_THREADS; i++)
    {
        pthread_join(workers[i].thread, nullptr);
    }
}

int main() {
    // start measuring time for only Mutex
    auto startMutex = chrono::high_resolution_clock::now();

    mutexExecution();    

    // end measuring time for only Mutex
    auto endMutex = chrono::high_resolution_clock::now();

    chrono::duration<double> durationMutex = endMutex - startMutex;

    // print the duration of the operation for only Mutex
    cout << "The whole operation (Mutex) took: " << durationMutex.count() << " seconds\n";

    // start measuring time for condition variables
    auto startCondition = chrono::high_resolution_clock::now();

    conditionExecution();

    // end measuring time for condition variables
    auto endCondition = chrono::high_resolution_clock::now();

    chrono::duration<double> durationCondition = endCondition - startCondition;

    // print the duration of the operation for condition variables
    cout << "The whole operation (Condition Variable) took: " << durationCondition.count() << " seconds\n";

    return 0;
}

