from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from numpy import *
import sys, os
if sys.platform == 'win32':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
import GL
import plant_propagation as ppa
import Elevator_hill as eh
import Elevator as el
import matplotlib.pyplot as plt

pygame.init()

surface = pygame.display.set_mode((800,640),OPENGL|DOUBLEBUF)
GL.resize(800,640)
GL.init()

view_angle_x = 90.0
view_angle_y = 0.0
view_distance = 1.0

cursor_pos = [0.0, 0.0, 0.0] #x, y, z

mouse_pressing = False

wireList = [[(0, 11, 1), (1, 11, 1), (1, 11, 2), (2, 11, 2), (2, 11, 3), (2, 10, 3), (2, 9, 3), (1, 9, 3), (1, 8, 3), (2, 8, 3), (2, 7, 3), (2, 6, 3), (2, 6, 2), (2, 5, 2), (2, 4, 2), (2, 3, 2), (1, 3, 2), (0, 3, 2), (0, 3, 3), (0, 2, 3)], [(0, 2, 12), (0, 3, 12)], [(0, 1, 6), (0, 1, 5), (0, 1, 4), (1, 1, 4), (1, 1, 3), (1, 1, 2), (0, 1, 2), (0, 1, 1)], [(0, 8, 2), (0, 9, 2), (0, 10, 2)], [(0, 1, 15), (0, 1, 14), (0, 1, 13), (1, 1, 13), (1, 1, 12), (0, 1, 12), (0, 2, 12)], [(0, 3, 12), (0, 3, 13), (0, 4, 13), (0, 5, 13), (0, 6, 13), (0, 7, 13)], [(0, 1, 15), (0, 2, 15), (0, 3, 15), (0, 4, 15), (1, 4, 15), (1, 4, 14), (1, 5, 14), (1, 5, 13), (1, 6, 13), (1, 6, 12), (1, 7, 12), (1, 7, 11), (1, 7, 10), (1, 7, 9), (2, 7, 9), (2, 7, 8), (2, 7, 7), (2, 7, 6), (2, 7, 5), (2, 6, 5), (3, 6, 5), (3, 6, 4), (3, 7, 4), (3, 7, 5), (4, 7, 5), (4, 8, 5), (4, 9, 5), (3, 9, 5), (2, 9, 5), (1, 9, 5), (1, 10, 5), (0, 10, 5), (0, 11, 5), (0, 11, 4), (1, 11, 4), (1, 11, 3), (0, 11, 3), (0, 12, 3), (1, 12, 3), (1, 12, 2), (1, 12, 1), (0, 12, 1), (0, 11, 1)], [(0, 11, 1), (0, 11, 0), (1, 11, 0), (1, 10, 0), (2, 10, 0), (2, 9, 0), (2, 8, 0), (2, 7, 0), (2, 6, 0), (2, 5, 0), (2, 4, 0), (2, 4, 1), (2, 3, 1), (3, 3, 1), (3, 4, 1), (4, 4, 1), (4, 4, 2), (5, 4, 2), (5, 4, 3), (5, 4, 4), (4, 4, 4), (3, 4, 4), (3, 4, 5), (3, 4, 6), (3, 4, 7), (2, 4, 7), (1, 4, 7), (1, 4, 8), (0, 4, 8)], [(0, 10, 9), (0, 10, 10), (0, 9, 10), (1, 9, 10), (1, 9, 11), (0, 9, 11), (0, 9, 12), (0, 9, 13), (1, 9, 13), (1, 8, 13), (1, 7, 13), (0, 7, 13)], [(0, 8, 2), (0, 8, 3), (0, 8, 4), (1, 8, 4), (1, 8, 5), (0, 8, 5), (0, 7, 5), (1, 7, 5), (1, 7, 6), (1, 7, 7), (1, 7, 8), (0, 7, 8), (0, 7, 9), (0, 8, 9)], [(0, 9, 1), (0, 10, 1), (1, 10, 1), (2, 10, 1), (2, 10, 2), (2, 9, 2), (1, 9, 2), (1, 10, 2), (1, 10, 3), (1, 10, 4), (1, 9, 4), (2, 9, 4), (2, 8, 4), (2, 7, 4), (2, 6, 4), (2, 5, 4), (1, 5, 4), (0, 5, 4)], [(0, 8, 2), (0, 7, 2), (0, 7, 3), (0, 6, 3), (1, 6, 3), (1, 5, 3), (2, 5, 3), (2, 4, 3), (2, 4, 4), (2, 4, 5), (2, 4, 6), (1, 4, 6), (0, 4, 6), (0, 4, 7), (0, 4, 8)], [(0, 7, 13), (0, 7, 12), (0, 8, 12), (0, 8, 11)], [(0, 8, 15), (0, 8, 14), (1, 8, 14), (2, 8, 14), (2, 8, 13), (2, 8, 12), (3, 8, 12), (3, 7, 12), (3, 6, 12), (3, 5, 12), (3, 4, 12), (2, 4, 12), (2, 4, 11), (2, 3, 11), (2, 3, 10), (3, 3, 10), (3, 2, 10), (3, 1, 10), (2, 1, 10), (1, 1, 10), (0, 1, 10)], [(0, 10, 9), (1, 10, 9), (1, 10, 10), (1, 10, 11), (2, 10, 11), (2, 9, 11), (2, 8, 11), (2, 7, 11), (3, 7, 11), (3, 6, 11), (3, 5, 11), (3, 5, 10), (2, 5, 10), (1, 5, 10), (0, 5, 10), (0, 5, 11)], [(0, 5, 4), (0, 4, 4), (0, 3, 4), (0, 2, 4), (0, 2, 3)], [(0, 5, 11), (0, 6, 11), (1, 6, 11), (2, 6, 11), (2, 6, 12), (2, 7, 12), (2, 7, 13), (3, 7, 13), (3, 8, 13), (3, 9, 13), (3, 10, 13), (2, 10, 13), (1, 10, 13), (0, 10, 13), (0, 11, 13), (0, 11, 12)], [(0, 1, 15), (0, 0, 15), (0, 0, 14), (1, 0, 14), (1, 0, 13), (2, 0, 13), (3, 0, 13), (3, 0, 12), (3, 0, 11), (2, 0, 11), (2, 0, 10), (2, 0, 9), (1, 0, 9), (1, 1, 9), (2, 1, 9), (2, 1, 8), (3, 1, 8), (3, 1, 7), (3, 2, 7), (3, 3, 7), (2, 3, 7), (1, 3, 7), (1, 3, 6), (1, 3, 5), (1, 3, 4), (1, 3, 3), (2, 3, 3), (3, 3, 3), (3, 4, 3), (3, 5, 3), (3, 6, 3), (3, 7, 3), (4, 7, 3), (4, 8, 3), (4, 8, 2), (4, 8, 1), (3, 8, 1), (2, 8, 1), (1, 8, 1), (0, 8, 1), (0, 8, 2)], [(0, 1, 10), (0, 1, 9), (0, 1, 8), (1, 1, 8), (1, 0, 8), (2, 0, 8), (2, 0, 7), (2, 0, 6), (2, 0, 5), (1, 0, 5), (1, 0, 4), (0, 0, 4), (0, 0, 3), (0, 0, 2), (1, 0, 2), (1, 0, 1), (0, 0, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0), (0, 3, 0), (0, 4, 0), (1, 4, 0), (1, 5, 0), (1, 6, 0), (1, 7, 0), (1, 8, 0), (1, 9, 0), (0, 9, 0), (0, 9, 1)], [(0, 1, 15), (0, 1, 16), (0, 2, 16), (0, 2, 17), (1, 2, 17), (1, 2, 16), (2, 2, 16), (2, 2, 15), (2, 2, 14), (2, 2, 13), (2, 2, 12), (2, 2, 11), (2, 2, 10), (2, 2, 9), (1, 2, 9), (1, 2, 8), (1, 2, 7), (0, 2, 7), (0, 2, 6), (0, 2, 5), (1, 2, 5), (1, 2, 4), (1, 2, 3), (0, 2, 3)], [(0, 9, 1), (1, 9, 1), (2, 9, 1), (3, 9, 1), (3, 9, 2), (3, 8, 2), (3, 8, 3), (3, 8, 4), (3, 8, 5), (2, 8, 5), (2, 8, 6), (2, 8, 7), (2, 8, 8), (1, 8, 8), (1, 8, 9), (1, 8, 10), (1, 8, 11), (1, 8, 12), (1, 9, 12), (2, 9, 12), (2, 9, 13), (2, 9, 14), (1, 9, 14), (0, 9, 14), (0, 9, 15), (0, 8, 15)], [(0, 8, 6), (0, 7, 6), (0, 6, 6), (0, 6, 5), (1, 6, 5), (1, 6, 4), (0, 6, 4), (0, 7, 4), (1, 7, 4), (1, 7, 3), (1, 7, 2), (1, 6, 2), (1, 5, 2), (1, 5, 1), (0, 5, 1)], [(0, 8, 15), (1, 8, 15), (1, 7, 15), (2, 7, 15), (3, 7, 15), (3, 6, 15), (3, 5, 15), (2, 5, 15), (2, 4, 15), (2, 3, 15), (1, 3, 15), (1, 3, 14), (1, 3, 13), (1, 2, 13), (1, 2, 12), (0, 2, 12)], [(0, 1, 15), (1, 1, 15), (1, 1, 14), (2, 1, 14), (2, 1, 13), (2, 1, 12), (2, 0, 12), (1, 0, 12), (1, 0, 11), (0, 0, 11), (0, 0, 10), (0, 0, 9), (0, 0, 8), (0, 0, 7), (1, 0, 7), (1, 1, 7), (2, 1, 7), (2, 1, 6), (2, 1, 5), (2, 1, 4), (2, 1, 3), (2, 1, 2), (2, 1, 1), (1, 1, 1), (0, 1, 1)], [(0, 8, 2), (1, 8, 2), (2, 8, 2), (2, 7, 2), (3, 7, 2), (3, 6, 2), (3, 5, 2), (3, 4, 2), (3, 3, 2), (3, 2, 2), (2, 2, 2), (2, 2, 3), (2, 2, 4), (2, 2, 5), (2, 2, 6), (2, 2, 7), (2, 2, 8), (3, 2, 8), (3, 2, 9), (4, 2, 9), (4, 2, 10), (4, 2, 11), (4, 2, 12), (3, 2, 12), (3, 2, 13), (3, 1, 13), (3, 1, 12), (3, 1, 11), (2, 1, 11), (1, 1, 11), (1, 2, 11), (0, 2, 11), (0, 2, 12)], [(0, 2, 14), (0, 3, 14), (0, 4, 14), (0, 5, 14), (0, 6, 14), (1, 6, 14), (1, 6, 15), (2, 6, 15), (2, 6, 16), (2, 7, 16), (1, 7, 16), (0, 7, 16)], [(0, 3, 12), (0, 4, 12), (1, 4, 12), (1, 5, 12), (2, 5, 12), (2, 5, 11), (1, 5, 11), (1, 4, 11), (1, 4, 10), (1, 4, 9), (1, 5, 9), (1, 5, 8), (1, 5, 7), (1, 5, 6), (1, 5, 5), (1, 4, 5), (1, 4, 4), (1, 4, 3), (1, 4, 2), (0, 4, 2), (0, 4, 1), (0, 5, 1)], [(0, 5, 1), (0, 7, 14), (1, 7, 14), (2, 7, 14), (3, 7, 14), (4, 7, 14), (5, 7, 14), (6, 7, 14), (0, 6, 1), (1, 6, 1), (2, 6, 1), (3, 6, 1), (4, 6, 1), (5, 6, 1), (6, 6, 1), (6, 5, 2), (6, 6, 2), (6, 7, 2), (6, 7, 3), (6, 7, 4), (6, 7, 5), (6, 7, 6), (6, 7, 7), (6, 7, 8), (6, 7, 9), (6, 7, 10), (6, 7, 11), (6, 7, 12), (0, 7, 13)], [(0, 10, 9), (0, 10, 8), (0, 10, 7), (0, 9, 7), (0, 9, 6), (0, 8, 6)], [(0, 5, 4), (0, 5, 5), (0, 4, 5), (0, 3, 5), (0, 3, 6), (0, 3, 7), (0, 3, 8), (0, 3, 9), (0, 3, 10), (1, 3, 10), (1, 3, 11), (1, 3, 12), (0, 3, 12)]]

