# -*- coding: utf-8 -*-
# FreeCAD tools of the JunkRig workbench
# (c) 2001 Juergen Riegel
# License LGPL

import FreeCAD, FreeCADGui, JunkResource

class CmdSail():
    def __init__(self):
        self.sail_panel = None

    def Activated(self):
        import Sail
        self.sail_panel = Sail.SailPanel()
        FreeCADGui.Control.showDialog(self.sail_panel)

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {'Pixmap': ':/icons/Sail.svg', 'MenuText': 'Sail Design', 'ToolTip': 'Sail Design'}

class CmdHelloWorld:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Hello, World!\n")
    def IsActive(self):
        return True
    def GetResources(self):
        return {'Pixmap': 'Sail.svg', 'MenuText': 'Hello World', 'ToolTip': 'Print Hello World'}

FreeCADGui.addCommand('JunkRig_HelloWorld', CmdHelloWorld())
FreeCADGui.addCommand('JunkRig_Sail', CmdSail())
