from cmu_graphics import *
import random
import math

# logistics
    # start with initial screen
    # menu button is always present
    # click menu button to show options
    # schedule
        # change view button is always present
        # create button is always present
        # pop up window
        # month view
            # click date to create
        # week view
            # click time to create
            # drag time to create
        # day view
            # click time to create
            # drag time to create
    # to do list
    # diary
    # tomato clock

# hard tasks
    # link button to screens
        # debug screen show
    # link coordinates/positions to time
        # think and code by today
    # store info for event class and draw
        # think and code by today

# internal cells
# get cell row and col
# correspond row and col to timeslot
# correspond time to row and col
# def getCellClicked()
# def getTimeSlotFromRowAndCol()
# def getRowAndColFromTime



class Event:
    def __init__(self, title, date, day, start, end, color, left, top):
        self.title = title
        self.date = date
        self.day = day
        # start and end are strings
        self.start = start
        self.end = end
        self.color = color
        # for drawing rectangles on the schedule
        self.left = left
        self.top = top
        self.width = 50
        timespan = getTimespan(self.start, self.end)
        self.height = getEventHeight(timespan)
    
    def __repr__(self):
        return f'{self.title} is from {self.start} to {self.end}.'
    
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

    def drawEvent(self):
        drawRect(self.left, self.top, self.width, )
        drawLabel(f'{self.title}', )

class Buttons:
    def __init__(self, message, centerX, centerY, width, height, color, size,
                 bold, italic, function):
        self.message = message
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.color = color
        self.size = size
        self.bold = bold
        self.italic = italic
        self.function = function

    def draw(self):
        drawRect(self.centerX, self.centerY, self.width, self.height,
                 align='center', fill=self.color)
        drawLabel(self.message, self.centerX, self.centerY, bold=self.bold,
                  italic=self.italic, fill='black')
        
    def checkForPress(self, app, mouseX, mouseY):
        left = self.centerX-(self.width/2)
        right = self.centerX+(self.width/2)
        top = self.centerY-(self.height/2)
        bottom = self.centerY+(self.height/2)
        if (left <= mouseX <= right) and (top <= mouseY <= bottom):
            self.function(app)
            return True


def onAppStart(app):
    # week schedule coordinates
    app.width = 800
    app.height = 800
    app.scheduleLeft = app.width/16
    app.scheduleTop = app.height/4
    app.scheduleWidth = app.width-app.width/8
    app.scheduleHeight = app.height/2+app.height/8
    # month schedule coordinates
    app.monthLeft = app.scheduleLeft
    app.monthTop = app.scheduleTop
    app.monthWidth = app.scheduleWidth
    app.monthHeight = app.scheduleHeight
    # draw week schedule helper 
    app.rows = 10
    app.cols = 7
    app.boardLeft = app.scheduleLeft
    app.boardTop = app.scheduleTop
    app.boardWidth = app.scheduleWidth
    app.boardHeight = app.scheduleHeight
    app.cellBorderWidth = app.width/400
    # event draw helper
    app.eventList = []
    app.drawMenu = False
    app.drawPopUpWindow = False
    app.drawAutoScheduleWindow = False
    # draw month schedule helper
    app.monthRows = 5
    app.monthCols = 7
    app.monthBoardLeft = app.monthLeft
    app.monthBoardTop = app.monthTop
    app.monthBoardWidth = app.monthWidth
    app.monthBoardHeight = app.monthHeight
    app.monthCellBorderWidth =app.width/400
    # draw week schedule internal grid
    app.internalRows = 40
    app.internalCols = 7
    app.internalBoardLeft = app.scheduleLeft
    app.internalBoardTop = app.scheduleTop
    app.internalBoardWidth = app.scheduleWidth
    app.internalBoardHeight = app.scheduleHeight
    # change screen helper
    app.drawInitialScreen = True
    app.drawSchedule = False
    app.drawToDoList = False
    app.drawDiary = False
    app.drawTimer = False
    app.drawMonthView = False
    app.drawWeekView = False
    # buttons
    app.initialButtons = [Buttons('Schedule', app.width/2, app.height/2, 
                                  app.height/4, app.height/16, 'lightskyblue', 
                                  25, True, True, setWeekScheduleScreen),
        Buttons('To Do List', app.width/2, app.height/2+2*app.height/16,
                app.height/4, app.height/16, 'lightskyblue', 25, True,
                True, setToDoListScreen),
        Buttons('Diary', app.width/2, app.height/2+2*2*app.height/16, 
                app.height/4, app.height/16, 'lightskyblue', 25, True, True, 
                setDiaryScreen),
        Buttons('Tomato Clock', app.width/2, app.height/2+2*3*app.height/16,
                app.height/4, app.height/16, 'lightskyblue', 25, True, True,
                setTimerScreen)
    ]
    app.menuButton = Buttons('Menu', app.width/25, app.height/32,2*app.width/25,
                             2*app.height/32, 'lightskyblue', 15, True, True,
                             menuButtonFunction)
    app.menuButtons = [Buttons('Month Schedule', app.width/6, 
                               app.height/13+app.height/32, app.width/6, 
                               app.height/20, 'lightskyblue', 15, True, True, 
                               setMonthScheduleScreen),
        Buttons('Week 1', app.width/6, app.height/13+2*app.height/32+app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                setWeekScheduleScreen),
        Buttons('Week 2', app.width/6, app.height/13+3*app.height/32+2*app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                None),
        Buttons('Week 3', app.width/6, app.height/13+4*app.height/32+3*app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                None),
        Buttons('Week 4', app.width/6, app.height/13+5*app.height/32+4*app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                None),
        Buttons('Week 5', app.width/6, app.height/13+6*app.height/32+5*app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                None),
        Buttons('To Do List', app.width/6, app.height/13+7*app.height/32+6*app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                setToDoListScreen),
        Buttons('Diary', app.width/6, app.height/13+8*app.height/32+7*app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                setDiaryScreen),
        Buttons('Tomato Clock', app.width/6, app.height/13+9*app.height/32+8*app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                setTimerScreen)
    ]
    app.createButton = Buttons('Create', app.width-app.width/8, app.height/16,
                                app.width/10, app.height/20, 'lightskyblue', 30,
                                True, True, createButtonFunction)
    app.closeCreateButton = Buttons('X', 3*app.width/4-app.width/64, 
                                    app.height/4+app.height/64,
                                    app.width/32, app.height/32, 'slateblue', 30,
                                    True, False, closeCreateButton)
    app.autoScheduleButton = Buttons('Auto-Schedule',app.width-app.width/8,
                                     app.height/8, app.width/5, app.height/20,
                                     'lightskyblue', 30, True, True, 
                                     autoScheduleFunction)
    app.closeAutoSchedule = Buttons('X',2*app.width/3-app.width/64,
                                    app.height/3+app.height/70, app.width/32,
                                    app.height/32, 'slateblue', 30, True, False,
                                    closeAutoScheduleWindow)

