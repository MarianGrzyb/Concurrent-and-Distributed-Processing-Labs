#!/bin/bash

process() {
    echo "Hello"
    sleep 4
    echo "Bye!"
}

for i in {1..6}; do
    process &
done

wait