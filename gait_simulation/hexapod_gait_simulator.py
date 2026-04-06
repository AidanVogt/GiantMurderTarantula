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
# NEUTRAL = 95.0
# LEG_UP = 20.0 # degrees to move from baseline
# PERIOD = 5.0 # seconds — time for one full up-down cycle

NEUTRAL = 95.0
LEG_UP = 40 # degrees to move from baseline
PERIOD = 5.0 # seconds — time for one full up-down cycle

# =============================================================================
# Run MuJoCo viewer
# =============================================================================
with mujoco.viewer.launch_passive(model, data) as viewer:
    phase_start = time.time()

    leg1_knee_id = act("knee1_act")
    print(leg1_knee_id)
    print(model.body_mass)
    
    while viewer.is_running():
        elapsed = time.time() - phase_start

        knee_target = NEUTRAL + LEG_UP * np.sin(2*np.pi*elapsed/PERIOD)
        
        print("range:", model.actuator_ctrlrange[leg1_knee_id])
        print("qpos:", data.qpos[model.jnt_qposadr[
            mj.mj_name2id(model, mj.mjtObj.mjOBJ_JOINT, "knee1_joint")
        ]])
        print("ctrl:", data.ctrl[leg1_knee_id])
        print("force:", data.actuator_force[leg1_knee_id])

        data.ctrl[leg1_knee_id] = knee_target

        mj.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)
        

# to run script: 
# mjpython hexapod_gait_simulator.py