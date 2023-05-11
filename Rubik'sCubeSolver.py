import tkinter as tk
from tkinter.font import BOLD
from tkinter import *   # Library For GUI
from random import randint 

# Declaring Arrays To Store In It 
MovesLST = []
LastScramb = []
F2LLST = []
StepsMovingLST = []
SolLength = 0

def CubeMake():     # creates a 3d LST representing a solved cube    //Ahmed
    global StepsMovingLST, F2LLST, MovesLST
    StepsMovingLST = [0, 0, 0, 0]
    F2LLST = []
    MovesLST = []
    colors= [[['W', 'W', 'W'],
             ['W', 'W', 'W'],
             ['W', 'W', 'W']],  # Upper Face --> White

            [['G', 'G', 'G'],
             ['G', 'G', 'G'],
             ['G', 'G', 'G']],  # Front Face --> Green

            [['R', 'R', 'R'],
             ['R', 'R', 'R'],
             ['R', 'R', 'R']],  # Right Face --> Red

            [['O', 'O', 'O'],
             ['O', 'O', 'O'],
             ['O', 'O', 'O']],  # Left Face --> Orange

            [['Y', 'Y', 'Y'],
             ['Y', 'Y', 'Y'],
             ['Y', 'Y', 'Y']],  # Down Face --> Yellow

            [['B', 'B', 'B'],
             ['B', 'B', 'B'],
             ['B', 'B', 'B']]]  # Back Face --> Blue

    return colors

cube = CubeMake()

def GetMoves():     # Returns A String Of Moves After Simplifying it    //Ahmed
    SimplifyMoves()
    s = ""
    for i in MovesLST:
        s += str(i) + " "
    s = str.replace(s, "i", "'")[:-1]
    return s

def GetScramb():    # Returns A string Of The Last Scramble  //Ahmed
    s = ""
    for i in LastScramb:
        s += str(i) + " "
    s = str.replace(s, "i", "'")[:-1]
    return s

def TransY(move):   # Transforms a given move into the corresponding move after a Y-rotation    //Ahmed
    if move[0] in ["U", "D"]:
        return move
    if move[0] == "F":
        return "R" + move[1:]
    if move[0] == "R":
        return "B" + move[1:]
    if move[0] == "B":
        return "L" + move[1:]
    if move[0] == "L":
        return "F" + move[1:]
    raise Exception("Invalid move to TransY: " + move)

def SimplifyMoves():    # Simplifies the moves LST by removing redundancies    //Ahmed
    global MovesLST, SolLength
    NewLst = []
    PreviousMove = ""
    YCounter = 0
    for move in MovesLST:
        if move == "Y":
            YCounter += 1
            YCounter %= 4
            continue
        if move == "Yi":
            YCounter += 3
            YCounter %= 4
            continue
        if move == "Y2":
            YCounter += 2
            YCounter %= 4
            continue
        if YCounter > 0:
            for i in range(YCounter):
                move = TransY(move)
        if PreviousMove == "" or PreviousMove == '':
            PreviousMove = move
            NewLst.append(move)
            continue
        if move[0] == PreviousMove[0]:
            if len(move) == 1:
                if len(PreviousMove) <= 1:
                    del NewLst[-1]
                    mv = move[0] + "2"
                    NewLst.append(mv)
                    PreviousMove = mv
                    continue
                if PreviousMove[1] == "i":
                    del NewLst[-1]
                    PreviousMove = NewLst[-1] if len(NewLst) > 0 else ""
                    continue
                if PreviousMove[1] == "2":
                    del NewLst[-1]
                    mv = move[0] + "i"
                    NewLst.append(mv)
                    PreviousMove = mv
                    continue
            if move[1] == "i":
                if len(PreviousMove) == 1:
                    del NewLst[-1]
                    PreviousMove = NewLst[-1] if len(NewLst) > 0 else ""
                    continue
                if PreviousMove[1] == "i":
                    del NewLst[-1]
                    mv = move[0] + "2"
                    NewLst.append(mv)
                    PreviousMove = mv
                    continue
                if PreviousMove[1] == "2":
                    del NewLst[-1]
                    mv = move[0]
                    NewLst.append(mv)
                    PreviousMove = mv
                    continue
            if move[1] == "2":
                if len(PreviousMove) == 1:
                    del NewLst[-1]
                    mv = move[0] + "i"
                    NewLst.append(mv)
                    PreviousMove = mv
                    continue
                if PreviousMove[1] == "i":
                    del NewLst[-1]
                    mv = move[0]
                    NewLst.append(mv)
                    PreviousMove = mv
                    continue
                if PreviousMove[1] == "2":
                    del NewLst[-1]
                    PreviousMove = NewLst[-1] if len(NewLst) > 0 else ""
                    continue
        NewLst.append(move)
        PreviousMove = move
    SolLength = len(NewLst)
    MovesLST = NewLst

def setup(face):    # sets up the cube to perform a move by rotating that face to the top   //Ahmed
    face = str.lower(face)
    if face == "f":
        move("X")
    elif face == "r":
        move("Zi")
    elif face == "l":
        move("Z")
    elif face == "d":
        move("X2")
    elif face == "b":
        move("Xi")
    else:
        raise Exception("Invalid setup; face: " + face)

def undo(face):  # performs the inverse of setup to restore the cube's previous orientation  //Ahmed
    face = str.lower(face)
    if face == "f":
        move("Xi")
    elif face == "r":
        move("Z")
    elif face == "l":
        move("Zi")
    elif face == "d":
        move("X2")
    elif face == "b":
        move("X")
    else:
        raise Exception("Invalid undo; face: " + face)


# Tokenizes a string of moves
def m(s):
    s = str.replace(s, "'", "i")
    k = s.split(' ')
    global MovesLST, SolLength
    SolLength += len(k)
    for word in k:
        MovesLST.append(word)
        move(word)


# performs a move by setting up, performing U moves, and undoing the setup  //Ahmed
def move(mv):
    mv = str.lower(mv)
    if mv == "u":
        UMov()
    elif mv == "u2":
        move("U");
        move("U");
    elif mv == "ui":
        move("U");
        move("U");
        move("U");
    elif mv == "f":
        setup("F");
        UMov();
        undo("F");
    elif mv == "f2":
        move("F");
        move("F");
    elif mv == "fi":
        move("F");
        move("F");
        move("F");
    elif mv == "r":
        setup("R");
        UMov();
        undo("R");
    elif mv == "r2":
        move("R");
        move("R");
    elif mv == "ri":
        move("R");
        move("R");
        move("R");
    elif mv == "l":
        setup("L");
        UMov();
        undo("L");
    elif mv == "l2":
        move("L");
        move("L");
    elif mv == "li":
        move("L");
        move("L");
        move("L");
    elif mv == "b":
        setup("B");
        UMov();
        undo("B");
    elif mv == "b2":
        move("B");
        move("B");
    elif mv == "bi":
        move("B");
        move("B");
        move("B");
    elif mv == "d":
        setup("D");
        UMov();
        undo("D");
    elif mv == "d2":
        move("D");
        move("D");
    elif mv == "di":
        move("D");
        move("D");
        move("D");
    elif mv == "x":
        Rot("X")
    elif mv == "x2":
        move("X");
        move("X");
    elif mv == "xi":
        move("X");
        move("X");
        move("X");
    elif mv == "y":
        Rot("Y")
    elif mv == "y2":
        move("Y");
        move("Y");
    elif mv == "yi":
        move("Y");
        move("Y");
        move("Y");
    elif mv == "z":
        Rot("Z")
    elif mv == "z2":
        move("Z");
        move("Z");
    elif mv == "zi":
        move("Z");
        move("Z");
        move("Z");
    elif mv == "uw":
        move("D");
        move("Y");
    elif mv == "uw2":
        move("UW");
        move("UW");
    elif mv == "uwi":
        move("UW");
        move("UW");
        move("UW");
    elif mv == "m":
        move("Li");
        move("R");
        move("Xi");
    elif mv == "mi":
        move("M");
        move("M");
        move("M");
    elif mv == "m2":
        move("M");
        move("M");
    elif mv == "rw":
        move("L");
        move("X");
    elif mv == "rwi":
        move("RW");
        move("RW");
        move("RW");
    elif mv == "rw2":
        move("RW");
        move("RW");
    elif mv == "fw":
        move("Bi");
        move("Z");
    elif mv == "fwi":
        move("FW");
        move("FW");
        move("FW");
    elif mv == "fw2":
        move("FW");
        move("FW");
    elif mv == "lw":
        move("R");
        move("Xi");
    elif mv == "lwi":
        move("LW");
        move("LW");
        move("LW");
    elif mv == "lw2":
        move("LW");
        move("LW");
    elif mv == "bw":
        move("F");
        move("Zi");
    elif mv == "bwi":
        move("BW");
        move("BW");
        move("BW");
    elif mv == "bw2":
        move("BW");
        move("BW");
    elif mv == "dw":
        move("U");
        move("Yi");
    elif mv == "dwi":
        move("DW");
        move("DW");
        move("DW");
    elif mv == "dw2":
        move("DW");
        move("DW");
    else:
        raise Exception("Invalid Move: " + str(mv))

