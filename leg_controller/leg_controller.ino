#include <ModbusMaster.h>
#include <SimpleFOC.h>
#include <SoftwareSerial.h>
#include <Wire.h>

#define INO_ADDRESS 0x15

#define IS_LEFT_STEPPER ((INO_ADDRESS == 0x12 || INO_ADDRESS == 0x13) ? 1 : 0)
#define REVERSE_DIRECTION ((INO_ADDRESS >= 0x13) ? 1 : 0)
#define STEP_UP_MULTIPLIER ((INO_ADDRESS == 0x13) ? 2 : 1)
#define STEP_UP_ITERS 800

#define MAX485_DE      8
#define MAX485_RE_NEG  9
#define RX_RS485 10
#define TX_RS485 11

#define HALL_A 2
#define HALL_B 3
#define HALL_C 4

#define EN_PIN 5
#define DIR_PIN 6
#define PUL_PIN 7

#define LIMIT_PIN 12
#define FLOOR_CONTACT_PIN A0

#define MOTOR_SPEED 175
#define HIP_MOVE_INTERVAL 20
#define HIP_HOME_INTERVAL 5
#define STEP_MAX_TIME_CONSTANT 50
#define MAX_ANGLE 25

#define PRINT_INTERVAL 500
#define HOMING_THRESHOLD 1

#define NOT_DONE 0
#define DONE 1

#define ACTION_NONE 0
#define ACTION_FORWARD 1
#define ACTION_BACKWARD 2
#define ACTION_UP 3
#define ACTION_DOWN 4 
#define ACTION_HOME_FORWARD 5
#define ACTION_HOME_BACKWARD 6
#define ACTION_ZERO 7
#define ACTION_HOME 8

#if INO_ADDRESS == 0x10 || INO_ADDRESS == 0x11
  SoftwareSerial RS485_serial(RX_RS485, TX_RS485);
#elif INO_ADDRESS >= 0x12 && INO_ADDRESS <= 0x15
  #define RS485_serial Serial1
#else
  #error "Unsupported INO_ADDRESS"
#endif

HallSensor encoder = HallSensor(HALL_A, HALL_B, HALL_C, 5);
ModbusMaster node;

bool forward = true;
unsigned long last_print = 0;
unsigned char current_action = ACTION_NONE;
float zero_offset = 0;
float min_angle = -MAX_ANGLE;
float max_angle = MAX_ANGLE;

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
  set_motor_speed();
  uint8_t high = 0;

  if (EN) high |= (1 << 0);
  if (FR) high |= (1 << 1);
  if (BK) high |= (1 << 2);

  high |= (1 << 3);

  node.writeSingleRegister(0x8000, ((uint16_t)high << 8) | 0x5);
}

float get_angle() {
  return encoder.getAngle() - zero_offset;
}

void set_motor_speed() {
  uint8_t result = node.writeSingleRegister(0x8005, MOTOR_SPEED);
  Serial.print("set motor speed result: ");
  Serial.println(result);
}

bool is_contacting_ground() {
  return analogRead(FLOOR_CONTACT_PIN) == 1023;
}

bool is_hitting_limit() {
  return !digitalRead(LIMIT_PIN);
}

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

void step_down() {
  Serial.println("stepping down");
  digitalWrite(DIR_PIN, IS_LEFT_STEPPER);
  digitalWrite(EN_PIN, LOW);
  for (int i = 0; i < (STEP_UP_ITERS * 0.8); i++) {
    // if (is_contacting_ground())
    //   break;
    encoder.update();
    digitalWrite(PUL_PIN, LOW);
    delayMicroseconds(1000);
    digitalWrite(PUL_PIN, HIGH);
    delayMicroseconds(1000);
  }
  digitalWrite(EN_PIN, HIGH);
}

void step_up() {
  Serial.print("stepping up by: ");
  Serial.println(STEP_UP_ITERS);
  digitalWrite(DIR_PIN, !IS_LEFT_STEPPER);
  digitalWrite(EN_PIN, LOW);
  for (int i = 0; i < STEP_UP_ITERS; i++) {
    encoder.update();
    digitalWrite(PUL_PIN, LOW);
    delayMicroseconds(1000);
    digitalWrite(PUL_PIN, HIGH);
    delayMicroseconds(1000);
  }
}

void move_forward(float angle) {
  float current_angle = get_angle();
  if (current_angle >= max_angle) {
    Serial.println("out of bounds");
    return;
  }

  float end_condition = current_angle + angle;
  if (end_condition > max_angle) end_condition = max_angle;

  Serial.print("end condition: ");
  Serial.println(end_condition);
  Serial.print("current angle: ");
  Serial.println(current_angle);

  set_forward();

  unsigned long step_time = millis();
  unsigned long max_time = (unsigned long)(angle * STEP_MAX_TIME_CONSTANT);

  while (current_action != ACTION_NONE && get_angle() < end_condition && get_angle() < max_angle) {
    encoder.update();

    if (millis() - step_time > max_time) {
      Serial.print("step timeout breaking...");
      Serial.println(millis() - step_time);
      break;
    }

    if (millis() - last_print > PRINT_INTERVAL) {
      Serial.print("end condition: ");
      Serial.print(end_condition);
      Serial.print(" current angle: ");
      Serial.println(get_angle());
      last_print = millis();
    }
  }

  non_braking_stop();
}

