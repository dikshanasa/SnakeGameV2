import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
high=0
file = open('hs.txt','r')
for l in file:
    high=int(l.strip())
file.close()

curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT                                             
score = 0
snake_body="*"

snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
food = [10,20]                                                     # First food co-ordinates

win.addch(food[0], food[1], 'O')                                   # Prints the food

while key != 27:    # While Esc key is not pressed
    win.border(0)
    win.addstr(0, 2, 'Score ' + str(score) + ' '+ 'High Score' + str(high)+' ')             
    win.addstr(0, 27, ' THE SNAKE ')                                   
    win.timeout(100)          
    
    prevKey = key                                                  # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event 


    if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
        key = -1                                                   
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # check for an invalid key is pressed
        key = prevKey

    # Calculates the new coordinates of the head of the snake. 
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1

    # If snake runs over itself
    if snake[0] in snake[1:]: break

    
    if snake[0] == food:                                            # When snake eats the food
        food = []
        if high<score:
            high=score
            file = open('hs.txt','w')
            file.write(str(high))
            file.close
        score += 1
        while food == []:
            food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
            if food in snake:
                 food = []
        win.addch(food[0], food[1], 'O')
    else:    
        last = snake.pop()                                          # [1] If it does not eat the food, length decreases
        win.addch(last[0], last[1], ' ')
    win.addch(snake[0][0], snake[0][1], '@')
    #snake body
    for seg in snake[1:]:
        win.addch(seg[0],seg[1],snake_body)
    
curses.endwin()
win.addstr(0, 0, "Score:"+str(score)+ "  High Score:"+str(high)+"",curses.A_REVERSE)
print(f"Final score = {score}, high score={high}")