gatesList = [(0, 1, 1), (0, 1, 6), (0, 1, 10), (0, 1, 15), (0, 2, 3), (0, 2, 12), (0, 2, 14), (0, 3, 12), (0, 4, 8), (0, 5, 1), (0, 5, 4), (0, 5, 11), (0, 5, 16), (0, 7, 13), (0, 7, 16), (0, 8, 2), (0, 8, 6), (0, 8, 9), (0, 8, 11), (0, 8, 15), (0, 9, 1), (0, 10, 2), (0, 10, 9), (0, 11, 1), (0, 11, 12)]



Dimensions = [18,7,13]
size = 0.1




def draw(Dimensions, gatesList):
    # CLEAR ALL----------------------------------------
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # BASIC CAMERA VIEW--------------------------------
    glTranslatef(0.0, 0.0, -51.0 * view_distance)
    glRotatef(view_angle_x, 1.0, 0.0, 0.0)
    glRotatef(view_angle_y, 0.0, 1.0, 0.0)
    # BOARD--------------------------------------------
    drawchip(Dimensions)
    # GATES -------------------------------------------
    for (x,y,z) in gatesList:
        glPushMatrix()
        glTranslatef(x-(Dimensions[0]/2),y, z-(Dimensions[2]/2))
        setcolor("4D00E8")
        glCallList(3)
        glPopMatrix()

    # WIRES--------------------------------------------
    glTranslatef(0.0, -0.01, 0.0)
    glPushMatrix()
    glCallList(2)
    glPopMatrix()
    # CURSOR-------------------------------------------
    glPushMatrix()
    glTranslatef(round(cursor_pos[0] / 2.10176) * 2.10176, cursor_pos[1],
                 round(cursor_pos[2] / 2.10176) * 2.10176)
    glCallList(4)
    glPopMatrix()
    pygame.display.flip()


