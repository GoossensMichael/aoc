#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

long fuel(long weight, bool accumulate) {
    long newFuel = weight / 3 - 2;

    if (newFuel >= 0) {
        if (accumulate) {
            return newFuel + fuel(newFuel, accumulate);
        } else {
            return newFuel;
        }
    } else {
        return 0;
    }
}

long solve(FILE* file, bool accumulate) {
    char line[256];

    long total = 0;
    while (fgets(line, sizeof(line), file)) {
        char* ptr;
        long weight = strtol(line, &ptr, 10);

        long fuelx = fuel(weight, accumulate);
        total += fuelx;
    }

    fclose(file);

    return total;
}

FILE* open(char const* const fileName) {
    return fopen(fileName, "r");
}


int main(int argc, char* argv[])
{
    char const* const fileNameTst = "input/day1_tst_input.txt";
    char const* const fileName = "input/day1_input.txt";

    {
        FILE* fileTst = open(fileNameTst);
        printf("Total test input p1: %ld\n", solve(fileTst, false));
        fclose(fileTst);

        FILE* file = open(fileName);
        printf("Total puzzle input p1: %ld\n", solve(file, false));
        fclose(file);
    }

    {
        FILE* fileTst = open(fileNameTst);
        printf("Total test input p2: %ld\n", solve(fopen(fileNameTst, "r"), true));
        fclose(fileTst);

        FILE* file = open(fileName);
        printf("Total puzzle input p2: %ld\n", solve(fopen(fileName, "r"), true));
        fclose(file);
    }

    return 0;
}
