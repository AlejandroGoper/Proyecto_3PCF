#!/usr/bin/bash/

# ================================================================
#       Script para bajar algun archivo de un servidor a local
#   Flags:
#	-r : ruta al archivo desde mi carpeta en el servidor
#	-f : nombre del archivo a descargar
#   	-s : servidor (cosmo o ares)
#
#
#   Autor: Alejandro Gomez
# ================================================================

echo "============================================================"
echo "  Descargando archivo ... "
echo "============================================================"

# Recibiendo parametros por linea de comando
while getopts r:f:s: flag
do
	case "${flag}" in
		r) root=${OPTARG};;
		f) file=${OPTARG};;
		s) server=${OPTARG};;
	esac
done

# Si el servidor es ares  
if [[ $server == "ares" ]]
then
	# Copio el archivo a mi carpeta en cosmoguest
	# Para ello necesito estar en el servidor de cosmoguest 
	scp gustavo@10.31.17.94:~/Data/3PCFGPU/Alejandro/$root/$file $file
elif [[ $server == "cosmo" ]]
then
	# Copio el archivo a mi carpeta en local
	scp cosmoguest@148.214.16.6:~/agomez/$root/$file $file
else 
	echo "Ha ocurrido un problema inesperado."
fi

echo "============================================================"
echo "                           OK                               "
echo "============================================================"