def setcolor(HEXcode):
    r = float(int(HEXcode[:2], 16)/255)
    g = float(int(HEXcode[2:4], 16)/255)
    b = float(int(HEXcode[4:], 16)/255)
    glColor3f(r,g,b)

# coordinates = [z,y,x]
def drawchip(coordinates):
    (x, y, z) = coordinates
    glBegin(GL_QUADS)
    #TOP
    glVertex3f(-0.5*x, 0.0, -0.5*z)
    glVertex3f(-0.5*x, 0.0, 0.5*z)
    glVertex3f(0.5*x, 0.0, 0.5*z)
    glVertex3f(0.5*x, 0.0, -0.5*z)
    setcolor("E89700")
    #QUADRANT -x
    glVertex3f(-0.5*(x+1), 0.0, 0.5*(z+1))
    glVertex3f(-0.5*(x+1), 0.0, -0.5*(z+1))
    glVertex3f(-0.5*x, 0.0, -0.5*(z+1))
    glVertex3f(-0.5*x, 0.0, 0.5*(z+1))
    #QUADRANT -z
    glVertex3f(0.5*(x+1), 0.0, -0.5*(z+1))
    glVertex3f(-0.5*x, 0.0, -0.5*(z+1))
    glVertex3f(-0.5*x, 0.0, -0.5*z)
    glVertex3f(0.5*(x+1), 0.0, -0.5*z)
    #QUADRANT +z
    glVertex3f(0.5*(x+1), 0.0, 0.5*(z+1))
    glVertex3f(-0.5*x, 0.0, 0.5*(z+1))
    glVertex3f(-0.5*x, 0.0, 0.5*z)
    glVertex3f(0.5*(x+1), 0.0, 0.5*z)
    #QUADRANT +x
    glVertex3f(0.5*(x+1), 0.0, 0.5*z)
    glVertex3f(0.5*(x+1), 0.0, -0.5*z)
    glVertex3f(0.5*x, 0.0, -0.5*z)
    glVertex3f(0.5*x, 0.0, 0.5*z)
    #BOTTOM
    glVertex3f(0.5*(x+1), -1.0, 0.5*(z+1))
    glVertex3f(0.5*(x+1), -1.0, -0.5*(z+1))
    glVertex3f(-0.5*(x+1), -1.0, -0.5*(z+1))
    glVertex3f(-0.5*(x+1), -1.0, 0.5*(z+1))
    setcolor("BF8C00")
    #LEFT
    glVertex3f(-0.5*(x+1), 0.0, -0.5*(z+1))
    glVertex3f(-0.5*(x+1), 0.0, 0.5*(z+1))
    glVertex3f(-0.5*(x+1), -1.0, 0.5*(z+1))
    glVertex3f(-0.5*(x+1), -1.0, -0.5*(z+1))
    #RIGHT
    glVertex3f(0.5*(x+1), 0.0, -0.5*(z+1))
    glVertex3f(0.5*(x+1), 0.0, 0.5*(z+1))
    glVertex3f(0.5*(x+1), -1.0, 0.5*(z+1))
    glVertex3f(0.5*(x+1), -1.0, -0.5*(z+1))
    #BACK
    glVertex3f(-0.5*(x+1), 0.0, 0.5*(z+1))
    glVertex3f(0.5*(x+1), 0.0, 0.5*(z+1))
    glVertex3f(0.5*(x+1), -1.0, 0.5*(z+1))
    glVertex3f(-0.5*(x+1), -1.0, 0.5*(z+1))
    #FRONT
    glVertex3f(-0.5 * (x+1), 0.0, -0.5 * (z+1))
    glVertex3f(0.5 * (x+1), 0.0, -0.5 * (z+1))
    glVertex3f(0.5 * (x+1), -1.0, -0.5 * (z+1))
    glVertex3f(-0.5 * (x+1), -1.0, -0.5 * (z+1))
    glEnd();

def get_input():
    global view_angle_x, view_angle_y, view_distance, cursor_pos, player_turn, mouse_pressing, last_white_piece_played, last_black_piece_played
    keystate = pygame.key.get_pressed()
    m_pos = pygame.mouse.get_pos()
    m_press = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit();
            sys.exit()
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    winX = m_pos[0]
    winY = float(viewport[3]) - m_pos[1]
    winZ = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    posX, posY, posZ = gluUnProject(winX, winY, winZ, modelview, projection,
                                    viewport)
    cursor_pos = [posX, 0.01, posZ]

    if keystate[K_UP] and view_angle_x < 90:  view_angle_x += 1.0
    if keystate[K_DOWN] and view_angle_x > 0:  view_angle_x -= 1.0
    if keystate[K_LEFT]:  view_angle_y += 1.0
    if keystate[K_RIGHT]:  view_angle_y -= 1.0
    if keystate[K_PAGEUP] and view_distance < 2.0:  view_distance += .03
    if keystate[K_PAGEDOWN] and view_distance > 0.5:  view_distance -= .03
    if keystate[
        K_END]:  view_distance = 1.0;  view_angle_y = 0.0;  view_angle_x = 90.0


def makeUsableGateList(gatelist):
    newGateList = []
    for (y, z, x) in gatelist:
        newGateList.append((x,y,z))
    return newGateList


def orderwire(wire):
    ordered = []
    ordered.append(wire[0])
    wireWithoutFirst = wire[1:]
    while len(ordered) < len(wire):
        for (x,y,z) in wireWithoutFirst:
            if (x,y,z) not in ordered:
                if  (x+1,y,z) == ordered[-1] or \
                    (x-1,y,z) == ordered[-1] or \
                    (x,y+1,z) == ordered[-1] or \
                    (x,y-1,z) == ordered[-1] or \
                    (x,y,z+1) == ordered[-1] or \
                    (x,y,z-1) == ordered[-1]:
                    ordered.append((x,y,z))
                    wireWithoutFirst.remove((x,y,z))
    return ordered


def makeUsableList(KLS_CC_List):
    newWireList = []
    orderedWireList = []
    for wire in KLS_CC_List:
        newWire = []
        for (y, z, x) in wire:
            newWire.append((x,y,z))
        newWireList.append(newWire)
    #for wire in newWireList:
    #   orderedWireList.append(orderwire(wire))
    return newWireList
    #return orderedWireList

#xyz #done
def getDirection(fromNode, toNode):
    if fromNode[0] < toNode[0]:
        return 'x+'
    elif fromNode[0] > toNode[0]:
        return 'x-'
    if fromNode[1] < toNode[1]:
        return 'y+'
    elif fromNode[1] > toNode[1]:
        return 'y-'
    if fromNode[2] < toNode[2]:
        return 'z+'
    elif fromNode[2] > toNode[2]:
        return 'z-'

