from cmu_graphics import *
import random
from PIL import Image
import math

# logistics
    # start with initial screen
    # menu button is always present
    # click menu button to show options
    # schedule
        # instructions Button
            # pop up window
        # create button is always present
            # pop up window (app.message)
                # title: textInput
                # day of the week : textInput(capital)
                # start time: textInput (num)
                # end time: textInput(num)
                # color: click to set color
                # save: when click create event
        # auto-schedule
            # title
            # preferred day
            # earliest start at
            # no later than
            # timespan
            # how many?
            # color
        # week view
            # click time to create
                # if there is an event
                    # edit the event
                # if there is no event
                    # create new event
                # onMousePress
            # drag time to create
                # onMouseDrag
                # onMouseRelease with drag
            # click "Create" to create
    # tomato clock



class Event:
    def __init__(self, title, day, start, end, color, cellList, function):
        self.title = title
        self.day = day
        # start and end are strings
        self.start = start
        self.end = end if end!= None else start+1
        self.color = color
        # for drawing rectangles on the schedule
        self.cellList = cellList
        self.function = function

    def __repr__(self):
        return (f'{self.title} is from {self.start} to {self.end}.')
    
    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        else:
            return ((self.title == other.title) and (self.day == self.day) 
                    and (self.start == other.start)
                    and (self.end == other.end) and (self.color == other.color))
        
    def __hash__(self):
        return hash(str(self))
    
    # Event class methods
    def changeTitle(self, title):
        self.title = title

    def changeDay(self, day):
        self.day = day

    def changeStart(self, start):
        self.start = start
    
    def changeEnd(self, end):
        self.end = end

    def changeColor(self, color):
        self.color = color

    def changeCellList(self, cellList):
        self.cellList = cellList

    def draw(self,app):
        # row, col provided
        # need: cellLeft, cellTop, cellWidth, cellHeight
        rowFirst, colFirst = self.cellList[0]
        cellLeftFirst, cellTopFirst = getCellLeftTop(app.boardLeft, app.boardTop,
                                                     app.boardWidth, app.boardHeight,
                                                     app.internalRows, app.internalCols,
                                                     rowFirst, colFirst)
        for row, col in self.cellList:
            cellLeft, cellTop = getCellLeftTop(app.boardLeft, app.boardTop, 
                                               app.boardWidth, app.boardHeight,
                                               app.internalRows, app.internalCols, 
                                               row, col)
            cellWidth, cellHeight = getCellSize(app.boardWidth, app.boardHeight,
                                        app.internalRows, app.internalCols)
            drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=self.color)
            app.board[row][col] = 'X'
        if len(self.cellList)==1:
            drawLabel(self.title, cellLeftFirst, cellTopFirst, size=13, 
                      align='left-top', fill='black')
        elif len(self.cellList)>=2:
            drawLabel(self.title, cellLeftFirst, cellTopFirst, size=13, 
                      align='left-top', fill='black')
            drawLabel(f'{self.start} - {self.end}', cellLeftFirst, 
                      cellTopFirst+cellHeight, align='left-top', fill='black')
        

    def checkForPress(self, app, mouseX, mouseY):
        rowFirst, colFirst = self.cellList[0]
        cellLeftFirst, cellTopFirst = getCellLeftTop(app.boardLeft, app.boardTop,
                                                     app.boardWidth, app.boardHeight,
                                                     app.internalRows, app.internalCols,
                                                     rowFirst, colFirst)
        cellWidth, cellHeight = getCellSize(app.boardWidth, app.boardHeight,
                                        app.internalRows, app.internalCols)
        left = cellLeftFirst
        right = cellLeftFirst + cellWidth
        top = cellTopFirst
        bottom = cellTopFirst + cellHeight*(len(self.cellList))
        if (left <= mouseX <= right) and (top <= mouseY <= bottom):
            self.function(app)
            app.title = self.title
            app.day = self.day
            app.start = self.start
            app.end = self.end
            app.color = self.color
        return True
    
    def returnSelectedEvent(self, app):
        return self

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
    # image
    app.image = Image.open('blueClock.png')
    app.image = app.image.resize((600, 600))
    app.image = CMUImage(app.image)
    # mouse
    app.x = 0
    app.y = 0
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
    app.cellBorderWidth = app.width/800
    # event draw helper
    app.eventList = []
    app.drawMenu = False
    app.drawPopUpWindow = False
    app.drawAutoScheduleWindow = False
    app.selectedEvent = None
    app.selectedCellStart = None
    app.selectedCellEnd = None
    # event action helper
    app.selectedCell = None
    app.title = ''
    app.day = ''
    app.start = ''
    app.end = ''
    app.color = ''
    app.cellList = []
    app.typeTitle = False
    app.typeDay = False
    app.typeStart = False
    app.typeEnd = False
    app.titleBorderColor = 'white'
    app.dayBorderColor = 'white'
    app.startBorderColor = 'white'
    app.endBorderColor = 'white'
    # auto-schedule action helper
    app.titleAutoSchedule = ''
    app.preferredDayAutoSchedule = ''
    app.startAutoSchedule = ''
    app.endAutoSchedule = ''
    app.timespanAutoSchedule = ''
    app.numberAutoSchedule = ''
    app.colorAutoSchedule = ''
    app.typeTitleAutoSchedule = False
    app.typePreferredDayAutoSchedule = False
    app.typeStartAutoSchedule = False
    app.typeEndAutoSchedule = False
    app.typeTimespanAutoSchedule = False
    app.typeNumberAutoSchedule = False
    app.titleAutoScheduleBorderColor = 'white'
    app.preferredDayAutoScheduleBorderColor = 'white'
    app.startAutoScheduleBorderColor = 'white'
    app.endAutoScheduleBorderColor = 'white'
    app.timespanAutoScheduleBorderColor = 'white'
    app.numberAutoScheduleBorderColor = 'white'
    # boolean
    app.drawInstructions = False
    app.drawReminder = False
    app.drawConflict = False
    app.drawNoEvent = False
    app.clickTimeToCreate = False
    app.dragTimeToCreate = False
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
    app.internalBoardHeight = app.height/2+app.height/8
    # event helper
    app.board = [[None]*app.internalCols for row in range(app.internalRows)]
    # buttons
    app.initialButtons = [Buttons('Schedule', app.width/4, 
                                  app.height/2+2*3*app.height/16, 
                                  app.height/4, app.height/16, 'lightskyblue', 
                                  25, True, True, setWeekScheduleScreen),
        Buttons('Tomato Clock', app.width/2+2*app.width/8, 
                app.height/2+2*3*app.height/16,
                app.height/4, app.height/16, 'lightskyblue', 25, True, True,
                setTimerScreen)
    ]
    app.menuButton = Buttons('Menu', app.width/25, app.height/32,2*app.width/25,
                             2*app.height/32, 'lightskyblue', 25, True, True,
                             menuButtonFunction)
    app.menuButtons = [Buttons('Week Schedule', app.width/6, 
                               app.height/13+3*app.height/64, app.width/6, 
                               app.height/20, 'lightskyblue', 15, True, True, 
                               setWeekScheduleScreen),
        Buttons('Tomato Clock', app.width/6, app.height/13+5*app.height/64+app.height/20,
                app.width/6, app.height/20, 'lightskyblue', 15, True, True,
                setTimerScreen)
    ]
    app.instructionButton = Buttons('Instructions', 3*app.width/16, app.height/8,
                                    app.width/6, app.height/20, 'lightskyblue',
                                    30, True, True, instructionButtonFunction)
    app.closeInstructionButton = Buttons('X', app.width/2+app.width/4,
            app.height/2-3*app.height/32-(1/2)*3*app.height/8, app.width/32, 
            app.height/32, 'slateblue', 30, True, False, closeInstructionFunction)
    app.createButton = Buttons('Create', app.width-app.width/8, app.height/16,
                                app.width/10, app.height/20, 'lightskyblue', 30,
                                True, True, createButtonFunction)
    L = ['orangered', 'sandybrown', 'lightgreen', 'paleturquoise', 'lightpink']
    app.eventButtons = [Buttons('X', 3*app.width/4-app.width/64, 
                                    app.height/4+app.height/64,
                                    app.width/32, app.height/32, 'slateblue', 30,
                                    True, False, closeCreateButton),
        Buttons('Title', app.width/4+app.width/16, 
                                app.height/4+app.height/16, app.width/16, 
                                app.height/32, 'lavender', 30, True, True, 
                                titleButtonFunction),
        Buttons('Day of the Week', app.width/2-app.width/8, app.height/4+9*app.height/64,
                app.width/8, app.height/32, 'lavender', 30, True, True,
                dayButtonFunction),
        Buttons('From', app.width/4+app.width/16, app.height/4+7*app.height/32,
                app.width/16, app.height/32, 'lavender', 30, True, True,
                startButtonFunction),
        Buttons('To', app.width/2+app.width/20, app.height/4+7*app.height/32,
                app.width/16, app.height/32, 'lavender', 30, True, True,
                endButtonFunction),
        Buttons('', app.width/4+app.width/8+app.width/32, app.height/4+6*app.height/16,
                app.width/32, app.height/32, L[0], 0, True, True,
                orangeredFunction),
        Buttons('', app.width/4+app.width/8+3*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[1], 0, True, True, sandybrownFunction),
        Buttons('', app.width/4+app.width/8+5*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[2], 0, True, True, lightgreenFunction),
        Buttons('', app.width/4+app.width/8+7*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[3], 0, True, True, paleturquoiseFunction),
        Buttons('', app.width/4+app.width/8+9*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[4], 0, True, True, lightpinkFunction),
        Buttons('Save', app.width/2+app.width/8+app.width/16,
                app.height/2+app.height/8+app.height/16, app.width/16, 
                app.width/32, 'lavender', 20, True, True, saveEventFunction),
        Buttons('Delete', app.width/2-app.width/8-app.width/16,
                app.height/2+app.height/8+app.height/16, app.width/16,
                app.width/32, 'lavender', 20, True, True, deleteEventFunction)
    ]
    app.autoScheduleButton = Buttons('Auto-Schedule',app.width-app.width/8,
                                     app.height/8, app.width/5, app.height/20,
                                     'lightskyblue', 30, True, True, 
                                     autoScheduleFunction)
    app.backtrackingButtons = [Buttons('X', 3*app.width/4-app.width/64, 
                                    app.height/4+app.height/64,
                                    app.width/32, app.height/32, 'slateblue', 30,
                                    True, False, closeAutoScheduleWindow),
        Buttons('Title', app.width/4+app.width/16, 
                                app.height/4+app.height/16, app.width/16, 
                                app.height/32, 'lavender', 30, True, True, 
                                titleAutoScheduleFunction),
        Buttons('Preferred Day', app.width/2-app.width/6, 
                app.height/4+4*app.height/32, app.width/8, app.height/32, 'lavender',
                30, True, True, preferredDayAutoScheduleFunction),
        Buttons('Start', app.width/4+app.width/16, app.height/4+6*app.height/32,
                app.width/16, app.height/32, 'lavender', 30, True, True,
                startAutoScheduleFunction),
        Buttons('End', app.width/2+app.width/20, app.height/4+6*app.height/32,
                app.width/16, app.height/32, 'lavender', 30, True, True,
                endAutoScheduleFunction), 
        Buttons('Timespan', app.width/4+app.width/16, app.height/4+8*app.height/32,
                app.width/10, app.height/32, 'lavender', 30, True, True,
                timespanAutoScheduleFunction),
        Buttons('How many?', app.width/2+app.width/16, app.height/4+8*app.height/32,
                app.width/10, app.height/32, 'lavender', 30, True, True,
                numberAutoScheduleFunction),
        Buttons('', app.width/4+app.width/8+app.width/32, app.height/4+6*app.height/16,
                app.width/32, app.height/32, L[0], 0, True, True,
                orangeredAutoScheduleFunction),
        Buttons('', app.width/4+app.width/8+3*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[1], 0, True, True, sandybrownAutoScheduleFunction),
        Buttons('', app.width/4+app.width/8+5*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[2], 0, True, True, lightgreenAutoScheduleFunction),
        Buttons('', app.width/4+app.width/8+7*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[3], 0, True, True, paleturquoiseAutoScheduleFunction),
        Buttons('', app.width/4+app.width/8+9*app.width/32, 
                app.height/4+6*app.height/16, app.width/32, app.height/32, 
                L[4], 0, True, True, lightpinkAutoScheduleFunction),
        Buttons('Save', app.width/2+app.width/8+app.width/16,
                app.height/2+app.height/8+app.height/16, app.width/16, 
                app.width/32, 'lavender', 20, True, True, saveAutoScheduleFunction)   
    ]
    # timer helpers
    app.stepsPerSecond = 1
    app.count = 60
    app.paused = True

