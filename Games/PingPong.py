import turtle as tk

# Window
win = tk.Screen()
win.title("Ping Pong")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)  # Reduces window update to make game smoother

# Score
score_a = 0
score_b = 0


# Paddle A
paddle_a = tk.Turtle()
paddle_a.speed(0)  # Speed of animation. 0 is maximum
paddle_a.shape("square")  # by default its 20x20 pixels
paddle_a.shapesize(stretch_wid=4, stretch_len=0.5)  # making the square bigger
paddle_a.color("white")
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = tk.Turtle()
paddle_b.speed(0)  # Speed of animation. 0 is maximum
paddle_b.shape("square")  # by default its 20x20 pixels
paddle_b.shapesize(stretch_wid=4, stretch_len=0.5)  # making the square bigger
paddle_b.color("white")
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = tk.Turtle()
ball.speed(0)  # Speed of animation not movement. 0 is maximum
ball.shape("circle")  # by default its 20x20 pixels
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2
ball.dy = 0.2

# Pen
pen = tk.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

"""Keyboard control functions"""


def paddle_a_up():
    win.listen()
    y = paddle_a.ycor()
    y += 20  # adds 20 pixels to y
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += 20  # adds 20 pixels to y
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


# Keyboard bindings
win.listen()  # listens/looks for keybord input

win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")

win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

# GameLoop
while True:
    win.update()  # Updates window

    # Moving the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    """ Border checking width=800, height=600 """
    # Hits top border
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1  # 2*-1 = -2. Direction reversed when border is hit

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Hits sides. Reset ball. Give score to opponent
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1

        # score update
        score_a += 1
        pen.clear()
        pen.write(
            f"Player A: {score_a}  Player B: {score_b}",
            align="center",
            font=("Courier", 24, "normal"),
        )

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1

        # score update
        score_b += 1
        pen.clear()
        pen.write(
            f"Player A: {score_a}  Player B: {score_b}",
            align="center",
            font=("Courier", 24, "normal"),
        )

    # Paddle & ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (
        ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40
    ):
        ball.setx(340)
        ball.dx *= -1
    if (ball.xcor() < -340 and ball.xcor() > -350) and (
        ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 50
    ):
        ball.setx(-340)
        ball.dx *= -1
