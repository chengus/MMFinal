from nanonav import BLE, NanoBot
import time

robot = NanoBot()

def turn_left_90(robot):
    robot.m2_backward(20)
    robot.m1_forward(20)
    time.sleep(0.75)
    robot.stop()
    time.sleep(0)

def turn_right_90(robot):
    robot.m1_backward(20)
    robot.m2_forward(20)
    time.sleep(0.75)
    robot.stop()
    time.sleep(0)

def move_one_block(robot):
    while True:
        if not robot.ir_left() and not robot.ir_right():
            robot.m1_forward(20)
            robot.m2_forward(20)
            time.sleep(0.05)
            robot.stop()
            time.sleep(0)
        elif robot.ir_left() and not robot.ir_right():
            robot.m1_forward(15)
            robot.m2_backward(15)
            time.sleep(0.1)
            robot.stop()
            time.sleep(0)
        elif not robot.ir_left() and robot.ir_right():
            robot.m2_forward(15)
            robot.m1_backward(15)
            time.sleep(0.1)
            robot.stop()
            time.sleep(0)
        elif robot.ir_left() and robot.ir_right():
            robot.m1_forward(25)
            robot.m2_forward(25)
            time.sleep(0.9)
            robot.stop()
            time.sleep(0)
            break

#as directional travels
def e(robot):
    turn_right_90(robot)
    move_one_block(robot)
    turn_left_90(robot)

def w(robot):
    turn_left_90(robot)
    move_one_block(robot)
    turn_right_90(robot)

def n(robot):
    move_one_block(robot)

def s(robot):
    turn_right_90(robot)
    turn_right_90(robot)
    move_one_block(robot)
    turn_right_90(robot)
    turn_right_90(robot)

def figure_8(robot):
    n(robot)
    e(robot)
    n(robot)
    w(robot)
    s(robot)
    e(robot)
    s(robot)
    w(robot)

ble = BLE(name="LDK")
ble.send(7)

while True:
    response = ble.read()

    #north
    if response == 5:
        n(robot)
        ble.send(7)
        response = ble.read()

    #east
    elif response == 3:
        e(robot)
        ble.send(7)
        response = ble.read()

    #south
    elif response == 0:
        s(robot)
        ble.send(7)
        response = ble.read()

    #west
    elif response == 1:
        w(robot)
        ble.send(7)
        response = ble.read()

    #figure 8
    elif response == 2:
        figure_8(robot)
        ble.send(7)
        response = ble.read()

    #wait for a response
    elif response == 7:
        response = ble.read()

