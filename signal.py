from nanonav import BLE

def wait_for_signal(response):
    signal = ''

    while True:
        response = ble.read()       #somehow prevents bluetooth from disconnecting

        #waiting for signal
        if response == 10:
            response = ble.read()

        #feels nothing
        elif response == 0:
            ble.send(5)         #go straight to execution ready
            response = ble.read()
        
        #feels breeze (hole)
        elif response == 1:
            signal = signal + 'B'
            ble.send(10)
            response = ble.read()
        
        #feels stench (wumpus)
        elif response == 2:
            signal = signal + 'S'
            ble.send(10)
            response = ble.read()
        
        #feels glitter (gold)
        elif response == 3:
            signal = signal + 'G'
            ble.send(10)
            response = ble.read()

        #hears scream (wumpus killed)
        elif response == 4:
            signal = signal + 'D'
            ble.send(10)
            response = ble.read()

        #all information received from coordinate, ready to execute next movement
        elif response == 5:
            return signal
        
        else:
            ble.send(10)

ble = BLE(name = 'Sprite1Robot')
response = ble.read()