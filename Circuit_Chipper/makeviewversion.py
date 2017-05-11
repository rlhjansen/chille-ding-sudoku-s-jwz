from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from numpy import *
import sys, os

import GL

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


Dimensions = [18,7,13]
size = 0.1



def draw(Dimensions):
    # CLEAR ALL----------------------------------------
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # BASIC CAMERA VIEW--------------------------------
    glTranslatef(0.0, 0.0, -51.0 * view_distance)
    glRotatef(view_angle_x, 1.0, 0.0, 0.0)
    glRotatef(view_angle_y, 0.0, 1.0, 0.0)
    # BOARD--------------------------------------------
    drawchip(Dimensions)
    # WIRES--------------------------------------------
    glTranslatef(0.0, -0.01, 0.0)
    glPushMatrix()
    glCallList(4)
    glPopMatrix()
    glPushMatrix()
    # CURSOR-------------------------------------------
    glTranslatef(round(cursor_pos[0] / 2.10176) * 2.10176, cursor_pos[1],
                 round(cursor_pos[2] / 2.10176) * 2.10176)
    glCallList(2)
    glPopMatrix()
    pygame.display.flip()



# coordinates = [z,y,x]
def drawchip(coordinates):
    (z, y, x) = coordinates
    glBegin(GL_QUADS)
    #TOP
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


def makeUsableList(KLS_CC_List):
    newWireList = []
    for wire in KLS_CC_List:
        newWire = []
        for (y,z,x) in wire:
            newWire.append((x,y,z))
        newWireList.append(newWire)
    return newWireList

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
        for k in range(4):
            if (EndCorner[4][j] == 5) or (EndCorner[4][j] == 6):
                Piecelist[5] = StartCorner[j]
            if (EndCorner[4][j] == 8) or (EndCorner[4][j] == 7):
                Piecelist[6] = StartCorner[j]
            if (EndCorner[4][j] == 4) or (EndCorner[4][j] == 3):
                Piecelist[2] = StartCorner[j]
            if (EndCorner[4][j] == 1) or (EndCorner[4][j] == 2):
                Piecelist[1] = StartCorner[j]
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
        for k in range(4):
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
        for k in range(4):
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


#######################################################################
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
    if gateDirection == 'y+' or gateDirection == 'y-':
        for i in range(4):
            if start[4][i] == 1 or start[4][i] == 5:
                Piecelist[0] = start[i]
            if start[4][i] == 2 or start[4][i] == 6:
                Piecelist[1] = start[i]
            if start[4][i] == 3 or start[4][i] == 7:
                Piecelist[2] = start[i]
            if start[4][i] == 4 or start[4][i] == 8:
                Piecelist[3] = start[i]
        for i in range(4):
            if end[4][i] == 1 or end[4][i] == 5:
                Piecelist[4] = end[i]
            if end[4][i] == 2 or end[4][i] == 6:
                Piecelist[5] = end[i]
            if end[4][i] == 3 or end[4][i] == 7:
                Piecelist[6] = end[i]
            if end[4][i] == 4 or end[4][i] == 8:
                Piecelist[7] = end[i]
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



def GetPointsGate(Gate, GateDirection, size, Dimensions):
    [x,y,z] = Gate
    coordx = -0.5* Dimensions[0] + x
    coordy = -0.5* Dimensions[1] + y
    coordz = -0.5* Dimensions[2] + z
    if GateDirection == 'x+':
        return [[size + coordx, -1 * size + coordy, -1 * size + coordz],
                [size + coordx, -1 * size + coordy, size + coordz],
                [size + coordx, size + coordy, size + coordz],
                [size + coordx, size + coordy, -1 * size + coordz],
                [2,3,7,6]]
    if GateDirection == 'x-':
        return [[-1 * size + coordx, -1 * size + coordy, -1 * size + coordz],
                [-1 * size + coordx, -1 * size + coordy, size + coordz],
                [-1 * size + coordx, size + coordy, size + coordz],
                [-1 * size + coordx, size + coordy, -1 * size + coordz],
                [1,4,8,5]]
    if GateDirection == 'y+':
        return [[-1 * size + coordx, size + coordy, -1 * size + coordz],
                [-1 * size + coordx, size + coordy, size + coordz],
                [size + coordx, size + coordy, size + coordz],
                [size + coordx, size + coordy, -1 * size + coordz],
                [5,8,7,6]]
    if GateDirection == 'y-':
        return [[-1 * size + coordx, -1 * size + coordy, -1 * size + coordz],
                [-1 * size + coordx, -1 * size + coordy, size + coordz],
                [size + coordx, -1 * size + coordy, size + coordz],
                [size + coordx, -1 * size + coordy, -1 * size + coordz],
                [1,4,3,2]]
    if GateDirection == 'z+':
        return [[-1 * size + coordx, size + coordy, size + coordz],
                [-1 * size + coordx, -1 * size + coordy, size + coordz],
                [size + coordx, -1 * size + coordy, size + coordz],
                [size + coordx, size + coordy, size + coordz],
                [8, 4, 3, 7]]
    if GateDirection == 'z-':
        return [[-1 * size + coordx, size + coordy, -1 * size + coordz],
                [-1 * size + coordx, -1 * size + coordy, -1 * size + coordz],
                [size + coordx, -1 * size + coordy, -1 * size + coordz],
                [size + coordx, size + coordy, -1 * size + coordz],
                [5, 1, 2, 6]]


# corner = [x,y,z, 'from', 'to']
# return = List of 4*[x, y, z] + lijst respectievelijk positie in cubus
# zie kubus.png
# 'and' part =  to do
def GetPointsCorner(corner, size, dimensions):
    coordx = -0.5*dimensions[0]+corner[0]
    coordy = -0.5*dimensions[1]+corner[1]
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
    for wire in List:
        for trapezoid in wire:
            print(trapezoid)
            for points in trapezoid:
                for vertex in points:
                    print(vertex)
                    [x,y,z] = vertex
                    glVertex3f(x,y,z)
    glEnd();
    glEndList()

#########################################################
def main(wireList, size, dimensions):
    List = makeUsableList(wireList)
    completeWireList = []
    for wire in List:
        newWire = makeNewWire(wire, size, dimensions)
        completeWireList.append(newWire)
    #"""
    TurnToObject(completeWireList)
    while True:
        draw(dimensions)
        get_input()
    #"""


########################################################3
def makeNewWire(wire, size, dimensions):
    newWire = []
    gatedirection = getDirection(wire[0],wire[1])
    cornerList = getCorners(wire)
    print(cornerList)
    #"""
    if len(cornerList) < 2:
        pass
        #GateGatePiece(wire[0], wire[-1], gatedirection, size, dimensions)
    else:
        #newWire.append(gateCornerPiece(wire[0], cornerList[0], gatedirection, size,
        #                    dimensions))
        #print(gateCornerPiece(wire[0], cornerList[0], gatedirection, size,
        #                    dimensions))
        for i in range(len(cornerList)-2):
            print('çorner')
            NewPiece = CornerCornerPiece(cornerList[i], cornerList[i+1], size, Dimensions)
            newWire.append(NewPiece)
        gatedirection = getDirection(wire[-2], wire[-1])
       # newWire.append(gateCornerPiece(wire[-1], cornerList[-1], gatedirection, size, dimensions))
    return newWire
    #"""




main(wireList, size, Dimensions)