# return type = [[x, y, z, 'from', 'towards'], [3, 0, 10, 'x-', 'z+'], etc]
def getCorners(List):
    cornerlist = []
    for i in range(len(List)- 2):
        fromDirection = getDirection(List[i],List[i+1])
        toDirection = getDirection(List[i+1], List[i+2])
        if fromDirection != toDirection:
            print((fromDirection, toDirection))
            corner = []
            for j in List[i+1]:
                corner.append(j)
            corner.append(fromDirection)
            corner.append(toDirection)
            cornerlist.append(corner)
    return cornerlist #List with nodes on which bends occur

# input type
# Gate = [x,y,z]
# corner = [x,y,z, 'from', 'to']
# gateDirection = 'x+' or variation
def gateCornerPiece(Gate, corner, gateDirection, size, dimensions):
    StartCorner = GetPointsCorner(corner, size, dimensions)
    EndCorner = GetPointsGate(Gate, gateDirection, size, dimensions)
    Piecelist = [[None] for i in range(8)]
    # cube in x direction
    print(gateDirection)
    print(StartCorner)
    print(EndCorner)
    if gateDirection == 'x+' or gateDirection == 'x-':
        for j in range(4):
            if (StartCorner[4][j] == 5) or (StartCorner[4][j] == 6):
                Piecelist[4] = StartCorner[j]
            if (StartCorner[4][j] == 8) or (StartCorner[4][j] == 7):
                Piecelist[7] = StartCorner[j]
            if (StartCorner[4][j] == 4) or (StartCorner[4][j] == 3):
                Piecelist[3] = StartCorner[j]
            if (StartCorner[4][j] == 1) or (StartCorner[4][j] == 2):
                Piecelist[0] = StartCorner[j]
        for j in range(4):
            if (EndCorner[4][j] == 5) or (EndCorner[4][j] == 6):
                Piecelist[5] = EndCorner[j]
            if (EndCorner[4][j] == 8) or (EndCorner[4][j] == 7):
                Piecelist[6] = EndCorner[j]
            if (EndCorner[4][j] == 4) or (EndCorner[4][j] == 3):
                Piecelist[2] = EndCorner[j]
            if (EndCorner[4][j] == 1) or (EndCorner[4][j] == 2):
                Piecelist[1] = EndCorner[j]
        return [[Piecelist[0], Piecelist[1], Piecelist[5], Piecelist[4]],
                [Piecelist[4], Piecelist[5], Piecelist[6], Piecelist[7]],
                [Piecelist[7], Piecelist[6], Piecelist[2], Piecelist[3]],
                [Piecelist[3], Piecelist[2], Piecelist[1], Piecelist[0]],
                [EndCorner[0], EndCorner[1], EndCorner[2], EndCorner[3]]]
    # cube in y direction
    if gateDirection == 'y+' or gateDirection == 'y-':
        for j in range(4):
            if (StartCorner[4][j] == 5) or (StartCorner[4][j] == 1):
                Piecelist[4] = StartCorner[j]
            if (StartCorner[4][j] == 8) or (StartCorner[4][j] == 4):
                Piecelist[7] = StartCorner[j]
            if (StartCorner[4][j] == 7) or (StartCorner[4][j] == 3):
                Piecelist[6] = StartCorner[j]
            if (StartCorner[4][j] == 6) or (StartCorner[4][j] == 2):
                Piecelist[5] = StartCorner[j]
        for j in range(4):
            if (EndCorner[4][j] == 5) or (EndCorner[4][j] == 1):
                Piecelist[0] = EndCorner[j]
            if (EndCorner[4][j] == 8) or (EndCorner[4][j] == 4):
                Piecelist[3] = EndCorner[j]
            if (EndCorner[4][j] == 7) or (EndCorner[4][j] == 3):
                Piecelist[2] = EndCorner[j]
            if (EndCorner[4][j] == 6) or (EndCorner[4][j] == 2):
                Piecelist[1] = EndCorner[j]
        return [[Piecelist[0], Piecelist[4], Piecelist[5], Piecelist[1]],
                [Piecelist[1], Piecelist[5], Piecelist[6], Piecelist[2]],
                [Piecelist[2], Piecelist[6], Piecelist[7], Piecelist[3]],
                [Piecelist[3], Piecelist[7], Piecelist[4], Piecelist[0]],
                [EndCorner[0], EndCorner[1], EndCorner[2], EndCorner[3]]]
    # cube in z direction
    if gateDirection == 'z+' or gateDirection == 'z-':
        for j in range(4):
            if (StartCorner[4][j] == 5) or (StartCorner[4][j] == 8):
                Piecelist[7] = StartCorner[j]
            if (StartCorner[4][j] == 6) or (StartCorner[4][j] == 7):
                Piecelist[6] = StartCorner[j]
            if (StartCorner[4][j] == 2) or (StartCorner[4][j] == 3):
                Piecelist[2] = StartCorner[j]
            if (StartCorner[4][j] == 1) or (StartCorner[4][j] == 4):
                Piecelist[3] = StartCorner[j]
        for j in range(4):
            if (EndCorner[4][j] == 5) or (EndCorner[4][j] == 8):
                Piecelist[4] = EndCorner[j]
            if (EndCorner[4][j] == 6) or (EndCorner[4][j] == 7):
                Piecelist[5] = EndCorner[j]
            if (EndCorner[4][j] == 2) or (EndCorner[4][j] == 3):
                Piecelist[1] = EndCorner[j]
            if (EndCorner[4][j] == 1) or (EndCorner[4][j] == 4):
                Piecelist[0] = EndCorner[j]
        return [[Piecelist[0], Piecelist[3], Piecelist[2], Piecelist[1]],
                [Piecelist[1], Piecelist[2], Piecelist[6], Piecelist[5]],
                [Piecelist[5], Piecelist[6], Piecelist[7], Piecelist[4]],
                [Piecelist[4], Piecelist[7], Piecelist[3], Piecelist[0]],
                [EndCorner[0], EndCorner[1], EndCorner[2], EndCorner[3]]]


