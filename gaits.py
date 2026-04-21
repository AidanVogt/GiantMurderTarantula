"""
Gait control bytes - hardcoded

FORWARD/BACKWARD MOVEMENT
Each movement "cycle" is divided into 10 steps, where the legs pass through the neutral starting point twice. The hexapod primarily uses a tripod gait to move. Since there are 6 legs, three will move up at any given time while the other 3 remain on the ground. The tripod groups are separated by a half period, meaning every 5 steps, the legs in the air will alternate. 

"""

# NOTE: Legs 0x13 (4), 0x14 (5), and 0x15 (6) movements need to be reversed (meaning forwards = backwards)

# testing rotation gait

# ACTIONS (forward/backward mean hip movement, up/down mean knee movement)
ACTION_NONE = 0
ACTION_FORWARD = 1
ACTION_BACKWARD = 2
ACTION_UP = 3
ACTION_DOWN = 4
ACTION_HOME_FORWARD = 5
ACTION_HOME_BACKWARD = 6
ACTION_ZERO = 7

# GAITS
GAIT_FORWARD = 0
GAIT_BACKWARD = 1
GAIT_TURN_LEFT = 2
GAIT_TURN_RIGHT = 3
GAIT_RAISE_TRIPOD = 5
GAIT_COOL = 6
GAIT_RAISE_ALL = 7
GAIT_LOWER_ALL = 8

gaits = {
    GAIT_FORWARD: [
        #### GROUP 1 LEGS 1, 3, 5 ####
        # up
        (ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE),
        
        # swing phase - leg in air, grounded legs move back
        (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
        
        # down
        (ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE),
        
        # return to neutral stance phace
        (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
        
        #### GROUP 2 LEGS 2, 4, 6 ####
        # up
        (ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
        
        # swing phase
        (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
        
        # down
        (ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN),
        
        # return to neutral stance phase
        (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
    ],
    
    # reverse of fwd
    GAIT_BACKWARD: [
        #### GROUP 1 LEGS 1, 3, 5 ####
        # up
        (ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE),
        
        # swing phase - leg in air, grounded legs move back
        (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
        
        # down
        (ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE),
        
        #### GROUP 2 LEGS 2, 4, 6 ####
        # up
        (ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
        
        # swing phase
        (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
        
        # down
        (ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN),
        
    ],
    
    GAIT_TURN_LEFT: [
        #### GROUP 1 LEGS 1, 3, 5 (RIGHT SIDE) SWING ####
        (ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE),
        
        # right legs swing backward, left grounded legs push backward (rotates CW)
        (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
        
        (ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE),

        #### GROUP 2 LEGS 2, 4, 6 (LEFT SIDE) SWING ####
        (ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
        
        # left legs swing forward, right grounded legs push forward (rotates CW)
        (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
        
        (ACTION_NONE,    ACTION_DOWN,     ACTION_NONE,    ACTION_DOWN,     ACTION_NONE,    ACTION_DOWN),
    ],
    
    GAIT_TURN_RIGHT: [
    #### GROUP 1 LEGS 1, 3, 5 (RIGHT SIDE) SWING ####
    (ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE),
    
    # right legs swing backward, left grounded legs push backward (rotates CW)
    (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
    
    (ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE),

    #### GROUP 2 LEGS 2, 4, 6 (LEFT SIDE) SWING ####
    (ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
    
    # left legs swing forward, right grounded legs push forward (rotates CW)
    (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
    
    (ACTION_NONE,    ACTION_DOWN,     ACTION_NONE,    ACTION_DOWN,     ACTION_NONE,    ACTION_DOWN),

    ],
    
    GAIT_COOL: [
        (ACTION_UP, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE),
        (ACTION_FORWARD, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE),
        (ACTION_BACKWARD, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE),
        (ACTION_FORWARD, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE),
        (ACTION_BACKWARD, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE),
        (ACTION_DOWN, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE, ACTION_NONE),
    ],
    
    GAIT_RAISE_TRIPOD: [
        # first set of three legs
        (ACTION_UP, ACTION_UP, ACTION_UP, ACTION_UP, ACTION_UP, ACTION_UP),
        (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
        (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
        (ACTION_DOWN, ACTION_DOWN, ACTION_DOWN, ACTION_DOWN, ACTION_DOWN, ACTION_DOWN),
    ],
    
    GAIT_RAISE_ALL: [
        (ACTION_UP, ACTION_UP, ACTION_UP, ACTION_UP, ACTION_UP, ACTION_UP),
    ],
    
    GAIT_LOWER_ALL: [
        (ACTION_DOWN, ACTION_DOWN, ACTION_DOWN, ACTION_DOWN, ACTION_DOWN, ACTION_DOWN),
    ]
}