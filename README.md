# Stereo Camera

ELP 4MP Dual Lens USB using OpenCV, Open Pose

## Install 
- sudo apt-get install python3-tk
- sudo apt-get install python3-pil python3-pil.imagetk
- pip install -r requirements.txt

## Ejecución de la interfaz de configuracion de la cámara
- python src/main.py

## Ejecucion Jetson
- python3 src/jetson.py ROBOT 

### ejemplo:
- python3 src/jetson.py reachy
- python3 src/jetson.py rosmasterx3plus
- python3 src/jetson.py stretch
- python3 src/jetson.py waiter

### ejemplo FPS:
- python3 src/jetson.py reachy 10
- python3 src/jetson.py rosmasterx3plus 10
- python3 src/jetson.py stretch 10
- python3 src/jetson.py waiter 10

## Grid
w izquierda
n centro
e derecha