# Initial Screen
def initialScreen_redrawAll(app):
    drawLabel('Peppermint Time', app.width/2, app.height/4, fill='royalblue',
              size=45, italic=True, bold=True)
    drawMenuButton(app)
    for button in app.initialButtons:
        button.draw()
    if app.drawMenu == True:
        drawMenu(app)

def initialScreen_onMousePress(app, mouseX, mouseY):
    for button in app.initialButtons:
        button.checkForPress(app, mouseX, mouseY)
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False

# Month Schedule Screen
def monthSchedule_redrawAll(app):
    # drawTitle
    drawLabel('Month Schedule', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)
    # draw panel with date
    drawMonthBoard(app)
    drawMonthBoardBorder(app)
    # draw menu
    drawMenuButton(app)
    # draw create button
    #drawCreateButton(app)
    if app.drawMenu == True:
        drawMenu(app)
    drawCreateButton(app)    
    if app.drawPopUpWindow == True:
        drawPopUpWindow(app)

def monthSchedule_onMousePress(app, mouseX, mouseY):
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False
    app.createButton.checkForPress(app, mouseX, mouseY)
    if app.drawPopUpWindow == True:
        app.closeCreateButton.checkForPress(app, mouseX, mouseY)

# Week 1 Schedule Screen
def weekSchedule_redrawAll(app):
    # drawTitle
    drawLabel('Week Schedule', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)
    # draw panel
    drawBoard(app)
    drawBoardBorder(app)
    # draw time
    cellWidth, cellHeight = getCellSize(app.boardWidth, app.boardHeight, 
                                        app.rows, app.cols)
    centerX = app.scheduleLeft-app.width/35
    for i in range(4):
        drawLabel(f'{i+8}AM', centerX, app.scheduleTop+cellHeight*i, size=8,
                  align='center')
    drawLabel('12PM', centerX, app.scheduleTop+cellHeight*4, size=8, 
              align='center')
    for i in range(5,11):
        drawLabel(f'{i-4}PM', centerX, app.scheduleTop+cellHeight*i, size=8, 
                  align='center')
    # draw days on top
    L = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
         'Saturday']
    for i in range(7):
        drawLabel(L[i], app.scheduleLeft+(cellWidth/2)+cellWidth*i, 
                  app.scheduleTop-app.width/50, size=9, align='center')
    # draw menu
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)
    # draw create button
    drawCreateButton(app)
    if app.drawPopUpWindow == True:
        drawPopUpWindow(app)
    drawAutoScheduleButton(app)
    if app.drawAutoScheduleWindow == True:
        drawAutoScheduleWindow(app)
    # draw internal grid
    drawInternalBoard(app)

