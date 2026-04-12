import mujoco as mj
import mujoco.viewer
import numpy as np
import time
import sys

# load hexapod model from config
model = mj.MjModel.from_xml_path("hexapod.xml")
data  = mj.MjData(model)

# helpers
def act(name):
    return mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)

def body(name):
    return mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)

# =============================================================================
# Constants and actuators
# =============================================================================

# mass in kg
LEG_MASS = 2
TORSO_MASS = 70

# seconds — time for one full up-down cycle
PERIOD = 5.0 
LEG_UP = 100 # upward leg movement (same for all legs)
HIP_SWING = np.radians(40)

DUTY_CYCLE = 0.4

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

# =============================================================================
# Gait Functions
# =============================================================================

def MoveTripod(act1, act2, act3, val1, val2, val3):
    data.ctrl[act1] = val1
    data.ctrl[act2] = val2
    data.ctrl[act3] = val3

def MoveOneLeg(id, val):
    data.ctrl[id] = val
    

def WiggleInPlace(elapsed):
    """ Coolness factor """
    
    # side1 hip
    hip_target = (HIP_SWING * 0.5) * (np.sin(2*np.pi*elapsed/PERIOD) + .1)
    
    # side2 hip
    grounded_hip_target = (HIP_SWING * 0.5) * (np.sin(2*np.pi*(elapsed + PERIOD)/PERIOD))
    
    # right side
    MoveOneLeg(hip1_id, hip_target)
    MoveOneLeg(hip3_id, hip_target)
    MoveOneLeg(hip5_id, hip_target)
    
    # left side
    MoveOneLeg(hip2_id, grounded_hip_target)
    MoveOneLeg(hip4_id, grounded_hip_target)
    MoveOneLeg(hip6_id, grounded_hip_target)
    

def DutyCycle(elapsed, phase_offset=0.0):
    """
    Returns (knee_lift, hip_angle) for a leg with a given phase offset.
    knee_lift is 0 when grounded, 1 when fully lifted.
    """
    
    # normalize time to [0, 1) within this period, with offset
    t = ((elapsed - phase_offset) % PERIOD) / PERIOD  # 0.0 to 1.0

    # --- KNEE: only lift during swing phase ---
    if t < DUTY_CYCLE:
        # swing phase: raise and lower using a half-cosine bump
        knee_lift = 0.5 * (1 - np.cos(np.pi * t / DUTY_CYCLE))
    else:
        # stance phase: firmly on ground
        knee_lift = 0.0

    # --- HIP: swing forward during swing, return during stance ---
    if t < DUTY_CYCLE:
        # swing phase: hip moves forward (full HIP_SWING range)
        hip_angle = HIP_SWING * 0.5 * np.cos(np.pi * t / DUTY_CYCLE)
    else:
        # stance phase: hip returns smoothly backward
        t_stance = (t - DUTY_CYCLE) / (1.0 - DUTY_CYCLE)  # 0 to 1
        hip_angle = -HIP_SWING * 0.5 * np.cos(np.pi * t_stance)

    return knee_lift, hip_angle

def Rotate(elapsed):
    # legs 1, 3, 5 — swing phase starts at t=0
    knee_a, hip_a = DutyCycle(elapsed, phase_offset=0.0)

    # legs 2, 4, 6 — offset by half period
    knee_b, hip_b = DutyCycle(elapsed, phase_offset=PERIOD * 0.5)

    # right side
    MoveOneLeg(leg1_knee_id,  knee_a * LEG_UP)
    MoveOneLeg(leg3_knee_id,  knee_a * LEG_UP)
    MoveOneLeg(leg5_knee_id, -knee_a * LEG_UP)  # mirrored

    MoveOneLeg(hip1_id, hip_a)
    MoveOneLeg(hip3_id, hip_a)
    MoveOneLeg(hip5_id, hip_a)

    # left side
    MoveOneLeg(leg2_knee_id,  knee_b * LEG_UP)
    MoveOneLeg(leg4_knee_id, -knee_b * LEG_UP)  # mirrored
    MoveOneLeg(leg6_knee_id, -knee_b * LEG_UP)  # mirrored

    MoveOneLeg(hip2_id, hip_b)
    MoveOneLeg(hip4_id, hip_b)
    MoveOneLeg(hip6_id, hip_b)
    

def Walk(elapsed):

    # legs 1, 3, 5
    knee_a, hip_a = DutyCycle(elapsed, phase_offset=0.0)

    # legs 2, 4, 6 — half period offset
    knee_b, hip_b = DutyCycle(elapsed, phase_offset=PERIOD * 0.5)

    # --- Group 1 ---
    MoveOneLeg(leg1_knee_id,  knee_a * LEG_UP)
    MoveOneLeg(leg3_knee_id,  knee_a * LEG_UP)
    MoveOneLeg(leg5_knee_id,  -knee_a * LEG_UP)

    MoveOneLeg(hip1_id,  hip_a)
    MoveOneLeg(hip3_id,  hip_a)
    MoveOneLeg(hip5_id,  -hip_a)

    # --- Group 2 ---
    MoveOneLeg(leg2_knee_id,  knee_b * LEG_UP)
    MoveOneLeg(leg4_knee_id,  -knee_b * LEG_UP)
    MoveOneLeg(leg6_knee_id,  -knee_b * LEG_UP)

    MoveOneLeg(hip2_id,  hip_b)
    MoveOneLeg(hip4_id, -hip_b)
    MoveOneLeg(hip6_id, -hip_b)

# =============================================================================
# Argument parsing
# =============================================================================
VALID_MODES = {"walk", "fun", "rotate"}
 
if len(sys.argv) < 2 or sys.argv[1] not in VALID_MODES:
    print(f"Usage: mjpython main.py <{'|'.join(VALID_MODES)}>")
    sys.exit(1)
 
mode = sys.argv[1]

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
    

    while viewer.is_running():
        elapsed = time.time() - phase_start
        
        if elapsed >= (PERIOD*2):
            phase_start = time.time()
            elapsed = 0

            
        ### PICK WHICH MODE TO VIEW

        if mode == "walk":
            Walk(elapsed)
        elif mode == "fun":
            WiggleInPlace(elapsed)
        elif mode == "rotate":
            Rotate(elapsed)
 
        mj.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)
        

# to run script: 
# mjpython hexapod_gait_simulator.py walk
# (other options are fun or rotate)