# Initial Screen
def initialScreen_redrawAll(app):
    drawImage(app.image, app.width/2, app.height/2+app.height/16, align='center')
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

# Instruction Page
def drawInstructions(app):
    app.closeInstructionButton.draw()
    # background panel
    drawRect(app.width/2, app.height/2-3*app.height/32, app.width/2, 3*app.height/8,
             fill='mediumpurple', borderWidth=3, border='slateblue',
             align='center')
    drawLabel("This schedule is in 15 minutes time slots.", 
              app.width/4+app.width/32, app.height/4+app.height/32, 
              size=15, align='left')
    drawLabel("1. Creating an event:", app.width/4+app.width/32, 
              app.height/4+2*app.height/32, size=15, align='left')
    drawLabel("a. Click the ‘Create’ button", app.width/4+app.width/16, 
              app.height/4+3*app.height/32, size=15, align='left')
    drawLabel("b. Click a time.", app.width/4+app.width/16, 
              app.height/4+4*app.height/32, size=15, align='left')
    drawLabel("c. Drag a time-slot.", app.width/4+app.width/16, 
              app.height/4+5*app.height/32, size=15, align='left')
    drawLabel("2. Plan a series of events using the auto-scheduler.", 
              app.width/4+app.width/32, app.height/4+6*app.height/32, 
              size=15, align='left')
    drawLabel("1. Click the 'Auto-Schedule' button.", app.width/4+app.width/16,
              app.height/4+7*app.height/32, size=15, align='left')
    drawLabel("2.Type in the timespan of your event as such", 
              app.width/4+app.width/16, app.height/4+8*app.height/32,
              size=15, align='left')
    drawLabel("Ex. 1h, 30min, 45min", app.width/4+3*app.width/32,
              app.height/4+9*app.height/32, size=15, align='left')

