import mujoco as mj
import mujoco.viewer
import numpy as np
import time

# load hexapod model from config
model = mj.MjModel.from_xml_path("hexapod.xml")
data  = mj.MjData(model)

GAIT_FREQ   = 0.5   # Hz of the sine gait (lower = slower leg movement)
SLOWDOWN    = 5.0   # real-time slowdown factor (1.0 = real-time, 5.0 = 5x slower)
 
dt = model.opt.timestep  # 0.002 s per step
 
# =============================================================================
# Gait functions
# Each returns a (12,) array of control targets:
#   indices 0,1 = hip1, knee1 ... 10,11 = hip6, knee6
# Hip:  positive = forward swing, negative = backward swing
# Knee: negative = lift foot up, near zero = foot down
# =============================================================================
 
def tripod_cw(t):
    """
    Tripod gait — clockwise rotation.
    Group A (legs 1,3,5 — indices 0,2,4): hip sweeps +
    Group B (legs 2,4,6 — indices 1,3,5): hip sweeps - (opposite phase)
    Opposing hip directions between groups creates rotation.
    """
    ctrl = np.zeros(12)
    for i in range(6):
        phase = 0 if i % 2 == 0 else np.pi
        hip_dir = 1.0 if i % 2 == 0 else -1.0   # groups sweep opposite directions
        ctrl[2*i]   =  0.4 * hip_dir * np.sin(2*np.pi*GAIT_FREQ*t + phase)  # hip
        ctrl[2*i+1] = -0.5 * np.abs(np.sin(2*np.pi*GAIT_FREQ*t + phase))    # knee lift
    return ctrl
 
def tripod_ccw(t):
    """
    Tripod gait — counter-clockwise rotation.
    Same as CW but hip directions flipped.
    """
    ctrl = np.zeros(12)
    for i in range(6):
        phase = 0 if i % 2 == 0 else np.pi
        hip_dir = -1.0 if i % 2 == 0 else 1.0   # flipped vs CW
        ctrl[2*i]   =  0.4 * hip_dir * np.sin(2*np.pi*GAIT_FREQ*t + phase)
        ctrl[2*i+1] = -0.5 * np.abs(np.sin(2*np.pi*GAIT_FREQ*t + phase))
    return ctrl
 
def wave_forward(t):
    """
    Wave gait — forward movement.
    Legs lift and swing one at a time in sequence (1→2→3→4→5→6).
    Most stable gait — 5 legs on ground at all times.
    All hips sweep in the same direction for forward thrust.
    """
    ctrl = np.zeros(12)
    n_legs = 6
    for i in range(n_legs):
        phase = (2*np.pi * i) / n_legs          # evenly spaced phase offsets
        ctrl[2*i]   =  0.4 * np.sin(2*np.pi*GAIT_FREQ*t + phase)            # hip forward
        ctrl[2*i+1] = -0.5 * np.clip(np.sin(2*np.pi*GAIT_FREQ*t + phase), 0, 1)  # lift on upswing only
    return ctrl
 
def wave_backward(t):
    """
    Wave gait — backward movement.
    Same as forward but hip direction reversed.
    """
    ctrl = np.zeros(12)
    n_legs = 6
    for i in range(n_legs):
        phase = (2*np.pi * i) / n_legs
        ctrl[2*i]   = -0.4 * np.sin(2*np.pi*GAIT_FREQ*t + phase)            # hip reversed
        ctrl[2*i+1] = -0.5 * np.clip(np.sin(2*np.pi*GAIT_FREQ*t + phase), 0, 1)
    return ctrl

# =============================================================================
# Run MuJoCo viewer
# =============================================================================

GAIT = tripod_ccw

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        data.ctrl[:] = GAIT(data.time)
        mj.mj_step(model, data)
        viewer.sync()
        time.sleep(dt * SLOWDOWN)
        

# to run script: 
# mjpython hexapod_gait_simulator.py