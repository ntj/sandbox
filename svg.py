import drawSvg as draw
import numpy as np
import random
from pprint import pprint
from coords import drawCoords

polygon = draw.Drawing(250, 250, origin='center', displayInline=False)
star1 = draw.Drawing(250, 250, origin='center', displayInline=False)
star2 = draw.Drawing(250, 250, origin='center', displayInline=False)

colors = ["yellow", "orange", "red", "purple",
          "blue", "green", "brown", "black", "pink"]


def getRandomColor():
    index = random.randint(0, len(colors)-1)
    return colors[index]


def zeichneDreieck(pts, color=None, xShift=0, yShift=0, drawing=None):
    if not color:
        color = getRandomColor()
    if not drawing:
        drawing = star2

    path = draw.Path(stroke_width=0.5, stroke='green',
                     fill=color, fill_opacity=0.6)

    path.M(pts[0][0] + xShift, pts[0][1] - yShift)

    length = len(pts)
    for i in range(1, length):
        path.l(pts[i][0] - pts[i-1][0], pts[i][1] - pts[i-1][1])
    path.Z()
    drawing.append(path)


def drawTriangles(triangles, drawing=None):
    for i, t in enumerate(triangles):
        index = random.randint(0, 6)
        zeichneDreieck(t, colors[(i + index) % 9], drawing=drawing)


def switchCoords(arr):
    result = np.array([[a[1], a[0]] for a in arr])
    return result


def generateClones(pts):
    pts1 = pts.dot([[1, 0], [0, -1]])
    pts2 = pts.dot([[-1, 0], [0, 1]])
    pts4 = switchCoords(pts)
    pts5 = pts4.dot([[1, 0], [0, -1]])
    pts6 = pts2.dot([[1, 0], [0, -1]])
    pts7 = pts4.dot([[-1, 0], [0, 1]]) - [0, 100]
    pts8 = pts4.dot([[-1, 0], [0, 1]])
    pts9 = pts4.dot([[1, 0], [0, -1]])
    pts10 = (pts - [50, 0]).dot([[-1, 0], [0, 1]]) + [50, 0]
    pts11 = (pts2 + [50, 0]).dot([[-1, 0], [0, 1]]) - [50, 0]
    pts3 = pts10.dot([[1, 0], [0, -1]])
    pts12 = (pts5 + [0, 50]).dot([[1, 0], [0, -1]]) - [0, 50]
    pts13 = (pts4 + [0, -50]).dot([[1, 0], [0, -1]]) + [0, 50]
    pts14 = (pts7 + [0, 50]).dot([[1, 0], [0, -1]]) - [0, 50]
    pts15 = (pts6 + [50, 0]).dot([[-1, 0], [0, 1]]) - [50, 0]
    pts16 = (pts8 + [0, -50]).dot([[1, 0], [0, -1]]) + [0, 50]

    triangles = [pts, pts1, pts2, pts3, pts4, pts5, pts6, pts7,
                 pts8, pts10, pts11, pts12, pts13, pts14, pts15, pts16]
    return triangles


def uniquePoints(triangles):
    points = {}
    for t in triangles:
        for point in t:
            x = point[0]
            y = point[1]
            if x in points.keys():
                if y in points[x].keys():
                    points[x][y].append(t)
                else:
                    points[x][y] = [t]
            else:
                points[x] = {y: [t]}

    return points


def drawUnicornEdges(unicorns, random=False, drawing=None):
    if not drawing:
        drawing = star2
    color = None
    opacity = 1
    for u in unicorns:
        triangle = u["t"][0]
        for i, t in enumerate(triangle):
            if t[0] == u["x"] and t[1] == u["y"]:
                if random:
                    color = getRandomColor()
                    opacity = 1
                else:
                    color = "white"
                    opacity = 0
                after = (i+1) % len(triangle)
                lines = draw.Lines(triangle[i-1][0], triangle[i-1][1], t[0], t[1], triangle[after][0], triangle[after][1],
                                   close=False,
                                   fill=color,
                                   fill_opacity=opacity,
                                   stroke='black')
                drawing.append(lines)


def drawUnicornCircles(unicorns, drawing=None):
    if not drawing:
        drawing = star2
    for u in unicorns:
        drawing.append(draw.Circle(u["x"], u["y"], 2,
                                   fill='red', stroke_width=0.3, stroke='black'))


def absPoints(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


if __name__ == "__main__":
    # first polygon
    a = [0, 0]
    b = [50, 0]
    ab = [(b[0] - a[0])/2, (b[1] - a[1])/2]
    c = [50, 50]
    bc = [(c[0] - b[0])/2, (c[1] - b[1])/2]
    ac = [(c[0] - a[0])/2, (c[1] - a[1])/2]
    number = 25
    points = []
    print(ab, bc, ac)

    for i in range(number):
        x = random.randint(0, 50)
        y = random.randint(0, 50)
        points.append([x, y])

    pts = np.array(points)
    pts = np.sort(pts, axis=0)
    final = [a]

    ablist = []
    bclist = []
    aclist = []

    for p in pts:
        absab = absPoints([p[0], p[1]], ab)
        absbc = absPoints([p[0], p[1]], bc)
        absac = absPoints([p[0], p[1]], ac)
        print(p, ":", absab, absbc, absac)
        if min(absab, absbc, absac) == absab:
            print("add")
            ablist.append(p)
        if min(absab, absbc, absac) == absbc:
            print("add")
            bclist.append(p)
        if min(absab, absbc, absac) == absac:
            print("add")
            aclist.append(p)

    print(len(ablist), len(bclist), len(aclist))

    for l in ablist:
        final.append(l)

    final.append(list(b))

    for l in bclist:
        final.append(l)

    final.append(list(c))

    for l in aclist:
        final.append(l)

    final = np.array(final)
    print(final)

    zeichneDreieck(final, drawing=polygon)

    # generate the other triangles
    triangles = generateClones(final)

    # draw triangles
    drawTriangles(triangles, drawing=star1)

    # build point-based data structure
    points = uniquePoints(triangles)

    # find point which don't overlap / are unique in the structure
    unicorns = []
    for x in points.keys():
        dic = points[x]
        for y in dic.keys():
            if len(points[x][y]) == 1:
                unicorns.append(
                    {
                        "x": x,
                        "y": y,
                        "t": points[x][y],
                    }
                )

    # draw those points to check
    # drawUnicornCircles(unicorns)

    # draw adjacent edges
    drawUnicornEdges(unicorns, random=True)
    drawCoords(drawing=polygon)
    drawCoords(drawing=star1)
    drawCoords(drawing=star2)

    polygon.saveSvg('polygon.svg')
    star1.saveSvg('star1.svg')
    star2.saveSvg('star2.svg')
