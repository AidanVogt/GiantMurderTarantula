const int INPUT_PIN = A0;

void setup() {
  pinMode(INPUT_PIN, INPUT_PULLDOWN);
  Serial.begin(9600);
}

void loop() {
  Serial.print("Reading:");
  Serial.println(analogRead(INPUT_PIN));
}