# start and end points are corners
# corner = [x,y,z, 'from', 'to']
# return = 4x trapeziod of points from corners, format:
# [[a,b,c,d],[e,f,g,h],[i,j,k,l],[m,n,o,p]]
def CornerCornerPiece(Startpoint, Endpoint, size, Dimensions):
    StartCorner = GetPointsCorner(Startpoint, size, Dimensions)
    EndCorner = GetPointsCorner(Endpoint, size, Dimensions)
    Piecelist = [[None] for i in range(8)]
    # cube x direction
    print(Startpoint[4])
    print(StartCorner)
    print(Endpoint[4])
    print(Endpoint)
    print(EndCorner)
    if Startpoint[4] == 'x+' or Startpoint[4] == 'x-':
        for j in range(4):
            if (StartCorner[4][j] == 5) or (StartCorner[4][j] == 6):
                Piecelist[4] = StartCorner[j]
            if (StartCorner[4][j] == 8) or (StartCorner[4][j] == 7):
                Piecelist[7] = StartCorner[j]
            if (StartCorner[4][j] == 4) or (StartCorner[4][j] == 3):
                Piecelist[3] = StartCorner[j]
            if (StartCorner[4][j] == 1) or (StartCorner[4][j] == 2):
                Piecelist[0] = StartCorner[j]
        for j in range(4):
            if (EndCorner[4][j] == 5) or (EndCorner[4][j] == 6):
                Piecelist[5] = EndCorner[j]
            if (EndCorner[4][j] == 8) or (EndCorner[4][j] == 7):
                Piecelist[6] = EndCorner[j]
            if (EndCorner[4][j] == 4) or (EndCorner[4][j] == 3):
                Piecelist[2] = EndCorner[j]
            if (EndCorner[4][j] == 1) or (EndCorner[4][j] == 2):
                Piecelist[1] = EndCorner[j]
        print(Piecelist)
        return [[Piecelist[0], Piecelist[1], Piecelist[5], Piecelist[4]],
                [Piecelist[4], Piecelist[5], Piecelist[6], Piecelist[7]],
                [Piecelist[7], Piecelist[6], Piecelist[2], Piecelist[3]],
                [Piecelist[3], Piecelist[2], Piecelist[1], Piecelist[0]]]
    # cube y direction
    if Startpoint[4] == 'y+' or Startpoint[4] == 'y-':
        for j in range(4):
            if (StartCorner[4][j] == 5) or (StartCorner[4][j] == 1):
                Piecelist[4] = StartCorner[j]
            if (StartCorner[4][j] == 8) or (StartCorner[4][j] == 4):
                Piecelist[7] = StartCorner[j]
            if (StartCorner[4][j] == 7) or (StartCorner[4][j] == 3):
                Piecelist[6] = StartCorner[j]
            if (StartCorner[4][j] == 6) or (StartCorner[4][j] == 2):
                Piecelist[5] = StartCorner[j]
        for j in range(4):
            if (EndCorner[4][j] == 5) or (EndCorner[4][j] == 1):
                Piecelist[0] = EndCorner[j]
            if (EndCorner[4][j] == 8) or (EndCorner[4][j] == 4):
                Piecelist[3] = EndCorner[j]
            if (EndCorner[4][j] == 7) or (EndCorner[4][j] == 3):
                Piecelist[2] = EndCorner[j]
            if (EndCorner[4][j] == 6) or (EndCorner[4][j] == 2):
                Piecelist[1] = EndCorner[j]
        print(Piecelist)
        return [[Piecelist[0], Piecelist[4], Piecelist[5], Piecelist[1]],
                [Piecelist[1], Piecelist[5], Piecelist[6], Piecelist[2]],
                [Piecelist[2], Piecelist[6], Piecelist[7], Piecelist[3]],
                [Piecelist[3], Piecelist[7], Piecelist[4], Piecelist[0]]]
    # cube z direction
    if Startpoint[4] == 'z+' or Startpoint[4] == 'z-':
        for j in range(4):
            if (StartCorner[4][j] == 5) or (StartCorner[4][j] == 8):
                Piecelist[7] = StartCorner[j]
            if (StartCorner[4][j] == 6) or (StartCorner[4][j] == 7):
                Piecelist[6] = StartCorner[j]
            if (StartCorner[4][j] == 2) or (StartCorner[4][j] == 3):
                Piecelist[2] = StartCorner[j]
            if (StartCorner[4][j] == 1) or (StartCorner[4][j] == 4):
                Piecelist[3] = StartCorner[j]
        for j in range(4):
            if (EndCorner[4][j] == 5) or (EndCorner[4][j] == 8):
                Piecelist[4] = EndCorner[j]
            if (EndCorner[4][j] == 6) or (EndCorner[4][j] == 7):
                Piecelist[5] = EndCorner[j]
            if (EndCorner[4][j] == 2) or (EndCorner[4][j] == 3):
                Piecelist[1] = EndCorner[j]
            if (EndCorner[4][j] == 1) or (EndCorner[4][j] == 4):
                Piecelist[0] = EndCorner[j]
        print(Piecelist)
        return [[Piecelist[0], Piecelist[3], Piecelist[2], Piecelist[1]],
                [Piecelist[1], Piecelist[2], Piecelist[6], Piecelist[5]],
                [Piecelist[5], Piecelist[6], Piecelist[7], Piecelist[4]],
                [Piecelist[4], Piecelist[7], Piecelist[3], Piecelist[0]]]


def GateGatePiece(startGate, endGate, gateDirection, size, dimensions):
    start = GetPointsGate(startGate, gateDirection, size, dimensions)
    newDirection = getDirection(endGate, startGate)
    end = GetPointsGate(endGate, newDirection, size, dimensions)
    Piecelist = [[None] for i in range(8)]
    if gateDirection == 'x+' or gateDirection == 'x-':
        for i in range(4):
            if start[4][i] == 5 or start[4][i] == 6:
                Piecelist[4] = start[i]
            if start[4][i] == 8 or start[4][i] == 7:
                Piecelist[7] = start[i]
            if start[4][i] == 4 or start[4][i] == 3:
                Piecelist[3] = start[i]
            if start[4][i] == 1 or start[4][i] == 2:
                Piecelist[0] == start[i]
        for i in range(4):
            if end[4][i] == 5 or end[4][i] == 6:
                Piecelist[5] = end[i]
            if end[4][i] == 8 or end[4][i] == 7:
                Piecelist[6] = end[i]
            if end[4][i] == 4 or end[4][i] == 3:
                Piecelist[2] = end[i]
            if end[4][i] == 1 or end[4][i] == 2:
                Piecelist[1] = end[i]
        return [[Piecelist[0], Piecelist[1], Piecelist[5], Piecelist[4]],
                [Piecelist[4], Piecelist[5], Piecelist[6], Piecelist[7]],
                [Piecelist[7], Piecelist[6], Piecelist[2], Piecelist[3]],
                [Piecelist[3], Piecelist[2], Piecelist[1], Piecelist[0]]]
    if gateDirection == 'z+' or gateDirection == 'z-':
        for i in range(4):
            if start[4][i] == 5 or start[4][i] == 8:
                Piecelist[4] = start[i]
            if start[4][i] == 6 or start[4][i] == 7:
                Piecelist[5] = start[i]
            if start[4][i] == 2 or start[4][i] == 3:
                Piecelist[1] = start[i]
            if start[4][i] == 1 or start[4][i] == 4:
                Piecelist[0] = start[i]
        for i in range(4):
            if end[4][i] == 5 or end[4][i] == 8:
                Piecelist[7] = end[i]
            if end[4][i] == 6 or end[4][i] == 7:
                Piecelist[6] = end[i]
            if end[4][i] == 2 or end[4][i] == 3:
                Piecelist[2] = end[i]
            if end[4][i] == 1 or end[4][i] == 4:
                Piecelist[3] = end[i]
        return [[Piecelist[0], Piecelist[3], Piecelist[2], Piecelist[1]],
                [Piecelist[1], Piecelist[2], Piecelist[6], Piecelist[5]],
                [Piecelist[5], Piecelist[6], Piecelist[7], Piecelist[4]],
                [Piecelist[4], Piecelist[7], Piecelist[3], Piecelist[0]]]