def Rot(axis):  # Rotates The Cube along the axis   //Ahmed
    axis = str.lower(axis)
    if axis == 'x':  # R
        temp = cube[0]
        cube[0] = cube[1]
        cube[1] = cube[4]
        cube[4] = cube[5]
        cube[5] = temp
        RotFaceCounterClockWise("L")
        RotFaceClockWise("R")
    elif axis == 'y':  # U
        temp = cube[1]
        cube[1] = cube[2]
        cube[2] = cube[5]
        cube[5] = cube[3]
        cube[3] = temp
        # after swaps,
        RotFaceClockWise("L")
        RotFaceClockWise("F")
        RotFaceClockWise("R")
        RotFaceClockWise("B")
        RotFaceClockWise("U")
        RotFaceCounterClockWise("D")
    elif axis == 'z':  # F
        temp = cube[0]
        cube[0] = cube[3]
        cube[3] = cube[4]
        cube[4] = cube[2]
        cube[2] = temp
        RotFaceClockWise("L");
        RotFaceClockWise("L");
        RotFaceClockWise("D");
        RotFaceClockWise("D");
        RotFaceClockWise("F")
        RotFaceCounterClockWise("B")
    else:
        raise Exception("Invalid rotation: " + axis)

def UMov():    # performs a U move     //Ahmed
    # rotate U face
    temp = cube[0][0][0]
    cube[0][0][0] = cube[0][2][0]
    cube[0][2][0] = cube[0][2][2]
    cube[0][2][2] = cube[0][0][2]
    cube[0][0][2] = temp
    temp = cube[0][0][1]
    cube[0][0][1] = cube[0][1][0]
    cube[0][1][0] = cube[0][2][1]
    cube[0][2][1] = cube[0][1][2]
    cube[0][1][2] = temp

    # rotate others
    temp = cube[5][2][0]
    cube[5][2][0] = cube[3][2][2]
    cube[3][2][2] = cube[1][0][2]
    cube[1][0][2] = cube[2][0][0]
    cube[2][0][0] = temp
    temp = cube[5][2][1]
    cube[5][2][1] = cube[3][1][2]
    cube[3][1][2] = cube[1][0][1]
    cube[1][0][1] = cube[2][1][0]
    cube[2][1][0] = temp
    temp = cube[5][2][2]
    cube[5][2][2] = cube[3][0][2]
    cube[3][0][2] = cube[1][0][0]
    cube[1][0][0] = cube[2][2][0]
    cube[2][2][0] = temp


# Rotates a particular face counter-clockwise   //Ahmed
def RotFaceCounterClockWise(face):
    RotFaceClockWise(face)
    RotFaceClockWise(face)
    RotFaceClockWise(face)


# Rotates a particular face clockwise   //Ahmed
def RotFaceClockWise(face):
    f_id = -1
    face = str.lower(face)
    if face == "u":
        f_id = 0
    elif face == "f":
        f_id = 1
    elif face == "r":
        f_id = 2
    elif face == "l":
        f_id = 3
    elif face == "d":
        f_id = 4
    elif face == "b":
        f_id = 5
    else:
        raise Exception("Invalid face: " + face)
    temp = cube[f_id][0][0]
    cube[f_id][0][0] = cube[f_id][2][0]
    cube[f_id][2][0] = cube[f_id][2][2]
    cube[f_id][2][2] = cube[f_id][0][2]
    cube[f_id][0][2] = temp
    temp = cube[f_id][0][1]
    cube[f_id][0][1] = cube[f_id][1][0]
    cube[f_id][1][0] = cube[f_id][2][1]
    cube[f_id][2][1] = cube[f_id][1][2]
    cube[f_id][1][2] = temp



def scramble(moves=25):     # Scrambles The Cube Randomly Within A given Number Or LST of moves   //Ahmed
    global LastScramb, MovesLST, SolLength, cube
    cube = CubeMake()
    if hasattr(moves, '__iter__'):  # scramble given a LST of moves
        m(moves)
        MovesLST = []
        SolLength = 0
        temp = moves.split(' ')
        LastScramb = temp
    else:  # scramble randomly a certain number of times
        MovesLST = []  # reset MovesLST
        LastScramb = []  # reset last scramble
        prevMove = ""
        for i in range(moves):
            while True:
                CurrentMove = ""
                r = randint(0, 5)
                if r == 0:
                    CurrentMove += "U"
                elif r == 1:
                    CurrentMove += "F"
                elif r == 2:
                    CurrentMove += "R"
                elif r == 3:
                    CurrentMove += "L"
                elif r == 4:
                    CurrentMove += "D"
                elif r == 5:
                    CurrentMove += "B"
                if CurrentMove == "U" and prevMove != "U" and prevMove != "D":
                    break
                if CurrentMove == "F" and prevMove != "F" and prevMove != "B":
                    break
                if CurrentMove == "R" and prevMove != "R" and prevMove != "L":
                    break
                if CurrentMove == "L" and prevMove != "L" and prevMove != "R":
                    break
                if CurrentMove == "D" and prevMove != "D" and prevMove != "U":
                    break
                if CurrentMove == "B" and prevMove != "B" and prevMove != "F":
                    break
            r = randint(0, 3)
            if r == 1:
                move(CurrentMove + "i")
                LastScramb.append(CurrentMove + "i")
            elif r == 2:
                move(CurrentMove + "2")
                LastScramb.append(CurrentMove + "2")
            else:
                move(CurrentMove)
                LastScramb.append(CurrentMove)
            prevMove = CurrentMove



def CrossTop():     # Solves the top cross as part of the OLL step  //Malek
    # if all the edges are all equal to eachother (all being white)
    if cube[0][0][1] == cube[0][1][0] == cube[0][1][2] == cube[0][2][1]:
        
        return
    # If this is true, we have our cross and we can go onto the next step
    else:
        while cube[0][0][1] != "W" or cube[0][1][0] != "W" or cube[0][1][2] != "W" or cube[0][2][1] != "W":
            if cube[0][1][0] == cube[0][1][2]:
                # if we have a horizontal line Just do alg
                m("F R U Ri Ui Fi")
                break  # breaking w/o having to recheck while conditions again, this will give us a cross
            elif cube[0][0][1] == cube[0][2][1]:
                # if we have a vertical line, do a U then alg
                m("U F R U Ri Ui Fi")
                break
            elif cube[0][0][1] != "W" and cube[0][1][0] != "W" and cube[0][1][2] != "W" and cube[0][2][1] != "W":
                # This would mean we have a dot case, so perform
                m("F U R Ui Ri Fi U F R U Ri Ui Fi")
                break
            elif cube[0][1][2] == cube[0][2][1] or cube[0][0][1] == cube[0][1][0]:
                # If we have an L case in the top left or the bottom right, will give us a line
                m("F R U Ri Ui Fi")
            else:
                # This is we dont have a line, dot, cross, or L in top left or bottom right
                m("U")



def isTopSolved():  # returns True if the top is solved  //Malek
    # determines if the top of the cube is solved.
    if cube[0][0][0] == cube[0][0][1] == cube[0][0][2] == cube[0][1][0] == cube[0][1][1] == cube[0][1][2] == cube[0][2][0] == cube[0][2][1] == \
            cube[0][2][2]:
        return True
    else:
        return False


# puts a single edge piece in the proper location for the cross
# Assumes the cross is formed on the bottom and is the yellow face
# Checks all edges in front/up face, then back-right/left if needed     //Malek
def putCrossEdge():
    global MovesLST
    for i in range(3):
        if i == 1:
            m("Ri U R F2")  # bring out back-right edge
        elif i == 2:
            m("L Ui Li F2")  # bring out back-left edge
        for j in range(4):
            for k in range(4):
                if "Y" in [cube[4][0][1], cube[1][2][1]]:
                    return
                m("F")
            m("U")



