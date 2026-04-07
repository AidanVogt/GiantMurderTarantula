const int EN = 5;
const int DIR = 6;
const int PUL = 7;
bool direction = false;

void setup() {
  pinMode(EN, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT); 

  digitalWrite(EN, LOW);
  digitalWrite(DIR, LOW);
  digitalWrite(PUL, LOW);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    if (Serial.read() == 'b') {
      digitalWrite(DIR, direction ? HIGH : LOW);
      direction = !direction;
    }

    while (Serial.available()) Serial.read();

    for (int i = 0; i < 1000; i++) {
      digitalWrite(PUL, HIGH);
      delayMicroseconds(3000);
      digitalWrite(PUL, LOW);
      delayMicroseconds(3000);
    }
  }
}
