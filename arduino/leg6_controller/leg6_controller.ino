#include <ModbusMaster.h>
#include <SimpleFOC.h>
#include <SoftwareSerial.h>
#include <Wire.h>

#define MAX485_DE      8
#define MAX485_RE_NEG  9

#define HALL_A 2
#define HALL_B 3
#define HALL_C 4

#define FLOOR_CONTACT_PIN A0

#define RX_RS485 10 
#define TX_RS485 11

#define MOTOR_SPEED 200
#define MOVE_INTERVAL 250

#define PRINT_INTERVAL 250

// I2C LEG ADDRESS
#define INO_ADDRESS 0x15

#define NOT_DONE 0
#define DONE 1

#define ACTION_NONE 0
#define ACTION_FORWARD 1
#define ACTION_BACKWARD 2
#define ACTION_UP 3
#define ACTION_DOWN 4
#define ACTION_HOME 5

HallSensor encoder = HallSensor(HALL_A, HALL_B, HALL_C, 5);
SoftwareSerial RS485_serial (RX_RS485, TX_RS485);
ModbusMaster node;

bool forward = true;
unsigned int last_print = 0;
int status = NOT_DONE;
unsigned char current_action = ACTION_NONE;

//////////////// MOTOR MOVEMENT FUNCS ////////////////

void preTransmission()
{
  digitalWrite(MAX485_RE_NEG, HIGH);
  digitalWrite(MAX485_DE, HIGH);
}

void postTransmission()
{
  digitalWrite(MAX485_RE_NEG, LOW);
  digitalWrite(MAX485_DE, LOW);
}

void setMotorState(bool EN, bool FR, bool BK) {
  uint8_t high = 0;

  if (EN) high |= (1 << 0);
  if (FR) high |= (1 << 1);
  if (BK) high |= (1 << 2);

  high |= (1 << 3);

  node.writeSingleRegister(0x8000, ((uint16_t)high << 8) | 0x5);
}

bool is_contacting_ground() {
  return analogRead(FLOOR_CONTACT_PIN) == 1023;
}

// not recommended for normal operation
void braking_stop() {
  Serial.println("braking stop (NOT RECOMMENDED)");
  setMotorState(0,0,1);
}

void non_braking_stop() {
  Serial.println("non braking stop");
  setMotorState(0,0,0);
}

void set_forward() {
  Serial.println("setted forward");
  setMotorState(1,0,0);
}

void set_backward() {
  Serial.println("setted backward");
  setMotorState(1,1,0);
}

void move_forward() {
  int end_condition = encoder.getAngle() + MOVE_INTERVAL;
  set_forward();
  while (encoder.getAngle() < end_condition) {
    encoder.update();

    if (millis() - last_print > PRINT_INTERVAL) {
      Serial.print("end condition: ");
      Serial.print(end_condition);
      Serial.print(" current angle: ");
      Serial.println(encoder.getAngle());
      last_print = millis();
    }
  }
  non_braking_stop();
}

void move_backward() {
  int end_condition = encoder.getAngle() - MOVE_INTERVAL;
  set_backward();
  while (encoder.getAngle() > end_condition) {
    encoder.update();

    if (millis() - last_print > PRINT_INTERVAL) {
      Serial.print("end condition: ");
      Serial.print(end_condition);
      Serial.print(" current angle: ");
      Serial.println(encoder.getAngle());
      last_print = millis();
    }
  }
  non_braking_stop();
}

void move_up() {
  // move stepper
}

void move_down() {
  // move stepper and read from contact sensor
}

void move_home() {
  // homing sequence
}

////////////////// I2C PARSING ////////////////
void receiveCommand(int numBytes) {
  while (Wire.available()) {
    unsigned char byte = Wire.read();
    if (byte >= 0x10) continue;

    current_action = byte;
  }
}

void sendStatus() {
  Wire.write(status);
}


void sendData() {
  Wire.write("Hello Pi");
}

////////////////// SETUP AND LOOP //////////////////
void setup()
{
  // I2C
  Wire.begin(INO_ADDRESS);
  Wire.onReceive(receiveCommand);
  Wire.onRequest(sendStatus);

  pinMode(MAX485_RE_NEG, OUTPUT);
  pinMode(MAX485_DE, OUTPUT);

  pinMode(FLOOR_CONTACT_PIN, INPUT);

  pinMode(HALL_A, INPUT_PULLUP);
  pinMode(HALL_B, INPUT_PULLUP);
  pinMode(HALL_C, INPUT_PULLUP);
  encoder.init();

  digitalWrite(MAX485_RE_NEG, LOW);
  digitalWrite(MAX485_DE, LOW);

  RS485_serial.begin(9600);
  Serial.begin(115200);

  node.begin(1, RS485_serial);
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  delay(500);

  node.writeSingleRegister(0x8005, MOTOR_SPEED);
  delay(100);

  last_print = millis();
}

int direction = 0;

void loop()
{
  encoder.update();
  if        (current_action == ACTION_FORWARD) {
    move_forward();
  } else if (current_action == ACTION_BACKWARD) {
    move_backward();
  } else if (current_action == ACTION_UP) {
    move_up();
  } else if (current_action == ACTION_DOWN) {
    move_down();
  } else if (current_action == ACTION_HOME) {
    move_home();
  }
  current_action = ACTION_NONE;
}