def GetPointsGate(Gate, GateDirection, size, Dimensions):
    [x,y,z] = Gate
    coordx = -0.5* Dimensions[0] + x
    coordy = y + 0.5
    coordz = -0.5* Dimensions[2] + z
    if GateDirection == 'x+':
        return [[(0.5 - size) + coordx, -1 * size + coordy, -1 * size + coordz],
                [(0.5 - size) + coordx, -1 * size + coordy, size + coordz],
                [(0.5 - size) + coordx, size + coordy, size + coordz],
                [(0.5 - size) + coordx, size + coordy, -1 * size + coordz],
                [2,3,7,6]]
    if GateDirection == 'x-':
        return [[-1 * (0.5 - size) + coordx, -1 * size + coordy, -1 * size + coordz],
                [-1 * (0.5 - size) + coordx, -1 * size + coordy, size + coordz],
                [-1 * (0.5 - size) + coordx, size + coordy, size + coordz],
                [-1 * (0.5 - size) + coordx, size + coordy, -1 * size + coordz],
                [1,4,8,5]]
    if GateDirection == 'y+':
        return [[-1 * size + coordx, (0.5 - size) + coordy, -1 * size + coordz],
                [-1 * size + coordx, (0.5 - size) + coordy, size + coordz],
                [size + coordx, (0.5 - size) + coordy, size + coordz],
                [size + coordx, (0.5 - size) + coordy, -1 * size + coordz],
                [5,8,7,6]]
    if GateDirection == 'y-':
        return [[-1 * size + coordx, -1 * (0.5 - size) + coordy, -1 * size + coordz],
                [-1 * size + coordx, -1 * (0.5 - size) + coordy, size + coordz],
                [size + coordx, -1 * (0.5 - size) + coordy, size + coordz],
                [size + coordx, -1 * (0.5 - size) + coordy, -1 * size + coordz],
                [1,4,3,2]]
    if GateDirection == 'z+':
        return [[-1 * size + coordx, size + coordy, (0.5 - size) + coordz],
                [-1 * size + coordx, -1 * size + coordy, (0.5 - size) + coordz],
                [size + coordx, -1 * size + coordy, (0.5 - size) + coordz],
                [size + coordx, size + coordy, (0.5 - size) + coordz],
                [8, 4, 3, 7]]
    if GateDirection == 'z-':
        return [[-1 * size + coordx, size + coordy, -1 * (0.5 - size) + coordz],
                [-1 * size + coordx, -1 * size + coordy, -1 * (0.5 - size) + coordz],
                [size + coordx, -1 * size + coordy, -1 * (0.5 - size) + coordz],
                [size + coordx, size + coordy, -1 * (0.5 - size) + coordz],
                [5, 1, 2, 6]]

def gatevertex(gatelist, pointlist):
    for i in pointlist:
        [x, y, z] = gatelist[i]
        glVertex3f(x, y, z)


# coord = [x,y,z]
def makegate(size):
    coordy = 0.5
    # Xcoords
    leftmost = -1*(0.5 - size)
    left = -1*size
    right = size
    rightmost = (0.5 - size)
    # Ycoords
    underbot = 0
    bot = coordy - (0.5- size)
    mid = coordy + size
    top = coordy +(0.5 - size)
    # Zcoords
    frontmost = -1*(0.5 - size)
    front = -1* size
    back = size
    backmost = (0.5-size)
    #append
    gatelist = [[left, bot, backmost],  #0
                [right, bot, backmost],  #1
                [rightmost, bot, back],  #2
                [rightmost, bot, front],  #3
                [right, bot, frontmost],  #4
                [left, bot, frontmost],  #5
                [leftmost, bot, front],  #6
                [leftmost, bot, back],  #7
                [left, bot, back],  #8
                [right, bot, back],  #9
                [right, bot, front],  #10
                [left, bot, front],  #11
                [left, mid, backmost],  #12
                [right, mid, backmost],  #13
                [rightmost, mid, back],  #14
                [rightmost, mid, front],  #15
                [right, mid, frontmost],  #16
                [left, mid, frontmost],  #17
                [leftmost, mid, front],  #18
                [leftmost, mid, back],  #19
                [left, mid, back],  # 20
                [right, mid, back],  # 21
                [right, mid, front],  # 22
                [left, mid, front],  # 23
                [left, top, back],  # 24
                [right, top, back],  # 25
                [right, top, front],  # 26
                [left, top, front], # 27
                [leftmost, bot, backmost], #28
                [rightmost, bot, backmost], #29
                [rightmost, bot, frontmost], #30
                [leftmost, bot, frontmost], #31
                [leftmost, underbot, backmost], #32
                [rightmost, underbot, backmost], #33
                [rightmost, underbot, frontmost], #34
                [leftmost, underbot, frontmost]] #35

    glGenLists(1)
    glNewList(3, GL_COMPILE)
    glBegin(GL_QUADS)
    # backblock
    gatevertex(gatelist, [0, 1, 13, 12])
    gatevertex(gatelist, [12, 13, 21, 20])
    gatevertex(gatelist, [8, 0, 12, 20])
    gatevertex(gatelist, [9, 1, 13, 21])
    # rightblock
    gatevertex(gatelist, [9, 2, 14, 21])
    gatevertex(gatelist, [2, 3, 15, 14])
    gatevertex(gatelist, [3, 10, 22, 15])
    gatevertex(gatelist, [21, 14, 15, 22])
    # frontblock
    gatevertex(gatelist, [10, 4, 16, 22])
    gatevertex(gatelist, [4, 5, 17, 16])
    gatevertex(gatelist, [5, 11, 23, 17])
    gatevertex(gatelist, [22, 16, 17, 23])
    # leftblock
    gatevertex(gatelist, [11, 6, 18, 23])
    gatevertex(gatelist, [6, 7, 19, 18])
    gatevertex(gatelist, [7, 8, 20,19])
    gatevertex(gatelist, [23,18,19,20])
    # topblock
    gatevertex(gatelist, [20, 21, 25, 24])
    gatevertex(gatelist, [21, 22, 26, 25])
    gatevertex(gatelist, [22, 23, 27, 26])
    gatevertex(gatelist, [23, 20, 24, 27])
    gatevertex(gatelist, [24, 25, 26, 27])
    # bottom
    gatevertex(gatelist, [28, 29, 33, 32])
    gatevertex(gatelist, [29, 30, 34, 33])
    gatevertex(gatelist, [30, 31, 35, 34])
    gatevertex(gatelist, [31, 28, 32, 35])
    gatevertex(gatelist, [32, 33, 34, 35])
    gatevertex(gatelist, [28, 29, 30, 31])
    glEnd();
    glEndList()


