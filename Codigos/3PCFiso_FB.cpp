#include <iostream>
#include <fstream>
#include <ctime>
#include <string.h>
#include "iso3PCF_FB.h"

using namespace std;

//Prototipos de funciones
void abrir_archivo(string,int, Puntos *);
void guardar_Histogramas(string, int, unsigned int ***);
void crear_Histogramas3D(int); // un solo parametro, pues son matrices cuadradas
void eliminar_Histogramas3D(int);
void eliminar_Datos();


//Variables globales
Puntos *DATA, *RAND;
unsigned int ***DDD, ***DDR, ***DRR, ***RRR;

// primer argumento del main es el nombre del archivo datos
// segundo argumento del main es el nombre del archivo rand
// tercer argumento es la cantidad de datos a trabajar
// cuarto argumento es el numero de bins
// quinto argumento es la distancia maxima
int main(int argc, char **argv){
    unsigned to,tf;
    int N = stoi(argv[3]), nb = stoi(argv[4]), d_max = stof(argv[5]); //cantidad de puntos N, numero de bins nb, d_max
    DATA = new Puntos[N];
    RAND = new Puntos[N];
    //Creo los nombres de los archivos
    string nombre1 = "test_DDDiso_", nombre2 = "DDRiso_", nombre3 = "DRRiso_", nombre4 = "RRRiso_";
    nombre1.append(argv[3]);
    nombre2.append(argv[3]);
    nombre3.append(argv[3]);
    nombre4.append(argv[3]);
    nombre1 += ".dat";
    nombre2 += ".dat";
    nombre3 += ".dat";
    nombre4 += ".dat";
    //cargo los datos
    abrir_archivo(argv[1],N,DATA);
    //abrir_archivo(argv[2],N,RAND);
    //Inicializo con 0 los histogramas
    crear_Histogramas3D(nb);
    //programa principal

    iso3PCF obj(DATA,RAND,N,nb,d_max); // instancio la clase
    to = clock();
    obj.calcular_Histogramas_Puros(DDD,RRR);
    //obj.calcular_Histogramas_Mixtos(DDR,DRR);
    tf = clock();
    
    obj.simetrizar_Histograma(DDD);
    obj.~iso3PCF(); // destruyo el objeto 

    cout << "Bin 19,19,19 = " << DDD[19][19][19] << endl; 
    //unsigned int ***nalgon = algo;
    guardar_Histogramas("test.dat",nb,DDD);
    eliminar_Datos(); // destruyo structs
    //guardar_Histogramas(nombre1,nb,DDD);
    //guardar_Histogramas(nombre2,nb,DDR);
    //guardar_Histogramas(nombre3,nb,DRR);
    //guardar_Histogramas(nombre4,nb,RRR);
   // eliminar_Histogramas3D(nb);
   double time = (double(tf-to)/CLOCKS_PER_SEC);
    cout << "Calculo realizado en: " << time << " seg"<< endl;
    return 0;
}

//toma los datos del archivo y los guarda en un arreglo de structuras.
void abrir_archivo(string nombre_archivo,int cantidad_puntos, Puntos *datos){
    ifstream archivo;
    archivo.open(nombre_archivo.c_str(), ios::in | ios::binary); //le indico al programa que se trata de un archivo binario con ios::binary
    if (archivo.fail()){
        cout << "Error al cargar el archivo " << endl;
        exit(1);
    }
    int c=0;
    float eliminar;
    while (!archivo.eof())
    {
        archivo >> datos[c].x >> datos[c].y >> datos[c].z >> eliminar; 
        c++;
    }
    archivo.close();
}

void guardar_Histogramas(string nombre, int dimension, unsigned int ***Matriz){
    int i,j,k,d = 0;
    //puntero a todo el array
    //unsigned int (*puntero_arreglo)[0][dimension][dimension*dimension] = reinterpret_cast<unsigned int(*)[0][dimension][dimension*dimension]>(Matriz);
    //unsigned int (*reshaped)[dimension][dimension*dimension][1] = (unsigned int (*)[dimension][dimension*dimension][1])Matriz;
    
    unsigned int **reshape = new unsigned int*[dimension];
    for ( i = 0; i < dimension; i++)
    {
        *(reshape + i) = new unsigned int[dimension*dimension];
    }
    
    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < 2; j++)
        {
            for (k= 0; k < 2; k++)
            {
               reshape[i][dimension*j + k] = Matriz[i][j][k];
            }
        }
    }

    ofstream archivo;
    archivo.open(nombre.c_str(),ios::out | ios::binary);
    if (archivo.fail()){
        cout << "Error al guardar el archivo " << endl;
        exit(1);
    }
    for (i = 0; i < dimension; i++)
    {
        for ( j = 0; j < dimension*dimension; j++)
        {
            archivo << reshape[i][j] << " "; 
        }
        archivo << endl;
    }
    archivo.close();
}

//Se crean matrices cuadradas y se inicializan con 0.0 
void crear_Histogramas3D(int dimension){
    int i,j,k;
    //reservación dinamica de memoria para un array de dimensiones cubicas
    DDD = new unsigned int**[dimension];
   // DDR = new unsigned int**[dimension];
   // DRR = new unsigned int**[dimension];
   // RRR = new unsigned int**[dimension];
    for (i = 0; i < dimension; i++)
    {
        *(DDD + i) = new unsigned int*[dimension];
     //   *(DDR + i) = new unsigned int*[dimension];
     //   *(DRR + i) = new unsigned int*[dimension];
     //   *(RRR + i) = new unsigned int*[dimension];
        for (j = 0; j < dimension; j++)
        {
            *(*(DDD+i)+j) = new unsigned int[dimension];
       //     *(*(DDR+i)+j) = new unsigned int[dimension];
       //     *(*(DRR+i)+j) = new unsigned int[dimension];
       //     *(*(RRR+i)+j) = new unsigned int[dimension];
        }
    }
    //inicializacion
    for (i = 0; i < dimension; i++)
    {
        for ( j = 0; j < dimension; j++)
        {
            for (k = 0; k < dimension; k++)
            {
                *(*(*(DDD + i) + j) + k)= 0;
             //   *(*(*(DDR + i) + j) + k)= 0;   
             //   *(*(*(DRR + i) + j) + k)= 0;
             //   *(*(*(RRR + i) + j) + k)= 0;
            }
        } 
    }
}

void eliminar_Histogramas3D(int dimension){
    int i,j;
    for (i = 0; i < dimension; i++)
    {
        for (j = 0; j < dimension; j++)
        {
            delete[] *(*(DDD + i) + j);
           // delete[] *(*(DDR + i) + j);
           // delete[] *(*(DRR + i) + j);
           // delete[] *(*(RRR + i) + j);
        }
        delete[] *(DDD + i);
       // delete[] *(DDR + i);
       // delete[] *(DRR + i);
       // delete[] *(RRR + i);
    }
    delete[] DDD;
    //delete[] DDR;
    //delete[] DRR;
    //delete[] RRR;
}

void eliminar_Datos(){
    delete[] DATA;
    delete[] RAND;
}