# Weekly Schedule Screen
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
    for i in range(11):
        drawLabel(f'{i+8}', centerX, app.scheduleTop+cellHeight*i, size=13,
                  align='center', bold=True)
    L = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
         'Saturday']
    for i in range(7):
        drawLabel(L[i], app.scheduleLeft+(cellWidth/2)+cellWidth*i, 
                  app.scheduleTop-app.width/50, size=13, align='center')
    # draw internal grid (invisible)
    drawInternalBoard(app)
    # draw event
    if app.eventList != []:
        for event in app.eventList:
            event.draw(app)
    # draw instruction page
    drawInstructionButton(app)
    if app.drawInstructions == True:
        drawInstructions(app)
    # draw create button & pop up window
    drawCreateButton(app)
    if (app.drawPopUpWindow == True):
        drawPopUpWindow(app)
    # draw reminder of input error
    if app.drawReminder == True:
        drawReminder(app)
    # draw conflict reminder
    if app.drawConflict == True:
        drawConflict(app)
    # draw "no event can be scheduled with auto-scheduler"
    if app.drawNoEvent == True:
        drawNoEvent(app)
    # draw auto-schedule button & pop up window
    drawAutoScheduleButton(app)
    if (app.drawAutoScheduleWindow == True):
        drawAutoScheduleWindow(app)
    # draw menu
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)
    # draw mouse
    drawCircle(app.x, app.y, app.width/200, fill='red')
    
def weekSchedule_onMouseMove(app, mouseX, mouseY):
    app.x = mouseX
    app.y = mouseY

def weekSchedule_onMousePress(app, mouseX, mouseY):
    # menu
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False
    # instructions page
    if ((app.drawPopUpWindow == False) and (app.drawAutoScheduleWindow == False)):
        app.instructionButton.checkForPress(app, mouseX, mouseY)
    if app.drawInstructions == True:
        app.closeInstructionButton.checkForPress(app, mouseX, mouseY)
    # create & pop up window
    if ((app.drawAutoScheduleWindow == False) and (app.drawInstructions == False)):
        app.createButton.checkForPress(app, mouseX, mouseY)
    # click an empty time to create event
    if ((app.drawPopUpWindow == False) and (app.drawAutoScheduleWindow == False)
        and (app.drawInstructions == False)):
        app. selectedCellStart = getCell(app, mouseX, mouseY)
        if app.selectedCellStart != None:
            row, col = app.selectedCellStart
            # check if this row & col has an event on or not:
            if ((app.board[row][col] == None) and (app.drawPopUpWindow == False)):
                app.clickTimeToCreate = True
    # auto-schedule & window
    if ((app.drawPopUpWindow == False) and (app.drawInstructions == False)):
        app.autoScheduleButton.checkForPress(app, mouseX, mouseY)
    if app.drawAutoScheduleWindow == True:
        for button in app.backtrackingButtons:
            if (button.checkForPress(app, mouseX, mouseY)==True):
                return
    # creating event
    if app.drawPopUpWindow == True:
        for button in app.eventButtons:
            if (button.checkForPress(app, mouseX, mouseY)==True):
                return
    # edit event
    for event in app.eventList:
            if ((app.drawPopUpWindow == False) and 
                (app.drawAutoScheduleWindow == False) and
                (app.drawInstructions == False) and
                (event.checkForPress(app, mouseX, mouseY) == True)):
                app.selectedEvent = event.returnSelectedEvent(app)
        
def weekSchedule_onMouseRelease(app, mouseX, mouseY):
    # click to create
    if (app.clickTimeToCreate == True) and (app.dragTimeToCreate == False):
        if ((app.selectedCellStart != None)):
            app.drawPopUpWindow = True
            clickTimeToCreate(app, app.selectedCellStart, app.selectedCellEnd)
    # drag to create
    if (app.dragTimeToCreate == True) and (app.clickTimeToCreate == True):
        if ((app.selectedCellStart != None) and (app.selectedCellEnd != None)):
            app.drawPopUpWindow = True
            dragTimeToCreate(app, app.selectedCellStart, app.selectedCellEnd)

def weekSchedule_onMouseDrag(app, mouseX, mouseY):
    app.x = mouseX
    app.y = mouseY
    if ((app.drawPopUpWindow == False) and (app.drawAutoScheduleWindow == False)
        and (app.drawInstructions == False)):
        app.selectedCellEnd = getCell(app, mouseX, mouseY)
        if (app.selectedCellStart != None) and (app.selectedCellEnd != None):
            # for a drag, we need to know start cell & end cell
            # start cell is given by onMousePress
            # end cell is given by onMouseDrag
            # we then need to know the cellList to check if there's conflict
            rowStart, colStart = app.selectedCellStart
            rowEnd, colEnd = app.selectedCellEnd
            cellList = getCellListRowStartAndRowEnd(rowStart, rowEnd, colStart)
            for (row, col) in cellList:
                if ((app.board[row][col] == None) and (app.drawPopUpWindow == False)):
                    app.dragTimeToCreate = True

