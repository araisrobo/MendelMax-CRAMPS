# HAL file for BeagleBone + TCT paralell port cape with 5 steppers and 3D printer board
import os

from machinekit import rtapi as rt
from machinekit import hal
from machinekit import config as c

from config import base
from config import motion

# initialize the RTAPI command client
rt.init_RTAPI()
# loads the ini file passed by linuxcnc
c.load_ini(os.environ['INI_FILE_NAME'])

motion.setup_motion(kinematics=c.find('KINS','KINEMATICS'))

# reading functions
hal.addf('motion-command-handler', 'servo-thread')

# Axis-of-motion Specific Configs (not the GUI)
# X [0] Axis
base.setup_stepper(section='AXIS_0', axisIndex=0, stepgenIndex=0, stepgenType='sim')
# Y [1] Axis
base.setup_stepper(section='AXIS_1', axisIndex=1, stepgenIndex=1, stepgenType='sim')
# Z [2] Axis
base.setup_stepper(section='AXIS_2', axisIndex=2, stepgenIndex=2, stepgenType='sim')
# Z [2] Axis
base.setup_stepper(section='AXIS_3', axisIndex=3, stepgenIndex=3, stepgenType='sim')
# Z [2] Axis
base.setup_stepper(section='AXIS_4', axisIndex=4, stepgenIndex=4, stepgenType='sim')

# Standard I/O - EStop, Enables, Limit Switches, Etc
errorSignals = ['temp-hw-error', 'watchdog-error', 'hbp-error']
base.setup_estop(errorSignals, thread='servo-thread')
base.setup_tool_loopback()

# write out functions
hal.addf('motion-controller', 'servo-thread')

# start haltalk server after everything is initialized
# else binding the remote components on the UI might fail
hal.loadusr('haltalk', wait=True)
