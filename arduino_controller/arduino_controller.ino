// Arduino Joystick Code 

// System Demo 1
// Turn on LED if the joystick is pointing in a certain direction
// Flash LEDs if button pushed

// JOYSTICK
const int VRX_PIN = A0;  // X
const int VRY_PIN = A1;  // Y
const int SW_PIN  = 2;   // btn

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

// other globals
const float max_potent_val = 1024;
const float fudge_fct = 0.1;
const float center = 512;

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

// scale raw potentiom. value between -1 and 1
float scaleAxis(int val) {
  float scaled = ((float)val - center)/max_potent_val;

  if (abs(scaled) < fudge_fct) {
    scaled = 0.0;
  }

  scaled = constrain(scaled * 2, -1.0, 1.0);

  return scaled;
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

  // read values
  int xValue = analogRead(VRX_PIN);
  int yValue = analogRead(VRY_PIN);
  int swValue = digitalRead(SW_PIN);

  // normalize potentiometer vals
  float x_norm = scaleAxis(xValue);
  float y_norm = scaleAxis(yValue);

  // pulse LED based on button press
  if (swValue == 0) {
    digitalWrite(RED_LED_PIN, HIGH);
    digitalWrite(BLUE_LED_PIN, HIGH);
    digitalWrite(WHITE_LED_PIN, HIGH);
    digitalWrite(GREEN_LED_PIN, HIGH);
  } else {
    LED_QUAD led_vals = joystickPositionToLED(x_norm, y_norm);

    analogWrite(RED_LED_PIN, led_vals.r);
    analogWrite(BLUE_LED_PIN, led_vals.b);
    analogWrite(WHITE_LED_PIN, led_vals.w);
    analogWrite(GREEN_LED_PIN, led_vals.g);
  }

  // things to read
  Serial.print(swValue);
  Serial.print(",");
  Serial.print(x_norm);
  Serial.print(",");
  Serial.print(y_norm);
  Serial.print("\n");
  delay(100);
}

