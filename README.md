# Giant Murder Tarantula Codebase
Our Website: https://sites.google.com/andrew.cmu.edu/giant-murder-tarantula/home

## Raspberry Pi Controls

The main files containing hexapod control logic are:

* main.py - main loop to convert Xbox input to hexapod movements
* gait_and_homing.py - functions to execute gait and homing commands
* i2c_comm.py - functions that handle sending data via I2C to Arduinos
* gaits.py - hardcoded gait movements
* joystick.py - functions to get values from Xbox joystick

## Arduino Controls

## Gait Simulation

* Conducted using MuJoCo, see gait_simulation directory for more details



https://sites.google.com/d/1mQd9A9ggBaWYSEkpAFHCOtGRjD__ACP-/p/1qHZSDDsDbNPuRTwRIgGkmJGMPe2rVlEq/edit
