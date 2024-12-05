from nanonav import BLE, NanoBot
import time

robot = NanoBot()

#travel directions 1 square each
def n(robot):
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

def s(robot):
    while True:
        if not robot.ir_left() and not robot.ir_right():
            robot.m1_backward(20)
            robot.m2_backward(20)
            time.sleep(0.1)
            robot.stop()
            time.sleep(0)
        elif robot.ir_left() and not robot.ir_right():
            robot.m1_backward(20)
            robot.m2_forward(20)
            time.sleep(0.1)
            robot.stop()
            time.sleep(0)
        elif not robot.ir_left() and robot.ir_right():
            robot.m2_backward(20)
            robot.m1_forward(20)
            time.sleep(0.1)
            robot.stop()
            time.sleep(0)
        elif robot.ir_left() and robot.ir_right():
            robot.m1_backward(25)
            robot.m2_backward(25)
            time.sleep(0.6)
            robot.stop()
            time.sleep(0)
            break

def e(robot):
    robot.m1_backward(20)
    robot.m2_forward(20)
    time.sleep(0.75)
    robot.stop()
    time.sleep(0)
    n(robot)
    robot.m2_backward(20)
    robot.m1_forward(20)
    time.sleep(0.7)
    robot.stop()
    time.sleep(0)

def w(robot):
    robot.m2_backward(20)
    robot.m1_forward(20)
    time.sleep(0.75)
    robot.stop()
    time.sleep(0)
    n(robot)
    robot.m1_backward(20)
    robot.m2_forward(20)
    time.sleep(0.75)
    robot.stop()
    time.sleep(0)

def home(robot):
    for i in range(len(movement)):
        if movement[i] == 'n':
            s(robot)
        elif movement[i] == 'e':
            w(robot)
        elif movement[i] == 's':
            n(robot)
        elif movement[i] == 'w':
            e(robot)

movement = []       #stores order of movements
ble = BLE(name="LDK")
ble.send(4)

while True:
    response = ble.read()

    #north
    if response == 0:
        n(robot)
        movement.append('n')
        ble.send(4)
        response = ble.read()

    #east
    elif response == 1:
        e(robot)
        movement.append('e')
        ble.send(4)
        response = ble.read()

    #south
    elif response == 2:
        s(robot)
        movement.append('s')
        ble.send(4)
        response = ble.read()

    #west
    elif response == 3:
        w(robot)
        movement.append('w')
        ble.send(4)
        response = ble.read()

    #wait for a response
    elif response == 4:
        response = ble.read()

    #command doesn't execute
    elif response == 5:
        movement.pop()      #remove failed movement
        ble.send(4)
        response = ble.read()

    #found gold, retrace steps to starting position
    elif response == 6:
        home(robot)
