from cmu_graphics import *
import random

# ideas:
# Schedule for Working (9 to 5) or (8 to 6)
# create event class

# Questions:
    # How to delete a class item?
    # How to align coordinate position to time?
    # How to make my board bigger (and how to adjust coordinates)?
    # How precise should my scheduler be in terms of time?
    # How do I update my app with real time?
    # complexity:
        # 1. let user draw?
        # 2. let user choose background color?
        # 3. ???


# to-do list
    # set up draw screen boolean
    # what colors choices to be included?
    # what time choices to be included?
    # user interface
    # add other screens
    # write helper functions
    # feature: edit and delete event
    # pop up window algorithm:
        # 1. boolean for each text entry?
            # select first, then enter text/number

# data: board = 800 x 800
    # initial screen
        # Peppermint Time: width/2. height/4
        # schedule: width/2, height/3
        # to do list: width/2, height/3 + height/6
    # schedule = 
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

###############################################################################
# new to do list
    # buttons class \/
        # create buttons according to screens
        # 
    # draw screens
        # month
        # week
        # day
    # create event
    # (maybe) day or week boundary
    # datetime module
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
        bottom = self.centerY-(self.height/2)
        if (left <= mouseX <= right) and (top <= mouseY <= bottom):
            self.function(app)


def onAppStart(app):
    # coordinates
    app.scheduleLeft = app.width/16
    app.scheduleTop = app.height/4
    app.scheduleWidth = app.width-app.width/8
    app.scheduleHeight = app.height/2+app.height/8
    # draw schedule helper 
    app.rows = 10
    app.cols = 7
    app.boardLeft = app.scheduleLeft
    app.boardTop = app.scheduleTop
    app.boardWidth = app.scheduleWidth
    app.boardHeight = app.scheduleHeight
    app.cellBorderWidth = app.width/400
    app.eventList = []
    app.drawMenu = False
    app.drawPopUpWindow = False
    # change screen helper
    app.drawInitialScreen = True
    app.drawSchedule = False
    app.drawToDoList = False
    app.drawDiary = False
    app.drawTimer = False
    app.drawMonthView = False
    app.drawWeekView = False
    # buttons
        # menu(recuring)
            #schedule(m)
            # to do list(m)
            # diary(i)
            # tomato clock(m)
        # schedule(i)
            # create(recuring)
                # colors
                # 
            # close create
        # to do list(i)
        # diary(i)
        # tomato clock(i)
    app.initialButtons = initialButtons
    app.menuButton = Buttons('Menu', app.width/40, app.height/80, app.width/20,
                             app.height/40, 'lightskyblue',15, True, True,
                             menuButtonFunction)

def redrawAll(app):
    # menu
    # schedule
        # change view button
        # create button
            # pop up window
        # month view
        # week view
        # day view
    # to-do list
    # diary
    # tomato clock




    # menu button is always drawn
    drawMenuButton(app)
    #for button in app.buttons:
        #button.draw()
    # draw initial screen
    if app.drawInitialScreen == True:
        # drawInitialScreen(app)
    # draw schedule
    # if app.drawSchedule == True:
        drawBoard(app)
        drawBoardBorder(app)
        #drawSchedule(app)
        drawEvents(app)
        drawCreateButton(app)
        if app.drawPopUpWindow == True:
            drawPopUpWindow(app)
    if app.drawMenu == True:
        drawMenu(app)
    # draw to-do list
    #if app.drawToDoList == True:
        #drawToDoList(app)
    # draw diary
    #if app.drawDiary == True:
        #drawDiary(app)
    # draw timer
    #if app.drawTimer == True:
        #drawTimer(app)

###############################################################################
# screen design Drawing Functions
# draw initial screen
def initialScreen_redrawAll(app):
    #centerX = app.width/2
    #height = app.height/16
    #L = ['Schedule', 'To Do List', 'Diary', 'Tomato Clock']
    drawLabel('Peppermint Time', app.width/2, app.height/4, fill='royalblue',
              size=45, italic=True, bold=True)
    drawMenuButton(app)
    for button in app.initialButtons:
        button.draw()
    #for i in range (4):
        #drawRect(centerX, app.height/2+2*i*height, app.height/4,
                 #height, fill='lightskyblue', align='center')
        #drawLabel(f'{L[i]}', app.width/2, app.height/2+2*i*height, 
                  #align='center',size=25, bold=True, italic=True)
        
        
    #drawLabel('To Do List')
    #drawRect(app.width/2,)
    #drawLabel('Diary')
    #drawRect(app.width/2,)
    #drawLabel('Tomato Clock')
 
    
