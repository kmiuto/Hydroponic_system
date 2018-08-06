/********************************************************************

This is a program for Hydroponic Machine.
If you excution this program, measurments and machine control start.

********************************************************************/
//include header file
#include<Arduino.h>
#include <DHT.h>

//pins for Temperature and Humidity Sensor
const int PIN_DHT = 8;
DHT dht(PIN_DHT,DHT11);

//pins for LED
const int upper_redPin = 3;
const int upper_greenPin = 9;
const int upper_bluePin = 10;

void setup() {
  Serial.begin(9600);
  dht.begin();
}

//control_upper_red_LED
void control_upper_red(){
  while(Serial.available() == 0){
  }
  if(Serial.available() > 0){
    String message = Serial.readStringUntil(";");
    int command = message.toInt();
    analogWrite(3,command);
    Serial.print("upper_red_OK\n");
  }
}

//control_upper_green_LED
void control_upper_green(){
  while(Serial.available() == 0){
  }
  if(Serial.available() > 0){
    String message = Serial.readStringUntil(";");
    int command = message.toInt();
    analogWrite(9,command);
    Serial.print("upper_green_OK\n");
  }
}

//control_upper_blue_LED
void control_upper_blue(){
  while(Serial.available() == 0){
  }
  if(Serial.available() > 0){
    String message = Serial.readStringUntil(";");
    int command = message.toInt();
    analogWrite(10,command);
    Serial.print("upper_blue_OK\n");
  }
}

//data send to Arduino.
void Send_data(){
  float Temp = Temp_Sensor();
  float Hum = Hum_Sensor();
  //Serial.print("Temperature:  ");
  Serial.print(Temp);
  Serial.print(",");
  //Serial.println(" degC");
  //Serial.print("Humidity:  ");
  Serial.print(Hum);
  Serial.print("\n");
  //Serial.println("%\t");
  return 0;
}

//Measure the temperature.
float Temp_Sensor(){
  float Temperature = dht.readTemperature();
  return Temperature;
}

//Measure the humidity.
float Hum_Sensor(){
  float Humidity = dht.readHumidity();
  return Humidity;
}

void loop() {
  if (Serial.available() > 0){
    char input_char = Serial.read();
    if (input_char == 'a'){
      Send_data();
    }
    else if (input_char == 'b'){
      Serial.print("Control_upper_red\n");
      control_upper_red();
    }
    else if (input_char == 'c'){
      Serial.print("Control_upper_green\n");
      control_upper_green();
    }
    else if (input_char == 'd'){
      Serial.print("Control_upper_blue\n");
      control_upper_blue();
    }
    else if (input_char == 'z'){
      Serial.print("connect_OK\n");
    }
    else{
      Serial.print("other\n");
    }
  }
  else{
  }
}

