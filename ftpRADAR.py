#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
#  
#  Copyright 2012 bellini.yanina <bellini.yanina@AGAGTICS001N>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from ftplib import FTP
import argparse

parser = argparse.ArgumentParser(description="Recupera los archivos de volúmenes desde los radares meterológicos")

parser.add_argument("radar", 
                    default="ANG", choices=["ANG", "PER", "PAR"], help="Indica de que radar se quieren los datos: ANG=Anguil, PER=Pergamino, PAR=Paraná")
parser.add_argument ("fechas", help="Fecha/s a procesar, formato: aaaammdd, mas de una separada por espacios")
parser.add_argument ("rango", default="240", choices=["120", "240", "480"], help="Indica el rango sobre el cual se quieren los datos: 120, 240, 480")
parser.add_argument("-variable", type=char , default="dBZ", choices=["dBZ", "ZDR", "KDP","RhoHV", "PhiDP","uPhiDP"],help="Variable a recuperar. Posibles valores dBZ, ZDR, RhoHV, KDP, PhiDP, uPhiDP. Valor por defecto: dBZ")
args = parser.parse_args()



#fechas= ['20110113','20110114','20110115','20110417','20110428','20110429','20111103','20111106','20111107','20111108','20111120','20111123','20111124','20111129']
#'20090921','20091116','' 05/12/2009 10/01/2010 11/01/2010 09/02/2010 18/11/2010 25/11/2010

extension="vol"

if args.radar == 'ANG':
	ftp = FTP('xx.xx.xx.xx')   # Ver la información de conexión nueva
	ftp.connect('xx.xx.xx.xx','xxxx')
	print ftp.login('usuario', 'contraseña')       
if arg.radar == 'PER':
	ftp = FTP('xx.xx.xx.xx')   # Ver la información de conexión nueva
	ftp.connect('xx.xx.xx.xx','xxx')
	print ftp.login('xxxx', 'xxx')       
if arg.radar == 'PAR':
	ftp = FTP('xx.xx.xx.xx')   # Ver la información de conexión nueva
	ftp.connect('xx.xx.xx.xx','xxx')
	print ftp.login('xxxx', 'xxx')       		

print "Cambiando de directorio .."
ftp.cwd("..")
print "Cambiando de directorio .."
ftp.cwd("..")

if args.rango == '240':
	print "Cambiando de directorio de 240 km"
	ftp.cwd("mnt/backup_anguil/VOL_240_ALL.vol")
if args.rango == '120':
	print "Cambiando de directorio de 120 km"
	ftp.cwd("mnt/backup_anguil/VOL_120_ALL.vol")
if args.rango == '480':
	#Todo: Generar código para 480 km

print "Pidiendo listado de archivos"
archivos = ftp.nlst()
print "Ordenando el listado de archivos"
archivos.sort()
print "Cantidad de archivos en el listado: %d" % len(archivos)		

#Para cada fecha en el listado
for fecha in fechas:
	print "Obteniendo todos los archivos correspondientes a la fecha: " + fecha 
	nombre_archivos = [i for i in archivos if i.startswith(fecha) and i.find(args.variable) >0 and i.endswith(extension)]
	print "Cantidad de archivos en la lista: %d" % len(nombre_archivos)

	print "Iniciando recuperación de archivos"
	for nombre_archivo in nombre_archivos:
		print "Tratando de traer el archivo: " + nombre_archivo
		ftp.retrbinary('RETR ' + nombre_archivo, open(nombre_archivo, 'wb').write)
		
print "Fin de conexión"
ftp.quit()





	
	

	

	



def main():
	
	return 0

if __name__ == '__main__':
	main()

