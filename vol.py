#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Completa-Blancos.py
#       
#       Autores: Santiago Banchero, Yanina Bellini Saibene
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       Este script es parte de la Tesis: 
#         “Estimación de ocurrencia de granizo en superficie mediante datos  
#          de radar meteorológico utilizando técnicas de data mining”.
#		correspondiente a la maestría en DM&KD de la Universidad Austral
#		Aspirante: Yanina Noemí Bellini Saibene
#

import struct
import sys
from math import log10
try:
	from PyQt4 import QtCore
except ImportError:
	raise ImportError,"Se requiere el modulo PyQt4.  Se puede descargar de http://www.riverbankcomputing.co.uk/software/pyqt/download"
try:
	from lxml import etree
except ImportError:
	raise ImportError,"Se requiere el modulo lxml. Se puede descargar de http://www.lfd.uci.edu/~gohlke/pythonlibs/"	
try:
	from numpy import array,nan,isfinite,zeros,float,sin,cos,pi,mgrid
except ImportError:
	raise ImportError,"Se requiere el modulo numpy. Se puede descargar de http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy"	

# Todo: Estos valores son los correspondientes a Anguil, en los .vol esta información está en radarinfo.  
# se podría ver de tomar los datos directamente desde alli y asi hacerlo genérico para cualquier radar
# Todo: These values are from Anguil radar. Inside .vol we can find this information, we will take this data from there.
lon = -63.990067
lat= -36.539683

#Todo: estos datos corresponden para el rango de 240 km, deberiamos generalizarlo para el de 120 y 480.
# These data correspond to the range of 240 km, we should generalize to the 120 and 480.
azimth = 360
bins = 480
rango=240
binres=0.5

R=12742/2; # Radio medio de la Tierra
m=2*pi*R/360
tipoArchivo=''

#Función que devuelve el encabezado del volumen
def get_header_vol(fh=None):
    try:
		linea = fh.next()
		xml = ''
		while linea:
			if linea.startswith('</volume>'):
				xml += linea
				break
			xml += linea
			linea = fh.next()
		return xml
    except StopIteration:
		raise StopIteration,"El archivo que se intenta abrir no contiene datos"	   
    

#Función que devuelve los Blobs con los datos del volumen
def get_blobs(fh=None):
    linea = fh.next()
    blobs = []
    bindata = ''
    while linea:
        #Si la linea empieza con <blob
        if linea.startswith('<BLOB blobi'):
            linea = fh.next()
            while linea:
                if linea.startswith('</BLOB>'):
                    blobs.append(bindata)
                    bindata = ''
                    break
                bindata += linea
                try:
				    linea = fh.next()
                except StopIteration,e:
				    linea = None
        try:
            linea = fh.next()
        except StopIteration,e:
            linea = None
            
    return blobs

#Función que imprime los datos de RADAR, extraido de la informacion contenida en el volumen.
def print_radarinfo(ri):
    name,wavelen,beamwidth = ri.getchildren()
    print """NOMBRE:    %s
WAVELEN:   %s
BEAMWIDTH: %s""" %(name.text,wavelen.text,beamwidth.text)


def print_slice(lst_slice):
    
    for sl in lst_slice:
        slice = sl.getchildren()
        for ele in slice:
            if ele.tag == 'slicedata':
                rayinfo,rawdata = ele.getchildren()
                print """Rays: %s Min: %s Max: %s BlobID: %s Depth: %s Type: %s Bins: %s """ %(rawdata.attrib['rays'],rawdata.attrib['min'],rawdata.attrib['max'],rawdata.attrib['blobid'],rawdata.attrib['depth'],rawdata.attrib['type'],rawdata.attrib['bins'])
    return rawdata.attrib['type']

#Función que realiza el cálculo del valor real de Reflectividad.
def get_depth_as_dbz(depth):
    return round(((float(depth) - 1.0)/(255.0 - 1.0))*(95.5 - (-31.5)) - 31.5,1)

#Función que realiza el cálculo del valor real de ZDR.  Los valores de las variables db_min, db_max, dmi y dma 
#se obtuvieron del manual del Rainbow.
def get_depth_as_zdr(depth):
    db_min = -8.0
    db_max = 12.0
    dmi = 1.0
    dma = 255.0
    return round(((float(depth) - dmi)/(dma - dmi))*(db_max - (db_min)) + db_min,3)

#Función que realiza el cálculo del valor real de PhiDP.  Los valores de las variables db_min, db_max, dmi y dma 
#se obtuvieron del manual del Rainbow. 
def get_depth_as_phidp(depth):
    db_min = 0.0
    db_max = 360.0
    dmi = 1.0   #digital number
    dma = 65535.0 #digital number
    return round(((float(depth) - dmi)/(dma - dmi))*(db_max - (db_min)) + db_min,3)

#Función que realiza el cálculo del valor real de KDP.  Los valores de las variables db_min, db_max, dmi y dma 
#se obtuvieron del manual del Rainbow.
def get_depth_as_kdp(depth):
    db_min = -20.0
    db_max = 20.0
    dmi = 1.0   #digital number
    dma = 65535.0 #digital number
    return round(((float(depth) - dmi)/(dma - dmi))*(db_max - (db_min)) + db_min,3)

