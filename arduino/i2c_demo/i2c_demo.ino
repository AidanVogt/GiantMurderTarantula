#include <Wire.h>

// LEG 1 ARDUINO ADDRESS
#define INO_ADDRESS 0x10

// match python
struct Instruction {
  int instr_type;
  int phase;
};

Instruction received;

void setup() {
  Wire.begin(INO_ADDRESS);
  Wire.onReceive(getInstruction);  // Register receive callback
  Serial.begin(9600);
}

void loop() {
  delay(100);
}

void getInstruction(int numBytes) {
  // Serial.println("numBytes");
  // Serial.println(numBytes);

  while (Wire.available()) {
    unsigned char c  = Wire.read();
    Serial.println(c);

    Wire.write(0x01);

  }
}