import FreeCAD, FreeCADGui
import os
from FreeCAD import Vector, ActiveDocument
from FreeCADGui import activeView
from Draft import makeLine, makeWire, makePoint
from math import cos, sin, pi, sqrt
from numpy import roots

ui_path = os.path.join(os.path.dirname(__file__), 'JunkRig.ui')

def sail_params(A, R, alpha, beta, Nf, U):
    """Calculate the sail dimensions from the given parameters.  Inputs:

     - A - the total sail area
     - R - the aspect ratio
     - alpha - the tack angle from horizontal
     - beta - the yard angle from vertical
     - Nf - the number of fan panels
     - U - the length of the luff of each fan panel

     This calculation uses the approximation that the fan panels are
     equilateral triangles.  The actual sail area will therefore be slightly
     above that requested.
     """
    # theta is the angle between battens in each fan panel
    theta = (pi/2 - alpha - beta) / Nf
    # LB is the batten length
    LB = roots([R * cos(alpha)**2 - cos(alpha)*cos(beta) + 0.5 * Nf * sin(theta),
                Nf * U * (1 - cos(alpha)),
                -A])
    # LB = roots([R * cos(alpha)**2 + cos(alpha) * cos(beta) + Nf * sin(theta) / 2,
    #             Nf * U,
    #             -A])
    print(LB)
    LB = max(LB)
    fan_height = LB * cos(beta)
    w = LB * cos(alpha)
    h = w * R
    q = h - fan_height - Nf * U
    actual = q * w
    print('Square area is {:.3f}'.format(actual))
    phi1 = pi / 2 - alpha
    phi2 = alpha + theta + pi/2
    for ii in range(Nf):
#        area = LB * sin(phi1 + phi2) / 2 * ( U * cos(phi2 - phi1) / 2 - LB * cos(phi2 + phi1) / 2)
        area = 0.5 * ( LB*U*sin(phi2) + LB*U*sin(phi1) - LB**2 * sin(phi1 + phi2))
        print('Panel area is {:.3f}, upper angle is {:.3f}'.format(area, phi2 * 180 / pi))
        actual += area
        phi1 -= theta
        phi2 += theta
    return w, q, LB, theta, actual

class SailPanel():
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi(str(ui_path))
    
    def accept(self):
        A = self.form.sa.value()
        R = self.form.aspect.value()
        beta = self.form.yard_angle.value() * pi / 180
        alpha = self.form.boom_angle.value() * pi / 180
        U = self.form.throat_spacing.value() / 1000
        Ns = self.form.square_panels.value()
        Nf = self.form.fan_panels.value()

        w, q, LB, theta, actual = sail_params(A, R, alpha, beta, Nf, U)
        self.form.actual.setText('{:.1f}'.format(actual))
        self.form.LB.setText('{:.1f}'.format(LB))

        part = ActiveDocument.addObject('App::Part', 'Part')
        ActiveDocument.Tip = part
        part.Label = 'Sail'
        activeView().setActiveObject('part', part)

        outline = []
        battens = []

        P = q / Ns
        for ii in range(Ns):
            p = ii * P
            points = [Vector(0, 0, p), Vector(w, 0, p + LB * sin(alpha))]
            if ii == 0:
                outline.extend(points)
            else:
                battens.append(points)
        outline.append(Vector(w, 0, q + LB*sin(alpha)))
        phi = alpha
        h_ii = q
        for ii in range(Nf + 1):
            batten_points = [Vector(0, 0, h_ii), Vector(LB * cos(phi), 0, h_ii + LB * sin(phi))]
            if ii > 0: outline.append(batten_points[1])
            if ii < Nf: battens.append(batten_points)
            h_ii += U
            phi += theta
        
        for ii in range(Nf + 1):
            outline.append(Vector(0, 0, h_ii))
            h_ii -= U
        
        outline.append(Vector(0, 0, 0))
        o_w = makeWire(outline)
        o_w.Label = 'Outline'
        part.addObject(o_w)
        for ii, batten in enumerate(battens):
            b_w = makeWire(batten)
            b_w.Label = "Batten {}".format(ii)
            part.addObject(b_w)
        c = o_w.Shape.CenterOfMass
        c = makePoint(c[0], c[1], c[2], (0, 1, 0))
        c.Label = 'CentreOfEffort'
        part.addObject(c)