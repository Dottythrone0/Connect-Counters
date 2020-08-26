import mysql.connector
import pygame
from guizero import App, Text, Window, TextBox, PushButton
import random
import time
import math
import numpy as np
import sys


pygame.init()



def read_records_from_db_table():

    #Establish connection to the database
    try:
        connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "HighScores" 
        )
    except: #if the connection is not successful then program execution is halted
        print('database connection error')
        sys.exit()

    cursor = connection.cursor()

    #SQL query to be executed
    sqlQuery1 = """
    SELECT Name, Score
    FROM HighScores
    ORDER BY Name ASC
    """
    #Player array declaration
    players = []

    #executes the SQL query and stores all records returned into a paramater called result
    cursor.execute(sqlQuery1)
    result = cursor.fetchall()
    
    
    #Add each record from the results of the query to the players array
    for record in result:
        players.append(record)
    connection.commit()
    connection.close() #closes database connection

    return players

def get_and_validate_name():
    global enteredName
    enteredName = input_box.value.capitalize() #forces the first character of the name entered to be upper case and stores the name in a variable called enteredName
    if len(enteredName) == 0 or len(enteredName) > 20: #input validation
        error_message.value = 'Please re-enter name. The name you enter should be a maximum of 20 characters'
    else:
        app.destroy() #closes the welcome screen       


def display_Welcome_Screen():
    global app
    app = App(title="Welcome Screen", height=500, width=500, bg = '#99CCFF')
    title = Text(app, text="Welcome to Connect Counters!", size=50)
    instructions_title = Text(app, text='Game instructions:', size=30)
    instruction_1 = Text(app, text='Connect Counters is a single player game where the player attempts to connect as many counters as they can on a 5x4 grid, against an AI. ')
    instruction_2 = Text(app, text='You will take it in turns with the AI to connect or block the AIs counters.')
    instruction_3 = Text(app, text='You can connect Counters in three ways – horizontally, vertically or diagonally.')
    instruction_4 = Text(app, text='The game will stop when the game board is completely full, and the greatest number of counters that you connect is calculated and stored')
    instruction_5 = Text(app, text='An appropriate message will be displayed informing you of the winner of the game and a leader board showing the top 5 scores will also be shown')
    instruction_6 = Text(app, text='The game will randomly choose who will go first and a message will be displayed at all times at the top of the screen informing you whos turn it is')
    instruction_7=Text(app,text='To get started playing, please enter your first name into the name field shown below and press the submit button at the bottom of the page to begin playing') 
    text = Text(app, text="Name:", align='left')
    global input_box
    input_box = TextBox(app, align='left')
    button = PushButton(app, text='Submit', align='bottom', command = get_and_validate_name) #When the user presses the submit button a subroutine that validates the name entered is run
    global error_message
    error_message = Text(app)
    app.display() #updates the welcome screen with text defined as above


def defineGameBoard():
    columns = 5
    rows = 4
    gameBoard = [[0 for x in range(columns)] for y in range(rows)] #creates a 2-D array called gameBoard that has 4 rows and 5 columns

    return rows, columns, gameBoard
    

def displayGameBoard(rows, columns, gameWindow):    
    #draws a blue rectangle 150px down from the top left of the screen of width 1000 and height 600
    pygame.draw.rect(gameWindow, (0, 0, 255), (0, 150, 1000, 600))
    
    for x in range(rows+1):
        for y in range(columns):
            #draws black circles 200 px apart on the x axis, starting at 100px to the right of the edge of the screen
            # and 150px apart vertically starting at 75px from the top of the screen on the y axis
            pygame.draw.circle(gameWindow, (0, 0, 0), (100*x*2 +100 , 75*y*2 +75), 50)

    return gameWindow

    


def decideFirstTurn():
    counter = 0
    choice = ['player', 'ai']
    firstTurn = random.choice(choice) #randomly chooses a random element of the choice array
    if firstTurn != 'player': #checks to see if the element choosen is not equal to 'player'
        counter = 1 #sets counter to 1 for the ai's move if the element chosen is not equal to 'player'
    
    return counter
    
