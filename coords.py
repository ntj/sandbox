import drawSvg as draw
import numpy as np
import random
from pprint import pprint

d = draw.Drawing(500, 500, origin='center', displayInline=False)


def drawCoords(drawing=None):
    if not drawing:
        drawing = d
    arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=4, orient='auto')
    arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5,
                            0.9, 0, fill='black', close=True))

    pathx = draw.Line(-100, 0, 100, 0, stroke='black', stroke_width=1, fill='none',
                      marker_end=None)
    pathy = draw.Line(0, -100, 0, 100, stroke='black', stroke_width=1, fill='none',
                      marker_end=None)

    for i in range(-100, 101, 10):
        linev = draw.Line(i, -100, i, 100, stroke='grey',
                          stroke_width=0.3, fill='none')
        lineh = draw.Line(-100, i, 100, i, stroke='grey',
                          stroke_width=0.3, fill='none')
        drawing.append(linev)
        drawing.append(lineh)

    drawing.append(pathx)
    drawing.append(pathy)