# corner = [x,y,z, 'from', 'to']
# return = List of 4*[x, y, z] + lijst respectievelijk positie in cubus
# zie kubus.png
# 'and' part =  to do
def GetPointsCorner(corner, size, dimensions):
    coordx = -0.5*dimensions[0]+corner[0]
    coordy = corner[1] +0.5
    coordz = -0.5*dimensions[2]+corner[2]
    # left/top face options and right/bottom
    if (corner[3] == 'x+' and corner[4] == 'y+') or \
        (corner[3] == 'y-' and corner[4] == 'x-') or \
        (corner[3] == 'x-' and corner[4] =='y-') or \
        (corner[3] == 'y+' and corner[4] == 'x+'):
        return [[-1 * size + coordx, size + coordy, -1 * size + coordz],
                [-1 * size + coordx, size + coordy, size + coordz],
                [size + coordx, -1 * size + coordy, size + coordz],
                [size + coordx, -1 * size + coordy, -1 * size + coordz],
                [5,8,3,2]]
    # back/top face options and front/bottom
    if (corner[3] == 'z-' and corner[4] == 'y+') or \
        (corner[3] == 'y-' and corner[4] == 'z+') or \
        (corner[3] == 'z+' and corner[4] == 'y-') or \
        (corner[3] == 'y+' and corner[4] == 'z-'):
        return [[-1 * size + coordx, size + coordy, size + coordz],
                [size + coordx, size + coordy, size + coordz],
                [size + coordx, -1 * size + coordy, -1 * size + coordz],
                [-1 * size + coordx, -1 * size + coordy, -1 * size + coordz],
                [8,7,2,1]]
    # right/top face options and left/bottom
    if (corner[3] == 'x-' and corner[4] == 'y+') or \
        (corner[3] == 'y-' and corner[4] == 'x+') or \
        (corner[3] == 'x+' and corner[4] == 'y-') or \
        (corner[3] == 'y+' and corner[4] == 'x-'):
        return [[size + coordx, size + coordy, size + coordz],
                [size + coordx, size + coordy, -1 * size + coordz],
                [-1 * size + coordx, -1 * size + coordy, -1 * size + coordz],
                [-1 * size + coordx, -1 * size + coordy, size + coordz],
                [7, 6, 1, 4]]
    # front/top face options and back/bottom
    if (corner[3] == 'z+' and corner[4] == 'y+') or \
        (corner[3] == 'y-' and corner[4] == 'z-') or \
        (corner[3] == 'z-' and corner[4] == 'y-') or \
        (corner[3] == 'y+' and corner[4] == 'z+'):
        return [[-1 * size + coordx, size + coordy, -1 * size + coordz],
                [size + coordx, size + coordy, -1 * size + coordz],
                [size + coordx, -1 * size + coordy, size + coordz],
                [-1 * size + coordx, -1 * size + coordy, size + coordz],
                [5,6,3,4]]
    # front/right face options and back/left
    if (corner[3] == 'z+' and corner[4] == 'x+') or \
        (corner[3] == 'x-' and corner[4] =='z-') or \
        (corner[3] == 'z-' and corner[4] == 'x-') or \
        (corner[3] == 'x+' and corner[4] == 'z+'):
        return [[size + coordx, -1 * size + coordy, -1 * size + coordz],
                [size + coordx, size + coordy, -1 * size + coordz],
                [-1 * size + coordx, size + coordy, size + coordz],
                [-1 * size + coordx, -1 * size + coordy, size + coordz],
                [2, 6, 8, 4]]
    # front/left face options and back/right
    if (corner[3] == 'z+' and corner[4] == 'x-') or \
        (corner[3] == 'x+' and corner[4] == 'z-') or \
        (corner[3] == 'z-' and corner[4] == 'x+') or \
        (corner[3] == 'x-' and corner[4] == 'z+'):
        return [[-1 * size + coordx, -1 * size + coordy, -1 * size + coordz],
                [-1 * size + coordx, size + coordy, -1 * size + coordz],
                [size + coordx, size + coordy, size + coordz],
                [size + coordx, -1 * size + coordy, size + coordz],
                [1,5,7,3]]

#########################################################
def TurnToObject(List):
    glGenLists(1)
    glNewList(2, GL_COMPILE)
    glBegin(GL_QUADS)
    print(List)
    lastlen = 0
    r = 1.0
    g = 0.0
    b = 0.0
    difflengths = []
    for wire in List:
        curlen = len(wire)
        if curlen not in difflengths:
            difflengths.append(curlen)
    diffcolour = len(difflengths)
    for wire in List:
        curlen = len(wire)
        if curlen > lastlen:
            lastlen = curlen
            g = g + 0.8/diffcolour
        glColor3f(r,g,b)
        for trapezoid in wire:
            print(trapezoid)
            for points in trapezoid:
                for vertex in points:
                    print(vertex)
                    [x,y,z] = vertex
                    glVertex3f(x,y,z)
    glEnd();
    glEndList()


def main(wireList, gatesList, size, dimensions):
    List = makeUsableList(wireList)
    completeWireList = []
    for wire in List:
        newWire = makeNewWire(wire, size, dimensions)
        completeWireList.append(newWire)
    completeWireList.sort(key=len)
    print(completeWireList)
    TurnToObject(completeWireList)
    gates = makeUsableGateList(gatesList)
    makegate(size)
    while True:
        draw(dimensions, gates)
        get_input()


def makeNewWire(wire, size, dimensions):
    newWire = []
    gatedirection = getDirection(wire[0],wire[1])
    cornerList = getCorners(wire)
    print(cornerList)
    #"""
    if len(cornerList) < 1:
        GateGatePiece(wire[0], wire[-1], gatedirection, size, dimensions)
    else:
        newWire.append(gateCornerPiece(wire[0], cornerList[0], gatedirection, size,
                            dimensions))
        for i in range(len(cornerList)-2):
            print('çorner')
            NewPiece = CornerCornerPiece(cornerList[i], cornerList[i+1], size, Dimensions)
            newWire.append(NewPiece)
        gatedirection = getDirection(wire[-2], wire[-1])
        newWire.append(gateCornerPiece(wire[-1], cornerList[-1], gatedirection, size, dimensions))
    return newWire
    #"""