def playerMove(rows, columns, gameBoard, counter, gameWindow, isGridFull):
    font = pygame.font.Font(None, 36) #Choose the font for the text
    text = font.render("It's your turn", 1, (255, 255, 255)) #Create the text
    gameWindow.blit(text, (800, 25))
    
    x, y = pygame.mouse.get_pos() #gets the position of the mouse cursor on the screen as an x and y co-ordinate
    pygame.draw.circle(gameWindow, (255, 0, 0), (x , 75), 50) #draws a circle/counter at the current x position of the mouse cursor
    
    #checks to see if the player has left clicked the mouse cursor over a column and then inserts a player counter into that column provided the column is not full
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and x < 200:
        gameBoard, counter, isGridFull = insert_counter(0, gameBoard, counter, isGridFull)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and x > 200 and x < 400:
        gameBoard, counter, isGridFull = insert_counter(1, gameBoard, counter, isGridFull)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and x > 400 and x < 600:
        gameBoard, counter, isGridFull = insert_counter(2, gameBoard, counter, isGridFull)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and x > 600 and x < 800:
        gameBoard, counter, isGridFull = insert_counter(3, gameBoard, counter, isGridFull)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and x > 800 and x < 1000:
        gameBoard, counter, isGridFull = insert_counter(4, gameBoard, counter, isGridFull)
    

    return counter, gameWindow, isGridFull
            
        

def insert_counter(columnNo, gameBoard, counter, isGridFull):
    
    not_full = False
    x = 3 #starts from the bottom of the gameBoard column
    
    while not_full == False and x >= 0 and counter == 0: #while the column is not full and its the players turn
        if gameBoard[x][columnNo] == 0: #checks to see if current element of the gameBoard is empty
            gameBoard[x][columnNo] = 1 #adds a player counter to that element if it is empty
            not_full = True # condition to exit while loop
            #alternates to the A.I's turn
            counter += 1
            counter = counter % 2
            #checks to see if the gameBoard is full
            isGridFull = check_if_board_is_full(gameBoard, rows, columns, isGridFull) #once a counter is inserted it checks to see if the gameBoard is full
        else:
            x -= 1 # If the bottom element of the gameBoard of that column is full, then it checks the element of that column above
    
    while not_full == False and x >= 0 and counter == 1: #while the column is not full and its the A.I's turn
        if gameBoard[x][columnNo] == 0: #checks to see if current element of the gameBoard is empty
            gameBoard[x][columnNo] = 2 #adds an A.I counter to that element if it is empty
            not_full = True # condition to exit while loop
            #alternates to the A.I's turn
            counter += 1
            counter = counter % 2
            #checks to see if the gameBoard is full
            isGridFull = check_if_board_is_full(gameBoard, rows, columns, isGridFull) #once a counter is inserted it checks to see if the gameBoard is full
        else:
            x -= 1 # If the bottom element of the gameBoard of that column is full, then it checks the element of that column above
        
    

    return gameBoard, counter, isGridFull
        
def draw_counter(gameBoard, rows, columns, gameWindow):
    for x in range(rows):
        for y in range(columns):
            if gameBoard[x][y] == 1:
                #draw a player counter in that element on the gameWindow
                pygame.draw.circle(gameWindow, (255, 0, 0), (100*y*2 +100 , 75*x*2 +225), 50)
            elif gameBoard[x][y] == 2:
                #draw a player counter in that element on the gameWindow
                pygame.draw.circle(gameWindow, (255, 255, 0), (100*y*2 +100 , 75*x*2 +225), 50)#draw yellow counter for ai
                