void move_backward(float angle) {
  float current_angle = get_angle();
  if (current_angle <= min_angle) {
    Serial.println("out of bounds");
    return;
  }

  float end_condition = current_angle - angle;
  if (end_condition < min_angle) end_condition = min_angle;

  Serial.print("end condition: ");
  Serial.println(end_condition);
  Serial.print("current angle: ");
  Serial.println(current_angle);

  set_backward();

  unsigned long step_time = millis();
  unsigned long max_time = (unsigned long)(angle * STEP_MAX_TIME_CONSTANT);

  while (current_action != ACTION_NONE && get_angle() > end_condition && get_angle() > min_angle) {
    encoder.update();

    if (millis() - step_time > max_time) {
      Serial.println(millis() - step_time);
      break;
    }

    if (millis() - last_print > PRINT_INTERVAL) {
      Serial.print("end condition: ");
      Serial.print(end_condition);
      Serial.print(" current angle: ");
      Serial.println(get_angle());
      last_print = millis();
    }
  }

  non_braking_stop();
}

void move_up() {
  step_up();
}

void move_down() {
  step_down();
}

void handle_forward(int angle) {
  if (REVERSE_DIRECTION)
    move_backward(angle);
  else
    move_forward(angle);
}

void handle_backward(int angle) {
  if (REVERSE_DIRECTION)
    move_forward(angle);
  else
    move_backward(angle);
}

void zero_encoder() {
  zero_offset = encoder.getAngle();
  Serial.print("zeroed encoder: ");
  Serial.println(zero_offset);
  Serial.print("current_angle");
  Serial.println(get_angle());
}

void go_home() {
  float angle = get_angle();
  if (abs(angle) < HOMING_THRESHOLD)
    return;

move_up();
  if (angle < 0)
    move_forward(-angle);
  else if (angle >= 0)
    move_backward(angle);
  move_down();
}

void receiveCommand(int numBytes) {
  while (Wire.available()) {
    unsigned char byte = Wire.read();
    if (byte >= 0x10) continue;
    current_action = byte;
  }
}

void sendStatus() {
  Wire.write(current_action == ACTION_NONE);
}

void setup()
{
  Wire.begin(INO_ADDRESS);
  Wire.onReceive(receiveCommand);
  Wire.onRequest(sendStatus);

  pinMode(MAX485_RE_NEG, OUTPUT);
  pinMode(MAX485_DE, OUTPUT);
  pinMode(FLOOR_CONTACT_PIN, INPUT);
  pinMode(LIMIT_PIN, INPUT_PULLUP);

  pinMode(HALL_A, INPUT_PULLUP);
  pinMode(HALL_B, INPUT_PULLUP);
  pinMode(HALL_C, INPUT_PULLUP);
  encoder.init();

  digitalWrite(MAX485_RE_NEG, LOW);
  digitalWrite(MAX485_DE, LOW);

  pinMode(EN_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(PUL_PIN, OUTPUT);

  digitalWrite(EN_PIN, HIGH);
  digitalWrite(DIR_PIN, LOW);
  digitalWrite(PUL_PIN, LOW);

  RS485_serial.begin(9600);
  Serial.begin(115200);

  node.begin(1, RS485_serial);
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  delay(500);

  set_motor_speed();
  delay(100);

  last_print = millis();
}

void get_action_serial() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'f')
      current_action = ACTION_FORWARD;
    if (c == 'b')
      current_action = ACTION_BACKWARD;
    if (c == 'u')
      current_action = ACTION_UP;
    if (c == 'd')
      current_action = ACTION_DOWN;
    if (c == 'c')
      set_motor_speed();
    if (c == 'l')
      current_action = ACTION_HOME_FORWARD;
    if (c == 'k')
      current_action = ACTION_HOME_BACKWARD;
    if (c == 'z')
      current_action = ACTION_ZERO;
    if (c == 'h')
      current_action = ACTION_HOME;
  }
}

void loop()
{
  encoder.update();
  get_action_serial();
  if        (current_action == ACTION_FORWARD) {
    Serial.println("RECEIVED ACTION_FORWARD");
    handle_forward(HIP_MOVE_INTERVAL);
  } else if (current_action == ACTION_BACKWARD) {
    Serial.println("RECEIVED ACTION_BACKWARD");
    handle_backward(HIP_MOVE_INTERVAL);
  } else if (current_action == ACTION_UP) {
    Serial.println("RECEIVED ACTION_UP");
    move_up();
  } else if (current_action == ACTION_DOWN) {
    Serial.println("RECEIVED ACTION_DOWN");
    move_down();
  } else if (current_action == ACTION_HOME_FORWARD) {
    Serial.println("RECEIVED ACTION_HOME_FORWARD");
    handle_forward(HIP_HOME_INTERVAL);
  } else if (current_action == ACTION_HOME_BACKWARD) {
    Serial.println("RECEIVED ACTION_HOME_BACKWARD");
    handle_backward(HIP_HOME_INTERVAL);
  } else if (current_action == ACTION_ZERO) {
    Serial.println("RECEIVED ACTION_ZERO");
    zero_encoder();
  } else if (current_action == ACTION_HOME) {
    Serial.println("RECEIVED ACTION_HOME");
    go_home();
  }
  current_action = ACTION_NONE;
}