def cross():    # The Solution First Step  //Malek
    for i in range(4):
        putCrossEdge()
        assert "Y" in [cube[4][0][1], cube[1][2][1]]
        if cube[1][2][1] == "Y":
            m("Fi R U Ri F2")  # orient if necessary
        m("Di")

    # permute to correct face: move down face until 2 are lined up,
    # then swap the other 2 if they need to be swapped  
    condition = False
    while not condition:
        fSame = cube[1][1][1] == cube[1][2][1]
        rSame = cube[2][1][1] == cube[2][1][2]
        bSame = cube[5][1][1] == cube[5][0][1]
        lSame = cube[3][1][1] == cube[3][1][0]
        condition = (fSame, rSame, bSame, lSame).count(True) >= 2
        if not condition:
            m("D")
    if (fSame, rSame, bSame, lSame).count(True) == 4:
        return
    assert (fSame, rSame, bSame, lSame).count(True) == 2
    if not fSame and not bSame:
        m("F2 U2 B2 U2 F2")  # swap front back
    elif not rSame and not lSame:
        m("R2 U2 L2 U2 R2")  # swap right left
    elif not fSame and not rSame:
        m("F2 Ui R2 U F2")  # swap front right
    elif not rSame and not bSame:
        m("R2 Ui B2 U R2")  # swap right back
    elif not bSame and not lSame:
        m("B2 Ui L2 U B2")  # swap back left
    elif not lSame and not fSame:
        m("L2 Ui F2 U L2")  # swap left front
    fSame = cube[1][1][1] == cube[1][2][1]
    rSame = cube[2][1][1] == cube[2][1][2]
    bSame = cube[5][1][1] == cube[5][0][1]
    lSame = cube[3][1][1] == cube[3][1][0]
    assert all([fSame, rSame, bSame, lSame])


# This is uses all the f2l algs to solve all the cases possible //Ahmed
def solveFrontSlot():
    # This will be F2L, with all 42 cases
    rmid = cube[2][1][1]
    fmid = cube[1][1][1]
    dmid = cube[4][1][1]
    # corner orientations if in U layer, first letter means the direction that the color is facing
    fCorU = cube[1][0][2] == dmid and cube[0][2][2] == fmid and cube[2][2][0] == rmid
    rCorU = cube[2][2][0] == dmid and cube[1][0][2] == fmid and cube[0][2][2] == rmid
    uCorU = cube[0][2][2] == dmid and cube[2][2][0] == fmid and cube[1][0][2] == rmid
    # Corner orientations for correct location in D layer
    fCorD = cube[1][2][2] == dmid and cube[2][2][2] == fmid and cube[4][0][2] == rmid
    rCorD = cube[2][2][2] == dmid and cube[4][0][2] == fmid and cube[1][2][2] == rmid
    dCorD = cube[4][0][2] == dmid and cube[1][2][2] == fmid and cube[2][2][2] == rmid  # This is solved spot
    # edge orientations on U layer, normal or flipped version based on F face
    norEdgeFU = cube[1][0][1] == fmid and cube[0][2][1] == rmid
    norEdgeLU = cube[3][1][2] == fmid and cube[0][1][0] == rmid
    norEdgeBU = cube[5][2][1] == fmid and cube[0][0][1] == rmid
    norEdgeRU = cube[2][1][0] == fmid and cube[0][1][2] == rmid
    norEdgeAny = norEdgeFU or norEdgeLU or norEdgeBU or norEdgeRU
    flipEdgeFU = cube[0][2][1] == fmid and cube[1][0][1] == rmid
    flipEdgeLU = cube[0][1][0] == fmid and cube[3][1][2] == rmid
    flipEdgeBU = cube[0][0][1] == fmid and cube[5][2][1] == rmid
    flipEdgeRU = cube[0][1][2] == fmid and cube[2][1][0] == rmid
    flipEdgeAny = flipEdgeFU or flipEdgeLU or flipEdgeBU or flipEdgeRU
    # edge orientations for normal or flipped insertion into slot
    norEdgeInsert = cube[1][1][2] == fmid and cube[2][2][1] == rmid  # This is solved spot
    flipEdgeInsert = cube[2][2][1] == fmid and cube[1][1][2] == rmid
    # these are for if the back right or front left slots are open or not
    backRight = cube[4][2][2] == dmid and cube[5][1][2] == cube[5][0][2] == cube[5][1][1] and cube[2][0][1] == cube[2][0][2] == rmid
    frontLeft = cube[4][0][0] == dmid and cube[1][1][0] == cube[1][2][0] == fmid and cube[3][2][0] == cube[3][2][1] == cube[3][1][1]

    if dCorD and norEdgeInsert:
        return
    # Cases
    elif fCorU and flipEdgeRU: 
        m("U R Ui Ri")
    elif rCorU and norEdgeFU:  
        m("F Ri Fi R")
    elif fCorU and norEdgeLU:  
        m("Fi Ui F")
    elif rCorU and flipEdgeBU: 
        m("R U Ri")
    # Reposition Edge
    elif fCorU and flipEdgeBU: 
        m("F2 Li Ui L U F2")
    elif rCorU and norEdgeLU:  
        m("R2 B U Bi Ui R2")
    elif fCorU and flipEdgeLU:  
        m("Ui R U2 Ri U2 R Ui Ri")
    elif rCorU and norEdgeBU:  
        m("U Fi U2 F Ui F Ri Fi R")
    # Reposition edge and Corner Flip
    elif fCorU and norEdgeBU: 
        m("Ui R Ui Ri U Fi Ui F")
    elif rCorU and flipEdgeLU:  
        if not backRight:
            m("Ri U R2 U Ri")
        else:
            m("Ui R U Ri U R U Ri")
    elif fCorU and norEdgeRU: 
        m("Ui R U2 Ri U Fi Ui F")
    elif rCorU and flipEdgeFU:  
        if not backRight:
            m("Ri U2 R2 U Ri")
        else:
            m("Ri U2 R2 U R2 U R")
    elif fCorU and norEdgeFU:  
        if not backRight:
            m("Ri U R Fi Ui F")
        else:
            m("U Fi U F Ui Fi Ui F")
    elif rCorU and flipEdgeRU: 
        m("Ui R Ui Ri U R U Ri")
    # Split Pair by Going Over
    elif fCorU and flipEdgeFU:  
        if not backRight:
            m("Ui Ri U R Ui R U Ri")
        elif not frontLeft:
            m("U R Ui Ri D R Ui Ri Di")
        else:
            m("U Ri F R Fi U R U Ri")
    elif rCorU and norEdgeRU:  
        m("R Ui Ri U2 Fi Ui F")
    elif uCorU and flipEdgeRU: 
        m("R U2 Ri Ui R U Ri")
    elif uCorU and norEdgeFU:  
        m("Fi U2 F U Fi Ui F")
    # Pair made on side
    elif uCorU and flipEdgeBU: 
        m("U R U2 R2 F R Fi")
    elif uCorU and norEdgeLU:  
        m("Ui Fi U2 F2 Ri Fi R")
    elif uCorU and flipEdgeLU:  
        m("R B U2 Bi Ri")
    elif uCorU and norEdgeBU:  
        m("Fi Li U2 L F")
    # Weird Cases
    elif uCorU and flipEdgeFU: 
        m("U2 R2 U2 Ri Ui R Ui R2")
    elif uCorU and norEdgeRU:  
        m("U Fi Li U L F R U Ri")
    # Corner in Place, edge in the U face (All these cases also have set-up moves in case the edge is in the wrong orientation
    elif dCorD and flipEdgeAny:  
        if flipEdgeBU:
            m("U")  
        elif flipEdgeLU:
            m("U2")  
        elif flipEdgeFU:
            m("Ui")  
        if not backRight:
            m("R2 Ui Ri U R2")
        else:
            m("Ri Fi R U R Ui Ri F")
    elif dCorD and norEdgeAny:  
        if norEdgeRU:
            m("U")  
        elif norEdgeBU:
            m("U2")  
        elif norEdgeLU:
            m("Ui")  
        m("U R Ui Ri F Ri Fi R")
    elif fCorD and flipEdgeAny:  
        if flipEdgeBU:
            m("U")  
        elif flipEdgeLU:
            m("U2")  
        elif flipEdgeFU:
            m("Ui")  
        m("R Ui Ri U R Ui Ri")
    elif rCorD and norEdgeAny:  
        if norEdgeRU:
            m("U")  
        elif norEdgeBU:
            m("U2")  
        elif norEdgeLU:
            m("Ui")  
        m("R U Ri Ui F Ri Fi R")
    elif fCorD and norEdgeAny: 
        if norEdgeRU:
            m("U")  
        elif norEdgeBU:
            m("U2")  
        elif norEdgeLU:
            m("Ui")  
        m("U2 R Ui Ri Fi Ui F")
    elif rCorD and flipEdgeAny:  
        if flipEdgeBU:
            m("U")  
        elif flipEdgeLU:
            m("U2")  
        elif flipEdgeFU:
            m("Ui")  
        m("R U Ri Ui R U Ri")
    # Edge in place, corner in U Face
    elif uCorU and flipEdgeInsert:  
        m("R U2 Ri Ui F Ri Fi R")
    elif uCorU and norEdgeInsert:  
        m("R2 U R2 U R2 U2 R2")
    elif fCorU and norEdgeInsert: 
        m("Ui R Ui Ri U2 R Ui Ri")
    elif rCorU and norEdgeInsert: 
        m("Ui R U2 Ri U R U Ri")
    elif fCorU and flipEdgeInsert:  
        m("U2 R Ui Ri Ui Fi Ui F")
    elif rCorU and flipEdgeInsert:  
        m("U Fi Ui F Ui R U Ri")
    elif dCorD and flipEdgeInsert:  
        m("R2 U2 F R2 Fi U2 Ri U Ri")
    elif fCorD and norEdgeInsert:  
        m("R2 U2 Ri Ui R Ui Ri U2 Ri")
    elif rCorD and norEdgeInsert:  
        m("R U2 R U Ri U R U2 R2")
    elif fCorD and flipEdgeInsert:  
        m("F2 Li Ui L U F Ui F")
    elif rCorD and flipEdgeInsert: 
        m("R Ui Ri Fi Li U2 L F")


