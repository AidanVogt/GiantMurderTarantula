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
# mass in kg
LEG_MASS = 2
TORSO_MASS = 70

# upward leg movement (same for all legs)
KNEE_NEUTRAL = 0
LEG_UP = 150 # amount to move from baseline
PERIOD = 5.0 # seconds — time for one full up-down cycle

# side-to-side leg movement
HIP_NEUTRAL = 0
HIP_PER = 10
HIP_SWING = np.radians(60)

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

def MoveOneLeg(id, val):
    data.ctrl[id] = val
    
# =============================================================================
# Run MuJoCo viewer
# =============================================================================
with mujoco.viewer.launch_passive(model, data) as viewer:
    phase_start = time.time()

    # https://mujoco.readthedocs.io/en/stable/computation/index.html#geactuation 

    # Set the masses
    model.body_mass[body("leg1")] = LEG_MASS
    model.body_mass[body("leg2")] = LEG_MASS
    model.body_mass[body("leg3")] = LEG_MASS
    model.body_mass[body("leg4")] = LEG_MASS
    model.body_mass[body("leg5")] = LEG_MASS
    model.body_mass[body("leg6")] = LEG_MASS
    
    model.body_mass[body("torso")] = TORSO_MASS
    print(model.body_mass)
    
    start = 1

    while viewer.is_running():
        elapsed = time.time() - phase_start
        
        if elapsed >= (PERIOD*2):
            phase_start = time.time()
            elapsed = 0
            start = (start % 2) + 1
        
        # knee up is fine
        knee_target = KNEE_NEUTRAL + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1)
        
        # hip swing
        hip_target = HIP_NEUTRAL + (HIP_SWING * 0.5) * (np.sin(2*np.pi*elapsed/HIP_PER))
        # hip_target = 0.5(HIP_SWING)
        
        if start == 1:
            
            # values for KNEE movement
            act1 = leg1_knee_id
            act2 = leg3_knee_id
            act3 = leg5_knee_id
            
            val1 = knee_target
            val2 = knee_target
            val3 = -knee_target
            
            # values for HIP movement
            hip_act1 = hip1_id
            hip_act2 = hip3_id
            hip_act3 = hip5_id


        elif start == 2:
            act1 = leg4_knee_id
            act2 = leg6_knee_id
            act3 = leg2_knee_id
            
            val1 = -knee_target
            val2 = -knee_target
            val3 = knee_target
            
            # values for HIP movement
            hip_act1 = hip4_id
            hip_act2 = hip6_id
            hip_act3 = hip2_id
        
    
        # MoveTripod(act1, act2, act3, val1, val2, val3)
        # MoveTripod(hip_act1, hip_act2, hip_act3, hip_target, hip_target, -hip_target)
        MoveOneLeg(leg6_knee_id, -150)
        MoveOneLeg(hip6_id, hip_target)

        # # right side, left side same except multiply by -1
        # knee_target = KNEE_NEUTRAL + LEG_UP * .5 * (1 - np.cos(2*np.pi*elapsed/PERIOD) + .1)
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