def weekSchedule_onKeyPress(app, key):
    # 'create' an event input
    if app.drawPopUpWindow == True:
        if key == 'enter':
            resetEventInput(app)
        if app.typeTitle == True:
            if key == 'backspace':
                app.title = app.title[:-1]
            elif len(app.title) < 13:
                if key == 'space':
                    app.title = app.title + ' '
                else:
                    app.title += key
        elif app.typeDay == True:
            if key == 'backspace':
                app.day = app.day[:-1]
            elif len(app.day) < 12:
                if key == 'space':
                    app.day = app.day + ' '
                else:
                    app.day += key
        elif app.typeStart == True:
            if key == 'backspace':
                app.start = app.start[:-1]
            elif len(app.start) < 5:
                if key == 'space':
                    app.start = app.start + ' '
                else:
                    app.start += key
        elif app.typeEnd == True:
            if key == 'backspace':
                app.end = app.end[:-1]
            elif len(app.end) < 5:
                if key == 'space':
                    app.end = app.end + ' '
                else:
                    app.end += key
    # auto-schedule input
    elif app.drawAutoScheduleWindow == True:
        if key == 'enter':
            resetAutoScheduleInput(app)
        if app.typeTitleAutoSchedule == True:
            if key == 'backspace':
                app.titleAutoSchedule = app.titleAutoSchedule[:-1]
            elif len(app.titleAutoSchedule) < 13:
                if key == 'space':
                    app.titleAutoSchedule = app.titleAutoSchedule + ' '
                else:
                    app.titleAutoSchedule += key
        elif app.typePreferredDayAutoSchedule == True:
            if key == 'backspace':
                app.preferredDayAutoSchedule = app.preferredDayAutoSchedule[:-1]
            elif len(app.preferredDayAutoSchedule) < 12:
                if key == 'space':
                    app.preferredDayAutoSchedule = app.preferredDayAutoSchedule + ' '
                else:
                    app.preferredDayAutoSchedule += key
        elif app.typeStartAutoSchedule == True:
            if key == 'backspace':
                app.startAutoSchedule = app.startAutoSchedule[:-1]
            elif len(app.startAutoSchedule) < 5:
                if key == 'space':
                    app.startAutoSchedule = app.startAutoSchedule + ' '
                else:
                    app.startAutoSchedule += key
        elif app.typeEndAutoSchedule == True:
            if key == 'backspace':
                app.endAutoSchedule = app.endAutoSchedule[:-1]
            elif len(app.end) < 5:
                if key == 'space':
                    app.endAutoSchedule = app.endAutoSchedule + ' '
                else:
                    app.endAutoSchedule += key
        elif app.typeTimespanAutoSchedule == True:
            if key == 'backspace':
                app.timespanAutoSchedule = app.timespanAutoSchedule[:-1]
            elif len(app.timespanAutoSchedule) < 6:
                if key == 'space':
                    app.timespanAutoSchedule = app.timespanAutoSchedule + ' '
                else:
                    app.timespanAutoSchedule += key
        elif app.typeNumberAutoSchedule == True:
            if key == 'backspace':
                app.numberAutoSchedule = app.numberAutoSchedule[:-1]
            elif len(app.numberAutoSchedule) < 2:
                if key == 'space':
                    app.numberAutoSchedule = app.numberAutoSchedule + ' '
                else:
                    app.numberAutoSchedule += key

# redrawAll helper functions
# draw menu (change gird)
def drawMenu(app):
    # background
    drawRect(0, 0, app.width/3, 5*app.height/16, fill='lavender')
    # buttons
    for button in app.menuButtons:
        button.draw()
    drawMenuButton(app)

def drawMenuButton(app):
    app.menuButton.draw()

# draw the 'Instructions' Button
def drawInstructionButton(app):
    app.instructionButton.draw()

# draw the 'Create' button
def drawCreateButton(app):
    app.createButton.draw()

# draw pop up window for creating an event
def drawPopUpWindow(app):
    # background panel
    drawRect(app.width/2, app.height/2, app.width/2, app.height/2,
             fill='mediumpurple', borderWidth=3, border='slateblue',
             align='center')
    # Button: rectangle and label
    # rectangle text box follow after
        # when click, (button function x6)
            # 1. reset all the other message boolean to False
            # 2. set app.typeThisSpecificMessage to True
    # in onKeyPress(app): set app.thisSpecificMessage to the current message
        # allow the user to input anything
        # but when creating event, only take in certain constraints (see TP.py)
        # save button: contraints, pop up window, only when things are right then add
    # in creating event: app.thisSpecificMessage correspond to the attribute
    for button in app.eventButtons:
        button.draw()
    # title
    drawRect(app.width/2+app.width/20, app.height/4+app.height/16, 
                app.width/3, app.height/32, fill='white', align='center',
                border=app.titleBorderColor)
    drawLabel(app.title, app.width/2+app.width/20-app.width/6+app.width/300,
               app.height/4+app.height/16,
              fill='black', size=15, italic=True, bold=False, align='left')
    # day
    drawRect(app.width/2+app.width/8, app.height/4+9*app.height/64,
             app.width/8, app.height/32, fill='white', align='center',
             border=app.dayBorderColor)
    drawLabel(app.day, app.width/2+app.width/8-app.width/16+app.width/300, 
              app.height/4+9*app.height/64, fill='black', size=15, 
              italic=True, bold=False, align='left')
    # start
    drawRect(app.width/2-app.width/12, app.height/4+7*app.height/32,
            app.width/12, app.height/32, fill='white', align='center',
            border=app.startBorderColor)
    drawLabel(app.start, app.width/2-app.width/12-app.width/24+app.width/300,
               app.height/4+7*app.height/32,
              fill='black', size=15, italic=True, bold=False, align='left')
    # end
    drawRect(app.width/2+app.width/8+app.width/32, app.height/4+7*app.height/32,
             app.width/12, app.height/32, fill='white', align='center',
             border=app.endBorderColor)
    drawLabel(app.end, app.width/2+app.width/8+app.width/32-app.width/24+app.width/300, 
              app.height/4+7*app.height/32, fill='black', size=15,
              italic=True, bold=False, align='left')
    # draw 'Color'
    drawRect(app.width/4+app.width/16, app.height/4+12*app.height/32,
                 app.width/12, app.height/32, align='center', fill='lavender')
    drawLabel('Color', app.width/4+app.width/16, app.height/4+12*app.height/32,
              size=15, italic=True, bold=True)
    drawRect(app.width/2, app.height/4+10*app.height/32, app.width/8, 
             app.height/32, fill='white', align='center')
    drawLabel(app.color, app.width/2, app.height/4+10*app.height/32,
              align='center', fill='black', size=12, italic=True, bold=True)

# draw the 'Auto-Schedule' Button
def drawAutoScheduleButton(app):
    app.autoScheduleButton.draw()

