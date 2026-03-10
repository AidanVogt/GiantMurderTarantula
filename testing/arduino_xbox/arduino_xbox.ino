// Arduino Joystick Code (Xbox integration)

// Turn on LED if the joystick is pointing in a certain direction

// LEDs
const int RED_LED_PIN = 11;
const int BLUE_LED_PIN = 10;
const int WHITE_LED_PIN = 9;
const int GREEN_LED_PIN = 6;


void setup() {

  // joystick setup
  Serial.begin(9600);

  // led setup
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(BLUE_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(WHITE_LED_PIN, OUTPUT);

}

void loop() {

    // check line
    if (Serial.available() > 0) {
        String line = Serial.readStringUntil('\n');
        
        int vals[4];
        int idx = 0;
        char *token = strtok((char*)line.c_str(), ",");
        
        while (token != NULL && idx < 4) {
            vals[idx++] = atoi(token);
            token = strtok(NULL, ",");
        }
        
        // write to LEDs
        if (idx == 4) {
            analogWrite(RED_LED_PIN,   vals[0]);
            analogWrite(BLUE_LED_PIN,  vals[1]);
            analogWrite(WHITE_LED_PIN, vals[3]);
            analogWrite(GREEN_LED_PIN, vals[2]);
        }
    }

}