def check_if_board_is_full(gameBoard, rows, columns, isGridFull):
    total = 0
    for x in range(rows):
        for y in range(columns): #traverse the gameBoard 2-D array
            if gameBoard[x][y] != 0: #check to see if each element of the 2-D array has either the player's or ai's counter
                total += 1 #if the element has a counter in it, then a total variable is incremented by 1

    if total == 20: #checks to see if all 20 elements of the 2-D array are full
        isGridFull = True
        #finds the winner of the game
        find_winner(rows, columns, gameBoard)

    return isGridFull

        
def minimax(gameBoard, depth, alpha, beta, maximisingPlayer, rows, columns, isGridFull):
    gameBoard = np.array(gameBoard)
    #checks to see if the gameBoard is full
    isGridFull = check_if_board_is_full(gameBoard, rows, columns, isGridFull)
    
    #gets each column that is not empty
    valid_columns = return_empty_columns(gameBoard)
   
    #checks to see if current node is terminal
    if depth == 0 or isGridFull:
        if isGridFull:
            return(None, 0)
        else:
            return (None, score_of_each_column(gameBoard)) #calls evaluation function when depth = 0

    if maximisingPlayer:
        value = -math.inf
        column = random.choice(valid_columns)
        for col in valid_columns:
            gameBoard_copy = np.copy(gameBoard) #creates a copy of the gameBoard
            gameBoard_copy, counter, isGridFull = insert_counter(col, gameBoard_copy, 1, isGridFull) #inserts a counter into each empty column
            newScore = minimax(gameBoard_copy, depth-1, alpha, beta, False, rows, columns, isGridFull)[1]
            if newScore > value: #returns the maximum value
                value = newScore
                column = col
            alpha = max(alpha, value)
            if alpha >= beta: #alpha - beta pruning
                break

        return column, value

    else: #minimising player
        value = math.inf
        column = random.choice(valid_columns)
        for col in valid_columns:
            gameBoard_copy = np.copy(gameBoard) #creates a copy of the gameBoard
            gameBoard_copy, counter, isGridFull = insert_counter(col, gameBoard_copy, 0, isGridFull)
            newScore = minimax(gameBoard_copy, depth-1, alpha, beta, True, rows, columns, isGridFull)[1]
            if newScore < value: #returns the minimum value
                value = newScore
                column = col
            beta = min(beta, value)
            if alpha >= beta: #alpha - beta pruning
                break

        return column, value
            
def return_empty_columns(gameBoard):
    count = 0
    valid_columns = []  
    for col in range(5): #for each column
        col_array = [int(i) for i in list(gameBoard[:,col])] #sets col_array to the current column
        for row in range(4): #starts a fixed loop for each element of the current column being looked at
            if col_array[row] == 0: #checks to see if the current element is empty
                count += 1 #counts that element if it is empty
        if count > 0: #if there is at least one empty location
            valid_columns.append(col) #then it adds the column number to an array called valid_columns
            count = 0 #reset count variable to 0 for the next column

    return valid_columns

            
