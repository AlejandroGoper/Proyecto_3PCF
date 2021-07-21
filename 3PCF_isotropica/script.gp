#Script para Gnuplot para construir las gráficas
#Por: Alejandro Gómez

#set title 'N_{partitions} = 19 +/- 2'
set xlabel 'Maximum distance [MPc]'
set ylabel 'Time [s]'
#Establece cuadricula de la grafica
set grid
#Establece dominio y rango
set xrange [0:130]
#set yrange [0:3.7]
set logscale y 10
#Ubica el nombre de las series de datos abajo a la derecha
set key bottom right
#Definimos función para reaizar ajuste
b = 0.001
f(x) = a*10**(b*x)
#Realizamos ajuste
fit f(x) 'R3PCF_512MPc.dat' using 1:3 via a,b
#Determinamos el formato de salida del archivo al ejecutar el script
set term png size 800,480
#Nombramos la imagen que se creara como salida
set output '3PCFiso_noBPC_512MPc_computationtime.png'
#Gaficamos en la imagen
plot '3PCF_512MPc.dat' using 1:3 title 'Box: 512 MPc' with points linestyle 7 pointsize 1 lc rgb '#0060ad', f(x) with lines lc "red" title sprintf("Fit: log y = log(%.4f) + (%.4f)x ",a,b)