# Returns true if the f2l Corner in FR spot is inserted and oriented correctly
def f2lCorner():
    return cube[4][0][2] == cube[4][1][1] and cube[1][2][2] == cube[1][1][1] and cube[2][2][2] == cube[2][1][1]  # This is solved spot


# Returns true if the f2l edge in FR spot is inserted and oriented correctly
def f2lEdge():
    return cube[1][1][2] == cube[1][1][1] and cube[2][2][1] == cube[2][1][1]  # This is solved spot


# Returns true if the f2l edge and corner are properly inserted and orientated in the FR position
def f2lCorrect():
    return f2lCorner() and f2lEdge()



def f2lEdgeOnTop(): # returns if the f2l edge is on the top layer at all  //Ahmed
    rmid = cube[2][1][1]
    fmid = cube[1][1][1]
    dmid = cube[4][1][1]
    # edge orientations on U layer, normal or flipped version based on F face
    norEdgeFU = cube[1][0][1] == fmid and cube[0][2][1] == rmid
    norEdgeLU = cube[3][1][2] == fmid and cube[0][1][0] == rmid
    norEdgeBU = cube[5][2][1] == fmid and cube[0][0][1] == rmid
    norEdgeRU = cube[2][1][0] == fmid and cube[0][1][2] == rmid
    norEdgeAny = norEdgeFU or norEdgeLU or norEdgeBU or norEdgeRU
    flipEdgeFU = cube[0][2][1] == fmid and cube[1][0][1] == rmid
    flipEdgeLU = cube[0][1][0] == fmid and cube[3][1][2] == rmid
    flipEdgeBU = cube[0][0][1] == fmid and cube[5][2][1] == rmid
    flipEdgeRU = cube[0][1][2] == fmid and cube[2][1][0] == rmid
    flipEdgeAny = flipEdgeFU or flipEdgeLU or flipEdgeBU or flipEdgeRU
    return norEdgeAny or flipEdgeAny


# returns true if the f2l edge is inserted. Can be properly orientated, or flipped. // Ahmed
def f2lEdgeInserted():
    rmid = cube[2][1][1]
    fmid = cube[1][1][1]
    # edge orientations for normal or flipped insertion into slot
    norEdgeInsert = cube[1][1][2] == fmid and cube[2][2][1] == rmid  # This is solved spot
    flipEdgeInsert = cube[2][2][1] == fmid and cube[1][1][2] == rmid
    return norEdgeInsert or flipEdgeInsert


# This is used to determine if the front f2l edge is inserted or not, the parameter is for the requested edge. takes BR, BL, and FL as valid    //Ahmed
def f2lEdgeInserted2(p):
    rmid = cube[2][1][1]
    fmid = cube[1][1][1]
    # edge orientations for normal or flipped insertion into slot
    norEdgeInsert = cube[1][1][2] == fmid and cube[2][2][1] == rmid  # This is solved spot
    flipEdgeInsert = cube[2][2][1] == fmid and cube[1][1][2] == rmid
    # Edge orientations in comparison to Front and Right colors
    BR = (cube[5][1][2] == fmid and cube[2][0][1] == rmid) or (cube[5][1][2] == rmid and cube[2][0][1] == fmid)
    BL = (cube[3][0][1] == fmid and cube[5][1][0] == rmid) or (cube[3][0][1] == rmid and cube[5][1][0] == fmid)
    FL = (cube[3][2][1] == fmid and cube[1][1][0] == rmid) or (cube[3][2][1] == rmid and cube[1][1][0] == fmid)

    if p == "BR":
        if BR:
            return True
        else:
            return False
    elif p == "BL":
        if BL:
            return True
        return False
    elif p == "FL":
        if FL:
            return True
        return False
    elif p == "FR":
        if norEdgeInsert or flipEdgeInsert:
            return True
    return False


# returns true if f2l corner is inserted, doesn't have to be orientated correctly   //Ahmed
def f2lCornerInserted():
    rmid = cube[2][1][1]
    fmid = cube[1][1][1]
    dmid = cube[4][1][1]
    # Corner orientations for correct location in D layer
    fCorD = cube[1][2][2] == dmid and cube[2][2][2] == fmid and cube[4][0][2] == rmid
    rCorD = cube[2][2][2] == dmid and cube[4][0][2] == fmid and cube[1][2][2] == rmid
    dCorD = cube[4][0][2] == dmid and cube[1][2][2] == fmid and cube[2][2][2] == rmid  # This is solved spot
    return fCorD or rCorD or dCorD


# Returns true if there is an f2l corner located in the FR orientation  //Ahmed
def f2lFRCor():
    rmid = cube[2][1][1]
    fmid = cube[1][1][1]
    dmid = cube[4][1][1]
    # corner orientations if in U layer, first letter means the direction that the color is facing
    fCorU = cube[1][0][2] == dmid and cube[0][2][2] == fmid and cube[2][2][0] == rmid
    rCorU = cube[2][2][0] == dmid and cube[1][0][2] == fmid and cube[0][2][2] == rmid
    uCorU = cube[0][2][2] == dmid and cube[2][2][0] == fmid and cube[1][0][2] == rmid
    return fCorU or rCorU or uCorU


# Returns true if there is an f2l Edge located in the FU position   //Ahmed
def f2lFUEdge():
    rmid = cube[2][1][1]
    fmid = cube[1][1][1]
    norEdgeFU = cube[1][0][1] == fmid and cube[0][2][1] == rmid
    flipEdgeFU = cube[0][2][1] == fmid and cube[1][0][1] == rmid
    return norEdgeFU or flipEdgeFU


# returns true if f2l corner is located on the U layer  //Ahmed
def f2lCornerOnTop():
    wasFound = False
    for i in range(4):  # Does 4 U moves to find the corner
        if f2lFRCor():
            wasFound = True
        m("U")
    return wasFound


# Will return the loction of the corner that belongs in the FR spot. Either returns BR, BL, FL, or FR.  //Malek
def f2lCornerCheck():   
    r = "FR"
    count = 0
    while count < 4:
        if count == 0:
            if f2lCornerInserted():
                r = "FR"
        elif count == 1:
            if f2lCornerInserted():
                r = "FL"
        elif count == 2:
            if f2lCornerInserted():
                r = "BL"
        elif count == 3:
            if f2lCornerInserted():
                r = "BR"
        m("D")
        count += 1
    return r



