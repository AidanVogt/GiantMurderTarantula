#include <SimpleFOC.h>

const int HALL_A = 2;
const int HALL_B = 3;
const int HALL_C = 4;
const int FB_PIN = 6;
const int EN_PIN = 7;

unsigned int last_print = 0;
int n_enabled = 1;
int go_forward = 0;

HallSensor encoder = HallSensor(HALL_A, HALL_B, HALL_C, 5);

void setup() {
  last_print = millis();

  pinMode(HALL_A, INPUT_PULLUP);
  pinMode(HALL_B, INPUT_PULLUP);
  pinMode(HALL_C, INPUT_PULLUP);

  Serial.begin(115200);
  Wire.begin();
  encoder.init();

  pinMode(FB_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);
  digitalWrite(EN_PIN, n_enabled);
  digitalWrite(FB_PIN, go_forward);
}

void loop() {
  encoder.update();

    if (millis() - last_print >= 150) {
    last_print = millis();

    if (Serial.available()) {
      if (Serial.read() == 'f') {
        if (!n_enabled) {
          Serial.println("DISABLE MOTOR BEFORE SWITHCING DIRECTION!!!");
          return;
        }
        Serial.print("setting FB_PIN to : ");
        Serial.print(go_forward);
        go_forward = !go_forward;
      } else {
        Serial.print("setting EN_PIN to : ");
        Serial.print(n_enabled);
        n_enabled = !n_enabled;
      }
      Serial.print("\n");

      digitalWrite(EN_PIN, n_enabled);
      digitalWrite(FB_PIN, go_forward);
      while (Serial.available()) Serial.read();
    }

    Serial.print(encoder.getAngle());
    Serial.print("\n");
  }
}
