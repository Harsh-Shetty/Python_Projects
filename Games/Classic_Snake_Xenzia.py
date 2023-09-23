import turtle
import random
import time

delay = 0.1
score = 0
highest_score = 0

# Snake Body
bodies = []

# Screen
s = turtle.Screen()
s.title("Classic Snake Xenzia")
s.bgcolor("white")  # 337315 shade of green (darker side)
s.tracer(0)
s.setup(width=600, height=600)  # Co-ordinate system. X-axis: +300  to -300

# border at the bottom to demarcate space for Scorebord
turtle.speed(5)
turtle.pensize(2)
turtle.penup()
turtle.goto(-310, -275)
turtle.pendown()
turtle.color("black")
turtle.forward(600)
turtle.penup()
turtle.ht()

# Creating Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("blue")
head.penup()  # Pen up so the snake doesn't draw a line as it passes
head.goto(0, 0)  # spwan at centre
head.direction = "stop"

#  Snake Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("white")
food.fillcolor("red")
food.penup()
food.goto(0, 200)

# Scoreboard
sb = turtle.Turtle()
sb.color("black")
sb.penup()
sb.ht()
sb.goto(-290, -290)
sb.write("Score: 0 | Highest Score: 0")


def moveup():
    if head.direction != "down":
        head.direction = "up"


def movedown():
    if head.direction != "up":
        head.direction = "down"


def moveleft():
    if head.direction != "right":
        head.direction = "left"


def moveright():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()  # Y-coordinate of head
        head.sety(y + 20)  #  move 20 units in the positive side (up)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)


# Key Mapping
s.listen()
s.onkey(moveup, "Up")  # Up = Up Arrow key
s.onkey(movedown, "Down")
s.onkey(moveleft, "Left")
s.onkey(moveright, "Right")

# Main Loop
while True:
    s.update()  # Updating the Screen
    # When collision with border of Screen appear of the opposite side
    if head.xcor() > 290:
        head.setx(-290)
    if head.xcor() < -290:
        head.setx(290)
    if head.ycor() > 290:
        head.sety(-245)
    if head.ycor() < -245:
        head.sety(290)
    # Collision with food
    if head.distance(food) < 20:
        # move food to Random location
        x = random.randint(-290, 290)
        y = random.randint(-245, 290)
        food.goto(x, y)

        # Defining snake body & its increase of Length functionality
        body = turtle.Turtle()
        body.speed(0)
        body.shape("square")
        body.color("#2c447a")
        body.penup()
        bodies.append(body)  # append Body of Snake to the empty list bodies
        # created in line 10

        # increase Score
        score += 10

        # change delay
        delay -= 0.001

        # update highest_score. highest_score isn't saved permanentaly
        # Every time the code is run it is set t0 0
        if score > highest_score:
            highest_score = score
        sb.clear()  # clear Scoreboard
        sb.write(f"Score: {score} | Highest Score: {highest_score}")

    # moving Snake body (turtle objects) one by one
    for index in range(len(bodies) - 1, 0, -1):
        a = bodies[index - 1].xcor()
        b = bodies[index - 1].ycor()
        bodies[index].goto(a, b)
    if len(bodies) > 0:
        a = head.xcor()
        b = head.ycor()
        bodies[0].goto(a, b)
    move()  # initiating move Function. Moving with Keyboard input

    # collision with Snake Body
    for body in bodies:
        if body.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Clear bodies after collision & reset game
            for body in bodies:
                body.ht()
            bodies.clear()
            score = 0
            delay = 0.1

            # Update Scoreboard
            sb.clear()
            sb.write(f"Score: {score} | Highest Score: {highest_score}")
    time.sleep(delay)
s.mainloop()
