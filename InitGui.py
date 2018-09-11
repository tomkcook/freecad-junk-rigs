# -*- coding: utf-8 -*-
# JunkRig gui init module
# (c) 2001 Juergen Riegel
# License LGPL
#import FreeCADGui, FreeCAD
#from FreeCAD import Workbench, Gui

class JunkRigWorkbench ( Workbench ):
    "JunkRig workbench object"
    Icon = FreeCAD.getHomePath() + "Mod/JunkRig/Resources/icons/JunkRigWorkbench.svg"
    MenuText = "Junk Rig"
    ToolTip = "Junk rig design workbench"
    
    def Initialize(self):
        # load the module
        import JunkRigGui
        self.appendToolbar('JunkRig',['JunkRig_Sail'])
        self.appendMenu('JunkRig',['JunkRig_Sail'])
    
    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(JunkRigWorkbench())
print("Init JunkRig")
