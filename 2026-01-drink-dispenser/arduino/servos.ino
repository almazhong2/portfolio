#include <Servo.h>
#include <string.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;


void setup() {
  Serial.begin(115200);
  while (Serial.available()) {
  Serial.read();  // flush junk
  }
  while(!Serial){;} // wait for serial port to connect

  servo1.attach(6);
  servo2.attach(7);
  servo3.attach(8);
  servo4.attach(9);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {


  if (Serial.available() > 0){
    String input = Serial.readStringUntil('\n');
    input.trim();
    int drink = input.toInt();
    
    if (drink == 1){ //coffee
      Serial.print("begin ");
      Serial.println(drink);
      delay(500);
      pour(servo1, 120, 5000);
      Serial.print("done ");
      Serial.println(drink);
      //servo1.write(0);
    }
    else if (drink == 2){ //water
      Serial.print("begin ");
      Serial.println(drink);
      delay(500);
      pour(servo2, 120, 5000);
      Serial.print("done ");
      Serial.println(drink);
      //servo2.write(0);
    }
    else if (drink == 3){ //soda
      Serial.print("begin ");
      Serial.println(drink);
      delay(500);
      pour(servo3, 120, 5000);
      Serial.print("done ");
      Serial.println(drink);
      //servo3.write(0);
    }
    else if (drink == 4){ //juice
      Serial.print("begin ");
      Serial.println(drink);
      delay(500);
      pour(servo4, 120, 50000);
      //servo4.write(0);
      Serial.print("done ");
      Serial.println(drink);
    }
    else{
      Serial.println("Invalid Selection");
      resetServos();
      delay(1000);
    }
    delay(1000);
  }
  
   
}

void pour(Servo& servo, int angle, int time){
  
  servo.write(angle);
  delay(time);
  servo.write(0);
  delay(500);
  

}

void ledTest(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

void resetServos(){
  servo1.write(0);			// Rotate to 0 degrees
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
}