def f2lEdgeCheck():     # Returns The Location Of The Edge That Belongs in FR Spot      //Ahmed
    if f2lEdgeInserted2("FL"):
        return "FL"
    elif f2lEdgeInserted2("BL"):
        return "BL"
    elif f2lEdgeInserted2("BR"):
        return "BR"
    elif f2lEdgeInserted2("FR"):
        return "FR"
    else:
        raise Exception("f2lEdgeCheck() Exception")


# This is for the case where the Edge is inserted, but the corner is not        //Ahmed
def f2lEdgeNoCorner():
    topEdgeTop = cube[0][2][1]
    topEdgeFront = cube[1][0][1]
    rmid = cube[2][1][1]
    bmid = cube[5][1][1]
    lmid = cube[3][1][1]
    fmid = cube[1][1][1]
    # This is for comparing the front edge to other various edges for advanced algs/lookahead
    BREdge = (topEdgeTop == rmid or topEdgeTop == bmid) and (topEdgeFront == rmid or topEdgeFront == bmid)
    BLEdge = (topEdgeTop == lmid or topEdgeTop == bmid) and (topEdgeFront == lmid or topEdgeFront == bmid)
    FLEdge = (topEdgeTop == fmid or topEdgeTop == lmid) and (topEdgeFront == fmid or topEdgeFront == lmid)
    if f2lCornerOnTop():
        while True:
            solveFrontSlot()
            if f2lCorrect():
                break
            m("U")
    else:
        if f2lCornerCheck() == "BR":
            if BREdge:
                m("Ri Ui R U2")
            else:
                m("Ri U R U")
        elif f2lCornerCheck() == "BL":
            if BLEdge:
                m("L U Li U")
            else:
                m("L Ui Li U2")
        elif f2lCornerCheck() == "FL":
            if FLEdge:
                m("Li U L Ui")
            else:
                m("Li Ui L")
    solveFrontSlot()

    if not f2lCorrect():
        raise Exception("Exception found in f2lEdgeNoCorner()")


# This is the case for if the corner is inserted, but the edge is not       //Ahmed
def f2lCornerNoEdge():
    topEdgeTop = cube[0][2][1]
    topEdgeFront = cube[1][0][1]
    rmid = cube[2][1][1]
    bmid = cube[5][1][1]
    lmid = cube[3][1][1]
    fmid = cube[1][1][1]
    # This is for comparing the front edge to other various edges for advanced algs/lookahead
    BREdge = (topEdgeTop == rmid or topEdgeTop == bmid) and (topEdgeFront == rmid or topEdgeFront == bmid)
    BLEdge = (topEdgeTop == lmid or topEdgeTop == bmid) and (topEdgeFront == lmid or topEdgeFront == bmid)
    FLEdge = (topEdgeTop == fmid or topEdgeTop == lmid) and (topEdgeFront == fmid or topEdgeFront == lmid)
    if f2lEdgeOnTop():
        while True:
            solveFrontSlot()
            if f2lCorrect():
                break
            m("U")
    else:
        if f2lEdgeCheck() == "BR":
            if BREdge:
                m("Ri Ui R U2")
            else:
                m("Ri U R U")
        elif f2lEdgeCheck() == "BL":
            if BLEdge:
                m("L U Li U")
            else:
                m("L Ui Li U2")
        elif f2lEdgeCheck() == "FL":
            if FLEdge:
                m("Li U L Ui")
            else:
                m("Li Ui L")
    solveFrontSlot()

    if not f2lCorrect():
        raise Exception("Exception found in f2lCornerNoEdge()")


# this is the case for if the corner is on top, and the edge is not. Neither are inserted properly. Edge must be in another slot.   //Ahmed
def f2lCornerTopNoEdge():
    topEdgeTop = cube[0][2][1]
    topEdgeFront = cube[1][0][1]
    rmid = cube[2][1][1]
    bmid = cube[5][1][1]
    lmid = cube[3][1][1]
    fmid = cube[1][1][1]
    # This is for comparing the front edge to other various edges for advanced algs/lookahead
    BREdge = (topEdgeTop == rmid or topEdgeTop == bmid) and (topEdgeFront == rmid or topEdgeFront == bmid)
    BLEdge = (topEdgeTop == lmid or topEdgeTop == bmid) and (topEdgeFront == lmid or topEdgeFront == bmid)
    FLEdge = (topEdgeTop == fmid or topEdgeTop == lmid) and (topEdgeFront == fmid or topEdgeFront == lmid)

    # Turn the top until the corner on the U face is in the proper position
    while True:
        if f2lFRCor():
            break
        m("U")
    # We will be checking additional edges to choose a more fitting alg for the sake of looking ahead
    if f2lEdgeCheck() == "BR":
        if BREdge:
            m("Ri Ui R")
        else:
            m("Ri U R")
    elif f2lEdgeCheck() == "BL":
        if BLEdge:
            m("U2 L Ui Li")
        else:
            m("L Ui Li U")
    elif f2lEdgeCheck() == "FL":
        if FLEdge:
            m("U2 Li Ui L U2")
        else:
            m("Li Ui L U")
    solveFrontSlot()

    if not f2lCorrect():
        raise Exception("Exception found in f2lCornerTopNoEdge()")


# This is the case for if the edge is on top, and the corner is not. Neither are inserted properly. Corner must be in another slot.
# The lookahead for this step is comparing the back edge to the slots, rather than the front one like other cases have      //Ahmed
def f2lEdgeTopNoCorner():
    BackEdgeTop = cube[0][0][1]
    BackEdgeBack = cube[5][2][1]
    rmid = cube[2][1][1]
    bmid = cube[5][1][1]
    lmid = cube[3][1][1]
    fmid = cube[1][1][1]
    rs1 = BackEdgeTop == rmid or BackEdgeTop == bmid
    rs2 = BackEdgeBack == rmid or BackEdgeBack == bmid
    # This is for comparing the back edge to other various edges for advanced algs/lookahead
    BREdge = rs1 and rs2
    BLEdge = (BackEdgeTop == lmid or BackEdgeTop == bmid) and (BackEdgeBack == lmid or BackEdgeBack == bmid)
    FLEdge = (BackEdgeTop == fmid or BackEdgeTop == lmid) and (BackEdgeBack == fmid or BackEdgeBack == lmid)

    # Turn the top until the corner on the U face is in the proper position
    while True:
        if f2lFUEdge():
            break
        m("U")
    # We will be checking additional edges to choose a more fitting alg for the sake of looking ahead
    if f2lCornerCheck() == "BR":
        if BREdge:
            m("Ri U R U")
        else:
            m("Ui Ri U R U")
    elif f2lCornerCheck() == "BL":
        if BLEdge:
            m("L Ui Li U2")
        else:
            m("U2 L U2 Li")
    elif f2lCornerCheck() == "FL":
        if FLEdge:
            m("Li Ui L")
        else:
            m("U Li Ui L")
    solveFrontSlot()

    if not f2lCorrect():
        raise Exception("Exception found in f2lEdgeTopNoCorner()")


# This is the case for if the edge or corner are not on top, and not inserted properly. They must both be in other slots.   //Malek
def f2lNoEdgeOrCorner():
    # The strategy here is to first find the corner and get it out. I will place it in the FR position where it belongs
    # I will then check if I have a case, and if we are all solved.
    # If I don't have it solved at this point, I will have to follow what happens in f2lCornerTopNoEdge()

    BackEdgeTop = cube[0][0][1]
    BackEdgeBack = cube[5][2][1]
    rmid = cube[2][1][1]
    bmid = cube[5][1][1]
    lmid = cube[3][1][1]
    fmid = cube[1][1][1]
    # This is for comparing the back edge to other various edges for advanced algs/lookahead
    BREdge = (BackEdgeTop == rmid or BackEdgeTop == bmid) and (BackEdgeBack == rmid or BackEdgeBack == bmid)
    BLEdge = (BackEdgeTop == lmid or BackEdgeTop == bmid) and (BackEdgeBack == lmid or BackEdgeBack == bmid)
    FLEdge = (BackEdgeTop == fmid or BackEdgeTop == lmid) and (BackEdgeBack == fmid or BackEdgeBack == lmid)

    # We will be checking additional edges to choose a more fitting alg for the sake of looking ahead
    if f2lCornerCheck() == "BR":
        if BREdge:
            m("Ri U R U")
        else:
            m("Ui Ri U R U")
    elif f2lCornerCheck() == "BL":
        if BLEdge:
            m("L Ui Li U2")
        else:
            m("U2 L U2 Li")
    elif f2lCornerCheck() == "FL":
        if FLEdge:
            m("Li Ui L")
        else:
            m("U Li Ui L")
    solveFrontSlot()

    if f2lCorrect():
        return
    else:
        f2lCornerTopNoEdge()

    if not f2lCorrect():
        raise Exception("Exception found in f2lNoEdgeOrCorner()")

