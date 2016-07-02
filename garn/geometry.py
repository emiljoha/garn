from math import sqrt


# 3D
sqrt3 = 17 / 10.0
def hexagon(pos, base):
    """ Find out if position is inside hexagon
    Hexagon with left down corner in (0,0)

    pos:tuple (x,y) descibing position
    base: length of base 
    returns: true or false if it is in the hexagon or not.
    """
    if (l1(pos, base) & l2(pos, base) & l3(pos, base) & l4(pos, base)
            & l5(pos, base) & l6(pos, base)):
        return True
    else:
        return False


def extension(pos, base, wire_length, lead_length):
    return False
    x, y, z = pos
    if (((y >= 0) and (y < lead_length)) or
            ((y >= wire_length -lead_length) and (y <= wire_length))):
        if(l1_lead((x, z), base) and l2_lead((x, z), base)
               and vertical_line(x, base)) and (not l2((x, z), base)):
            return True
    else:
        return False


def l1(pos, b):
    """ Find out if position is under line 1

    top of the hexagon
    """
    x, y = pos
    if (y < sqrt(3) * b / 2.0):
        return True
    else:
        return False


def l2(pos, b):
    """ Find out if position is under line 2
    
    right top
    """
    x, y = pos
    if (y < sqrt(3) * (b - x)):
        return True
    else:
        return False


def l3(pos, b):
    """ Find out if position is over line 3

    right bottom
    """
    x, y = pos
    if (y >= sqrt(3) * (x - b)):
        return True
    else:
        return False


def l4(pos, b):
    """ Find out if position is over line 4

    bottom
    """
    x, y = pos
    if (y >= - sqrt(3) * b / 2.0):
        return True
    else:
        return False


def l5(pos, b):
    """ Find out if position is over line 5

    left bottom
    """
    x, y = pos
    if (y >= - sqrt(3) * (x + b)):
        return True
    else:
        return False


def l6(pos, b):
    """ Find out if position is under line 6

    left top
    """
    x, y = pos
    if (y < sqrt(3) * (x + b)):
        return True
    else:
        return False


# 2D
def rectangle(pos, base, length):
    """ Find out if position is inside rectange

    rectange with left down corner in (0,0)

    pos:tuple (x,y) descibing position
    base: length of base 
    returns: true or false if it is in the hexagon or not.
    """
    if (l12(pos, base, length) & l22(pos, base, length)
            & l32(pos, base, length) & l42(pos, base, length)):
        return True
    else:
        return False

def l12(pos, b, l):
    """ Find out if position is under line 1

    top of the rectangle
    """
    x, y = pos
    if (y < b):
        return True
    else:
        return False


def l22(pos, b, l):
    """ Find out if position is under line 2

    right side
    """
    x, y = pos
    if (x < l):
        return True
    else:
        return False


def l32(pos, b, l):
    """ Find out if position is over line 3

     bottom
    """
    x, y = pos
    if (y >= 0):
        return True
    else:
        return False


def l42(pos, b, l):
    """ Find out if position is over line 4

    left
    """
    x, y = pos
    if (x >= 0):
        return True
    else:
        return False
