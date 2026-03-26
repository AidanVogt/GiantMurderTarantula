import mujoco as mj
import mujoco.viewer
import numpy as np
import time

# load hexapod model from config
model = mj.MjModel.from_xml_path("rudimentary_hexapod.xml")
data  = mj.MjData(model)

GAIT_FREQ = 0.3   # Hz of the sine gait (lower = slower leg movement)
SLOWDOWN = 5.0   # real-time slowdown factor (1.0 = real-time, 5.0 = 5x slower)
dt = model.opt.timestep  # 0.002 s per step (fromprev)

# globals
N_LEGS = 6
SWING_HEIGHT=0.4 # meters
SWING_DURATION=2 # seconds
STANCE_DURATION=1 #seconds

 
# Nominal foot rest positions in body frame (x, y, z), shape [6, 3] TODO adjust if needed
LEG_OFFSETS = np.array([
    [ 0.15,  0.10, -0.12],  # L1 front-left
    [ 0.00,  0.12, -0.12],  # L2 mid-left
    [-0.15,  0.10, -0.12],  # L3 rear-left
    [ 0.15, -0.10, -0.12],  # R1 front-right
    [ 0.00, -0.12, -0.12],  # R2 mid-right
    [-0.15, -0.10, -0.12],  # R3 rear-right
])
 
# phase matrices (L1, L2, L3, L4, L5, L6)
TRIPOD_GAIT = np.array([
    0, np.pi, 0,
    np.pi, 0, np.pi,
])

# RIPPLE_GAIT = np.array([
#     0, 2*np.pi/3, 4*np.pi/3,
#     np.pi/3, np.pi, 5*np.pi/3,
# ])

# # TODO fix tripod gait funcs

def tripod_gait_rotation(t, cw = True):
    
    ctrl = np.zeros(12)
    
    pass

def ripple_gait(t, forward=True):
    """Forward and backward RIPPLE gait""" 
    
    

    pass
 
def wave_gait(t, forward=True):
    """Forward and backward wave gait"""
    
    ctrl = np.zeros(12)
    
    if not forward:
        for i in range(N_LEGS):
            phase = (2*np.pi * i) / N_LEGS
            ctrl[2*i]   = -0.4 * np.sin(2*np.pi*GAIT_FREQ*t + phase)            # hip reversed
            ctrl[2*i+1] = -0.5 * np.clip(np.sin(2*np.pi*GAIT_FREQ*t + phase), 0, 1)
    
    else:
        for i in range(N_LEGS):
            phase = (2*np.pi * i) / N_LEGS
            ctrl[2*i] = 0.4 * np.sin(2*np.pi*GAIT_FREQ*t + phase) # fwd
            ctrl[2*i+1] = -0.5 * np.clip(np.sin(2*np.pi*GAIT_FREQ*t + phase), 0, 1) # lift

    return ctrl
    

# try this.....
def gait_commands(
    t: float,
    swing_period: float,
    stance_period: float,
    phase_matrix: np.ndarray,        # shape [6]
    stride_vector: np.ndarray,       # (dx, dy) in body frame per full cycle
    body_height: float = 0.18,
) -> list[dict]:
    """
    Returns one command dict per leg for the current timestep t.

    Each command:
        {
          'leg':        int,         # 0–5
          'mode':       'swing' | 'stance',
          'foot_pos':   np.ndarray,  # target (x, y, z) in body frame
          'phase':      float,       # current phase θᵢ(t) in [0, 2π)
        }
    """
    T          = swing_period + stance_period
    omega      = 2 * np.pi / T
    theta_sw   = 2 * np.pi * swing_period / T   # swing window boundary

    commands = []
    for i in range(6):
        phase = (omega * t + phase_matrix[i]) % (2 * np.pi)
        rest  = LEG_OFFSETS[i].copy()
        rest[2] -= (body_height - 0.12)         # adjust for commanded height

        if phase < theta_sw:
            # ── SWING ──────────────────────────────────────────────────────
            # normalised progress through swing: 0 → 1
            s = phase / theta_sw

            # interpolate foot from -stride/2 to +stride/2
            xy_offset = stride_vector * (s - 0.5)

            # raised half-sine arc
            z_lift = SWING_HEIGHT * np.sin(np.pi * s)

            foot_pos = rest.copy()
            foot_pos[0] += xy_offset[0]
            foot_pos[1] += xy_offset[1]
            foot_pos[2] += z_lift
            mode = 'swing'

        else:
            # ── STANCE ─────────────────────────────────────────────────────
            # normalised progress through stance: 0 → 1
            s = (phase - theta_sw) / (2 * np.pi - theta_sw)

            # foot sweeps backward relative to body (body moves forward)
            xy_offset = stride_vector * (0.5 - s)

            foot_pos = rest.copy()
            foot_pos[0] += xy_offset[0]
            foot_pos[1] += xy_offset[1]
            mode = 'stance'

        commands.append({
            'leg':      i,
            'mode':     mode,
            'foot_pos': foot_pos,
            'phase':    phase,
        })

    return commands

# =============================================================================
# Run MuJoCo viewer
# =============================================================================

# true dir = forward, false = backward
# true dir = CW, false = CCW
GAIT = wave_gait
DIR = True 

with mujoco.viewer.launch_passive(model, data) as viewer:
    
    while viewer.is_running():
        data.ctrl[:] = GAIT(data.time, DIR)
        mj.mj_step(model, data)
        viewer.sync()
        time.sleep(dt * SLOWDOWN)
        
        
def ctrl_callback(model, data):
    t = data.time
    stride = np.array([0.06, 0.0])   # walking straight, 6 cm stride

    cmds = gait_commands(
        t             = t,
        swing_period  = 0.3,
        stance_period = 0.9,
        phase_matrix  = WAVE_GAIT,
        stride_vector = stride,
    )

    for cmd in cmds:
        q = inverse_kinematics(cmd['foot_pos'], leg_index=cmd['leg'])
        leg_joint_slice = slice(cmd['leg'] * 3, cmd['leg'] * 3 + 3)
        data.ctrl[leg_joint_slice] = q

mujoco.set_mjcb_control(ctrl_callback)

# to run script: 
# mjpython hexapod_gait_simulator.py