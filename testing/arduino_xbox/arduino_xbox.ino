// Arduino Joystick Code (Xbox integration)

// Turn on LED if the joystick is pointing in a certain direction

// LEDs
const int RED_LED_PIN = 11;
const int BLUE_LED_PIN = 10;
const int WHITE_LED_PIN = 9;
const int GREEN_LED_PIN = 6;

struct LED_QUAD {
  uint8_t r;
  uint8_t b;
  uint8_t w;
  uint8_t g;
};

// helper for byte conversion
uint8_t toByteValue(float v) {
  return (uint8_t)constrain(v * 255.0, 0.0, 255.0);
}

LED_QUAD joystickPositionToLED(float scaled_x, float scaled_y) {
  LED_QUAD leds = {0, 0, 0, 0};

  // Y axis
  if (scaled_y >= 0) {
    leds.r    = toByteValue(scaled_y);
  }
  else {
    leds.b = toByteValue(-scaled_y);
  }

  // X axis
  if (scaled_x >= 0) {
    leds.w = toByteValue(scaled_x);
  }
  else { 
    leds.g  = toByteValue(-scaled_x);
  }

  return leds;
}

void setup() {

  // joystick setup
  Serial.begin(9600);
  pinMode(SW_PIN, INPUT_PULLUP);

  // led setup
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(BLUE_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(WHITE_LED_PIN, OUTPUT);

}

void loop() {

    // only write if data packet is sent
    if (Serial.available() > 9) {
        // first byte is a specifier
        char header = Serial.read();

        // read x and y from Pi
        float x, y;
        Serial.readBytes((char*)&x, 4);
        Serial.readBytes((char*)&y, 4);

        // convert to LED vals
        LED_QUAD led_vals = joystickPositionToLED(x, y);

        // change LED brightness
        analogWrite(RED_LED_PIN, led_vals.r);
        analogWrite(BLUE_LED_PIN, led_vals.b);
        analogWrite(WHITE_LED_PIN, led_vals.w);
        analogWrite(GREEN_LED_PIN, led_vals.g);

        // print read stuff
        Serial.print(header); // first byte specifies instruction (can remove later)
        Serial.print(x);
        Serial.print(",");
        Serial.print(y);
        Serial.print("\n");
    }


    delay(100);
}

