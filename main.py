import turtle, functools, time, random

#sets the score for both players at 0
score = [0, 0]

def createPaddle(pos):
    # creates the left paddle
    paddle = turtle.Turtle()
    #sets the speed to the fastest
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("black")
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    #prevents it from drawing a line as it moves
    paddle.penup()
    paddle.goto(pos[0], pos[1])
    return paddle

def createBall(pos, speed):
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("black")
    ball.penup()
    ball.goto(pos[0], pos[1])
    ball.dx = speed
    ball.dy = speed
    return ball

#creates a display so the user can see the scores
def createPen():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("black")
    #this is so it doesnt leave lines when its moved
    pen.penup()
    #hides the turtle, we just want to see the text
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Player 1: 0 Player 2: 0", align="center", font=("Courier", 24, "normal"))
    return pen

def bindKeys(win, leftPaddle, rightPaddle):
    win.listen()
    #function that actually binds the key
    def bind(paddle, upKey, downKey):
        #binds a paddle to the move up function
        win.onkeypress(functools.partial(moveUp, paddle), upKey)
        #binds a paddle to the movedown function
        win.onkeypress(functools.partial(moveDown, paddle), downKey)

    #binds the keys for the left paddle
    bind(leftPaddle, "w", "s")
    #binds the keys for the right paddle
    bind(rightPaddle, "Up", "Down")

#function to move up
def moveUp(paddle):
    #gets the y coordinate of the paddle
    y = paddle.ycor()
    y += 40
    paddle.sety(y)

def moveDown(paddle):
    # gets the y coordinate of the paddle
    y = paddle.ycor()
    y -= 40
    paddle.sety(y)

#function is called whenever a somebody scores
def newRound(ball):
    #gets the new direction for the X and Y directions (negative or positive)
    xDir = random.randint(0, 1)
    yDir = random.randint(0, 1)

    #0 is negative, 1 is positive
    if xDir == 0:
        ball.dx *= -1

    if yDir == 0:
        ball.dy *= -1

#when a player scores, this function handles that
def playerScored(win, ball, player, pen):
    print(player + " scored")

    if player == "left":
        score[0] += 1
    else:
        score[1] += 1

    ball.goto(0, 0)
    ball.dx *= -1
    win.update()

    #updates the score for the user
    pen.clear()
    pen.write("Player 1: " + str(score[0]) + " Player 2: " + str(score[1]), align="center", font=("Courier", 24, "normal"))

    time.sleep(1)

    newRound(ball)

#function starts the main game loop
def mainLoop(win, leftPaddle, rightPaddle, ball, width, height, ballSpeed, pen):
    #Main Game Loop
    while True:
        #updates the screen every loop
        win.update()

        #begin moving the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        #if left paddle scores
        if ball.xcor() >= (width/2):
            playerScored(win, ball, "left", pen)


        #if right paddle scores
        if ball.xcor() <= -(width / 2):
            playerScored(win, ball, "right", pen)

        #checks the borders for y
        if ball.ycor() > (height/2) or ball.ycor() <= -(height/2):
            ball.dy *= -1

        #paddle and ball collisions
        #if the ball hits the right paddle
        if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < rightPaddle.ycor() + 40) and (ball.ycor() > rightPaddle.ycor() - 40):
            ball.setx(340)
            ball.dx *= -1

        # #if the ball hits the right paddle
        if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < leftPaddle.ycor() + 40) and (ball.ycor() > leftPaddle.ycor() - 40):
            ball.setx(-340)
            ball.dx *= -1

#creates and initializes everything
def start():
    # creates window
    win = turtle.Screen()
    win.title("Pong")
    win.bgcolor("white")

    #all the settings for configuration basically
    width = 800
    height = 600
    ballSpeed = 0.10

    win.setup(width=width, height=height)
    # doesn't update the frame - we update it ourselves w the gameloop (i think)
    win.tracer(0)

    #creates the paddles
    leftPaddle = createPaddle([-350, 0])
    rightPaddle = createPaddle([350, 0])
    #creates ball, passes position and speed
    ball = createBall([0, 0], ballSpeed)

    #begins listing to keys
    bindKeys(win, leftPaddle, rightPaddle)

    #creates a pen to keep track of the score
    pen = createPen()

    #starts the mainloop
    mainLoop(win, leftPaddle, rightPaddle, ball, width, height, ballSpeed, pen)

start()