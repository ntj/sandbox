import drawSvg as draw
from shapely.affinity import scale
from shapely.ops import transform
from shapely.geometry import Polygon
import numpy as np

d = draw.Drawing(200, 200, origin='center', displayInline=False)


def zeichneDreieck(pts, color, xShift = 0, yShift = 0):
    path = draw.Path(stroke_width=0.5, stroke='green',
              fill=color, fill_opacity=0.6)
    
    path.M(pts[0][0] + xShift, pts[0][1] - yShift)

    length = len(pts)
    for i in range(1,length):
        path.l(pts[i][0] -  pts[i-1][0], pts[i][1] - pts[i-1][1])
    path.Z()
    d.append(path)
    
def switchCoords(arr):
    result = np.array([[a[1],a[0]] for a in arr])
    return result

if __name__ == "__main__":
    
    pts = np.array(
        [[0, 5],
         [5, 0],
         [20, 5],
         [35, 0],
         [50, 0],
         [50, 10],
         [45, 20],
         [50,30],
         [50,33],
         [48,38],
         [50,42],
         [50, 50],
         [45, 45],
         [45, 42],
         [38,38],
         [35,35],
         [30,20],
         [20,20],
         [10,10]])

    pts1 = pts.dot([[1,0],[0,-1]])
    pts2 = pts.dot([[-1,0],[0,1]])
    pts3 = pts1.dot([[-1,0],[0,1]])
    pts4 = switchCoords(pts)
    pts5 = pts4.dot([[1,0],[0,-1]])
    pts6 = pts2.dot([[1,0],[0,-1]])
    pts7 = switchCoords(pts3)
    pts8 = pts4.dot([[-1,0],[0,1]])
    pts9 = pts4.dot([[1,0],[0,-1]])
    pts10 = (pts - [50,0]).dot([[-1,0],[0,1]]) + [50,0]
    pts11 = (pts2 + [50,0]).dot([[-1,0],[0,1]]) - [50,0]
    pts12 = (pts5 + [0,50]).dot([[1,0],[0,-1]]) - [0,50]
    pts11 = (pts2 + [50,0]).dot([[-1,0],[0,1]]) - [50,0]
    pts13 = (pts4 + [0,-50]).dot([[1,0],[0,-1]]) + [0,50]
    pts14 = (pts7 + [0,50]).dot([[1,0],[0,-1]]) - [0,50]
    pts15 = (pts6 + [50,0]).dot([[-1,0],[0,1]]) - [50,0]
    pts16 = (pts8 + [0,-50]).dot([[1,0],[0,-1]]) + [0,50]
    
    zeichneDreieck(pts,"yellow")
    zeichneDreieck(pts1,"orange")
    zeichneDreieck(pts2,"red")
    zeichneDreieck(pts3,"purple", xShift=100)
    zeichneDreieck(pts4,"blue")
    zeichneDreieck(pts5,"green")
    zeichneDreieck(pts6,"orange")
    zeichneDreieck(pts7,"blue")
    zeichneDreieck(pts8,"yellow")
    zeichneDreieck(pts10,"brown")
    zeichneDreieck(pts11,"brown")
    zeichneDreieck(pts12,"brown")
    zeichneDreieck(pts13,"brown")
    zeichneDreieck(pts14,"red")
    zeichneDreieck(pts15,"green")
    zeichneDreieck(pts16,"purple")


    d.saveSvg('example.svg')