# draw pop up window for auto schedule
def drawAutoScheduleWindow(app):
    # background panel
    drawRect(app.width/2, app.height/2, app.width/2, app.height/2,
             fill='mediumpurple', borderWidth=3, border='slateblue',
             align='center')
    # draw buttons in onAppStart (include this app.closeAutoScheulde button)
    for button in app.backtrackingButtons:
        button.draw()
    # title
        # simply draw this on each event (as a class attribute)
    drawRect(app.width/2+app.width/20, app.height/4+app.height/16, 
             app.width/3, app.height/32, fill='white', align='center',
             border=app.titleAutoScheduleBorderColor)
    drawLabel(app.titleAutoSchedule, 
              app.width/2+app.width/20-app.width/6+app.width/300,
              app.height/4+app.height/16,
              fill='black', size=15, italic=True, bold=False, align='left')
    # prefered day of the week?
        # col of all the event
    drawRect(app.width/2+app.width/32, app.height/4+4*app.height/32,
             app.width/6, app.height/32, fill='white', align='center',
             border=app.preferredDayAutoScheduleBorderColor)
    drawLabel(app.preferredDayAutoSchedule, 
              app.width/2+app.width/32-app.width/12+app.width/300, 
              app.height/4+4*app.height/32, fill='black', size=15, 
              italic=True, bold=False, align='left')
    # prefered earliest start time
        # create cellList start from this time(row)
    drawRect(app.width/2-app.width/12, app.height/4+6*app.height/32,
             app.width/12, app.height/32, fill='white', align='center',
             border=app.startAutoScheduleBorderColor)
    drawLabel(app.startAutoSchedule, 
              app.width/2-app.width/12-app.width/24+app.width/300,
              app.height/4+6*app.height/32,
              fill='black', size=15, italic=True, bold=False, align='left')
    # prefered latest end time
        # create cellList end by this time(row-1)
    drawRect(app.width/2+app.width/8+app.width/32, app.height/4+6*app.height/32,
             app.width/12, app.height/32, fill='white', align='center',
             border=app.endAutoScheduleBorderColor)
    drawLabel(app.endAutoSchedule, 
              app.width/2+app.width/8+app.width/32-app.width/24+app.width/300, 
              app.height/4+6*app.height/32, fill='black', size=15,
              italic=True, bold=False, align='left')
    # timespan
        # len(cellList)
    drawRect(app.width/2-app.width/16, app.height/4+8*app.height/32, app.width/12,
             app.height/32, fill='white', align='center',
             border=app.timespanAutoScheduleBorderColor)
    drawLabel(app.timespanAutoSchedule, 
              app.width/2-app.width/16-app.width/24+app.width/300, 
              app.height/4+8*app.height/32, fill='black', size=15, italic=True,
              bold=False, align='left')
    # how many of this event?
        # len(cellListList) which is a 2d list
    drawRect(app.width/2+app.width/8+app.width/20, app.height/4+8*app.height/32, 
             app.width/12, app.height/32, fill='white', align='center',
             border=app.numberAutoScheduleBorderColor)
    drawLabel(app.numberAutoSchedule, 
              app.width/2+app.width/8+app.width/20-app.width/24+app.width/300,
              app.height/4+8*app.height/32, fill='black', size=15, italic=True,
              bold=False, align='left')
    # rest time?
        # len(restCellList)
    # color
        # same as create event
    drawRect(app.width/4+app.width/16, app.height/4+6*app.height/16,
                 app.width/12, app.height/32, align='center', fill='lavender')
    drawLabel('Color', app.width/4+app.width/16, app.height/4+6*app.height/16,
              size=15, italic=True, bold=True)
    drawRect(app.width/2, app.height/4+10*app.height/32, app.width/8, 
             app.height/32, fill='white', align='center')
    drawLabel(app.colorAutoSchedule, app.width/2, app.height/4+10*app.height/32,
              align='center', fill='black', size=12, italic=True, bold=True)

# To-Do List Screen
def toDoList_redrawAll(app):
    drawLabel('To Do List', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)

def toDoList_onMousePress(app, mouseX, mouseY):
    # menu
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
    # menu
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)

def diary_onMousePress(app, mouseX, mouseY):
    # menu
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
    drawLabel(app.count, app.width/2, app.height/2, fill='lightskyblue', 
              size=50, italic=True, bold=True)
    drawLabel('Press s to start the timer', app.width/2, app.height-app.height/4, 
              size=22, italic=True)
    drawLabel('Press p to pause the timer', app.width/2, app.height-3*app.height/16,
              size=22, italic=True)
    drawLabel('Press r to reset the timer', app.width/2, app.height-app.height/8,
              size=22, italic=True)


def timer_onMousePress(app, mouseX, mouseY):
    # menu
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False

def timer_onKeyPress(app, key):
    if key == 'r':
        app.count = 60
        app.paused = True
    elif key == 'p' and (app.count != 60):
        app.paused = True if app.paused == False else False
    elif key == 's':
        app.paused = False

def timer_onStep(app):
    if not app.paused:
        app.count -= 1
    if app.count == 0:
        app.count = 60
        app.paused = True

###############################################################################
# general helper functions
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
                     app.monthCols, row, col)

def drawMonthBoardBorder(app):
    drawRect(app.monthBoardLeft, app.monthBoardTop, app.monthBoardWidth,
             app.monthBoardHeight, fill=None, border='black', 
             borderWidth=2*app.monthCellBorderWidth, opacity=20)

def drawInternalBoard(app):
    for row in range(app.internalRows):
        for col in range(app.internalCols):
            drawCell(app, app.boardLeft, app.boardTop, app.boardWidth, 
                     app.boardHeight, 
                     app.internalRows, app.internalCols, row, col, 0)

# helper of helper functions
def drawCell(app, boardLeft, boardTop, boardWidth, boardHeight, 
             rows, cols, row, col, opacity): 
    cellLeft, cellTop = getCellLeftTop(boardLeft, boardTop, 
                                       boardWidth, boardHeight,
                                       rows, cols, row, col)
    cellWidth, cellHeight = getCellSize(boardWidth, boardHeight,
                                        rows, cols)
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

################################################################################
# event helper
# get (row, col) from mouse click
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app.boardWidth, 
                                        app.boardHeight, 
                                        app.internalRows, app.internalCols)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.internalRows) and (0 <= col < app.internalCols):
      return (row, col)
    else:
      return None

# get time from (row, col)
def getStartTimeFromRow(app, cell):
    time = ''
    row, col = cell
    # every 4 rows, add an hour
    # every row, add 15 minutes
    if row % 4 == 0:
        time = str(int(8+(row/4)))
    else:
        time = f'{int(8+((row-(row%4))/4))}:{15*int((row%4))}'
    return time

