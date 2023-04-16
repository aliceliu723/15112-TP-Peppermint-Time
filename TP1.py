from cmu_graphics import *
import random

# ideas:
# Schedule for Working (9 to 5) or (8 to 6)
# create event class

# Questions:
    # How to delete a class item?
    # How to align coordinate position to time?

# to-do list
    # draw time on schedule
    # 

# data:
    # schedule = 400
        # left = 25 = app.width/16
        # top = 100 = app.height/4
        # width = 350
        # height = 250
    # PepperMint Time = app.width/2, app.height/8
    # event
        # width = 50 = app.width/8
        # height = timespan
    # time (8am-6pm) = 10h
        # grid = 50 x 25

class Event:
    def __init__(self, title, day, start, end, color, left, top):
        self.title = title
        self.day = day
        self.start = start
        self.end = end
        self.color = color
        # for drawing rectangles on the schedule
        self.left = left
        self.top = top
        self.width = 50
        self.height = 25
    
    def __repr__(self):
        return f'{self.title} is starting at {self.start}.'
    
    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        else:
            return ((self.title == other.title) and (self.start == other.start)
                    and (self.end == other.end))
        
    def __hash__(self):
        return hash(str(self))
    
    # Event class methods
    def changeColor(self, color):
        self.color = color

    def changeStart(self, start):
        self.start = start
    
    def changeEnd(self, end):
        self.end = end

    def changeTitle(self, title):
        self.title = title

    #  Q: how do you delete a class element???
    def deleteEvent(self):
        pass


# schedule codes
    # draw schedule (using 2d list method rn)
    # create event
    # pop up window code
# modify feature (background)
# to-do list codes
# diary codes
# timer codes
# MVP
def onAppStart(app):
    app.scheduleLeft = app.width/16
    app.scheduleTop = app.height/4
    app.scheduleWidth = app.width-app.width/8
    app.scheduleHeight = app.height/2+app.height/8
    app.rows = 10
    app.cols = 7
    app.boardLeft = app.scheduleLeft
    app.boardTop = app.scheduleTop
    app.boardWidth = app.scheduleWidth
    app.boardHeight = app.scheduleHeight
    app.cellBorderWidth = app.width/400
    app.eventList = []
    app.drawMenu = False

def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawSchedule(app)
    drawEvents(app)
    drawCreateButton(app)
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth, opacity = 20)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth, opacity = 20)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    print(getCellSize(app))
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

# screen design
def drawSchedule(app):
    # drawTitle
    drawLabel('PepperMint Time', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)
    # draw panel
    drawRect(app.scheduleLeft, app.scheduleTop, app.scheduleWidth, 
             app.scheduleHeight, border='black', borderWidth=2, 
             opacity=10)
    # draw grid
    for i in range(4):
        drawLabel(f'{i+8} AM', 12, app.scheduleTop+25*i, size=7)
    drawLabel('12 PM', 12, app.scheduleTop+25*4, size=7)
    for i in range(1,7):
        drawLabel(f'{i} PM', 12, app.scheduleTop+100+25*i, size=7)
    #drawLabel('Monday', )
# if mouse press is within a day, create an event with corresponding day
# if mouse drag is within a day, create an event with time corresponding

    L = [('Monday', 50), ('Tuesday',100), ('Wednesday', 150), ('Thursday', 200),
        ('Friday', 250), ('Saturday', 300), ('Sunday', 350)]
    for day, width in L:
        drawLabel(day, width, 91, size=9)

def drawEvents(app):
    pass

def drawMenuButton(app):
    # menu
    drawRect(0, 0, 20, 20, fill='skyblue')
    for i in range(3):
        drawLine(5, 5+5*i, 15, 5+5*i, fill='black', opacity=50)
    
    # create button
def drawCreateButton(app):
    drawRect(5, 30, 50, 30, fill='lightskyblue')
    drawLabel('Create', 30, 45, fill='black')

def drawMenu(app):
    drawRect(0, 0, 100, 300, fill='white')
    drawMenuButton(app)

# User Interface
def onMousePress(app, mouseX, mouseY):
    # menu
    if (0 <= mouseX <= 20) and (0 <= mouseY <= 20):
        app.drawMenu = True if app.drawMenu==False else False


    # create
    # press and create
    #if 100 < mouseY < 350:
        #if 25 < mouseX < 75:
            #app.eventList.append(Event('Title', ''))
            


def onMouseDrag(app, mouseX, mouseY):
    pass
    # set boundaries
    # Monday: 25-75
    # Tuesday: 75-125
    # Wednesday: 125-175
    # Thursday: 175-225
    # Friday: 225-275
    # Saturday: 275-325
    # Sunday: 325-375

def onMouseRelease(app, mouseX, mouseY):
    pass

def onKeyPress(app, key):
    pass

def onKeyRelease(app, key):
    pass

# for timer
def onStep(app):
    pass




def main():
    runApp()

main()