def weekSchedule_onMousePress(app, mouseX, mouseY):
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False
    app.createButton.checkForPress(app, mouseX, mouseY)
    if app.drawPopUpWindow == True:
        app.closeCreateButton.checkForPress(app, mouseX, mouseY)
    app.autoScheduleButton.checkForPress(app, mouseX, mouseY)
    if app.drawAutoScheduleWindow == True:
        app.closeAutoSchedule.checkForPress(app, mouseX, mouseY)
    
    # getting cell position
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        app.selectedCell = selectedCell
        if selectedCell == None: # not a cell on the board, reset app.selection
        app.selection = None
    else: # cell on board, check if it is already has a move
        row, col = selectedCell
        if app.board[row][col] == None: # empty
            app.selection = selectedCell
        else:
            app.selection = None


# draw menu (change gird)
def drawMenu(app):
    # background
    drawRect(0, 0, app.width/3, 7*app.height/8, fill='lavender')
    # buttons
    for button in app.menuButtons:
        button.draw()
    drawMenuButton(app)

def drawMenuButton(app):
    app.menuButton.draw()

# draw the 'Create' button
def drawCreateButton(app):
    app.createButton.draw()

# draw pop up window for creating an event
def drawPopUpWindow(app):
    # background panel
    drawRect(app.width/2, app.height/2, app.width/2, app.height/2,
             fill='mediumpurple', borderWidth=3, border='slateblue',
             align='center')
    drawRect(3*app.width/4-app.width/64, app.height/4+app.height/64,
             app.width/32, app.height/32, fill='slateblue', align='center')
    app.closeCreateButton.draw()
    
    # title
    # date
    # day
    # start time
    # end time
    # color
    L = ['orangered', 'sandybrown', 'lightgreen', 'paleturquoise', 'lightpink']
    #for i in range(5):
        #drawCircle(165+i*30, 275, 10, fill=L[i])

# draw the 'Auto-Schedule' Button
def drawAutoScheduleButton(app):
    app.autoScheduleButton.draw()

# draw pop up window for auto schedule
def drawAutoScheduleWindow(app):
    # background panel
    drawRect(app.width/2, app.height/2, app.width/3, app.height/3, 
             fill='mediumpurple', borderWidth=3, border='slateblue',
             align='center')
    app.closeAutoSchedule.draw()
    # timespan
    # week number
    # color

def drawEvents(app):
    pass   



# To-Do List Screen
def toDoList_redrawAll(app):
    drawLabel('To Do List', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)

def toDoList_onMousePress(app, mouseX, mouseY):
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False

# Diary Screen
def diary_redrawAll(app):
    drawLabel('Diary', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)

def diary_onMousePress(app, mouseX, mouseY):
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False

# Timer Screen
def timer_redrawAll(app):
    drawLabel('Tomato Clock', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)

def timer_onMousePress(app, mouseX, mouseY):
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False

# User Interface

def showMenu(app):
    app.drawMenu = True if app.drawMenu == False else False

            


#def onMouseDrag(app, mouseX, mouseY):
    #pass
    # set boundaries
    # Monday: 25-75
    # Tuesday: 75-125
    # Wednesday: 125-175
    # Thursday: 175-225
    # Friday: 225-275
    # Saturday: 275-325
    # Sunday: 325-375

#def onMouseRelease(app, mouseX, mouseY):
    #pass

#def onKeyPress(app, key):
    #pass

#def onKeyRelease(app, key):
    pass

# for timer
#def onStep(app):
    #pass

###############################################################################
# helper functions
# draw
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, app.boardLeft, app.boardTop, app.boardWidth, 
                     app.boardHeight, app.rows, app.cols, row, col, 20)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth, opacity = 20)

def drawMonthBoard(app):
    for row in range(app.monthRows):
        for col in range(app.monthCols):
            drawMonthCellWithDate(app, app.monthBoardLeft, app.monthBoardTop, 
                     app.monthBoardWidth, app.monthBoardHeight, app.monthRows,
                     app.monthCols, row, col, 20)

def drawMonthBoardBorder(app):
    drawRect(app.monthBoardLeft, app.monthBoardTop, app.monthBoardWidth,
             app.monthBoardHeight, fill=None, border='black', 
             borderWidth=2*app.monthCellBorderWidth, opacity=20)

