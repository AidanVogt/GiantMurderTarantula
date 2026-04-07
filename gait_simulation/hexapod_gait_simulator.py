import mujoco as mj
import mujoco.viewer
import numpy as np
import time

# load hexapod model from config
# model = mj.MjModel.from_xml_path("hexapod.xml")
model = mj.MjModel.from_xml_path("hexapod.xml")
data  = mj.MjData(model)

# XML REF
# Actuators 
# 0-5: hip1, hip2, hip3, hip4, hip5, hip6
# 6-11: knee1, knee2, knee3, knee4, knee5, knee6

def act(name):
    return mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)

def body(name):
    return mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)

# specify which legs move in tandem
tripod_group1 = [
    (act("hip1_act"), act("knee1_act")), # front right
    (act("hip3_act"), act("knee3_act")), # back right
    (act("hip5_act"), act("knee5_act")), # middle left
]
tripod_group2 = [
    (act("hip2_act"), act("knee2_act")),   # front left
    (act("hip4_act"), act("knee4_act")),   # mid right
    (act("hip6_act"), act("knee6_act")),   # back left
]


# testing

MASS = 2

# upward leg movement
NEUTRAL = 0
LEG_UP = 150 # amount to move from baseline
PERIOD = 5.0 # seconds — time for one full up-down cycle

HIPN = 0
HIP_PER = 10

# LEG 1
HIPN = 0
HIP1_swing = 20 # amount to move from baseline
HIP1_per = 10.0 # seconds — time for one full up-down cycle

# LEG 2
HIP2 = 0
HIP2_swing = 20 # amount to move from baseline
HIP2_per = 10.0 # seconds — time for one full up-down cycle

# LEG 3
HIP3 = 0
HIP3_swing = 20 # amount to move from baseline
HIP3_per = 10.0 # seconds — time for one full up-down cycle

# LEG 4
HIP4 = 0
HIP4_swing = 20 # amount to move from baseline
HIP4_per = 10.0 # seconds — time for one full up-down cycle

# LEG 5
HIP5 = 0
HIP5_swing = 20 # amount to move from baseline
HIP5_per = 10.0 # seconds — time for one full up-down cycle

# LEG 6
HIP6 = 0
HIP6_swing = 20 # amount to move from baseline
HIP6_per = 10.0 # seconds — time for one full up-down cycle

# actuators
leg1_knee_id = act("knee1_act")
hip1_id = act("hip1_act")

leg2_knee_id = act("knee2_act")
hip2_id = act("hip2_act")

leg3_knee_id = act("knee3_act")
hip3_id = act("hip3_act")

leg4_knee_id = act("knee4_act")
hip4_id = act("hip4_act")

leg5_knee_id = act("knee5_act")
hip5_id = act("hip5_act")

leg6_knee_id = act("knee6_act")
hip6_id = act("hip6_act")

def MoveTripod(act1, act2, act3, val1, val2, val3):
    data.ctrl[act1] = val1
    data.ctrl[act2] = val2
    data.ctrl[act3] = val3


def MoveTripodGroupA(leg1, leg2, leg3, elapsed):
    # move each leg up and down to start
    
    knee_target = NEUTRAL + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1)
    
    data.ctrl[leg1] = knee_target
    data.ctrl[leg2] = knee_target
    data.ctrl[leg3] = -knee_target
    
def MoveTripodGroupB(leg1, leg2, leg3, elapsed):
    
    knee_target = NEUTRAL + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1)
    
    data.ctrl[leg1] = -knee_target
    data.ctrl[leg2] = -knee_target
    data.ctrl[leg3] = knee_target
    
    

# =============================================================================
# Run MuJoCo viewer
# =============================================================================
with mujoco.viewer.launch_passive(model, data) as viewer:
    phase_start = time.time()

    # https://mujoco.readthedocs.io/en/stable/computation/index.html#geactuation 

    # Set the mass
    model.body_mass[body("leg1")] = MASS
    model.body_mass[body("leg2")] = MASS
    model.body_mass[body("leg3")] = MASS
    model.body_mass[body("leg4")] = MASS
    model.body_mass[body("leg5")] = MASS
    model.body_mass[body("leg6")] = MASS
    
    model.body_mass[body("torso")] = 140
    print(model.body_mass)
    
    start = 1

    while viewer.is_running():
        elapsed = time.time() - phase_start
        
        if elapsed >= (PERIOD*2):
            phase_start = time.time()
            elapsed = 0
            start = (start % 2) + 1
            
        knee_target = NEUTRAL + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1)
        # hip_target = HIPN + swing * .5 * (np.sin(2*np.pi*elapsed/HIP_PER))
        
        if start == 1:
            act1 = leg1_knee_id
            act2 = leg3_knee_id
            act3 = leg5_knee_id
            
            val1 = knee_target
            val2 = knee_target
            val3 = -knee_target


        elif start == 2:
            act1 = leg4_knee_id
            act2 = leg6_knee_id
            act3 = leg2_knee_id
            
            val1 = -knee_target
            val2 = -knee_target
            val3 = knee_target
            
        
    
        MoveTripod(act1, act2, act3, val1, val2, val3)
        

        # # right side, left side same except multiply by -1
        # knee_target = NEUTRAL + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1)
        # hip_target = HIPN + swing * .5 * (np.sin(2*np.pi*elapsed/HIP_PER))
        
        # if start == 4 or start == 5 or start == 6:
        #     knee_target *= -1
    
        # data.ctrl[leg_id] = knee_target
        # data.ctrl[hip_id] = hip_target

        mj.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)
        

# to run script: 
# mjpython hexapod_gait_simulator.py


# print("range:", model.actuator_ctrlrange[leg1_knee_id])
# print("ctrl:", data.ctrl[leg1_knee_id])
# print("force:", data.actuator_force[leg1_knee_id])