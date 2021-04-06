#TAN YONG DE S10185158K
#P08
#5 Aug 2019
#######################
#      Maze Game      #
#   PRG1 Assignment   #
#######################

#Program Description
#====================
#This program allows the user to input their own file to play a maze game in which the map is based upon the file.
#Users will be able to view, configure, export as well as create their own maze if they do not have one.
#Users can also play their maze using Raspberry Pi and challenge their friends via the leaderboard feature.

""" ========== Start of Functions ========== """
#The try and except block in Python is used to catch and handle exceptions. (meant for validation)

#Function to display options in main menu
def main_menu():
    menu_list = ["Read and load maze from file", "View maze", "Play maze game", \
             "Configure current maze", "Export maze to file", "Create new maze", \
             "Play maze using SenseHAT", "View leaderboard", "Exit Maze"]
    print("MAIN MENU")
    print("{:=<9}".format(""))
    for i in range(len(menu_list)):
        if i == len(menu_list)-1:
            print()
            print("[{}] {}".format(0, menu_list[i])) #for option 0 - Exit Maze Game
        else:
            print("[{}] {}".format(i + 1, menu_list[i]))     
    try:
        option = int(input("\nEnter your option: ")) #Check if option is an integer
        return option
    except ValueError:
        print("\nPlease only enter the options stated on the menu\n")
    
#Function to display options in configuration menu (for option 4 configuring the maze)          
def config_menu():
    menu_list = ["Create Wall (X)", "Create Passageway (O)", "Create Start Point (A)", \
                 "Create End Point (B)", "Exit to Main Menu"]
    print("CONFIGURATION MENU")
    print("{:=<25}".format(""))
    for i in range(len(menu_list)):
        if i == len(menu_list)-1:
            print()
            print("[{}] {}".format(0, menu_list[i])) #for option 0 - Exit Configuration Menu
        else:
            print("[{}] {}".format(i + 1, menu_list[i]))

#This function is used to find the coordinates of the start point (row by column) of the maze list
def start(maze_list):
    matrixA = []
    for row in maze_list:
        if "A" in row:
            rowA = matrixA.append(maze_list.index(row))
            columnA = matrixA.append(row.index("A"))
    return matrixA

#This function is used to find the coordinates of the start point (row by column) of the maze list
def end(maze_list):
    matrixB = []
    for row in maze_list:
        if "B" in row:
            rowB = matrixB.append(maze_list.index(row))
            columnB = matrixB.append(row.index("B"))
    return matrixB

#This function is used to open user-input file, store it in a nested loop according to the lines read in the file and load it
def load_maze(file_name):
    maze_list = [] #Turn the list into nested list according to the amount of lines read
    file = file_name
    for item in file:
        temp_list = []
        for element in item:   
            if element.upper() == "X" or element.upper() == "O" or element.upper() == "A" or element.upper() == "B": #only takes in X,O,A,B elements from the file input
                temp_list.append(element) #append all items in the file into a temp list
        maze_list.append(temp_list) #append all the temp lists into a nested list
    file.close()
    return maze_list

#This function is used to view the maze list created
def view_maze(maze_list):
    for i in maze_list:
        print(i)

#This function is used to allow the user to control and play the game
def play_maze(game_list,control):    
    rowA = start(game_list)[0]
    columnA = start(game_list)[1]

    if control == "W":
        if game_list[rowA-1][columnA] == "B":
            return False
        elif game_list[rowA-1][columnA] == "X":
            print("Invalid movement. Please try again.")
        else:
            game_list[rowA-1][columnA], game_list[rowA][columnA] = game_list[rowA][columnA], game_list[rowA-1][columnA] #To swap "A" with "O" 
   
    elif control == "S":
        if game_list[rowA+1][columnA] == "B":
            return False
        elif game_list[rowA+1][columnA] == "X":
            print("Invalid movement. Please try again.")
        else:
            game_list[rowA+1][columnA], game_list[rowA][columnA] = game_list[rowA][columnA], game_list[rowA+1][columnA] 

    elif control == "A":
        if game_list[rowA][columnA-1] == "B":
            return False
        elif game_list[rowA][columnA-1] == "X":
            print("Invalid movement. Please try again.")
        else:
            game_list[rowA][columnA-1], game_list[rowA][columnA] = game_list[rowA][columnA], game_list[rowA][columnA-1]

    elif control == "D":
        if game_list[rowA][columnA+1] == "B":
            return False
        if game_list[rowA][columnA+1] == "X":
            print("Invalid movement. Please try again.")
        else:
            game_list[rowA][columnA+1], game_list[rowA][columnA] = game_list[rowA][columnA], game_list[rowA][columnA+1]

#This function is used to replace the game items e.g.(X,O,A,B)
def config_maze(maze_list,choice,row,column):
    if choice == 1:
        maze_list[row][column] = "X"
    if choice == 2:
        maze_list[row][column] = "O"
    if choice == 3:
        maze_list[row][column] = "A"
    if choice == 4:
        maze_list[row][column] = "B"
    return maze_list

