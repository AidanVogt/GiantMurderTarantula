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

MASS = 0

# upward leg movement
NEUTRAL = 0
LEG_UP = 150 # amount to move from baseline
PERIOD = 5.0 # seconds — time for one full up-down cycle

HIPN = 0

# LEG 1
HIPN = 0
HIP1_swing = 50 # amount to move from baseline
HIP1_per = 10.0 # seconds — time for one full up-down cycle

# LEG 2
HIP2 = 0
HIP2_swing = 50 # amount to move from baseline
HIP2_per = 10.0 # seconds — time for one full up-down cycle

# LEG 3
HIP3 = 0
HIP3_swing = 2000 # amount to move from baseline
HIP3_per = 10.0 # seconds — time for one full up-down cycle

# LEG 4
HIP4 = 0
HIP4_swing = 100 # amount to move from baseline
HIP4_per = 10.0 # seconds — time for one full up-down cycle

# LEG 5
HIP5 = 0
HIP5_swing = 50 # amount to move from baseline
HIP5_per = 10.0 # seconds — time for one full up-down cycle

# LEG 6
HIP4 = 0
hip_swing = 100 # amount to move from baseline
hip_per = 10.0 # seconds — time for one full up-down cycle

# =============================================================================
# Run MuJoCo viewer
# =============================================================================
with mujoco.viewer.launch_passive(model, data) as viewer:
    phase_start = time.time()

    # https://mujoco.readthedocs.io/en/stable/computation/index.html#geactuation 
    leg1_knee_id = act("knee6_act")
    hip1_id = act("hip6_act")

    
    leg_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "legpart1")
    leg2_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "legpart2")
    print(leg_id)

    # Set the mass
    # model.body_mass[leg_id] = MASS
    # model.body_mass[leg2_id] = MASS
    # print(model.body_mass)
    
    # print(model.body_mass)

    
    while viewer.is_running():
        elapsed = time.time() - phase_start

        # right side
        # knee_target = NEUTRAL + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1)
        hip_target = HIPN + hip_swing * .5 * (np.sin(2*np.pi*elapsed/hip_per))
        
        # left side
        knee_target = (0 + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1))*-1
        
        print("range:", model.actuator_ctrlrange[leg1_knee_id])
        print("ctrl:", data.ctrl[leg1_knee_id])
        print("force:", data.actuator_force[leg1_knee_id])

        data.ctrl[leg1_knee_id] = knee_target
        data.ctrl[hip1_id] = hip_target

        mj.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)
        

# to run script: 
# mjpython hexapod_gait_simulator.py