# draw schedule
def schedule_redrawAll(app):
    # drawTitle
    drawLabel('Schedule', app.width/2, app.height/8, fill='skyblue', 
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

    # draw days on top
    L = [('Monday', 50), ('Tuesday',100), ('Wednesday', 150), ('Thursday', 200),
        ('Friday', 250), ('Saturday', 300), ('Sunday', 350)]
    for day, width in L:
        drawLabel(day, width, 91, size=9)

# draw pop up window for creating an event
def drawPopUpWindow(app):
    # background panel
    drawRect(100, 100, 200, 200, fill='mediumpurple', borderWidth=3,
             border='slateblue')
    drawRect(285, 100, 15, 15, fill='slateblue')
    drawLabel('X', 292.5, 107.5, size=10)
    # title
    drawLabel('Title:', 110, 125, size=15, align='left')
    drawRect(150, 115, 130, 25, fill='white')
    # day
    drawLabel('Day:', 110, 175, size=15, align='left')
    drawRect(150, 165, 80, 25, fill='white')
    # start time
    drawLabel('Start:', 110, 225, size=15, align='left')
    drawRect(150, 215, 45, 25, fill='white')
    # end time
    drawLabel('End:', 205, 225, size=15, align='left')
    drawRect(245, 215, 45, 25, fill='white')
    # color
    drawLabel('Color:', 110, 275, size=15, align='left')
    L = ['orangered', 'sandybrown', 'lightgreen', 'paleturquoise', 'lightpink']
    for i in range(5):
        drawCircle(165+i*30, 275, 10, fill=L[i])

def drawEvents(app):
    pass

# draw the 'Create' button
def drawCreateButton(app):
    drawRect(320, 35, 50, 30, fill='lightskyblue')
    drawLabel('Create', 345, 50, fill='black', align='center')

# draw menu
def drawMenu(app):
    drawRect(0, 0, 120, 250, fill='lavender')
    # schedule
    drawRect(60, 50, 95, 25, fill='lightskyblue', align='center')
    drawLabel('Schedule', 60, 50, size=15, align='center')
    # to-do list
    drawRect(60, 100, 95, 25, fill='lightskyblue', align='center')
    drawLabel('To-Do List', 60, 100, size=15, align='center')
    # diary
    drawRect(60, 150, 95, 25, fill='lightskyblue', align='center')
    drawLabel('Diary', 60, 150, size=15, align='center')
    # timer
    drawRect(60, 200, 95, 25, fill='lightskyblue', align='center')
    drawLabel('Tomato Clock', 60, 200, size=15, align='center')
    # draw menu button
    drawMenuButton(app)

def drawMenuButton(app):
    app.menuButton.draw()
    # menu
    #drawRect(0, 0, 20, 20, fill='skyblue')
    #for i in range(3):
        #drawLine(5, 5+5*i, 15, 5+5*i, fill='black', opacity=50)
    

# draw To-Do List
def toDoList_redrawAll(app):
    drawLabel('To Do List', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)

# draw diary
def drawDiary(app):
    drawLabel('Diary', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)

# draw timer
def drawTimer(app):
    drawLabel('Tomato Clock', app.width/2, app.height/8, fill='skyblue', 
              size=30, italic=True, bold=True)

# User Interface
def onMousePress(app, mouseX, mouseY):
    for button in app.buttons:
        button.checkForPress(app, mouseX, mouseY)
    # click to show menu
    if (0 <= mouseX <= 20) and (0 <= mouseY <= 20):
        app.drawMenu = True if app.drawMenu==False else False
    # show schedule screen
    if app.drawMenu == True:
        if (12.5 <= mouseX <= 107.5) and (37.5 <= mouseY <= 62.5):
            reset(app)
            app.drawSchedule = True
            app.drawMenu = False
    # click to show pop up window
    if (app.drawMenu == False) and (app.drawSchedule == True):
        if (320 <= mouseX <= 370) and (35 <= mouseY <= 65):
            app.drawPopUpWindow = True
    # click to close pop up window
        if (285 <= mouseX <= 300) and (100 <= mouseY <= 115):
            app.drawPopUpWindow = False
    # show to do list screen
    if app.drawMenu == True:
        if (12.5 <= mouseX <= 107.5) and (87.5 <= mouseY <= 112.5):
            reset(app)
            app.drawToDoList = True
            app.drawMenu = False
    # show diary screen
    if app.drawMenu == True:
        if (12.5 <= mouseX <= 107.5) and (137.5 <= mouseY <= 162.5):
            reset(app)
            app.drawDiary = True
            app.drawMenu = False
    # show timer screen
    if app.drawMenu == True:
        if (12.5 <= mouseX <= 107.5) and (187.5 <= mouseY <= 212.5):
            reset(app)
            app.drawTimer = True
            app.drawMenu = False

    # create @ current time?
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

###############################################################################
# helper functions
# draw
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

def distance(x, y, a, b):
    return (((x-a)**2)+((y-b)**2))**0.5

# need to be finished
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

# buttons
initialButtons = [Buttons('Schedule', app.width/2, app.height/2, app.height/4, 
                app.height/16, 'lightskyblue', 25, True, True, 
                setActiveScreen('schedule')),
        Buttons('To Do List', app.width/2, app.height/2+2*app.height/16,
                app.height/4, app.height/16, 'lightskyblue', 25, True,
                True, setActiveScreen('toDoList')),
        Buttons('Diary', app.width/2, app.height/2+2*2*app.height/16, 
                app.height/4, app.height/16, 'lightskyblue', 25, True, True, 
                setActiveScreen('diary')),
        Buttons('Tomato Clock', app.width/2, app.height/2+2*3*app.height/16,
                app.height/4, app.height/16, 'lightskyblue', 25, True, True,
                setActiveScreen('timer'))
]


# buttons functions
def menuButtonFunction(app):
    app.drawMenu = True


def main():
    runApp(width=800, height=800)
    runAppWithScreens(initialScreen='initialScreen')

main()
