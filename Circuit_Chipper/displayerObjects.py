import os, sys
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

pygame.init()


def main(Textures, number):
    for i in range(number):
        glGenLists(1)
        glNewList(7+i, GL_COMPILE)  # Black Marble
        glColor3f(0.20*i, 0.09, 0.39)
        glPushMatrix()
        glScalef(1.0, 1.0, 1.0)
        Sphere = gluNewQuadric()
        gluQuadricTexture(Sphere, GL_TRUE)
        gluSphere(Sphere, 0.75, 5, 5)
        glPopMatrix()
        glEndList()
    # BOARD --------------------------------------
    glGenLists(1)
    glNewList(1, GL_COMPILE)  # Board
    glBegin(GL_QUADS)
    # TOP BORDER
    # Quad 1
    glColor3f(0.09, 0.09, 0.09)
    glVertex3f(-21.0, 0.0, -21.0)
    glVertex3f(-19, 0.0, -21.0)
    glVertex3f(-19, 0.0, 21.0)
    glVertex3f(-21.0, 0.0, 21.0)
    # Quad 2
    glVertex3f(21.0, 0.0, -21.0)
    glVertex3f(19, 0.0, -21.0)
    glVertex3f(19, 0.0, 21.0)
    glVertex3f(21.0, 0.0, 21.0)
    # Quad 3
    glVertex3f(-19, 0.0, 19)
    glVertex3f(19, 0.0, 19)
    glVertex3f(19, 0.0, 21.0)
    glVertex3f(-19, 0.0, 21.0)
    # Quad 4
    glVertex3f(-19, 0.0, -19)
    glVertex3f(19, 0.0, -19)
    glVertex3f(19, 0.0, -21.0)
    glVertex3f(-19, 0.0, -21.0)
    # SIDES
    # Left Side
    glVertex3f(-21.0, -3.0, -21.0)
    glVertex3f(-21.0, 0.0, -21.0)
    glVertex3f(-21.0, 0.0, 21.0)
    glVertex3f(-21.0, -3.0, 21.0)
    # Right Side
    glVertex3f(21.0, -3.0, -21.0)
    glVertex3f(21.0, 0.0, -21.0)
    glVertex3f(21.0, 0.0, 21.0)
    glVertex3f(21.0, -3.0, 21.0)
    # Bottom Side
    glVertex3f(-21.0, -3.0, 21.0)
    glVertex3f(-21.0, 0.0, 21.0)
    glVertex3f(21.0, 0.0, 21.0)
    glVertex3f(21.0, -3.0, 21.0)
    # Top Side
    glVertex3f(-21.0, -3.0, -21.0)
    glVertex3f(-21.0, 0.0, -21.0)
    glVertex3f(21.0, 0.0, -21.0)
    glVertex3f(21.0, -3.0, -21.0)
    # BOTTOM
    glVertex3f(-21.0, -3.0, -21.0)
    glVertex3f(21.0, -3.0, -21.0)
    glVertex3f(21.0, -3.0, 21.0)
    glVertex3f(-21.0, -3.0, 21.0)
    glEnd();
    # GRID
    glBegin(GL_QUADS)
    glVertex3f(-19.0, 0.0, -19.0)
    glVertex3f(19.0, 0.0, -19.0)
    glVertex3f(19.0, 0.0, 19.0)
    glVertex3f(-19.0, 0.0, 19.0)
    glEnd();
    glEndList()

    glGenLists(1)
    glNewList(2, GL_COMPILE)  # White Marble
    glColor3f(0.20, 0.09, 0.09)
    glPushMatrix()
    glScalef(1.0, 0.5, 1.0)
    Sphere = gluNewQuadric()
    gluQuadricTexture(Sphere, GL_TRUE)
    gluSphere(Sphere, 0.75, 80, 80)
    glPopMatrix()
    glEndList()

    glGenLists(1)
    glNewList(3, GL_COMPILE)  # Black Marble
    glColor3f(0.20, 0.09, 0.39)
    glPushMatrix()
    glScalef(1.0, 0.5, 1.0)
    Sphere = gluNewQuadric()
    gluQuadricTexture(Sphere, GL_TRUE)
    gluSphere(Sphere, 0.75, 80, 80)
    glPopMatrix()
    glEndList()

    glGenLists(1)
    glNewList(4, GL_COMPILE)  # Select
    glColor3f(0.20, 0.09, 0.09)
    glBegin(GL_QUADS)
    glVertex3f(-2.175, 0.0, -2.175)
    glVertex3f(2.175, 0.0, -2.175)
    glVertex3f(2.175, 0.0, 2.175)
    glVertex3f(-2.175, 0.0, 2.175)
    glEnd();
    glEndList()

    glGenLists(1)
    glNewList(5, GL_COMPILE)
    glColor3f(0.20, 0.09, 0.09)
    glBegin(GL_QUADS)
    # TOP
    glVertex3f(-0.5, 1.0, -0.5)
    glVertex3f(0.5, 1.0, -0.5)
    glVertex3f(0.5, 1.0, 0.5)
    glVertex3f(-0.5, 1.0, 0.5)
    # SIDES
    # Left Side
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 1.0, -0.5)
    glVertex3f(-0.5, 1.0, 0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    # Right Side
    glVertex3f(0.5, 0.0, -0.5)
    glVertex3f(0.5, 1.0, -0.5)
    glVertex3f(0.5, 1.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    # Bottom Side
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(-0.5, 1.0, 0.5)
    glVertex3f(0.5, 1.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    # Top Side
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 1.0, -0.5)
    glVertex3f(0.5, 1.0, -0.5)
    glVertex3f(0.5, 0.0, -0.5)
    # BOTTOM
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glEnd();
    glEndList()


