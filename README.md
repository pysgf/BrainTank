# Brain Tank
## Summary
This is a little project to teach programming skills as well as basic AI.
For now you can play with the DummyBrain in brain.py or implement your own.

## Making a Brain
Copy brains/wander.py to brains/yourname.py and add "yourname" it to config.py.
For now it will only read the first two brains listed...

## Simulation Rules
Every time a trank becomes "idle" it will run the `think()` function associated
with that brain to queue up more commands. The tank then executes these, 
which can take a variable amount of time.
Tanks can also fire shots in the direction they are facing. 
They must turn to aim.  The shots move at twice the speed of a tank.

### Tile Rules
  * Crossing dirt will take twice as long as regular tiles.
  * The tank will abort a move if it runs into a blocking tile or other tank.
  * Turning one facing takes half a second, turning twice takes one second.
  * Shots can destroy blocking tiles such as trees or rocks.
  * Driving into water will destroy the tank.

## TODO
  1. Add explosions and other animations.
  2. Add GUI elements like victory screen, etc.

## Requirements
  * [Python 2.7+][http://www.python.org/]
  * [Pyglet][http://pyglet.org/]
    * Windows users should use [pip][http://www.pip-installer.org/] to install
    * OSX users should use [this fork][http://code.google.com/r/evilphillip-cocoa-ctypes/]

## Licensing
The code is GPLv3, but the art is not.

### Attribution
  * The Planet Cute sprites are from the venerable Danc. Check out his [site][http://www.lostgarden.com].
  * The tank is by Saypen on [Open Game Art][http://opengameart.org/content/american-tank].
  * Everything else I've made and is in the public domain.