def drawInternalBoard(app):
    for row in range(app.internalRows):
        for col in range(app.internalCols):
            drawCell(app, app.internalBoardLeft, app.internalBoardTop, 
                     app.internalBoardWidth, app.internalBoardHeight, 
                     app.internalRows, app.internalCols, row, col, 100)

# helper of helper functions
def drawCell(app, boardLeft, boardTop, boardWidth, boardHeight, 
             rows, cols, row, col, opacity): 
    cellLeft, cellTop = getCellLeftTop(boardLeft, boardTop, 
                                       boardWidth, boardHeight,
                                       rows, cols, row, col)
    cellWidth, cellHeight = getCellSize(app.boardWidth, app.boardHeight,
                                        app.rows, app.cols)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth, opacity=opacity)

def getCellLeftTop(boardLeft, boardTop, boardWidth, boardHeight, 
                   rows, cols, row, col):
    cellWidth, cellHeight = getCellSize(boardWidth, boardHeight,
                                        rows, cols)
    cellLeft = boardLeft + col * cellWidth
    cellTop = boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(boardWidth, boardHeight, rows, cols):
    cellWidth = boardWidth / cols
    cellHeight = boardHeight / rows
    return (cellWidth, cellHeight)

def getCellDate(app, row, col):
    maxRowNum = app.cols
    date = (row)*app.cols + (col+1)
    return date

def drawMonthCellWithDate(app, boardLeft, boardTop, boardWidth, boardHeight, 
             rows, cols, row, col): 
    cellLeft, cellTop = getCellLeftTop(boardLeft, boardTop, 
                                       boardWidth, boardHeight,
                                       rows, cols, row, col)
    cellWidth, cellHeight = getCellSize(boardWidth, boardHeight,
                                        rows, cols)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth, opacity = 20)
    drawLabel(f'{getCellDate(app, row, col)}', cellLeft+app.width/160, 
              cellTop+app.width/160, 
              align='left-top', size=10, italic=True)


def distance(x, y, a, b):
    return (((x-a)**2)+((y-b)**2))**0.5



# event helper
# get (row, col) from mouse click
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app.internalBoardWidth, 
                                        app.internalBoardHeight, 
                                        app.internalRows, app.internalCols)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None
    
# get time from (row, col)
def getTimeFromPosition(app):
    pass

# get time span from (row, col)
def getTimeSpanFromPosition(app):
    pass

# get (row, col) from time
def getPositionFromTime(app):
    pass



def getTimespan(start, end):
    pass
    # 1. both start and end are am
    # 2. both start and end are pm
    # 3. start is am, end is pm
    #if ('am' in start) and ('am' in end):

    #elif ('pm' in start) and ('pm' in end):

    #elif ('am' in start) and ('pm' in end):


def getEventHeight(timespan):
    pass

def reset(app):
    app.drawInitialScreen = False
    app.drawSchedule = False
    app.drawToDoList = False
    app.drawDiary = False
    app.drawTimer = False

def setWeekScheduleScreen(app):
    setActiveScreen("weekSchedule")

def setMonthScheduleScreen(app):
    setActiveScreen("monthSchedule")

def setToDoListScreen(app):
    setActiveScreen("toDoList")

def setDiaryScreen(app):
    setActiveScreen("diary")

def setTimerScreen(app):
    setActiveScreen("timer")

# buttons
initialButtons = [Buttons('Schedule', app.width/2, app.height/2, app.height/4, 
                app.height/16, 'lightskyblue', 25, True, True, 
                setWeekScheduleScreen),
        Buttons('To Do List', app.width/2, app.height/2+2*app.height/16,
                app.height/4, app.height/16, 'lightskyblue', 25, True,
                True, setToDoListScreen),
        Buttons('Diary', app.width/2, app.height/2+2*2*app.height/16, 
                app.height/4, app.height/16, 'lightskyblue', 25, True, True, 
                setDiaryScreen),
        Buttons('Tomato Clock', app.width/2, app.height/2+2*3*app.height/16,
                app.height/4, app.height/16, 'lightskyblue', 25, True, True,
                setTimerScreen)
]

scheduleButtons = []
# buttons functions
def menuButtonFunction(app):
    app.drawMenu = True if app.drawMenu == False else False

def createButtonFunction(app):
    if app.drawPopUpWindow == False:
        app.drawPopUpWindow = True

def closeCreateButton(app):
    app.drawPopUpWindow = False

def autoScheduleFunction(app):
    if app.drawAutoScheduleWindow == False:
        app.drawAutoScheduleWindow = True

def closeAutoScheduleWindow(app):
    app.drawAutoScheduleWindow = False

def main():
    # runApp(width=800, height=800)
    runAppWithScreens(width=800, height=800, initialScreen='initialScreen')

main()