# Will return true if the f2l is completed
def isf2lDone():
    rside = cube[2][0][1] == cube[2][0][2] == cube[2][1][1] == cube[2][1][2] == cube[2][2][1] == cube[2][2][2]
    bside = cube[5][0][0] == cube[5][0][1] == cube[5][0][2] == cube[5][1][0] == cube[5][1][1] == cube[5][1][2]
    lside = cube[3][0][0] == cube[3][0][1] == cube[3][1][0] == cube[3][1][1] == cube[3][2][0] == cube[3][2][1]
    fside = cube[1][1][0] == cube[1][1][1] == cube[1][1][2] == cube[1][2][0] == cube[1][2][1] == cube[1][2][2]
    return rside and bside and lside and fside

# f2l will solve the first 2 layers, checks for each case, then does a Y move to check the next
def f2l():
    pairsSolved = 0
    uMoves = 0
    while pairsSolved < 4:
        if not f2lCorrect():
            # while not f2lCorrect():
            while uMoves < 4:  # 4 moves before checking rare cases
                solveFrontSlot()
                if f2lCorrect():
                    pairsSolved += 1
                    F2LLST.append("Normal Case")
                    break
                else:
                    F2LLST.append("Scanning")
                    uMoves += 1
                    m("U")
            if not f2lCorrect():
                if not f2lCornerInserted() and f2lEdgeInserted():
                    F2LLST.append("Rare case 1")
                    f2lEdgeNoCorner()
                    pairsSolved += 1
                elif not f2lEdgeInserted() and f2lCornerInserted():
                    F2LLST.append("Rare case 2")
                    f2lCornerNoEdge()
                    pairsSolved += 1
                # At this point, they can't be inserted, must be in U or other spot
                elif not f2lEdgeOnTop() and f2lCornerOnTop():
                    F2LLST.append("Rare Case 3")
                    f2lCornerTopNoEdge()
                    pairsSolved += 1
                elif f2lEdgeOnTop() and not f2lCornerOnTop():
                    F2LLST.append("Rare Case 4")
                    f2lEdgeTopNoCorner()
                    solveFrontSlot()
                    pairsSolved += 1
                elif not f2lEdgeOnTop() and not f2lCornerOnTop():
                    F2LLST.append("Rare Case 5")
                    f2lNoEdgeOrCorner()
                    pairsSolved += 1
                else:
                    raise Exception("f2l Impossible Case Exception")
        else:
            pairsSolved += 1
        F2LLST.append("We have ")
        F2LLST.append(str(pairsSolved))
        uMoves = 0
        m("Y")
    assert (isf2lDone())

def fish():
    return [cube[0][0][0], cube[0][0][2], cube[0][2][0], cube[0][2][2]].count(cube[0][1][1]) == 1

def sune():
    m("R U Ri U R U2 Ri")

def antisune():
    m("R U2 Ri Ui R Ui Ri")

def getfish():  # //Malek
    for i in range(4):
        if fish():
            return
        sune()
        if fish():
            return
        antisune()
        m("U")
    assert fish()

def bOLL():  # //Malek
    getfish()
    if fish():
        while cube[0][0][2] != cube[0][1][1]:
            m("U")
        if cube[1][0][0] == cube[0][1][1]:
            antisune()
        elif cube[5][2][0] == cube[0][1][1]:
            m("U2");
            sune();
        else:
            raise Exception("Error")
    else:
        raise Exception("Failed to set up")
    assert isTopSolved()

def getCornerState():
    corner0 = cube[1][0][0] == cube[1][1][1] and cube[3][2][2] == cube[3][1][1]
    corner1 = cube[1][0][2] == cube[1][1][1] and cube[2][2][0] == cube[2][1][1]
    corner2 = cube[5][2][2] == cube[5][1][1] and cube[2][0][0] == cube[2][1][1]
    corner3 = cube[5][2][0] == cube[5][1][1] and cube[3][0][2] == cube[3][1][1]
    return [corner0, corner1, corner2, corner3]

def permuteCorners(): # Orients Top Layer Corners Properly //Malek
    for i in range(2):
        for j in range(4):
            num = getCornerState().count(True)
            if num == 4:
                return
            if num == 1:
                index = getCornerState().index(True)
                for k in range(index):
                    m("Y")
                if cube[1][0][2] == cube[2][1][1]:
                    m("R2 B2 R F Ri B2 R Fi R")
                else:
                    m("Ri F Ri B2 R Fi Ri B2 R2")
                for f in range(index):
                    m("Yi")
                return
            m("U")
        m("R2 B2 R F Ri B2 R Fi R")

def permuteEdges():  # Does permutation of the top layer edges, must be H, Z or U perms after orientation   //Malek
    if all(getEdgeState()):
        return
    if cube[1][0][1] == cube[5][1][1] and cube[5][2][1] == cube[1][1][1]:  # H perm
        m("R2 U2 R U2 R2 U2 R2 U2 R U2 R2")
    elif cube[1][0][1] == cube[2][1][1] and cube[2][1][0] == cube[1][1][1]:  # Normal Z perm
        m("U Ri Ui R Ui R U R Ui Ri U R U R2 Ui Ri U")
    elif cube[1][0][1] == cube[3][1][1] and cube[3][1][2] == cube[1][1][1]:  # Not oriented Z perm
        m("Ri Ui R Ui R U R Ui Ri U R U R2 Ui Ri U2")
    else:
        uNum = 0
        while True:
            if cube[5][2][0] == cube[5][2][1] == cube[5][2][2]:  # solid bar is on back then
                if cube[3][1][2] == cube[1][0][0]:  # means we have to do counter clockwise cycle
                    m("R Ui R U R U R Ui Ri Ui R2")
                    break
                else:
                    m("R2 U R U Ri Ui Ri Ui Ri U Ri")
                    break
            else:
                m("U")
                uNum += 1
        for x in range(uNum):
            m("Ui")


def getEdgeState():  
    fEdge = cube[1][0][1] == cube[1][1][1]
    rEdge = cube[2][1][0] == cube[2][1][1]
    bEdge = cube[5][2][1] == cube[5][1][1]
    lEdge = cube[3][1][2] == cube[3][1][1]
    return [fEdge, rEdge, bEdge, lEdge]

def bPLL(): # //Malek
    # For Corners
    permuteCorners()
    assert all(getCornerState())
    #For Edges
    permuteEdges()
    assert all(getEdgeState())


def isSolved():
    uside = cube[0][0][0] == cube[0][0][1] == cube[0][0][2] == cube[0][1][0] == cube[0][1][1] == cube[0][1][2] == cube[0][2][0] == cube[0][2][
        1] == cube[0][2][2]
    fside = cube[1][0][0] == cube[1][0][1] == cube[1][0][2] == cube[1][1][0] == cube[1][1][1] == cube[1][1][2] == cube[1][2][0] == cube[1][2][
        1] == cube[1][2][2]
    rside = cube[2][0][0] == cube[2][0][1] == cube[2][0][2] == cube[2][1][0] == cube[2][1][1] == cube[2][1][2] == cube[2][2][0] == cube[2][2][
        1] == cube[2][2][2]
    lside = cube[3][0][0] == cube[3][0][1] == cube[3][0][2] == cube[3][1][0] == cube[3][1][1] == cube[3][1][2] == cube[3][2][0] == cube[3][2][
        1] == cube[3][2][2]
    dside = cube[4][0][0] == cube[4][0][1] == cube[4][0][2] == cube[4][1][0] == cube[4][1][1] == cube[4][1][2] == cube[4][2][0] == cube[4][2][
        1] == cube[4][2][2]
    bside = cube[5][0][0] == cube[5][0][1] == cube[5][0][2] == cube[5][1][0] == cube[5][1][1] == cube[5][1][2] == cube[5][2][0] == cube[5][2][
        1] == cube[5][2][2]
    return uside and fside and rside and lside and dside and bside


def solve():
    cross()
    SimplifyMoves()
    StepsMovingLST[0] = SolLength
    f2l()
    SimplifyMoves()
    StepsMovingLST[1] = SolLength - StepsMovingLST[0]
    CrossTop()
    getfish()
    bOLL()
    SimplifyMoves()
    StepsMovingLST[2] = SolLength - StepsMovingLST[1] - StepsMovingLST[0]
    bPLL()
    SimplifyMoves()
    StepsMovingLST[3] = SolLength - StepsMovingLST[2] - StepsMovingLST[1] - StepsMovingLST[0]
    assert (isSolved())