#This function is used to export the maze list into a file
def export_maze(filename,maze_list):
    records = 0
    file = open(filename,"w+")
    for items in maze_list:
        records +=1
        file.writelines(items)
        file.write("\n")
    file.close()
    print("File {} has been created with {} records.".format(filename,records))
     
#This function is used to create a new list according to the dimensions input by the user
def create_maze(dimensions):
    d_list = dimension.split(",")
    maze_list = []
    for row in range(int(d_list[0])):
        sublist = []
        for column in range(int(d_list[1])):
            sublist.append("X")
        maze_list.append(sublist)

    print("A new maze of {} by {} has been created.".format(int(d_list[0]),int(d_list[1])))
    print("Please run configure maze to start configuring new maze.")
    return maze_list

#This function is used to allow the users to play their maze on a Raspberry Pi
def senseHat_maze(maze_list,matrixA):
    from sense_hat import SenseHat
    sense = SenseHat()

    #For Raspberry Pi, the x and y axis are opposite of the maze_list's. So for x in Raspberry Pi i put the value of Y from the maze_list, vice versa.
    x = matrixA[1]
    y = matrixA[0]

    #This is to set the colors to the pixel
    X = [128,128,128] #Grey
    O = [0,0,0] #Black
    B  = [0,255,0] #Green
    A = [255,0,0] #Red
                    
    map = []
    row = 0
    col = 0
    #This 2 loops are to calculate the row and column of the maze. Only 8 by 8 maze is allowed for this option to work.
    for sublist in range(len(maze_list)):
        row += 1
    for val in range(len(maze_list[sublist])):
        col += 1
        
    if (row,col) != (8,8):
        print("Please use an 8 by 8 maze.")
        return
    else:
        for sublist in maze_list: #The purpose of this to convert the nested list(maze_list) into a 64-length list
            for val in sublist:
                if val == "X":
                   map.append(X)
                elif val == "O":
                    map.append(O)
                elif val == "B":
                    map.append(B)
                elif val == "A":
                    map.append(A)
   
    sense.set_pixels(map)
    sense.set_pixel(x, y, A)
    play = True
    while play:
      for event in sense.stick.get_events():
        if event.action == "pressed":
          sense.set_pixel(x, y, O)
          
          #y > 0 prevents the user from going over the map. maze_list[y-1][x] prevents the user from touching the wall(X)
          if event.direction == "up" and y > 0 and maze_list[y-1][x] != "X": 
            if maze_list[y-1][x] == "B":
              play = False
            else: 
              y = y - 1
              
          elif event.direction == "down" and y < 7 and maze_list[y+1][x] != "X":
            if maze_list[y+1][x] == "B":
              play = False
            else: 
              y = y + 1
              
          elif event.direction == "left" and x > 0 and maze_list[y][x-1] != "X":
            if maze_list[y][x-1] == "B":
              play = False
            else:
              x = x - 1

          elif event.direction == "right" and x < 7 and maze_list[y][x+1] != "X":
            if maze_list[y][x+1] == "B":
              play = False
            else:
              x = x + 1
              
          else: #If the direction is middle, do nothing
              pass
          sense.set_pixel(x, y, A)
          
    if play == False:
        sense.show_message("You have completed the maze!", text_colour=[101,67,33],back_colour=[0,0,0]) #brown text, black background
    sense.clear()
    
#This function sorts the score in the leaderboard(nested list) in a descending order          
def sort_leaderboard(leaderboard):
    for i in range(0, len(leaderboard)): 
        for j in range(0, len(leaderboard)-1): 
            if (leaderboard[j][1] < leaderboard[j + 1][1]): 
                leaderboard[j], leaderboard[j+1] = leaderboard[j + 1], leaderboard[j] #Swap the position of the lists
    return leaderboard 

""" ========== End of Functions ========== """

