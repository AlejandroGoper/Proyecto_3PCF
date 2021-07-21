# Por Alejandro Gómez
# Este script es para realizar una grafica con ajuste logaritmico usando gnuplot

set title '3PCFiso - noBPC - 30 bins - Histogram DDD'
set xlabel 'dmax [MPc]'
set ylabel 'Time [s]'
#Establece cuadricula de la grafica
set grid
#Establece dominio y rango
set xrange [20:190]
#set yrange [0:3.7]
set logscale y 10
#Ubica el nombre de las series de datos abajo a la derecha
set key bottom right
#Definimos función para reaizar ajuste
b = 0.001
f(x) = a*10**(b*x)
#Realizamos ajuste
fit f(x) 'time_results_hDDD_3iso_512MPc.dat' using 2:3 via a,b
#Determinamos el formato de salida del archivo al ejecutar el script
set term png size 800,480
#Nombramos la imagen que se creara como salida
set output '3PCFiso_hDDD_512MPc.png'
#Gaficamos en la imagen
plot 'time_results_hDDD_3iso_512MPc.dat' using 2:3 title 'Box data-512MPc-0' with points linestyle 7 pointsize 1 lc rgb '#0060ad', f(x) with lines lc "red" title sprintf("Fit: log y = log(%.3e) + (%.3e)x ",a,b)