def score_of_each_column(gameBoard):

    #centre column
    
    centre = [int(i) for i in list(gameBoard[:, 5//2])] #sets centre to the third column of board
    
    count = centre.count(2)
    score = count * 3

    #score horizontal
    for row in range(4):
        row_array = [int(i) for i in list(gameBoard[row,:])]  #sets row_array to the current index/row of the gameBoard
        for col in range(2):
            sub_row_array = row_array[col:col+4] #sets window to the first 4 elements of the row_array list
            score += assignScores(sub_row_array)

    #score vertical

    for col in range(5):
        col_array = [int(i) for i in list(gameBoard[:,col])]
        score += assignScores(col_array)


    #score of both diagonals
    #+ve slope diagonal

    for row in range(1):
        for col in range(2):
            pos_diagonal_array = [gameBoard[row+i][col+i] for i in range(4)]
            score += assignScores(pos_diagonal_array)

    #-ve slope diagonal
    for row in range(1):
        for col in range(2):
            neg_diagonal_array = [gameBoard[row+3-i][col+i] for i in range(4)]
            score += assignScores(neg_diagonal_array)
    
    return score
    
def assignScores(sub_array):
    score = 0 #sets score variable to 0
    
    if sub_array.count(2) == 4: #checks to see if there are 4 ai counters/2s in the current array
        score += 100 #adds 100 to the score variable
    elif sub_array.count(2) == 3 and sub_array.count(0) == 1:
        score += 5
    elif sub_array.count(2) == 2 and sub_array.count(0) == 2:
        score += 2

    if sub_array.count(1) == 3 and sub_array.count(0) == 1: #checks to see if there are 3 player counters/1s in the current array
        score -= 4 #subtracts 4 away from the score variable

    return score
      
    

def find_winner(rows, columns, gameBoard):
    playerHighScore = []
    aiHighScore = []

    for x in range((rows)-2): #vertical sequences
        for y in range(columns):
            if gameBoard[x][y] == gameBoard[x+1][y] and gameBoard[x][y] == 1:
                playerHighScore.append(2)
                if gameBoard[x+1][y] == gameBoard[x+2][y]:
                    playerHighScore.append(3)
                    if (gameBoard[x][y] == gameBoard[0][y] and gameBoard[x][y] == gameBoard[3][y]) and x == 1:
                        playerHighScore.append(4)
            elif gameBoard[x][y] == gameBoard[x+1][y] and gameBoard[x][y] == 2:
                aiHighScore.append(2)
                if gameBoard[x+1][y] == gameBoard[x+2][y]:
                    aiHighScore.append(3)
                    if (gameBoard[x][y] == gameBoard[0][y] and gameBoard[x][y] == gameBoard[3][y]) and x == 1:
                        aiHighScore.append(4)
    for x in range(rows): #horizontal sequences
            for y in range((columns)-2):
                if gameBoard[x][y] == gameBoard[x][y+1] and gameBoard[x][y] == 1:
                    playerHighScore.append(2)
                    if gameBoard[x][y+1] == gameBoard[x][y+2]:
                        playerHighScore.append(3)
                        if (gameBoard[x][y] == gameBoard[x][0] or gameBoard[x][y] == gameBoard[x][4]) and y == 1:
                            playerHighScore.append(4)
                            if (gameBoard[x][y] == gameBoard[x][0] and gameBoard[x][y] == gameBoard[x][4]) and y == 1:
                                playerHighScore.append(5)
                elif gameBoard[x][y] == gameBoard[x][y+1] and gameBoard[x][y] == 2:
                    aiHighScore.append(2)
                    if gameBoard[x][y+1] == gameBoard[x][y+2]:
                        aiHighScore.append(3)
                        if (gameBoard[x][y] == gameBoard[x][0] or gameBoard[x][y] == gameBoard[x][4]) and y == 1:
                            aiHighScore.append(4)
                            if (gameBoard[x][y] == gameBoard[x][0] and gameBoard[x][y] == gameBoard[x][4]) and y == 1:
                                aiHighScore.append(5)
                            
    for x in range((rows)-2): #diagonal sequences top left to bottom right
        for y in range((columns)-2):
            if gameBoard[x][y] == gameBoard[x+1][y+1] and gameBoard[x][y] == 1:
                playerHighScore.append(2)
                if gameBoard[x+1][y+1] == gameBoard[x+2][y+2]:
                    playerHighScore.append(3)
                    if ((gameBoard[x][y] == gameBoard[0][0] and gameBoard[x][y] == gameBoard[3][3]) and (x == 1 and y == 1)) or ((gameBoard[x][y] == gameBoard[0][1] and gameBoard[x][y] == gameBoard[3][4]) and (x ==1 and y == 2)):
                        playerHighScore.append(4)
            elif gameBoard[x][y] == gameBoard[x+1][y+1] and gameBoard[x][y] == 2:
                aiHighScore.append(2)
                if gameBoard[x+1][y+1] == gameBoard[x+2][y+2]:
                    aiHighScore.append(3)
                    if ((gameBoard[x][y] == gameBoard[0][0] and gameBoard[x][y] == gameBoard[3][3]) and (x == 1 and y == 1)) or ((gameBoard[x][y] == gameBoard[0][1] and gameBoard[x][y] == gameBoard[3][4]) and (x ==1 and y == 2)):
                        aiHighScore.append(4)

    for x in range((rows)-2): #diagonal sequences top right to bottom left
       for y in range(4, 1, -1):
           if gameBoard[x][y] == gameBoard[x+1][y-1] and gameBoard[x][y] == 1:
               playerHighScore.append(2)
               if gameBoard[x+1][y-1] == gameBoard[x+2][y-2]:
                   playerHighScore.append(3)
                   if ((gameBoard[x][y] == gameBoard[0][3] and gameBoard[x][y] == gameBoard[3][0]) and (x == 1 and y == 2)) or ((gameBoard[x][y] == gameBoard[0][4] and gameBoard[x][y] == gameBoard[3][1]) and (x ==1 and y == 3)):
                       playerHighScore.append(4)
           elif gameBoard[x][y] == gameBoard[x+1][y-1] and gameBoard[x][y] == 2:
                aiHighScore.append(2)
                if gameBoard[x+1][y-1] == gameBoard[x+2][y-2]:
                    aiHighScore.append(3)
                    if ((gameBoard[x][y] == gameBoard[0][3] and gameBoard[x][y] == gameBoard[3][0]) and (x == 1 and y == 2)) or ((gameBoard[x][y] == gameBoard[0][4] and gameBoard[x][y] == gameBoard[3][1]) and (x ==1 and y == 3)):
                        aiHighScore.append(4)
    global playerMax, aiMax
    playerMax = playerHighScore[0]
    aiMax = aiHighScore[0]
    
    #find max algorithm to find the greatest sequence of counters connected by the player
    for x in range(1, len(playerHighScore)):
        if playerHighScore[x] > playerMax:
            playerMax = playerHighScore[x]

    #find max algorithm to find the greatest sequence of counters connected by the player
    
    for x in range(1, len(aiHighScore)):
        if aiHighScore[x] > aiMax:
            aiMax = aiHighScore[x]


    return playerMax, aiMax

    
def display_winner(playerMax, aiMax, gameWindow):
    font = pygame.font.Font(None, 36) #Choose the font for the text
    if playerMax > aiMax:
        text = font.render("You Win!", 1, (0, 0, 0)) #Create the text
        gameWindow.blit(text, (450, 50))        
    elif playerMax < aiMax:
        text = font.render("You lose!", 1, (0, 0, 0)) #Create the text
        gameWindow.blit(text, (500, 50))
    else:
        text = font.render("Draw", 1, (0, 0, 0)) #Create the text
        gameWindow.blit(text, (500, 50))
    text2 = font.render("You connected "+ str(playerMax)+" counters", 1, (0, 0, 0))
    text3 = font.render("The ai connected "+ str(aiMax)+" counters", 1, (0, 0, 0))
    gameWindow.blit(text2, (350, 100))
    gameWindow.blit(text3, (350, 150))

    
    
                    
def binarySearch(enteredName, players, playerMax):
    low = 0
    high = len(players)-1
    found = False
    change = False
    add = False
    position = 0
    while not found and low <= high: #countines to loop until the enteredName is found or until it is determined that the name isn't in the array
        mid = (low + high)//2 #sets mid to the integer value of low + high/2
        if enteredName == players[mid][0]: #checks to see if current element being looked at is equal to the name entered by the user
            position = mid #stores the location of the name
            players[position] = list(players[position]) #changes the record with the enteredName to a list from a tuple to allow for further changes
            found = True #exit loop condition
        elif enteredName > players[mid][0]:
            low = mid + 1 #starts search to the right of the mid location
        else:
            high = mid - 1 #starts search to the left of the mid location
    if found == True and players[position][1] < playerMax: #checks to see if the score associated with the stored record is less than the players new score
        players[position][1] = playerMax #if it is, then their new score is stored
        change = True
    elif found == False: #if there is no occurance of the players name in the array
        player = [enteredName, playerMax]
        players.append(player) #then the players name and score are added to the players array
        add = True
    
    return players, change, add
        
def insertionSort(players):
    for i in range(1, len(players)):
        currentRecord = players[i] #stores the current element of the players array
        position = i #stores the current index of the loop
        while position > 0 and players[position][1] > players[position-1][1]:
            players[position] = players[position-1]
            position -= 1
            players[position] = currentRecord


    leaderBoard = App(title="LeaderBoard", height=500, width=500, bg = '#99CCFF') #defines properties of the leaderBoard
    title = Text(leaderBoard, text="Leaderboard", size=50)
    leaderBoard_headings = Text(leaderBoard, text= "Name "+" Score") #defines text on screen
    if len(players) < 5: #if there are less than 5 players and scores in the players array
        for i in range(0, len(players)-1): #then, display all the records
            leaderBoard_contents = Text(leaderBoard, text= players[i])
    else: #if there are more than 5 players and scores in the players array
        for i in range(5):#then, the first 5 records are displayed
            leaderBoard_contents = Text(leaderBoard, text= players[i])
        
    leaderBoard.display() #updates the leaderBoard screen with the text defined above

def update_DB_table(change, add, playerMax, enteredName):
    
    #Establish connection to the database
    try:
        connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "HighScores" 
        )
    except:
        print('database connection error')
        sys.exit()
    
    cursor = connection.cursor()

    sqlQuery2 = " UPDATE HighScores SET Score = %s WHERE Name = %s"
    sqlQuery3 = "INSERT INTO HighScores(Name, Score) VALUES(%s, %s)"

    if change == True: #if a player score was changed
        cursor.execute(sqlQuery2, (playerMax, enteredName))#then, update the record stored in the database table
        connection.commit()
    elif add == True: #if a new record was added to the player array
        cursor.execute(sqlQuery3, (enteredName, playerMax)) #then, insert the record into the database table
        connection.commit()
    connection.close() #closes the database connection
        
        
    
    

#Main program

players = read_records_from_db_table() #reads the records from the database table into an array called players
display_Welcome_Screen() #displays the welcome screen to the user
rows, columns, gameBoard = defineGameBoard() #creates the gameBoard 2-D array
gameWindow = pygame.display.set_mode((1000, 750)) #creates the gameWindow
pygame.display.set_caption("Connect Counters")
counter = decideFirstTurn() #decides who goes first


isGridFull = False
run = True

while isGridFull == False and run == True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
       run = False
    gameWindow.fill((0, 0, 0))
    gameWindow = displayGameBoard(rows, columns, gameWindow) #displays the gameBoard to the user
    
    if counter == 0: #if its the players turn then check to see if they are clicking the screen to add a counter
       counter, gameWindow, isGridFull = playerMove(rows, columns, gameBoard, counter, gameWindow, isGridFull)
       
    elif counter == 1:
        column, value = minimax(gameBoard, 5, -math.inf, math.inf, True, rows, columns, isGridFull)
        gameBoard, counter, isGridFull = insert_counter(column, gameBoard, counter, isGridFull)

    draw_counter(gameBoard, rows, columns, gameWindow) #draws the counters on the screen
        
    

    pygame.display.update() #updates the display

while isGridFull == True and run == True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
       run = False
    gameWindow.fill((153,204,255))
    display_winner(playerMax, aiMax, gameWindow) #displays the winner of the game to the user
    pygame.display.update() #updates the screen
    time.sleep(5)
    run = False
    pygame.quit()
players, change, add = binarySearch(enteredName, players, playerMax) #checks to see if the player has played before
insertionSort(players) #sorts the players array into descending order of Score and displays the leaderBoard to the user
update_DB_table(change, add, playerMax, enteredName) #makes neccessary changes to the player's record in the database table


  
pygame.quit()




