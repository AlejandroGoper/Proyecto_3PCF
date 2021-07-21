#include <cmath>

struct Puntos{
    float x;
    float y;
    float z;
};


// distancias euclidea en 2 y 3D
template <typename TDG1>
TDG1 euclidean_dist3D(TDG1 x, TDG1 y, TDG1 z){
    return sqrt(x*x + y*y + z*z);
}
