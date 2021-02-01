import drawSvg as draw
import numpy as np
import random
from pprint import pprint
from coords import drawCoords
import os

colors = ["yellow", "orange", "red", "purple",
          "blue", "green", "brown", "black", "pink"]


def getRandomColor():
    index = random.randint(0, len(colors)-1)
    return colors[index]


def zeichneDreieck(pts, color=None, drawing=None):
    opacity = 0.6
    if not color:
        color = getRandomColor()
        opacity = 0
    if not drawing:
        drawing = star2

    path = draw.Path(stroke_width=1, stroke='grey',
                     fill=color, fill_opacity=opacity)

    path.M(pts[0][0], pts[0][1])

    length = len(pts)
    for i in range(1, length):
        path.l(pts[i][0] - pts[i-1][0], pts[i][1] - pts[i-1][1])
    path.Z()
    drawing.append(path)


def drawTriangles(triangles, drawing=None):
    for i, t in enumerate(triangles):
        index = random.randint(0, 6)
        # zeichneDreieck(t, colors[(i + index) % 9], drawing=drawing)
        zeichneDreieck(t, drawing=drawing)


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
                    opacity = 0.6
                else:
                    color = "white"
                    opacity = 0
                after = (i+1) % len(triangle)
                lines2 = draw.Lines(triangle[i-1][0], triangle[i-1][1], t[0], t[1], triangle[after][0], triangle[after][1],
                                    close=False,
                                    fill=color,
                                    fill_opacity=opacity,
                                    stroke='black',
                                    stroke_width=1)
                lines1 = draw.Lines(triangle[i-1][0], triangle[i-1][1], t[0], t[1], triangle[after][0], triangle[after][1],
                                    close=False,
                                    fill=None,
                                    fill_opacity=0,
                                    stroke='black',
                                    stroke_width=1)
                star2.append(lines2)
                star1.append(lines1)


def drawUnicornCircles(unicorns, drawing=None):
    if not drawing:
        drawing = star2
    for u in unicorns:
        drawing.append(draw.Circle(u["x"], u["y"], 2,
                                   fill='red', stroke_width=0.3, stroke='black'))


def absPoints(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def point(a, b, c, x, y, z):
    return[a[0] * x + b[0] * y + c[0] * z, a[1] * x + b[1] * y + c[1] * z]


def wanted(x, y, threshold):
    if abs(x-y) < threshold:
        return True
    if y < threshold:
        return True
    if abs(x - 50) < threshold:
        return True

    return False


def createPolygon(nrPoints, nrPointsLine, threshold, name):
    # first polygon
    a = [0, 0]
    b = [50, 0]
    ab = [(b[0] - a[0])/2, 0]
    c = [50, 50]
    bc = [50, (c[1] - b[1])/2]
    ac = [25, 25]
    points = []

    for i in range(nrPoints):
        found = False
        while not found:
            x = random.uniform(0, 1)
            y = random.uniform(0, 1 - x)
            z = 1 - x - y
            p = point(a, b, c, x, y, z)
            found = wanted(p[0], p[1], threshold)
        points.append(p)

    final = [a]

    pts = np.array(points)
    pts = np.sort(pts, axis=0)

    ablist = []
    bclist = []
    aclist = []
    for a in range(nrPointsLine):
        ablist.append([float(random.randint(0, 50)), 0.0])
        bclist.append([50.0, float(random.randint(0, 50))])
        num = random.randint(0, 50)
        aclist.append([num, num])

    for p in pts:
        if abs(p[0] - p[1]) < 8:
            aclist.append(p)
            continue
        absab = absPoints([p[0], p[1]], ab)
        absbc = absPoints([p[0], p[1]], bc)
        if min(absab, absbc) == absab:
            ablist.append(p)
        if min(absab, absbc) == absbc:
            bclist.append(p)

    ablist.sort(key=lambda e: e[0])

    for l in ablist:
        final.append(l)

    if random.randint(0, 10) % 2 == 1:
        final.append(b)

    bclist.sort(key=lambda e: e[1])

    for l in bclist:
        final.append(l)

    aclist.sort(key=lambda e: e[0], reverse=True)

    if random.randint(0, 10) % 2 == 1:
        final.append(c)

    for l in aclist:
        final.append(l)

    final = np.array(final)

    zeichneDreieck(final, drawing=polygon)

    # generate the other triangles
    triangles = generateClones(final)

    # draw triangles
    # drawTriangles(triangles, drawing=star1)

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
    # drawCoords(drawing=polygon)
    # drawCoords(drawing=star1)
    # drawCoords(drawing=star2)


if __name__ == "__main__":
    os.system('rm img/*')

    nrGifs = 9

    with open('index.html', 'w') as myFile:
        myFile.write('<html>\n')
        myFile.write('<body>\n')
        myFile.write('<a name="start">\n')
        for i in range(nrGifs):
            myFile.write('<a href="#{0}">'.format(i))
            myFile.write(
                '<img src="img/star{0}.gif" width="250" /></a>'.format(i))
        myFile.write('<br /><br />')
        saveNames = []

        for g in range(nrGifs):
            print("Create stars run {0}".format(g))
            nrStars = 10
            nrPoints = random.randint(1, 20)
            nrPointsLine = random.randint(3, 8)
            threshold = random.randint(3, 20)
            myFile.write('<br />Konfiguration {0}, Parameter: {1}-{2}-{3}&nbsp;<a href="#start">zurück</a><br />'.format(
                g, nrPoints, nrPointsLine, threshold))
            myFile.write('<table>')
            myFile.write('<tr><a name="{0}"></tr>'.format(g))
            myFile.write('<tr><td>')
            for i in range(nrStars):
                polygon = draw.Drawing(
                    250, 250, origin='center', displayInline=False)
                star1 = draw.Drawing(
                    250, 250, origin='center', displayInline=False)
                star2 = draw.Drawing(
                    250, 250, origin='center', displayInline=False)
                name = '-{0}-{1}-{2}-{3}-{4}.svg'.format(g, i,
                                                         nrPoints, nrPointsLine, threshold)
                createPolygon(nrPoints, nrPointsLine,
                              threshold, name)
                arc = draw.ArcLine(0, 97, 8, -50, 234, stroke='black',
                                   stroke_width=1, fill='white', fill_opacity=1)
                circle = draw.Circle(
                    0, 97, 4, stroke='black', stroke_width=1, fill='white', fill_opacity=1)
                star1.append(arc)
                star1.append(circle)
                polygon.saveSvg('img/polygon' + name)
                star1.saveSvg('img/star1' + name)
                star2.saveSvg('img/star2' + name)
                if nrPoints > 3:
                    saveNames.append(name)

                myFile.write('<img src="img/star1-{0}-{1}-{2}-{3}-{4}.svg" width="250"><img src="img/star2-{0}-{1}-{2}-{3}-{4}.svg" width="250">'.format(
                    g, i, nrPoints, nrPointsLine, threshold))
                myFile.write('</td></tr>\n')
            myFile.write('</table><br />\n')

        myFile.write('</body>\n')
        myFile.write('</html>')
    print(len(saveNames))
    for i, name in enumerate(saveNames[:10]):
        os.system(
            'cp img/star2{0} img/star2-{1}.svg'.format(name, i))
        os.system(
            'cp img/polygon{0} img/polygon-{1}.svg'.format(name, i))
        os.system(
            'cp img/polygon{0} img/star1-{1}.svg'.format(name, i))

for g in range(nrGifs):
    os.system(
        'convert -delay 110 -loop 0 -density 200 img/star2-{0}-*.svg img/star{0}.gif'.format(g))