######################################################################################################
'''                                         GUI PART                                                '''
######################################################################################################
# Globals Used In GUI
root = None
frame = None
canvas = None
ScramLBL = None
SolLBL = None
SolNoTB = None
isTransparent = None
F2LNumberLabel = None
CrossNumberLabel = None
OLLNumberLabel = None
PLLNumberLabel = None
SimulateBestLabel = None
SimulateWorstLabel = None

# cubePoints are all of the x and y coordinates for the polygons used for the tiles 
def cubePoints():
    # h and w may be changed to allow the cube to be moved around the screen
    h = 125
    w = 115
    # right face
    # layer 1
    r00p = [0 + w, 0 + h, 0 + w, 50 + h, 33 + w, 30 + h, 33 + w, -20 + h]
    r01p = [33 + w, -20 + h, 33 + w, 30 + h, 66 + w, 10 + h, 66 + w, -40 + h]
    r02p = [66 + w, -40 + h, 66 + w, 10 + h, 99 + w, -10 + h, 99 + w, -60 + h]
    # layer 2
    r10p = [0 + w, 50 + h, 0 + w, 100 + h, 33 + w, 80 + h, 33 + w, 30 + h]
    r11p = [33 + w, 30 + h, 33 + w, 80 + h, 66 + w, 60 + h, 66 + w, 10 + h]
    r12p = [66 + w, 10 + h, 66 + w, 60 + h, 99 + w, 40 + h, 99 + w, -10 + h]
    # layer 3
    r20p = [0 + w, 100 + h, 0 + w, 150 + h, 33 + w, 130 + h, 33 + w, 80 + h]
    r21p = [33 + w, 80 + h, 33 + w, 130 + h, 66 + w, 110 + h, 66 + w, 60 + h]
    r22p = [66 + w, 60 + h, 66 + w, 110 + h, 99 + w, 90 + h, 99 + w, 40 + h]
    # left face (left face will be front face, however called l face to distinguish between the left and right)
    # layer 1
    l00p = [-66 + w, -40 + h, -66 + w, 10 + h, -99 + w, -10 + h, -99 + w, -60 + h]
    l01p = [-33 + w, -20 + h, -33 + w, 30 + h, -66 + w, 10 + h, -66 + w, -40 + h]
    l02p = [0 + w, 0 + h, 0 + w, 50 + h, -33 + w, 30 + h, -33 + w, -20 + h]
    # layer 2
    l10p = [-66 + w, 10 + h, -66 + w, 60 + h, -99 + w, 40 + h, -99 + w, -10 + h]
    l11p = [-33 + w, 30 + h, -33 + w, 80 + h, -66 + w, 60 + h, -66 + w, 10 + h]
    l12p = [0 + w, 50 + h, 0 + w, 100 + h, -33 + w, 80 + h, -33 + w, 30 + h]
    # layer 3
    l20p = [-66 + w, 60 + h, -66 + w, 110 + h, -99 + w, 90 + h, -99 + w, 40 + h]
    l21p = [-33 + w, 80 + h, -33 + w, 130 + h, -66 + w, 110 + h, -66 + w, 60 + h]
    l22p = [0 + w, 100 + h, 0 + w, 150 + h, -33 + w, 130 + h, -33 + w, 80 + h]
    # up face
    # layer 1
    u00p = [0 + w, -75 + h, -33 + w, -94 + h, 0 + w, -111 + h, 33 + w, -94 + h]
    u01p = [36 + w, -57 + h, 0 + w, -75 + h, 33 + w, -94 + h, 69 + w, -76 + h]
    u02p = [66 + w, -40 + h, 36 + w, -57 + h, 69 + w, -76 + h, 99 + w, -60 + h]
    # layer 2
    u10p = [-33 + w, -57 + h, -66 + w, -77 + h, -33 + w, -94 + h, 0 + w, -75 + h]
    u11p = [0 + w, -38 + h, -33 + w, -57 + h, 0 + w, -75 + h, 36 + w, -57 + h]
    u12p = [33 + w, -20 + h, 0 + w, -38 + h, 36 + w, -57 + h, 66 + w, -40 + h]
    # layer 3
    u20p = [-66 + w, -40 + h, -99 + w, -60 + h, -66 + w, -77 + h, -33 + w, -57 + h]
    u21p = [-33 + w, -20 + h, -66 + w, -40 + h, -33 + w, -57 + h, 0 + w, -38 + h]
    u22p = [0 + w, 0 + h, -33 + w, -20 + h, 0 + w, -38 + h, 33 + w, -20 + h]

    dh = h + 200
    dw = w
    # d face
    # layer 1
    d00p = [0 + dw, -75 + dh, -33 + dw, -94 + dh, 0 + dw, -111 + dh, 33 + dw, -94 + dh]
    d01p = [36 + dw, -57 + dh, 0 + dw, -75 + dh, 33 + dw, -94 + dh, 69 + dw, -76 + dh]
    d02p = [66 + dw, -40 + dh, 36 + dw, -57 + dh, 69 + dw, -76 + dh, 99 + dw, -60 + dh]
    # layer 2
    d10p = [-33 + dw, -57 + dh, -66 + dw, -77 + dh, -33 + dw, -94 + dh, 0 + dw, -75 + dh]
    d11p = [0 + dw, -38 + dh, -33 + dw, -57 + dh, 0 + dw, -75 + dh, 36 + dw, -57 + dh]
    d12p = [33 + dw, -20 + dh, 0 + dw, -38 + dh, 36 + dw, -57 + dh, 66 + dw, -40 + dh]
    # layer 3
    d20p = [-66 + dw, -40 + dh, -99 + dw, -60 + dh, -66 + dw, -77 + dh, -33 + dw, -57 + dh]
    d21p = [-33 + dw, -20 + dh, -66 + dw, -40 + dh, -33 + dw, -57 + dh, 0 + dw, -38 + dh]
    d22p = [0 + dw, 0 + dh, -33 + dw, -20 + dh, 0 + dw, -38 + dh, 33 + dw, -20 + dh]

    cubearr = [[[u00p, u01p, u02p],
             [u10p, u11p, u12p],
             [u20p, u21p, u22p]],  # Upside

            [[l00p, l01p, l02p],
             [l10p, l11p, l12p],
             [l20p, l21p, l22p]],  # front face (used l to denote the left showing face)

            [[r02p, r12p, r22p],
             [r01p, r11p, r21p],
             [r00p, r10p, r20p]],  # right face (different than other faces because it is formatted differently)

            [[d20p, d21p, d22p],
             [d10p, d11p, d12p],
             [d00p, d01p, d02p]]]  # downside
    return cubearr

def clickCanvas(canvas):
    global isTransparent
    isTransparent = not isTransparent
    canvas.delete(ALL)
    drawCube()


# DrawCanvas will take the root and draw a new canvas, also returning it.
def drawCanvas(root):
    canvas = tk.Canvas(root, width=225, height=330, background='black')
    canvas.grid(row=0, column=0)
    canvas.bind("<Button-1>", lambda e: clickCanvas(canvas))
    return canvas


# Used to get the word for each color, used in drawCube(canvas()
def getColor(element):
    if element == 'B':
        return "#06F"  
    elif element == 'W':
        return "white"
    elif element == 'G':
        return "green"
    elif element == 'Y':
        return "yellow"
    elif element == 'O':
        return "orange"
    elif element == 'R':
        return "#D11"


# drawCube() will take the already created canvas and draw the cube with polygons whose points are defined in cubePoints()
def drawCube():
    global isTransparent, canvas
    pts = cubePoints()
    for j in range(3):
        for k in range(3):
            canvas.create_polygon(pts[3][j][k], fill=getColor(cube[4][j][k]), outline="#000", width=2)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if isTransparent:
                    frontTiles = (i == 1) and ((j == 1 and k == 2) or (j == 2 and k == 2) or (j == 2 and k == 1))
                    rightTiles = (i == 2) and ((j == 1 and k == 2) or (j == 2 and k == 2) or (j == 2 and k == 1))
                    if frontTiles or rightTiles:    # To Make the part in the face that covers the down part transparent
                        canvas.create_polygon(pts[i][j][k], fill="", outline="#000", width=2)
                    else:
                        canvas.create_polygon(pts[i][j][k], fill=getColor(cube[i][j][k]), outline="#000", width=2)
                else:
                    canvas.create_polygon(pts[i][j][k], fill=getColor(cube[i][j][k]), outline="#000", width=2)