step_list = [] #Used to store the amount of steps made by the user to complete the maze
name_list = [] #Used to store the player's input name
while True:
    
    option = main_menu()
    
    if option == 1: #Reading and loading the maze

        print("Option [1]: Read and load maze from file")
        print("{:=<40}".format(""))
        print()
        file_name = input("Enter the name of the data file ")
        try:
            file_name = open(file_name)
            maze_list = load_maze(file_name) #Load maze function
            print("Number of lines read: {}".format(len(maze_list)))
        except FileNotFoundError:
            print("File not found, please try again.")
        except OSError: #Invalid File Path
            print("Invalid file path, please try again.")
            
        print()
        
    elif option == 2: #Viewing the maze

        print("Option [2]: View Maze")
        print("{:=<40}".format(""))
        print()
        try:
            view_maze(maze_list) #View maze function
        except NameError:
            print("Please make a maze list first.")
        
        print()

    elif option == 3: #Playing the maze
        
        from copy import deepcopy
        print("Option [3]: Play maze game")
        print("{:=<40}".format(""))
        print()
        try:
            maze_list 
            try:
                len(start(maze_list)) == 2 and len(end(maze_list)) == 2 #Check for a start and end point
                game_list = deepcopy(maze_list) #Duplicate another list without affecting the original
                view_maze(game_list)
                print()
                print("Location of Start (A) = (Row {}, Column {})".format(start(game_list)[0],start(game_list)[1]))
                print("Location of End (B) = (Row {}, Column {})".format(end(game_list)[0],end(game_list)[1]))
                print()
                directions = ["W","A","S","D","M"]
                game = True
                steps = 0      
                while True:
                    print()
                    control = input("Press 'W' for UP, 'A' for LEFT, 'S' for DOWN, 'D' for RIGHT, 'M' for MAIN MENU ").upper()
                    if control in directions:
                        if control == directions[-1]:
                            break
                        else:
                            steps += 1
                            game = play_maze(game_list,control) #Call the game movement function
                            if game == False:
                                print()
                                print("Congratulations you have completed the maze in {} steps!".format(steps))
                                name = input("Please enter your name ")
                                step_list.append(steps)
                                name_list.append(name)
                                break
                            else:
                                print()
                                for i in game_list:
                                    print(i)
            except IndexError:
                print("Please configure your maze so that you have a start and end point (A,B).")           
        except NameError:
            print("Please make a maze list first.")
            
        print()

    elif option == 4: #Configuring the maze

        print("Option [4]: Configure current maze")
        print()
        print("{:=<40}".format(""))
        print()
        try:
            view_maze(maze_list)
            print()
            config_menu()
            configure = True
            while configure:
                print()
                choice = input("Enter your option ")
                print()
                try:
                    choice = int(choice) 
                    if choice >= 1 and choice <= 4:
                        print("Enter the coordinates of the item you wish to change E.G. Row, Column ")
                        row = int(input("Enter the row "))
                        column = int(input("Enter the column "))
                        print()
                        maze_list = config_maze(maze_list,choice,row,column) #Config maze function
                        view_maze(maze_list)
                    elif choice == 0:
                        configure = False
                        break
                    else:
                        print("\nPlease enter options shown in the configuration menu.\n")
                        config_menu() #Function for displaying configuration menu
                        
                except ValueError: #Checks whether choice input is an integer
                    print("\nPlease enter options shown in the configuration menu.\n")
                    config_menu()
                except IndexError: #Checks for coordinates
                    print("\nCoordinates not found. Please try again. \n")
                    view_maze(maze_list)         
        except NameError:
            print("Please make a maze list first.")
            
        print()

    elif option == 5: #Exporting the maze

        print("Option [5]: Export maze to file")
        print()
        print("{:=<35}".format(""))
        print()
        try:
            maze_list
            filename = input("Enter filename to save to: ")
            export_maze(filename,maze_list)  #Export maze function
        except NameError:
            print("Please make a maze list first.\n")
        except FileNotFoundError:
            print("Please enter file name.\n")
                        
    elif option == 6: #Creating new maze

        print("Option [6]: Create new maze")
        print()
        print("{:=<35}".format(""))
        print()
        choice = input("This will empty the current maze. Are you sure?(Y or N): ").upper()
        print()
        if choice == "Y":
            try:
                dimension = input("Enter the dimension of the maze (row, column): ")
                maze_list = create_maze(dimension)
            except IndexError:
                print("Please enter dimension (row, column).")
            except ValueError:
                print("Please enter the dimension (row, column) in integers.")
                
        print()

    elif option == 7: #Sensehat
        
        try:
            matrixA = start(maze_list) #Used to allow the senseHat function to have the co-ordinates of the start point (A)
            senseHat_maze(maze_list,matrixA) #SenseHat function *Only works for Raspberry Pi
        except NameError:
            print("\nPlease make a maze list first.\n")
        except ModuleNotFoundError:
            print("Please use this option on a Raspberry Pi.\n")
            
    elif option == 8: #View leaderboard
        
        print("Option [8]: View leaderboard")
        print()
        print("{}{:>30}".format("Name","Score"))
        print("{:=<35}".format(""))
        leaderboard = []
        score_list = []
        for i in step_list: #Convert steps to score
            if i <= 23: #It takes 23 steps to complete the original maze game
                score = 3000
            else:
                score = 3000 - ((i - 23) * 50)
            score_list.append(score)
            
        for x in range(len(name_list)):
            leaderboard.append([name_list[x],score_list[x]]) #Make a nested list
    
        leaderboard = sort_leaderboard(leaderboard) #Function to sort the leaderboard in descending order (according to score)
        for x in range(len(leaderboard)):
            print("{:<10}{:>25}".format(leaderboard[x][0],leaderboard[x][1]))
            
    elif option == 0:
        
        print("Exiting...")
        break
    
    else:
        print("\nPlease enter the options shown on the menu.\n")
