"""
Gait control bytes - hardcoded

FORWARD/BACKWARD MOVEMENT
Each movement "cycle" is divided into 10 steps, where the legs pass through the neutral starting point twice. The hexapod primarily uses a tripod gait to move. Since there are 6 legs, three will move up at any given time while the other 3 remain on the ground. The tripod groups are separated by a half period, meaning every 5 steps, the legs in the air will alternate. 

"""

# ACTIONS (forward/backward mean hip movement, up/down mean knee movement)
ACTION_NONE = 0
ACTION_FORWARD = 1
ACTION_BACKWARD = 2
ACTION_UP = 3
ACTION_DOWN = 4
ACTION_HOME = 5

# GAITS
GAIT_FORWARD = 0
GAIT_BACKWARD = 1
GAIT_TURN_LEFT = 2
GAIT_TURN_RIGHT = 3
GAIT_HOME = 5
GAIT_COOL = 6

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
        
        # return to neutral stance phace
        (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
        
        #### GROUP 2 LEGS 2, 4, 6 ####
        # up
        (ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
        
        # swing phase
        (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
        
        # down
        (ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN),
        
        # return to neutral stance phase
        (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
    ],
    
    GAIT_TURN_LEFT: [
        (ACTION_FORWARD, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
        (ACTION_FORWARD, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
    ],
    
    GAIT_TURN_RIGHT: [
    #### GROUP 1 LEGS 1, 3, 5 (RIGHT SIDE) SWING ####
    (ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE),
    
    # right legs swing backward, left grounded legs push backward (rotates CW)
    (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
    (ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD),
    
    (ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE, ACTION_DOWN, ACTION_NONE),
    
    # stance: left legs continue, right legs neutral
    (ACTION_NONE, ACTION_FORWARD, ACTION_NONE, ACTION_FORWARD, ACTION_NONE, ACTION_FORWARD),
    (ACTION_NONE, ACTION_FORWARD, ACTION_NONE, ACTION_FORWARD, ACTION_NONE, ACTION_FORWARD),

    #### GROUP 2 LEGS 2, 4, 6 (LEFT SIDE) SWING ####
    (ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP, ACTION_NONE, ACTION_UP),
    
    # left legs swing forward, right grounded legs push forward (rotates CW)
    (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
    (ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD, ACTION_FORWARD, ACTION_BACKWARD),
    
    (ACTION_NONE,    ACTION_DOWN,     ACTION_NONE,    ACTION_DOWN,     ACTION_NONE,    ACTION_DOWN),
    
    # stance: right legs continue, left legs neutral
    (ACTION_FORWARD, ACTION_NONE,    ACTION_FORWARD,  ACTION_NONE,    ACTION_FORWARD,  ACTION_NONE),
    (ACTION_FORWARD, ACTION_NONE,    ACTION_FORWARD,  ACTION_NONE,    ACTION_FORWARD,  ACTION_NONE),
],
    
    GAIT_HOME: [
        # home 3 legs at a time to prevent instability
        (ACTION_HOME, ACTION_NONE, ACTION_HOME, ACTION_NONE, ACTION_HOME, ACTION_NONE), 
        (ACTION_NONE, ACTION_HOME, ACTION_NONE, ACTION_HOME, ACTION_NONE, ACTION_HOME), 
    ],
    
    GAIT_COOL: [
        (ACTION_FORWARD, ACTION_NONE, ACTION_FORWARD, ACTION_NONE, ACTION_FORWARD, ACTION_NONE),
        (ACTION_BACKWARD, ACTION_NONE, ACTION_BACKWARD, ACTION_NONE, ACTION_BACKWARD, ACTION_NONE),
    ],
    
}