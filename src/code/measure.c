#include "measure.h"

double calculateCylinderValue(double height, double radius)
{
    double cylinderValue = 0;

    cylinderValue = (PI_VAL*radius*radius)*height;

    return cylinderValue;
}