def getEndTimeFromRow(app, cell):
    time = ''
    row, col = cell
    
    if row % 4 == 0:
        time = f'{int(8+(row/4))}:{15}'
    else:
        min = row%4
        if min == 3:
            time = str(int(8+((row+1)//4)))
        else:
            time = f'{int(8+((row-min)/4))}:{15*(min+1)}'
    return time

def getDayFromCol(app, cell):
    day = ''
    row, col = cell
    if col == 0:
        day = 'Sunday'
    elif col == 1:
        day = 'Monday'
    elif col == 2:
        day = 'Tuesday'
    elif col == 3:
        day = 'Wednesday'
    elif col == 4:
        day = 'Thursday'
    elif col == 5:
        day = 'Friday'
    elif col == 6:
        day = 'Saturday'
    return day

# get row from time
def getRowFromTime(time):
    hour = 8
    min = 0
    row = 0
    if ':' in time:
        after = time.find(':')
        hour = int(time[:after])
        min = int(time[after+1:])
        row = ((hour-8)*4) + (min//15)
    else:
        hour = int(time)
        row = (hour-8)*4
    return row
      
# get col from day
def getColFromDay(day):
    if day == 'Sunday':
        col = 0
    elif day == 'Monday':
        col = 1
    elif day == 'Tuesday':
        col = 2
    elif day == 'Wednesday':
        col = 3
    elif day == 'Thursday':
        col = 4
    elif day == 'Friday':
        col = 5
    elif day == 'Saturday':
        col = 6
    return col

# get cell list from start time and end time
def getCellList(start, end, day):
    cellList = []
    startRow = getRowFromTime(start)
    # this endRow is not drawn
    endRow = getRowFromTime(end)
    col = getColFromDay(day)
    # endRow is exclive (how it supposed to be)
    for i in range(startRow, endRow):
        cellList.append((i, col))
    return cellList

def getCellListRowStartAndRowEnd(rowStart, rowEnd, col):
    cellList = []
    for i in range(rowStart, rowEnd):
        cellList.append((i, col))
    return cellList

def resetEventInput(app):
    app.typeTitle = False
    app.typeDay = False
    app.typeStart = False
    app.typeEnd = False
    app.titleBorderColor = 'white'
    app.dayBorderColor = 'white'
    app.startBorderColor = 'white'
    app.endBorderColor = 'white'

def resetEventMessage(app):
    app.title = ''
    app.day = ''
    app.start = ''
    app.end = ''
    app.color = ''
    app.cellList = []

def resetAutoScheduleInput(app):
    app.typeTitleAutoSchedule = False
    app.typePreferredDayAutoSchedule = False
    app.typeStartAutoSchedule = False
    app.typeEndAutoSchedule = False
    app.typeTimespanAutoSchedule = False
    app.typeNumberAutoSchedule = False
    app.titleAutoScheduleBorderColor = 'white'
    app.preferredDayAutoScheduleBorderColor = 'white'
    app.startAutoScheduleBorderColor = 'white'
    app.endAutoScheduleBorderColor = 'white'
    app.timespanAutoScheduleBorderColor = 'white'
    app.numberAutoScheduleBorderColor = 'white'

def resetAutoScheduleMessage(app):
    app.titleAutoSchedule = ''
    app.preferredDayAutoSchedule = ''
    app.startAutoSchedule = ''
    app.endAutoSchedule = ''
    app.timespanAutoSchedule = ''
    app.numberAutoSchedule = ''
    app.colorAutoSchedule = ''

# screen setting functions
def setWeekScheduleScreen(app):
    setActiveScreen("weekSchedule")
    app.drawPopUpWindow = False
    app.drawAutoScheduleWindow = False
    app.drawInstructions = False

def setTimerScreen(app):
    setActiveScreen("timer")
    app.drawPopUpWindow = False
    app.drawAutoScheduleWindow = False
    app.drawInstructions = False

# menu button functions
def menuButtonFunction(app):
    app.drawMenu = True if app.drawMenu == False else False

# instructions
def instructionButtonFunction(app):
    if app.drawInstructions == False:
        app.drawInstructions = True
    app.drawConflict = False
    app.drawReminder = False
    app.drawNoEvent = False

def closeInstructionFunction(app):
    app.drawInstructions = False

# 'Create' event pop up window button functions
def createButtonFunction(app):
    if app.drawPopUpWindow == False:
        app.drawPopUpWindow = True
    app.drawConflict = False
    app.drawReminder = False
    app.drawNoEvent = False
    resetEventInput(app)
    resetEventMessage(app)

def closeCreateButton(app):
    app.selectedEvent = None
    resetEventMessage(app)
    app.drawPopUpWindow = False

def titleButtonFunction(app):
    resetEventInput(app)
    app.typeTitle = True
    app.titleBorderColor = 'black'

def dayButtonFunction(app):
    resetEventInput(app)
    app.typeDay = True
    app.dayBorderColor = 'black'

def startButtonFunction(app):
    resetEventInput(app)
    app.typeStart = True
    app.startBorderColor = 'black'

def endButtonFunction(app):
    resetEventInput(app)
    app.typeEnd = True
    app.endBorderColor = 'black'

def orangeredFunction(app):
    app.color = 'orangered'

def sandybrownFunction(app):
    app.color = 'sandybrown'

def lightgreenFunction(app):
    app.color = 'lightgreen'

def paleturquoiseFunction(app):
    app.color = 'paleturquoise'

def lightpinkFunction(app):
    app.color = 'lightpink'

# auto-schedule button functions
def autoScheduleFunction(app):
    if app.drawAutoScheduleWindow == False:
        app.drawAutoScheduleWindow = True
    app.drawConflict = False
    app.drawReminder = False
    app.drawNoEvent = False
    resetAutoScheduleInput(app)
    resetAutoScheduleMessage(app)

def closeAutoScheduleWindow(app):
    app.selectedEvent = None
    resetAutoScheduleMessage(app)
    app.drawAutoScheduleWindow = False

def titleAutoScheduleFunction(app):
    resetAutoScheduleInput(app)
    app.typeTitleAutoSchedule = True
    app.titleAutoScheduleBorderColor = 'black'

def preferredDayAutoScheduleFunction(app):
    resetAutoScheduleInput(app)
    app.typePreferredDayAutoSchedule = True
    app.preferredDayAutoScheduleBorderColor = 'black'

def startAutoScheduleFunction(app):
    resetAutoScheduleInput(app)
    app.typeStartAutoSchedule = True
    app.startAutoScheduleBorderColor = 'black'

def endAutoScheduleFunction(app):
    resetAutoScheduleInput(app)
    app.typeEndAutoSchedule = True
    app.endAutoScheduleBorderColor = 'black'

def timespanAutoScheduleFunction(app):
    resetAutoScheduleInput(app)
    app.typeTimespanAutoSchedule = True
    app.timespanAutoScheduleBorderColor = 'black'

def numberAutoScheduleFunction(app):
    resetAutoScheduleInput(app)
    app.typeNumberAutoSchedule = True
    app.numberAutoScheduleBorderColor = 'black'

def orangeredAutoScheduleFunction(app):
    app.colorAutoSchedule = 'orangered'

def sandybrownAutoScheduleFunction(app):
    app.colorAutoSchedule = 'sandybrown'

def lightgreenAutoScheduleFunction(app):
    app.colorAutoSchedule = 'lightgreen'

def paleturquoiseAutoScheduleFunction(app):
    app.colorAutoSchedule = 'paleturquoise'

def lightpinkAutoScheduleFunction(app):
    app.colorAutoSchedule = 'lightpink'

def saveAutoScheduleFunction(app):
    # default value
    title = '(No Title)'
    preferredDay = None
    start = None
    end = None
    timespan = None
    cellListLength = None
    rawCellListList = None
    number = None
    color = 'lightskyblue'
    # check app.messages conditions:
    if (app.titleAutoSchedule != '') and (len(app.titleAutoSchedule) <= 13):
            title = app.titleAutoSchedule
    if ((app.preferredDayAutoSchedule == 'Monday')or 
        (app.preferredDayAutoSchedule == 'Tuesday') or 
        (app.preferredDayAutoSchedule == 'Wednesday') or 
        (app.preferredDayAutoSchedule == 'Thursday') or 
        (app.preferredDayAutoSchedule == 'Friday') or 
        (app.preferredDayAutoSchedule == 'Saturday') or 
        (app.preferredDayAutoSchedule == 'Sunday')):
            preferredDay = app.preferredDayAutoSchedule
    if ((app.startAutoSchedule != '') and (1<=len(app.startAutoSchedule)<=5)):
        if ((app.startAutoSchedule.isdigit()) and 
            (8 <= int(app.startAutoSchedule) <= 17)):
            start = app.startAutoSchedule
        elif (':' in app.startAutoSchedule) and (app.start.count(':')==1):
            if ((8<=int(app.startAutoSchedule[0])<=9) or 
                (10<=(int(app.startAutoSchedule[0:2]))<=17)):
                index = app.startAutoSchedule.find(':')
                after = app.startAutoSchedule[index+1:]
                if ((after == '00') or (after == '15') or (after == '30') or
                    (after == '45')):
                    start = app.startAutoSchedule
    if ((app.endAutoSchedule != '') and (1<=len(app.endAutoSchedule)<=5)):
        if ((app.endAutoSchedule.isdigit()) and 
            (8 <= int(app.endAutoSchedule) <= 18)):
            end = app.endAutoSchedule
        elif ((':' in app.endAutoSchedule) and 
              (app.endAutoSchedule.count(':')==1)):
            if ((8<=int(app.endAutoSchedule[0])<=9) or 
                (10<=(int(app.endAutoSchedule[0:2]))<=18)):
                index = app.endAutoSchedule.find(':')
                after = app.endAutoSchedule[index+1:]
                if ((after == '00') or (after == '15') or (after == '30') or
                    (after == '45')):
                    end = app.endAutoSchedule
    if app.colorAutoSchedule != None:
        color = app.colorAutoSchedule
    if (app.timespanAutoSchedule != None):
        timespan = app.timespanAutoSchedule
        cellListLength = getCellListLengthFromTimespan(timespan)
    if ((app.numberAutoSchedule != None) and (app.numberAutoSchedule.isdigit())):
        number = int(app.numberAutoSchedule)
    if ((start != None) and (end != None) and (preferredDay != None) and
        (cellListLength != None)):
        rawCellListList = getRawCellListList(start, end, preferredDay,cellListLength)
        print(rawCellListList)
    if (rawCellListList != None) and (number != None):
        cellListList = autoScheduleBacktracking(app, rawCellListList, [], number)
        print(cellListList)
        if (cellListList != []) and (cellListList != None):
            for cellList in cellListList:
                if cellList != []:
                    print('sb')
                    start = getStartTimeFromRow(app, cellList[0])
                    end = getEndTimeFromRow(app, cellList[-1])
                    if ((title != None) and (preferredDay != None) and
                        (start != None) and (end != None) and (color != None) and 
                        (cellList != [])):

                        event = Event(title, preferredDay, start, end, color, 
                                    cellList, eventFunction)
                        app.eventList.append(event)
                else:
                    app.drawNoEvent = True
        else:
            app.drawNoEvent = True
    else:
        app.drawReminder = True
    app.selectedEvent = None
    app.drawAutoScheduleWindow = False
    resetAutoScheduleMessage(app)

def autoScheduleBacktracking(app, rawCellListList, cellListList, num):
    # we found a solution, return it
    if len(cellListList) == num:
        return cellListList
    else:
        # loop through all the possible timeslots (cellLists)
        for cellList in rawCellListList:
            # legality check
            if isLegal(app, cellList):
                cellListList.append(cellList)
                for (row, col) in cellList:
                    app.board[row][col] = 'X'
                # recursively solve
                solution = autoScheduleBacktracking(app, rawCellListList[1:],
                                                    cellListList, num)
                if solution != None:
                    return solution
                for (row, col) in cellList:
                    app.board[row][col] = None
                cellListList.pop()
    return None

# backtracking helper functions
def isLegal(app, cellList):
    for (row, col) in cellList:
        if app.board[row][col] == 'X':
            return False
    return True

def getRawCellListList(start, end, day, cellListLength):
    rawCellListList = []
    rowStart = getRowFromTime(start)
    rowEnd = getRowFromTime(end)
    col = getColFromDay(day)
    for i in range(rowStart, rowEnd):
        cellList = []
        if(i + cellListLength <= rowEnd):
            for k in range(cellListLength):
                cellList.append(((i+k), col))
        rawCellListList.append(cellList)
    while [] in rawCellListList:
        rawCellListList.remove([])
    return rawCellListList

def getCellListLengthFromTimespan(timespan):
    length = None
    if 'h' in timespan:
        hourIndex = timespan.find('h')
        hour = timespan[:hourIndex]
        length = int(hour)*4
    elif 'min' in timespan:
        minIndex = timespan.find('min')
        min = timespan[:minIndex]
        if (min == '00'):
            length = 0
        elif (min == '15'):
            length = 1
        elif (min == '30'):
            length = 2
        elif (min == '45'):
            length = 3
    return length

# event creation helper functions
def eventFunction(app):
    if app.drawPopUpWindow == False:
        app.drawPopUpWindow = True 
    app.drawConflict = False
    app.drawReminder = False
    app.drawNoEvent = False

def checkForConflict(app, cellList):
    if cellList != []:
        for (row, col) in cellList:
            if app.board[row][col] == 'X':
                return True
    return False
    
def clickTimeToCreate(app, selectedCellStart, selectedCellEnd):
    app.selectedEvent = None
    app.day = getDayFromCol(app, selectedCellStart)
    app.start = getStartTimeFromRow(app, selectedCellStart)
    app.end = ''
    app.drawConflict = False
    app.drawReminder = False
    app.drawNoEvent = False
    app.selectedCellStart = None
    app.clickTimeToCreate = False
    app.dragTimeToCreate = False

def dragTimeToCreate(app, selectedCellStart, selectedCellEnd):
    app.selectedEvent = None
    app.day = getDayFromCol(app, selectedCellStart)
    app.start = getStartTimeFromRow(app, selectedCellStart)
    #!!!problem
    app.end = getEndTimeFromRow(app, selectedCellEnd)
    if app.end == None:
        app.end = ''
    app.drawConflict = False
    app.drawReminder = False
    app.drawNoEvent = False
    app.selectedCellStart = None
    app.selectedCellEnd = None
    app.dragTimeToCreate = False
    app.clickTimeToCreate = False

def deleteEventFunction(app):
    # if we know which event we are working with
    # app.eventList.remove(event)
    if app.selectedEvent != None:
        app.eventList.remove(app.selectedEvent)
        for (row, col) in app.selectedEvent.cellList:
            app.board[row][col] = None
    else:
        app.drawReminder = True
    app.selectedEvent = None
    app.drawPopUpWindow = False
    resetEventMessage(app)

def saveEventFunction(app):
    # editing existing event
    # if we know which event we are working with:
    if app.selectedEvent != None:
        title = app.selectedEvent.title
        day = app.selectedEvent.day
        start = app.selectedEvent.start
        end = app.selectedEvent.end
        cellList = app.selectedEvent.cellList
        app.selectedEvent.changeTitle(app.title)
        if ((app.day == 'Monday')or (app.day == 'Tuesday') or (app.day == 'Wednesday')
            or (app.day == 'Thursday') or (app.day == 'Friday') or 
            (app.day == 'Saturday') or (app.day == 'Sunday')):
            app.selectedEvent.changeDay(app.day)
        else:
            app.drawReminder = True
        if ((app.start != '') and (1<=len(app.start)<=5)):
            if (app.start.isdigit()) and (8 <= int(app.start) <= 17):
                app.selectedEvent.changeStart(app.start)
            elif (':' in app.start) and (app.start.count(':')==1):
                if (8<=int(app.start[0])<=9) or (10<=(int(app.start[0:2]))<=17):
                    index = app.start.find(':')
                    after = app.start[index+1:]
                    if ((after == '') or (after == '00') or (after == '15') or 
                        (after == '30') or (after == '45')):
                        app.selectedEvent.changeStart(app.start)
                    else:
                        app.drawReminder = True
                else:
                    app.drawReminder = True
            else:
                app.drawReminder = True
        else:
            app.drawReminder = True
        if ((app.end != '') and (1<=len(app.end)<=5)):
            if (app.end.isdigit()) and (8 <= int(app.end) <= 18):
                app.selectedEvent.changeEnd(app.end)
            elif (':' in app.end) and (app.end.count(':')==1):
                if (8<=int(app.end[0])<=9) or (10<=(int(app.end[0:2]))<=18):
                    index = app.end.find(':')
                    after = app.end[index+1:]
                    if ((after == '') or (after == '00') or (after == '15') or 
                        (after == '30') or (after == '45')):
                        app.selectedEvent.changeEnd(app.end)
                    else:
                        app.drawReminder = True
                else:
                    app.drawReminder = True
            else:
                app.drawReminder = True
        else:
            app.drawReminder = True
        app.selectedEvent.changeColor(app.color)
        if ((app.selectedEvent.start != None) and (app.selectedEvent.end != None) 
            and (app.selectedEvent.day != None)):
            app.cellList = getCellList(app.selectedEvent.start, 
                                       app.selectedEvent.end, 
                                       app.selectedEvent.day)
            if ((app.cellList != None) and (app.cellList != [])):
                conflict = checkForConflict(app, app.cellList)
            else:
                conflict = False
            if ((app.cellList != None) and (app.cellList != []) 
                and (conflict == False)):
                app.selectedEvent.changeCellList(app.cellList)
                for (row, col) in cellList:
                    app.board[row][col] = None
            elif conflict == True:
                app.drawConflict = True
                app.selectedEvent.changeTitle(title)
                app.selectedEvent.changeDay(day)
                app.selectedEvent.changeStart(start)
                app.selectedEvent.changeEnd(end)
            else:
                app.drawReminder = True
                app.selectedEvent.changeTitle(title)
                app.selectedEvent.changeDay(day)
                app.selectedEvent.changeStart(start)
                app.selectedEvent.changeEnd(end)
    # default values
    else:
        title = '(No Title)'
        day = None
        start = None
        end = None
        color = 'lightskyblue'
        cellList = []
        # check if all the attributes meet requirements
        if (app.title != '') and (len(app.title) <= 13):
            title = app.title
        if ((app.day == 'Monday')or (app.day == 'Tuesday') or (app.day == 'Wednesday')
            or (app.day == 'Thursday') or (app.day == 'Friday') or 
            (app.day == 'Saturday') or (app.day == 'Sunday')):
            day = app.day
        if ((app.start != '') and (1<=len(app.start)<=5)):
            if (app.start.isdigit()) and (8 <= int(app.start) <= 17):
                start = app.start
            elif (':' in app.start) and (app.start.count(':')==1):
                if (8<=int(app.start[0])<=9) or (10<=(int(app.start[0:2]))<=17):
                    index = app.start.find(':')
                    after = app.start[index+1:]
                    if ((after == '00') or (after == '15') or (after == '30') or
                        (after == '45')):
                        start = app.start
        if ((app.end != '') and (1<=len(app.end)<=5)):
            if (app.end.isdigit()) and (8 <= int(app.end) <= 18):
                end = app.end
            elif (':' in app.end) and (app.end.count(':')==1):
                if (8<=int(app.end[0])<=9) or (10<=(int(app.end[0:2]))<=18):
                    index = app.end.find(':')
                    after = app.end[index+1:]
                    if ((after == '00') or (after == '15') or (after == '30') or
                        (after == '45')):
                        end = app.end
        if app.color != '':
            color = app.color
        if (start != None) and (end != None) and (day != None):
            cellList = getCellList(start, end, day)
        # create an event
        # conflict == True: meaning there is a conflict
        # conflict == False: meaning there is no conflict
        if cellList != []:
            conflict = checkForConflict(app, cellList)
        else:
            conflict = False
        if ((day != None) and (start != None) and (end != None)
            and (color != None)  and (cellList != []) and (conflict == False)):
            event = Event(title, day, start, end, color, cellList, eventFunction)
        # append the event to app.eventList
            app.eventList.append(event)
        elif conflict == True:
            app.drawConflict = True
        else:
            app.drawReminder = True
    app.selectedEvent = None
    app.drawPopUpWindow = False
    resetEventMessage(app)

def drawConflict(app):
    drawRect(app.width/4-app.width/16, app.height-app.height/12, 
             app.width/2+app.width/8, app.height/12,
             fill='mediumpurple', borderWidth=3, border='slateblue')
    drawLabel('There is a conflict in existing events!', app.width/2, 
              app.height-app.height/24, size=20)

def drawReminder(app):
    drawRect(app.width/4-app.width/16, app.height-app.height/12, 
             app.width/2+app.width/8, app.height/12,
             fill='mediumpurple', borderWidth=3, border='slateblue')
    drawLabel('Something might be wrong!  Check you input!', app.width/2, 
              app.height-app.height/24, size=20)

def drawNoEvent(app):
    drawRect(app.width/4-app.width/16, app.height-app.height/12, 
             app.width/2+app.width/8, app.height/12,
             fill='mediumpurple', borderWidth=3, border='slateblue')
    drawLabel("Sorry, Your event can't be scheduled.", app.width/2, 
              app.height-app.height/24, size=20)

def main():
    runAppWithScreens(width=800, height=800, initialScreen='initialScreen')

main()
