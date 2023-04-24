from cmu_graphics import *
import random
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
                # date: textInput(num)
                # day: textInput(capital)
                # start: textInput (num)
                # end: textInput(num)
                # color: click to set color
                # save: when click create event
        # month view
            # click date to create
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
        # day view
            # click time to create
            # drag time to create
    # to do list
    # diary
    # tomato clock

class Event:
    def __init__(self, title, date, day, start, end, color, cellList, function):
        self.title = title
        self.date = date
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
            return ((self.date == other.date) and (self.day == self.day) 
                    and (self.start == other.start)
                    and (self.end == other.end))
        
    def __hash__(self):
        return hash(str(self))
    
    # Event class methods
    def changeTitle(self, title):
        self.title = title

    def changeDate(self, date):
        self.date = date

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
            app.date = self.date
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
    app.date = ''
    app.day = ''
    app.start = ''
    app.end = ''
    app.color = ''
    app.cellList = []
    app.typeTitle = False
    app.typeDate = False
    app.typeDay = False
    app.typeStart = False
    app.typeEnd = False
    # boolean
    app.drawReminder = False
    app.drawConflict = False
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
    L = ['orangered', 'sandybrown', 'lightgreen', 'paleturquoise', 'lightpink']
    app.eventButtons = [Buttons('X', 3*app.width/4-app.width/64, 
                                    app.height/4+app.height/64,
                                    app.width/32, app.height/32, 'slateblue', 30,
                                    True, False, closeCreateButton),
        Buttons('Title', app.width/4+app.width/16, 
                                app.height/4+app.height/16, app.width/16, 
                                app.height/32, 'lavender', 30, True, True, 
                                titleButtonFunction),
        Buttons('Date', app.width/4+app.width/16, app.height/4+5*app.height/32,
                app.width/16, app.height/32, 'lavender', 30, True, True,
                dateButtonFunction),
        Buttons('Day', app.width/2+app.width/20, app.height/4+5*app.height/32,
                app.width/16, app.height/32, 'lavender', 30, True, True,
                dayButtonFunction),
        Buttons('Start', app.width/4+app.width/16, app.height/4+4*app.height/16,
                app.width/16, app.height/32, 'lavender', 30, True, True,
                startButtonFunction),
        Buttons('End', app.width/2+app.width/20, app.height/4+4*app.height/16,
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
    for button in app.eventButtons:
        button.checkForPress(app, mouseX, mouseY)
    # rn: pop up window appear on both screen (debug)
    #if app.drawPopUpWindow == True:
        #app.closeCreateButton.checkForPress(app, mouseX, mouseY)

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
    for i in range(11):
        drawLabel(f'{i+8}', centerX, app.scheduleTop+cellHeight*i, size=10,
                  align='center', bold=True)
    # for i in range(4):
    #     drawLabel(f'{i+8}AM', centerX, app.scheduleTop+cellHeight*i, size=8,
    #               align='center')
    # drawLabel('12PM', centerX, app.scheduleTop+cellHeight*4, size=8, 
    #           align='center')
    # for i in range(5,11):
    #     drawLabel(f'{i-4}PM', centerX, app.scheduleTop+cellHeight*i, size=8, 
    #               align='center')
    # draw days on top
    L = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
         'Saturday']
    for i in range(7):
        drawLabel(L[i], app.scheduleLeft+(cellWidth/2)+cellWidth*i, 
                  app.scheduleTop-app.width/50, size=9, align='center')
    # draw internal grid
    drawInternalBoard(app)
    # draw menu
    if app.eventList != []:
        for event in app.eventList:
            event.draw(app)
    # draw create button
    drawCreateButton(app)
    if app.drawPopUpWindow == True:
        drawPopUpWindow(app)
    if app.drawReminder == True:
        drawReminder(app)
    if app.drawConflict == True:
        drawConflict(app)
    drawAutoScheduleButton(app)
    # rn: pop up window and auto schedule window can appear at the same time (De)
    if app.drawAutoScheduleWindow == True:
        drawAutoScheduleWindow(app)
    drawMenuButton(app)
    if app.drawMenu == True:
        drawMenu(app)
    

def weekSchedule_onMousePress(app, mouseX, mouseY):
    app.menuButton.checkForPress(app, mouseX, mouseY)
    if app.drawMenu == True:
        for button in app.menuButtons:
            button.checkForPress(app, mouseX, mouseY)
            if button.checkForPress(app, mouseX, mouseY) == True:
                app.drawMenu = False
    # create & pop up window
    app.createButton.checkForPress(app, mouseX, mouseY)
    # click an empty time to create event
    if (app.drawPopUpWindow == False) and (app.drawAutoScheduleWindow == False):
        app. selectedCellStart = getCell(app, mouseX, mouseY)
        if app.selectedCellStart != None:
            row, col = app.selectedCellStart
            # check if this row & col has an event on or not:
            if ((app.board[row][col] == None) and (app.drawPopUpWindow == False)):
                app.clickTimeToCreate = True
                #app.drawPopUpWindow = True
                #clickTimeToCreate(app, app.selectedCellStart)
    # auto-schedule & window
    app.autoScheduleButton.checkForPress(app, mouseX, mouseY)
    if app.drawAutoScheduleWindow == True:
        if (app.closeAutoSchedule.checkForPress(app, mouseX, mouseY)==True):
            return
    # creating event
    for button in app.eventButtons:
        if (button.checkForPress(app, mouseX, mouseY)==True):
            return
    # edit event
    for event in app.eventList:
            if ((app.drawPopUpWindow == False) and 
                (app.drawAutoScheduleWindow == False) and
                (event.checkForPress(app, mouseX, mouseY) == True)):
                app.selectedEvent = event.returnSelectedEvent(app)
    
        
def weekSchedule_onMouseRelease(app, mouseX, mouseY):
    if (app.clickTimeToCreate == True) and (app.dragTimeToCreate == False):
        if ((app.selectedCellStart != None) and (app.selectedCellEnd != None)):
            app.drawPopUpWindow = True
            clickTimeToCreate(app, app.selectedCellStart, app.selectedCellEnd)
    elif (app.dragTimeToCreate == True) and (app.clickTimeToCreate == True):
        if ((app.selectedCellStart != None) and (app.selectedCellEnd != None)):
            app.drawPopUpWindow = True
            dragTimeToCreate(app, app.selectedCellStart, app.selectedCellEnd)

def weekSchedule_onMouseDrag(app, mouseX, mouseY):
    if (app.drawPopUpWindow == False) and (app.drawAutoScheduleWindow == False):
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
    elif app.typeDate == True:
        if key == 'backspace':
            app.date = app.date[:-1]
        elif len(app.date) < 2:
            if key == 'space':
                app.date = app.title + ' '
            else:
                app.date += key
    elif app.typeDay == True:
        if key == 'backspace':
            app.day = app.day[:-1]
        elif len(app.day) < 12:
            if key == 'space':
                app.day = app.title + ' '
            else:
                app.day += key
    elif app.typeStart == True:
        if key == 'backspace':
            app.start = app.start[:-1]
        elif len(app.start) < 5:
            if key == 'space':
                app.start = app.title + ' '
            else:
                app.start += key
    elif app.typeEnd == True:
        if key == 'backspace':
            app.end = app.end[:-1]
        elif len(app.end) < 5:
            if key == 'space':
                app.end = app.title + ' '
            else:
                app.end += key


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
    #app.closeCreateButton.draw()
    for button in app.eventButtons:
        button.draw()
    # title
    drawRect(app.width/2+app.width/20, app.height/4+app.height/16, 
                app.width/3, app.height/32, fill='white', align='center')
    drawLabel(app.title, app.width/2+app.width/20-app.width/6,
               app.height/4+app.height/16,
              fill='black', size=15, italic=True, bold=False, align='left')
    # date
    drawRect(app.width/2-app.width/12, app.height/4+5*app.height/32,
             app.width/12, app.height/32, fill='white', align='center')
    drawLabel(app.date, app.width/2-app.width/12-app.width/24, 
              app.height/4+5*app.height/32,
              fill='black', size=15, italic=True, bold=False, align='left')
    # day
    drawRect(app.width/2+app.width/8+app.width/32, app.height/4+5*app.height/32,
             app.width/8, app.height/32, fill='white', align='center')
    drawLabel(app.day, app.width/2+app.width/8+app.width/32-app.width/16, 
              app.height/4+5*app.height/32, fill='black', size=15, 
              italic=True, bold=False, align='left')
    # start
    drawRect(app.width/2-app.width/12, app.height/4+4*app.height/16,
            app.width/12, app.height/32, fill='white', align='center')
    drawLabel(app.start, app.width/2-app.width/12-app.width/24,
               app.height/4+4*app.height/16,
              fill='black', size=15, italic=True, bold=False, align='left')
    # end
    drawRect(app.width/2+app.width/8+app.width/32, app.height/4+4*app.height/16,
             app.width/12, app.height/32, fill='white', align='center')
    drawLabel(app.end, app.width/2+app.width/8+app.width/32-app.width/24, 
              app.height/4+4*app.height/16, fill='black', size=15,
              italic=True, bold=False, align='left')
    # draw 'Color'
    drawRect(app.width/4+app.width/16, app.height/4+6*app.height/16,
                 app.width/12, app.height/32, align='center', fill='lavender')
    drawLabel('Color', app.width/4+app.width/16, app.height/4+6*app.height/16,
              size=15, italic=True, bold=True)

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
            time = str(int(8+((row+1)%4)))
        else:
            time = f'{int(8+((row-min)/4))}:{15*(min+1)}'

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
    endRow = getRowFromTime(end)
    col = getColFromDay(day)
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
    app.typeDate = False
    app.typeDay = False
    app.typeStart = False
    app.typeEnd = False

def resetEventMessage(app):
    app.title = ''
    app.date = ''
    app.day = ''
    app.start = ''
    app.end = ''
    app.color = ''
    app.cellList = []

# screen setting functions
def setWeekScheduleScreen(app):
    setActiveScreen("weekSchedule")
    app.drawPopUpWindow = False

def setMonthScheduleScreen(app):
    setActiveScreen("monthSchedule")
    app.drawPopUpWindow = False

def setToDoListScreen(app):
    setActiveScreen("toDoList")
    app.drawPopUpWindow = False

def setDiaryScreen(app):
    setActiveScreen("diary")
    app.drawPopUpWindow = False

def setTimerScreen(app):
    setActiveScreen("timer")
    app.drawPopUpWindow = False

# buttons functions
def menuButtonFunction(app):
    app.drawMenu = True if app.drawMenu == False else False

def createButtonFunction(app):
    if app.drawPopUpWindow == False:
        app.drawPopUpWindow = True
    app.drawConflict = False
    app.drawReminder = False
    resetEventInput(app)
    resetEventMessage(app)

def closeCreateButton(app):
    app.selectedEvent = None
    resetEventMessage(app)
    app.drawPopUpWindow = False

def autoScheduleFunction(app):
    if app.drawAutoScheduleWindow == False:
        app.drawAutoScheduleWindow = True

def closeAutoScheduleWindow(app):
    app.drawAutoScheduleWindow = False

def titleButtonFunction(app):
    resetEventInput(app)
    app.typeTitle = True

def dateButtonFunction(app):
    resetEventInput(app)
    app.typeDate = True

def dayButtonFunction(app):
    resetEventInput(app)
    app.typeDay = True

def startButtonFunction(app):
    resetEventInput(app)
    app.typeStart = True

def endButtonFunction(app):
    resetEventInput(app)
    app.typeEnd = True

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

def eventFunction(app):
    if app.drawPopUpWindow == False:
        app.drawPopUpWindow = True 
    app.drawConflict = False
    app.drawReminder = False

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
    if selectedCellEnd != None:
        app.end = getEndTimeFromRow(app, selectedCellEnd)
    if app.end == None:
        app.end = ''
    app.drawConflict = False
    app.drawReminder = False
    app.selectedCellStart = None
    app.clickTimeToCreate = False

def dragTimeToCreate(app, selectedCellStart, selectedCellEnd):
    app.selectedEvent = None
    app.day = getDayFromCol(app, selectedCellStart)
    app.start = getStartTimeFromRow(app, selectedCellStart)
    app.end = getStartTimeFromRow(app, selectedCellEnd)
    if app.end == None:
        app.end = ''
    app.drawConflict = False
    app.drawReminder = False
    app.selectedCellStart = None
    app.selectedCellEnd = None
    app.dragTimeToCreate = False

def deleteEventFunction(app):
    # if we know which event we are working with
    # app.eventList.remove(event)
    if app.selectedEvent != None:
        app.eventList.remove(app.selectedEvent)
    else:
        app.drawReminder = True
    app.selectedEvent = None
    app.drawPopUpWindow = False
    resetEventMessage(app)

def saveEventFunction(app):
    # editing existing event
    # if we know which event we are working with:
    if app.selectedEvent != None:
        app.selectedEvent.changeTitle(app.title)
        app.selectedEvent.changeDate(app.date)
        app.selectedEvent.changeDay(app.day)
        app.selectedEvent.changeStart(app.start)
        app.selectedEvent.changeEnd(app.end)
        app.selectedEvent.changeColor(app.color)
        app.cellList = getCellList(app.start, app.end, app.day)
        app.selectedEvent.changeCellList(app.cellList)
    # default values
    else:
        title = '(No Title)'
        date = None
        day = None
        start = None
        # get end an hour after start
        end = None
        color = 'lightskyblue'
        cellList = []
        # check if all the attributes meet requirements
        if (app.title != '') and (len(app.title) <= 25):
            title = app.title
        if ((app.date != '') and (app.date.isdigit()) and (len(app.date) <= 2) and 
            (1<=int(app.date)<=31)):
            date = app.date
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
        if (start != None) and (end != None):
            cellList = getCellList(start, end, day)
        # create an event
        # conflict == True: meaning there is a conflict
        # conflict == False: meaning there is no conflict
        if cellList != []:
            conflict = checkForConflict(app, cellList)
        else:
            conflict = False
        if ((date != None) and (day != None) and (start != None) and (end != None)
            and (color != None) and (conflict == False)):
            event = Event(title, date, day, start, end, color, cellList, eventFunction)
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

def main():
    # runApp(width=800, height=800)
    runAppWithScreens(width=800, height=800, initialScreen='initialScreen')

main()
