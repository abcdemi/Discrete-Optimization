import math
import functools
from functools import cmp_to_key   # required for cmp_to_key
def cmp(a, b):
    return (a > b) - (a < b) 
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def subtract(self, p):
    	return Point(self.x - p.x, self.y - p.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
def cross_product(p1, p2):
	return p1.x * p2.y - p2.x * p1.y

def direction(p1, p2, p3):
	return  cross_product(p3.subtract(p1), p2.subtract(p1))

def distance_sq(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
# find the point with minimum y coordinate
# in case of tie choose the point with minimun x-coordinate
def find_min_y(points):
    miny = 999999
    mini = 0
    for i, point in enumerate(points):
        if point.y < miny:
            miny = point.y
            mini = i
        if point.y == miny:
            if point.x < points[mini].x:
                mini = i
    return points[mini], mini

# comparator for the sorting 
def polar_comparator(p1, p2, p0):
    d = direction(p0, p1, p2)
    if d < 0:
        return -1
    if d > 0:
        return 1
    if d == 0:
        if distance_sq(p1, p0) < distance_sq(p2, p0):
            return -1
        else:
            return 1

def graham_scan(points):
    # let p0 be the point with minimum y-coordinate,
    # or the leftmost such point in case of a tie
    p0, index = find_min_y(points)

    # swap p[0] with p[index]
    points[0], points[index] = points[index], points[0]

    # sort the points (except p0) according to the polar angle
    # made by the line segment with x-axis in anti-clockwise direction
    sorted_polar = sorted(points[1:], key = cmp_to_key(lambda p1, p2: polar_comparator(p1,p2,p0)))
    # nums.sort(key=cmp_to_key(lambda x, y: 1 if str(x)+str(y) < str(y)+str(x) else -1))
    # if more than two points are collinear with p0, keep the farthest
    to_remove = []
    for i in range(len(sorted_polar) - 1):
        d = direction(sorted_polar[i], sorted_polar[i + 1], p0)
        if d == 0:
            to_remove.append(i)
    sorted_polar = [i for j, i in enumerate(sorted_polar) if j not in to_remove]

   
    m = len(sorted_polar)
    if m < 2:
        print('Convex hull is empty')

    else:
        stack = []
        stack_size = 0
        stack.append(points[0])
        stack.append(sorted_polar[0])
        stack.append(sorted_polar[1])
        stack_size = 3

        for i in range(2, m):
            while (True):
                d = direction(stack[stack_size - 2], stack[stack_size - 1], sorted_polar[i])
                if d < 0: # if it makes left turn
                    break
                else: # if it makes non left turn
                    stack.pop()
                    stack_size -= 1
            stack.append(sorted_polar[i])
            stack_size += 1
    return stack

points = []
points.append(Point(0, 0))
points.append(Point(7, 0))
points.append(Point(3, 1))
points.append(Point(5, 2))
points.append(Point(3, 3))
points.append(Point(1, 4))
points.append(Point(9, 6))
points.append(Point(5, 5))
a = graham_scan(points)
for p in a:
    print((p.x,p.y))