# input examples
# netlist_list = [2,4,3], average_.. = 5, methods = [ppa,helev,decrmut]
def create_graph(netlist_list, average_over_X_repeats, methods):
    for net in netlist_list:
        if "ppa" in methods:
            ppa_results = [None]*average_over_X_repeats
        if "helev" in method:
            helev_results = [None]*average_over_X_repeats
        if "decrmut" in method:
            decrmut_results = [None]*average_over_X_repeats
        for method in methods:
            if method == "ppa":
                #line length plot
                for k in range(average_over_X_repeats):
                    ppa_results[k] = ppa.PPA_data(net)
                ppa_iteration_sizes = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    ppa_iteration_sizes[k] = len(ppa_results[k][0])
                ppa_average_lengths = [0]*max(ppa_iteration_sizes)
                for k in range(average_over_X_repeats):
                    for i in range(len(ppa_results[k][0])-1):
                        ppa_average_lengths[i] += ppa_results[k][0][i]
                ppa_iteration_sizes.sort()
                for k in range(len(ppa_average_lengths)-1):
                    while k > ppa_iteration_sizes[0]:
                        del ppa_iteration_sizes[0]
                    ppa_average_lengths[k] = ppa_average_lengths[k]/len(ppa_iteration_sizes)
                plt.plot(ppa_average_lengths)

                # generation point plot
                ppa_generation_amount = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    ppa_generation_amount[k] = len(ppa_results[k][1])
                ppa_average_generation_points = [0]*max(ppa_generation_amount)
                for k in range(average_over_X_repeats):
                    for i in range(len(ppa_results[k][1])-1):
                        ppa_average_generation_points[i] += ppa_results[k][1][i]
                for i in ppa_average_generation_points:
                    ppa_average_generation_points[i] = ppa_average_generation_points[i]/average_over_X_repeats
                for xc in ppa_average_generation_points:
                    plt.axvline(x=xc, color='r')

                #earliest/average first constraint satisfaction
                first_constraint_satisfaction_list = []
                for k in range(average_over_X_repeats):
                    first_constraint_satisfaction_list.append(ppa_results[k][2])
                # for earliest use min(...), for average use sum(...)/average_over..
                plt.axhline(sum(first_constraint_satisfaction_list)/average_over_X_repeats, color='y')

                #data possibilities
                best_heights = []
                for k in average_over_X_repeats:
                    best_heights.append(ppa_results[k][4])
                best_lengths = []
                for k in average_over_X_repeats:
                    best_lengths.append(ppa_results[k][5])
                best_orders = []
                for k in average_over_X_repeats:
                    best_orders.append(ppa_results[k][3])
                combined_height_order = []
                for k in average_over_X_repeats:
                    combined_height_order.append([best_heights[k], best_orders[k]])
                #sort
                best_lengths, combined_height_order = (list(x) for x in zip(
                    *sorted(zip(best_lengths, combined_height_order),
                            key=lambda pair: pair[0])))

                best_height = combined_height_order[0][0]
                best_order = combined_height_order[0][1]
                best_length = best_lengths[0]

            if method == "helev":
                for k in range(average_over_X_repeats):
                    helev_results[k] = eh.hill_climber_data(net)
                # line length plot
                iteration_amount = len(helev_results[0][0])
                helev_average_lengths = [0]*iteration_amount
                for k in range(average_over_X_repeats):
                    for i in range(len(helev_results[k][0]) - 1):
                        helev_average_lengths[i] += helev_results[k][0][i]
                for k in range(len(helev_average_lengths) - 1):
                    helev_average_lengths[k] = ppa_average_lengths[k] / average_over_X_repeats
                plt.plot(helev_average_lengths)


                # earliest/average first constraint satisfaction
                first_constraint_satisfaction_list = []
                for k in range(average_over_X_repeats):
                    first_constraint_satisfaction_list.append(
                        helev_results[k][1])
                # for earliest use min(...), for average use sum(...)/average_over..
                plt.axhline(sum(
                    first_constraint_satisfaction_list) / average_over_X_repeats,
                            color='g')

                # data possibilities
                best_heights = []
                for k in average_over_X_repeats:
                    best_heights.append(helev_results[k][3])
                best_lengths = []
                for k in average_over_X_repeats:
                    best_lengths.append(helev_results[k][4])
                best_orders = []
                for k in average_over_X_repeats:
                    best_orders.append(helev_results[k][2])
                combined_height_order = []
                for k in average_over_X_repeats:
                    combined_height_order.append(
                        [best_heights[k], best_orders[k]])
                # sort
                best_lengths, combined_height_order = (list(x) for x in zip(
                    *sorted(zip(best_lengths, combined_height_order),
                            key=lambda pair: pair[0])))

                best_height = combined_height_order[0][0]
                best_order = combined_height_order[0][1]
                best_length = best_lengths[0]

            if method == "decrmut":
                for k in range(average_over_X_repeats):
                    decrmut_results[k] = eh.decreasing_mutations(net)
                #line length plot
                decrmut_iteration_sizes = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    decrmut_iteration_sizes[k] = len(decrmut_results[k][0])
                decrmut_average_lengths = [0]*max(decrmut_iteration_sizes)
                for k in range(average_over_X_repeats):
                    for i in range(len(decrmut_results[k][0])-1):
                        decrmut_average_lengths[i] += decrmut_results[k][0][i]
                decrmut_iteration_sizes.sort()
                for k in range(len(decrmut_average_lengths)-1):
                    while k > decrmut_iteration_sizes[0]:
                        del decrmut_iteration_sizes[0]
                    decrmut_average_lengths[k] = decrmut_average_lengths[k]/len(decrmut_iteration_sizes)
                plt.plot(decrmut_average_lengths)

                # generation point plot
                decrmut_generation_amount = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    decrmut_generation_amount[k] = len(decrmut_results[k][1])
                decrmut_average_generation_points = [0]*max(decrmut_generation_amount)
                for k in range(average_over_X_repeats):
                    for i in range(len(decrmut_results[k][1])-1):
                        decrmut_average_generation_points[i] += decrmut_results[k][1][i]
                for i in decrmut_average_generation_points:
                    decrmut_average_generation_points[i] = decrmut_average_generation_points[i]/average_over_X_repeats
                for xc in decrmut_average_generation_points:
                    plt.axvline(x=xc, color='c')

                #earliest/average first constraint satisfaction
                first_constraint_satisfaction_list = []
                for k in range(average_over_X_repeats):
                    first_constraint_satisfaction_list.append(decrmut_results[k][2])
                # for earliest use min(...), for average use sum(...)/average_over..
                plt.axhline(sum(first_constraint_satisfaction_list)/average_over_X_repeats, color='m')

                #data possibilities
                best_heights = []
                for k in average_over_X_repeats:
                    best_heights.append(decrmut_results[k][4])
                best_lengths = []
                for k in average_over_X_repeats:
                    best_lengths.append(decrmut_results[k][5])
                best_orders = []
                for k in average_over_X_repeats:
                    best_orders.append(decrmut_results[k][3])
                combined_height_order = []
                for k in average_over_X_repeats:
                    combined_height_order.append([best_heights[k], best_orders[k]])
                #sort
                best_lengths, combined_height_order = (list(x) for x in zip(
                    *sorted(zip(best_lengths, combined_height_order),
                            key=lambda pair: pair[0])))

                best_height = combined_height_order[0][0]
                best_order = combined_height_order[0][1]
                best_length = best_lengths[0]


        standard_elevator_solution = el.return_value_elevator(net)


#main(wireList, gatesList, size, Dimensions)

ppa.PPA_graph([2])