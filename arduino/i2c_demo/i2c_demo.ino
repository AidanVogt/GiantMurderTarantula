#include <Wire.h>

// LEG 1 ARDUINO ADDRESS
#define INO_ADDRESS 0x10

// is processing done
bool FINISHED = false;

void setup() {
  Wire.begin(INO_ADDRESS);
  Wire.onReceive(getInstruction);  // Register receive callback
  Wire.onRequest(sendFinished);
  Serial.begin(9600);
}

void loop() {
  delay(100);
}

void getInstruction(int numBytes) {
  Serial.println("numBytes");
  Serial.println(numBytes);

  while (Wire.available()) {
    FINISHED = false;
    delay(100);
    unsigned char c  = Wire.read();
    Serial.println(c);
    FINISHED = true;
  }
}

void sendFinished(){
  if (FINISHED) {
    // Wire.write(0x01);
    Wire.write(211);
  }

  else {
    Wire.write(0x00);
  }

}