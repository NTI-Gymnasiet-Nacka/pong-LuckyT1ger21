from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time


move_values = {
    "Up": False,
    "Down": False,
    "W": False,
    "S": False
}


def up_true():
    move_values["Up"] = True


def up_false():
    move_values["Up"] = False


def down_true():
    move_values["Down"] = True


def down_false():
    move_values["Down"] = False


def w_true():
    move_values["W"] = True


def w_false():
    move_values["W"] = False


def s_true():
    move_values["S"] = True


def s_false():
    move_values["S"] = False


def check_for_wall(ball: Ball) -> None:
    global current_time
    if ball.ycor() >= 270 or ball.ycor() <= -260:
        if time.time()-current_time > 0.5:
            ball.bounce_angle()
            current_time = time.time()


def paddle_bounce(ball: Ball):
    global current_time_1
    if time.time()-current_time_1 > 0.5:
        ball.paddle_bounce()
        current_time_1 = time.time()


screen = Screen()
screen.setup(800, 560)
screen.bgcolor("black")
screen.setworldcoordinates(-400+10, -280, 400, 280)
name1 = screen.textinput(title="", prompt="Name of Player1")
name2 = screen.textinput(title="", prompt="Name of Player2")
while True:
    try:
        max_points = screen.textinput(
            title="", prompt="At what score should the match end?")
        max_points = int(max_points)
    except ValueError:
        continue
    break
screen.title("Pong")
screen.tracer(0)
middle_line = Turtle()
middle_line.penup()
middle_line.goto(0, -280)
middle_line.pencolor("gray")
middle_line.pensize(10)
middle_line.pendown()
middle_line.goto(0, 300)
middle_line.color("Black")
for i in range(35):
    middle_line.penup()
    middle_line.goto(10, 2*10*(i+0.5)-280)
    middle_line.pendown()
    middle_line.goto(-10, 2*10*(i+0.5)-280)


current_time = time.time()
current_time_1 = time.time()
screen.update()


def main() -> None:
    game_is_on = True
    scoreboard = Scoreboard(name1=name1, name2=name2)
    ball = Ball()
    paddle_r = Paddle("right")
    paddle_l = Paddle("left")
    screen.onkeypress(up_true, "Up")
    screen.onkeyrelease(up_false, "Up")
    screen.onkeypress(down_true, "Down")
    screen.onkeyrelease(down_false, "Down")
    screen.onkeypress(w_true, "w")
    screen.onkeyrelease(w_false, "w")
    screen.onkeypress(s_true, "s")
    screen.onkeyrelease(s_false, "s")
    while game_is_on:
        screen.update()
        time.sleep(0.0035)
        ball.move()
        if paddle_r.collision(ball.position()):
            paddle_bounce(ball)
        if paddle_l.collision(ball.position()):
            paddle_bounce(ball)
        screen.listen()
        if move_values["Up"]:
            paddle_r.go_up()
        if move_values["Down"]:
            paddle_r.go_down()
        if move_values["W"]:
            paddle_l.go_up()
        if move_values["S"]:
            paddle_l.go_down()
        check_for_wall(ball)
        screen.update()
        if ball.xcor() >= 400:
            ball.round_over(True)
            scoreboard.increase_score_r()
            paddle_l.new_round()
            paddle_r.new_round()

        if ball.xcor() <= -400:
            ball.round_over(False)
            scoreboard.increase_score_l()
            paddle_l.new_round()
            paddle_r.new_round()

        if scoreboard.score_l == max_points or scoreboard.score_r == max_points:
            middle_line.clear()
            ball.reset()
            paddle_l.reset()
            paddle_r.reset()
            if scoreboard.score_l == max_points:
                scoreboard.game_over(False)
            elif scoreboard.score_r == max_points:
                scoreboard.game_over(True)
            game_is_on = False
            screen.update()

    screen.exitonclick()


if __name__ == "__main__":
    main()
