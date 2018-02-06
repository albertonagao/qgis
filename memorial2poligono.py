# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MemorialDescrPoligono
                                 A QGIS plugin
 Memorial Descritivo para Polígono
                              -------------------
        begin                : 2018-01-16
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Alberto Tuioshi Nagao
        email                : alberto.nagao@
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
from qgis._core import *
import resources
# Import the code for the dialog
from memorial2poligono_dialog import MemorialDescrPoligonoDialog
import os.path

class MemorialDescrPoligono:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MemorialDescrPoligono_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MemorialDescrPoligono')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MemorialDescrPoligono')
        self.toolbar.setObjectName(u'MemorialDescrPoligono')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MemorialDescrPoligono', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = MemorialDescrPoligonoDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/MemorialDescrPoligono/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Poligono do Memorial Descritivo'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)

    def select_output_file(self):
        filename = QFileDialog.getOpenFileName (self.dlg, 'Open file', 'c:\\planurb', '*.txt')
        self.dlg.lineEdit.setText(filename)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MemorialDescrPoligono'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def principal(self):
        arquivo = self.dlg.lineEdit.text()
        output_file = open(arquivo, 'r')
        points = []
        for linha in output_file:
            if (linha.find('Inicia-se') != -1):
                linb = linha[linha.find('Inicia-se'):linha.find('Todas as') - 1]
                while (linb.find('rtice P') != -1):
                    linA = linb
                    Vert = linA[linA.find('rtice P') + 6:linA.find(',', linA.find('rtice P') + 6)]
                    y = linA[linA.find(', de coordenadas N') + 19:linA.find(' m e E', linA.find(
                        ', de coordenadas N') + 19)]
                    x = linA[linA.find('m e E') + 6:linA.find(' m', linA.find('m e E') + 6)]
                    linb = linA[linA.find('m e E') + 18:]
                    if len(points) == 0:
                        x1,y1 = x,y
                    points.append(QgsPoint(float(x),float(y)))
                points.append(QgsPoint(float(x1), float(y1)))

        layer = QgsVectorLayer('Polygon?crs=epsg:31981', os.path.basename(os.path.dirname(arquivo)), 'memory')
        prov = layer.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygon([points]))
        prov.addFeatures([feat])
        layer.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayers([layer])

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            self.principal()
