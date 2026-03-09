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

    // only write if data packet is sent
    if (Serial.available() >= 5) {

        // check if in sync
        if (Serial.read() != 0xFF) return;

        // read led vals from pi
        int n = Serial.read();
        int s = Serial.read();
        int e = Serial.read();
        int w = Serial.read();

        // change LED brightness
        analogWrite(RED_LED_PIN, n);
        analogWrite(BLUE_LED_PIN, s);
        analogWrite(WHITE_LED_PIN, w);
        analogWrite(GREEN_LED_PIN, e);
    }

    delay(100);
}


