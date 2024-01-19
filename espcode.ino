#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* serverAddress = "http://192.168.190.210:8080/eye_data";

#define ENA   12          
#define ENB   25          
#define IN_1  13          
#define IN_2  14          
#define IN_3  5          
#define IN_4  4          
int speedCar = 800;         


void setup() {
 pinMode(ENA, OUTPUT);
 pinMode(ENB, OUTPUT);  
 pinMode(IN_1, OUTPUT);
 pinMode(IN_2, OUTPUT);
 pinMode(IN_3, OUTPUT);
 pinMode(IN_4, OUTPUT); 
 Serial.begin(9600);

 WiFi.begin("known", "Sundar@1009");
 while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
 Serial.println("Connected to WiFi");
}

 

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverAddress);
    int httpCode = http.GET();

    if (httpCode > 0) {
      String payload = http.getString();

      if(payload=="Left"){
        Serial.println("Left");
        goLeft();

      }

      else if(payload=="Right"){
        Serial.println("Right");
        goRight();

      }

      else if(payload=="Centre"){
        Serial.println("Centre");
        goAhead();

      }
      
      else if(payload=="Blink"){
        Serial.println("Stop");
        stopChair ();
   
      }

    }
    else {
      Serial.println("Error on HTTP request");
      stopChair ();
    }

    http.end();

  }
}

void goAhead()
{ 
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
      delay(1000);
  }

void goRight()
{ 
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
      delay(1000);
  }

void goLeft()
{
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);
      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
      delay(1000);
  }

void stopChair ()
{  
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
      delay(1000);
 }