#Función que realiza el cálculo del valor real de RhoHV.  Los valores de las variables db_min, db_max, dmi y dma 
#se obtuvieron del manual del Rainbow.
def get_depth_as_rho(depth):
    db_min = 0.0
    db_max = 1.0
    dmi = 1.0   #digital number
    dma = 255.0 #digital number
    return round(((float(depth) - dmi)/(dma - dmi))*(db_max - (db_min)) + db_min,3)

#Función que obtiene la matriz de datos reales del volumen procesado
def get_matriz_vol(d,tipoArchivo):
    inicio = 0
    blob = zeros((azimth,bins),dtype=float)
    for az in range(azimth):
        
        un_bin = d.data()[inicio:inicio + bins]
        #print "Len: ",len(un_bin)
        
        inicio += bins
        #recorro un_bin obviando el primer byte que es el separador
        #for b in range(1,bins):
        for i,b in enumerate(un_bin):
            ndepth = struct.unpack_from('B',b)
            #print az,i,b,ndepth[0],get_depth_as_dbz(ndepth[0])
            if ndepth[0] == 0:
                blob[az][i] = -99.0
                #nros.append(nan)
            elif ndepth[0] > 0:
				if tipoArchivo=='dBZ':
					#print 'Pase por aca:'+tipoArchivo
					blob[az][i] = get_depth_as_dbz(ndepth[0])
				if tipoArchivo=='KDP':
					#print 'Pase por aca:'+tipoArchivo
					blob[az][i] = get_depth_as_kdp(ndepth[0])
				if tipoArchivo=='ZDR':
					#print 'Pase por aca:'+tipoArchivo
					blob[az][i] = get_depth_as_zdr(ndepth[0])
				if tipoArchivo=='RhoHV':
					#print 'Pase por aca:'+tipoArchivo
					blob[az][i] = get_depth_as_rho(ndepth[0])
				if tipoArchivo=='PhiDP':
					#print 'Pase por aca:'+tipoArchivo
					blob[az][i] = get_depth_as_phidp(ndepth[0])
						
               
    return blob #[::-1,:]

def get_angulos(d):
    inicio = 0
    bytes = 2
    
    db_min = 0.0
    db_max = 359.995
    dmi = 0.0
    dma = 65535.0
    
    grados = []
    startangle = None
    for az in range(len(d)):
        un_bin = d.data()[inicio:inicio + bytes][::-1]
        
        inicio += bytes
        if len(un_bin) == 2:
            angulo = struct.unpack_from('H',un_bin)
            if len(grados) == 0:
                startangle = round(((float(angulo[0]) - dmi)/(dma - dmi))*(db_max - (db_min)) + db_min,3)
            grados.append(round(((float(angulo[0]) - dmi)/(dma - dmi))*(db_max - (db_min)) + db_min,3))
            print round(((float(angulo[0]) - dmi)/(dma - dmi))*(db_max - (db_min)) + db_min,3)
    return startangle,grados


  
# Cuerpo principal del Script
if __name__ == '__main__':
    
    #Se recibe como argumento el nombre del archivo .vol a procesar
    f_name = sys.argv[1]
    
    
    f = open(f_name,'rb')
    xml_header = get_header_vol(f)
    blobs = get_blobs(f)

    vol = etree.fromstring(xml_header)
    root = vol.getroottree().getroot()
    
    #Algunos volumenes vienen con mas información, agregan el nodo history, para eso hacemos el control de errores.
    try:
		scan, radarinfo = root.getchildren()
    except ValueError:
		scan, radarinfo, history = root.getchildren()
		
    print_radarinfo(radarinfo)
    slice = scan.findall('slice')
    tipoArchivo= print_slice(slice)
    print 'Tipo Archivo:'+tipoArchivo
    print 'BLOBS: %i' % len(blobs)
    bandas = []
    grados = []
    
    for i,bl in enumerate(blobs):
        #up=QtCore.qUncompress(blobs[1])
        up=QtCore.qUncompress(bl)
        #nros = []
        
        if i % 2 == 0:
            print 'Blob',i,len(up) - bins,azimth*bins,len(up) - bins==azimth*bins
            startangle, grados = get_angulos(up)
               
        
        if i % 2 <> 0:
                print 'Blob',i,len(up) - bins,azimth*bins,len(up) - bins==azimth*bins
                
                blobs_img = get_matriz_vol(up,tipoArchivo)
                
                fo = open(sys.argv[1]+'_%i.txt'%i,'wb')
                fo.write('lon lat dbz\n')
                
                aux_a = blobs_img[:round(360 - startangle)]
                aux_b = blobs_img[round(360 - startangle):]
                blobs_img = array(list(aux_b)+list(aux_a))
                
                points = []
                values = []
                
                for ray in grados:
                    for bi in range(bins):
                        y = lat + ((bi*0.5)/m) * cos((ray)*pi/180)
                        x = lon + ((bi*0.5)/m) * sin((ray)*pi/180)/cos( y * pi/180)
                        
                        
                        points.append([x,y])
                        fo.write("%f %f %f\n" %(x,y,blobs_img[ray][bi]))
                        values.append(blobs_img[ray][bi])
                fo.close()
