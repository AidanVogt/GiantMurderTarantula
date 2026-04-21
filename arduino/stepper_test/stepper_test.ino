const int EN = 5;
const int DIR = 6;
const int PUL = 7;
bool direction = false;
bool enable;

void setup() {
  pinMode(EN, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT); 

  digitalWrite(EN, LOW);
  digitalWrite(DIR, LOW);
  digitalWrite(PUL, HIGH);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'b') {
      digitalWrite(DIR, direction ? HIGH : LOW);
      direction = !direction;
      return;
    } else if (c == 'e') {
      Serial.println(enable);
      digitalWrite(EN, enable ? HIGH : LOW);
      enable = !enable;
      return;
    }



    while (Serial.available()) Serial.read();

    for (int i = 0; i < 2000; i++) {
      digitalWrite(PUL, LOW);
      delayMicroseconds(2000);
      digitalWrite(PUL, HIGH);
      delayMicroseconds(2000);
    }
  }
}
