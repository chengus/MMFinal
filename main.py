from nanonav import BLE, NanoBot
import time

# Create a NanoBot object
robot = NanoBot()

#travel directions 1 square each
def forward(robot):     #1
    while True:
        if not robot.ir_left() and not robot.ir_right():
            robot.m1_forward(17)
            robot.m2_forward(17)
            time.sleep(0.1)
            robot.stop()
            time.sleep(0)
        elif robot.ir_left() and not robot.ir_right():
            robot.m1_forward(20)
            robot.m2_backward(20)
            time.sleep(0.2)
            robot.stop()
            time.sleep(0)
        elif not robot.ir_left() and robot.ir_right():
            robot.m2_forward(20)
            robot.m1_backward(20)
            time.sleep(0.2)
            robot.stop()
            time.sleep(0)
        elif robot.ir_left() and robot.ir_right():
            robot.m1_forward(20)
            robot.m2_forward(20)
            time.sleep(1.25)
            robot.stop()
            time.sleep(0)
            break

def down(robot):    #3?????
    robot.m1_backward(20)
    robot.m2_forward(20)
    time.sleep(2)
    robot.stop()
    time.sleep(0)
    forward(robot)
    robot.m1_backward(20)
    robot.m2_forward(20)
    time.sleep(2)
    robot.stop()
    time.sleep(0)

def right(robot):   #2
    robot.m1_backward(20)
    robot.m2_forward(20)
    time.sleep(0.8)
    robot.stop()
    time.sleep(0)
    forward(robot)
    robot.m2_backward(20)
    robot.m1_forward(20)
    time.sleep(0.8)
    robot.stop()
    time.sleep(0)

def left(robot):
    robot.m2_backward(20)
    robot.m1_forward(20)
    time.sleep(0.8)
    robot.stop()
    time.sleep(0)
    forward(robot)
    robot.m1_backward(20)
    robot.m2_forward(20)
    time.sleep(0.8)
    robot.stop()
    time.sleep(0)

ble = BLE(name="NanoNav1")
ble.send(0)
response = ble.read()

while True:
    #no motion
    if response == 0:
        response = ble.read()

    #move forward 1
    elif response == 1:
        forward(robot)
        ble.send(0)
        response = ble.read()
        #y += 1     coordinate

    #move right
    elif response == 2:
        right(robot)
        ble.send(0)
        response = ble.read()
        #x += 1

    #move down
    elif response == 3:
        down(robot)
        ble.send(0)
        reponse = ble.read()
        #x -= 1

    #move left
    elif reponse == 4:
        left(robot)
        ble.send(0)
        reponse = ble.read()
        #x -= 1
    else:
        break

ble = BLE(name="NanoNav")

ble.send(43)
response = ble.read()
# wait until something changes, indicating a response
while response == 43:
    response = ble.read()
    time.sleep(0.5)

print("Received: ", response)

### test ir sensors ###
while True:
    print(f'left: {robot.ir_left()}    right: {robot.ir_right()}')
    time.sleep(0.5)
