Vol
===

Script de Python que se utilizan con los archivos en VolWin y VolLinux para procesar los volumenes de los radares de INTA

Instalación
-----------

1) Para su funcionamiento es necesario instalar los siguientes programas:

- Python 2.7 (https://www.python.org/download/releases/2.7/)

- PyQt para Python 2.7

- Numpy para Python 2.7

- Lxml para Python 2.7

- Gdal para Python 2.7

- Pyodbc para Python 2.7


Todos estos complementos se pueden descargar desde: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

2) Copiar la carpeta puntos en el lugar donde se quieren procesar los datos.

3) Copiar y descomprimir template-grilla-TM-LIMPIA.zip

4) Copiar los script de Python y los procesos por lotes (Windows o Linux de acuerdo a la plataforma a utilizar)

Detalles instalación Windows: https://github.com/INTA-Radar/VolWin/blob/master/README.md

Uso
---
* Para descargar los archivos: ftpRadar.py
* Para convertir a formato ASCII y GeoTIFF:
   - Linux: utilizar los procesos por lotes que se encuentran en: https://github.com/INTA-Radar/VolLinux
   - Windows: utilizar los procesos por lotes que se encuentran en: https://github.com/INTA-Radar/VolWin
* Para obtener datos de las imágenes: ver https://github.com/INTA-Radar/ImgCompuestas/blob/master/README.md 

Autores
-------

* Yanina Bellini (yabellini@gmail.com)
* Santiago Banchero

Licencia
--------

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or  (at your option) any later version.
 
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