# Used to create a new instance of a cube to be solved, changes scramble and solution labels as well
def GUInewCube():
    global canvas, ScramLBL, SolLBL, SolNoTB, cube, StepsMovingLST
    global PLLNumberLabel, F2LNumberLabel, CrossNumberLabel, OLLNumberLabel, F2LLST, MovesLST
    StepsMovingLST = [0, 0, 0, 0]
    cube = CubeMake()
    F2LLST = []
    MovesLST = []
    ScramLBL.configure(text="Scramble will be displayed here")
    SolLBL.configure(text="Solution will be displayed here")
    SolNoTB.configure(text=0)
    CrossNumberLabel.configure(text=StepsMovingLST[0])
    F2LNumberLabel.configure(text=StepsMovingLST[1])
    OLLNumberLabel.configure(text=StepsMovingLST[2])
    PLLNumberLabel.configure(text=StepsMovingLST[3])
    canvas.delete(ALL)
    drawCube()


# GUImakeMove is used to make moves based on what is in the EntryBox. After clicking Draw, it will redraw the canvas with the updated cube
def GUImakeMove(move):
    global canvas
    if move.get() == "":
        return
    m(move.get())
    canvas.delete(ALL)
    drawCube()


# GUIScramble will do a scramble of 25 on the cube, then update the canvas with the new cube
def GUIScramble():
    global ScramLBL, canvas
    scramble(25)
    ScramLBL.configure(text=GetScramb())
    canvas.delete(ALL)
    drawCube()

# GUISolve will wolve the cube using the solve function, then update the canvas with the new, solved, cube
def GUISolve():
    global canvas, SolLBL, SolNoTB, StepsMovingLST
    global PLLNumberLabel, F2LNumberLabel, CrossNumberLabel, OLLNumberLabel
    solve()
    SolLBL.configure(text=GetMoves())
    SolNoTB.configure(text=SolLength)
    CrossNumberLabel.configure(text=StepsMovingLST[0])
    F2LNumberLabel.configure(text=StepsMovingLST[1])
    OLLNumberLabel.configure(text=StepsMovingLST[2])
    PLLNumberLabel.configure(text=StepsMovingLST[3])
    canvas.delete(ALL)
    drawCube()

# This is used to copy the given string to the users clipboard
def CopyToClipBoard(word):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(word)
    r.destroy()

# This is used for the rotation of the cube with buttons. It takes in either a Yi or Y move to be executed
def GUIyRotation(given):
    global canvas
    if given == "Y" or given == "y":
        move('y')
    elif given == "Yi" or given == "Y'" or given == "yi" or given == "y'":
        move('yi')
    canvas.delete(ALL)
    drawCube()

# Function to create a welcome message with instructions to use the application
def InfoGUI():
    rt = tk.Tk()
    rt.geometry("445x107+50+50") 
    rt.wm_title("Application Start")
    rt.resizable(False, False)  
    InfoGUIy(rt)
    rt.mainloop()
    GUI()

# The instructions that will be shown in the first frame
def InfoGUIy(rt):
    frame = Frame(rt)
    frame.configure(bg="black")
    frame.grid(row=0, column=0)
    wel = "\t\tWelcome To Our Cube Solver Application, \n\tPlease Read the following instructions to can use the application:"
    i1 = "- Write the moves you want and press on the execute button to apply it on the cube"
    i2 = "- You can press on scramble button to make the cube scramble randomly"
    i3 = "- Click the solve button to solve"

    InfoLBL = Label(frame,
                      text=wel + "\n" + i1 + "\n" + i2 + "\n" + i3 ,
                      justify=LEFT, bg='black', fg='white')
    InfoLBL.grid(row=0, column=0)
    InfoQuitBTN = Button(frame, text="Let's Go", fg="black", command=lambda: rt.destroy())
    InfoQuitBTN.grid(row=1, column=0)

# Main GUI Function
def GUI():
    global root
    root = tk.Tk()
    root.configure(bg="black")
    root.geometry("590x380+50+50") 
    root.wm_title("Solver Application")
    root.resizable(False, False)  
    GUIy()
    root.mainloop()

def GUIy():
    global root, canvas, ScramLBL, SolLBL, SolNoTB, frame, isTransparent
    global PLLNumberLabel, F2LNumberLabel, CrossNumberLabel, OLLNumberLabel, SimulateBestLabel, SimulateWorstLabel

    isTransparent = False
    canvas = drawCanvas(root)
    drawCube()

    move = StringVar(value="")

    frame = Frame(root)
    frame.configure(bg="black")
    frame.grid(row=0, column=1, sticky="n")

    Rframe = Frame(root)
    Rframe.configure(bg="black")
    Rframe.grid(row=0, column=0, sticky="n")

    Welcome = Label(frame, bg="black", fg="white",font=BOLD, text="Welcome to Our Application\n").grid(row=1, column=0)
    NewCubeBTN = Button(frame, bg="blue" , text="New Cube", command=lambda: GUInewCube())
    NewCubeBTN.grid(row=2, column=1, sticky="w")
    MoveInsertLBL = Label(frame, bg="black", fg="white" , text="Enter moves:").grid(row=2, column=0)
    MoveInsertTB = Entry(frame, textvariable=move).grid(row=3, column=0)
    ExecBTN = Button(frame, text="Execute", command=lambda: GUImakeMove(move)).grid(row=3, column=1, sticky="w")
    ScramLBL = Label(frame, bg="black", fg="white" ,text="Scramble will be displayed here", wraplength=180, justify=CENTER, height=2)
    ScramLBL.grid(row=4, column=0, columnspan=2)
    ScramBTN = Button(frame, text="Scramble", bg="cyan", command=lambda: GUIScramble()).grid(row=5, column=0, sticky="w")
    CopyScramBTN = Button(frame, text="Copy Scramble", bg="cyan", command=lambda: CopyToClipBoard(GetScramb())).grid(row=5, column=1, sticky="w")
    SolveBTN = Button(frame, text="Solve Cube", bg="red", command=lambda: GUISolve()).grid(row=7, column=0, sticky="w")  
    CopyScramBTN = Button(frame, text="Copy Solution", bg="red", command=lambda: CopyToClipBoard(GetMoves())).grid(row=7, column=1, sticky="w")
    SolLBL = Label(frame, bg="black", fg="orange", text="Solution will be displayed here", wraplength=250, justify=CENTER, height=8)
    SolLBL.grid(row=9, column=0, columnspan=2)
    SolNoLBL = Label(frame, bg="black", fg="red", text="\t          Total number of moves used:")
    SolNoLBL.grid(row=10, column=0, sticky="e")
    SolNoTB = Label(frame, bg="green", font=BOLD ,text="0")
    SolNoTB.grid(row=10, column=1, sticky="w")
    CrossInfoLBL = Label(frame, bg="black" ,text="")
    CrossInfoLBL.grid(row=11, column=0, sticky="e")
    CrossNumberLabel = Label(frame, bg="black", text="0")
    CrossNumberLabel.grid(row=11, column=1, sticky="w")
    F2LInfoLBL = Label(frame, bg="black", text="")
    F2LInfoLBL.grid(row=12, column=0, sticky="e")
    F2LNumberLabel = Label(frame, bg="black", text="0")
    F2LNumberLabel.grid(row=12, column=1, sticky="w")
    OLLInfoLBL = Label(frame, bg="black", text="")
    OLLInfoLBL.grid(row=13, column=0, sticky="e")
    OLLNumberLabel = Label(frame, bg="black", text="0")
    OLLNumberLabel.grid(row=13, column=1, sticky="w")
    PLLInfoLBL = Label(frame, bg="black", text="")
    PLLInfoLBL.grid(row=14, column=0, sticky="e")
    PLLNumberLabel = Label(frame, bg="black", text="0")
    PLLNumberLabel.grid(row=14, column=1, sticky="w")
    YrotationButton = Button(Rframe, text="<-- Y", command=lambda: GUIyRotation("Y"))
    YrotationButton.grid(row=1, column=0)
    YirotationButton = Button(Rframe, text="Y' -->", command=lambda: GUIyRotation("Yi"))
    YirotationButton.grid(row=1, column=1)

InfoGUI()   # Start With the instructions frame, then press on 'Let's Go' to go to the application
