#Script para Gnuplot para construir las gráficas
#Por: Alejandro Gómez

#set title 'N_{partitions} = 49 +/- 2'
set xlabel 'Maximum distance [MPc]'
set ylabel 'Time [s]'
#Establece cuadricula de la grafica
set grid
#Establece dominio y rango
set xrange [0:180]
#set yrange [0:1]
set logscale y 10
#Ubica el nombre de las series de datos abajo a la derecha
set key bottom right
#Definimos función para reaizar ajuste
b = 0.001
f(x) =a*10**(b*x)
#Realizamos ajuste
fit f(x) 'R2PCFiso_512MPc.dat' using 1:3 via a,b
d = 0.001
g(x) = c*10**(d*x)
fit g(x) 'R2PCFiso_1GPc.dat' using 1:3 via c,d
f = 0.001
h(x) = e*10**(f*x)
fit h(x) 'R2PCFiso_2GPc.dat' using 1:3 via e,f
#Determinamos el formato de salida del archivo al ejecutar el script
set term png size 800,480
#Nombramos la imagen que se creara como salida
set output '2PCFiso_noBPC_computationtime.png'
#Gaficamos en la imagen
plot 'R2PCFiso_512MPc.dat' using 1:3:4 title 'Box: 512 MPc' with yerrorbars linestyle 7 pointsize 1 lc rgb '#0060ad', f(x) with lines lc "blue" title sprintf("Fit: log y = log(%.4f) + (%.4f)x",a,b), 'R2PCFiso_1GPc.dat' using 1:3:4 title 'Box: 1 GPc' with yerrorbars linestyle 7 pointsize 1 lc rgb '#daa520', g(x) with lines lc "yellow" title sprintf("Fit: log y = log(%.4f) + (%.4f)x",c,d), 'R2PCFiso_2GPc.dat' using 1:3:4 title 'Box: 2 GPc' with yerrorbars linestyle 7 pointsize 1 lc rgb '#2e8b57', h(x) with lines lc "green" title sprintf("Fit: log y = log(%.4f) + (%.4f)x",e,f)
