#include <stdio.h>
#include <stdlib.h>
#include "main.h"

int main(int argc, char *argv[])
{
    if(argc <= 2)   printf("\nThis program calculates value of a cylinder that for given height and radius\nPlease type a height value first, and type a radius value second as arguments to program\n\n");
    else
    {
        printf("\nCalculating the cylinder value\n\n");
        printf("  ");
        double cylinder_value=0;

        double height_value = atof(argv[1]);
        double radius_value = atof(argv[2]);

        printf("\nHeight:  %.3f\n", height_value);
        printf("Radius:  %.3f\n", radius_value);

        cylinder_value = cylinderValue(height_value, radius_value);

        printf("The value of cylinder is: %.3f\n", cylinder_value);
        printf("Job is done...\n");
    }

    return 0;
}