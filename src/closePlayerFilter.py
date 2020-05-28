import numpy as np
import matplotlib.pyplot as plt

def checkInterSec (x1, x2, x3, y1, y2, y3, Radius):
    # x1,y1 and x2,y2 are the coordinates on the same team
    # x3,y3 is the coordinate of the opponent, where Radius defines the circle which he covers 
    # subtract values to shift the opponent to origin (0,0)
    x1 = x1-x3
    x2 = x2-x3
    y1 = y1-y3
    y2 = y2-y3
    dr = np.sqrt(pow((x2-x1),2)+pow(y2-y1,2))
    D = (x1*y2)-(x2*y1)
    d = pow(Radius,2)*pow(dr,2)-pow(D,2)
    if d < 0:
        check = "Player is free" #he's free
    if d > 0:
        check = "Player is NOT free" #he's not free
    return check

def exampleRun():
    # Example run
    x1 = 2
    x2 = 8
    x3 = 8
    y1 = 3
    y2 = 8
    y3 = 5
    OpponentCircle = .7

    fig, ax = plt.subplots()
    plt.plot([x1, x2], [y1, y2], 'ro')
    plt.plot([x3],[y3], 'bo')
    plt.plot([x1,x2], [y1, y2], '--')
    Circ = plt.Circle((x3,y3), OpponentCircle, fill = False)
    ax.add_artist(Circ)

    print(checkInterSec(x1,x2,x3,y1,y2,y3,OpponentCircle))

    plt.show()

exampleRun()