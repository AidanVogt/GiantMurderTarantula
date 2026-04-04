import mujoco as mj
import mujoco.viewer
import numpy as np
import time

# load hexapod model from config
model = mj.MjModel.from_xml_path("hexapod.xml")
data  = mj.MjData(model)

# XML REF
# Actuators 
# 0-5: hip1, hip2, hip3, hip4, hip5, hip6
# 6-11: knee1, knee2, knee3, knee4, knee5, knee6

def act(name):
    return mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)

# phase matrices (L1, L2, L3, L4, L5, L6)
TRIPOD_GAIT = np.array([
    0, np.pi, 0,
    np.pi, 0, np.pi,
])

# specify which legs move in tandem
tripod_group1 = [
    (act("hip1_act"), act("knee1_act")), # front right
    # (act("hip3_act"), act("knee3_act")), # back right
    # (act("hip5_act"), act("knee5_act")), # middle left
]
tripod_group2 = [
    (act("hip2_act"), act("knee2_act")),   # front left
    (act("hip4_act"), act("knee4_act")),   # mid right
    (act("hip6_act"), act("knee6_act")),   # back left
]


# set globals 
STEP_HEIGHT   = 0.2   # angle (rad) to lift leg
STEP_FORWARD  = 0.6  # angle (rad) for forward stroke
STEP_BACK     = -0.6  # angle (rad) for back stroke (stance push)
SWING_TIME    = 0.5   # seconds for swing phase
STANCE_TIME   = 0.5   # seconds for stance phase
DURATION = 2

def SetTripod(group, hip_angle, knee_angle, ctrl):
    print(group)
    for hip, knee in group:
        ctrl[hip] = hip_angle
        ctrl[knee] = knee_angle

def SetStance(group, ctrl):
    """Leg on ground, pushing backward."""
    # SetTripod(group, hip_angle=STEP_BACK, knee_angle=0.0, ctrl=ctrl)
    SetTripod(group, hip_angle=0, knee_angle=0.0, ctrl=ctrl)

def SetSwing(group, ctrl):
    """Leg lifted and swinging forward."""
    # SetTripod(group, hip_angle=STEP_FORWARD, knee_angle=STEP_HEIGHT, ctrl=ctrl)
    pass

def Test(group, ctrl):
    SetTripod(group, 0, 10, ctrl)


# =============================================================================
# Run MuJoCo viewer
# =============================================================================

# true dir = forward, false = backward
# true dir = CW, false = CCW
DIR = True 

with mujoco.viewer.launch_passive(model, data) as viewer:
    phase = 0  # 0 = A swings, 1 = B swings
    phase_start = time.time()

    while viewer.is_running():
        now = time.time()
        elapsed = now - phase_start
        duration = DURATION

        if elapsed > 10:
            phase = 1 - phase   # flip phase
            phase_start = now
            elapsed = 0

        if phase == 0:
            Test(tripod_group1, data.ctrl)
        # else:
            
        #     Test(tripod_group2, data.ctrl)

        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)
        
    

# to run script: 

# mjpython hexapod_gait_simulator.py