# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MemorialDescrPoligono
                                 A QGIS plugin
 Memorial Descritivo para Polígono
                             -------------------
        begin                : 2018-01-16
        copyright            : (C) 2018 by Alberto Tuioshi Nagao
        email                : alberto.nagao@
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MemorialDescrPoligono class from file MemorialDescrPoligono.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .memorial2poligono import MemorialDescrPoligono
    return MemorialDescrPoligono(iface)
