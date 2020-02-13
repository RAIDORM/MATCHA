#include <SoftwareSerial.h>

#include "CLCD.h"

SoftwareSerial rfid(7, 8);
CLCD lcd(0x00, 20, 4);
String readed;

void setup() {
  Serial.begin(9600);
  rfid.begin(19200);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(1, 6);
  lcd.print("Bonjour");
  lcd.setCursor(2, 1);
  lcd.print("Passer votre carte");
}

void loop() {
  rfid.write((uint8_t) 0xFF);
  rfid.write((uint8_t) 0x00);
  rfid.write((uint8_t) 0x01);
  rfid.write((uint8_t) 0x82);
  rfid.write((uint8_t) 0x83);

  delay(500);

  while (rfid.available() > 0) {
    readed += String(rfid.read(), HEX);
  }
  if (readed != "ff02824cd0") {
    Serial.println(readed.substring(17, 25));
    delay(500);
  }
  readed = "";
  if (Serial.available() > 0) {
    lcd.clear();
    String tickets = Serial.readString();
    if (tickets == "dv") {
      lcd.setCursor(1, 4);
      lcd.print("Deja valide");
      digitalWrite(2, HIGH);
      delay(1000);
      digitalWrite(2, LOW);
    } else {
      if (tickets == "-1") {
        lcd.setCursor(1, 0);
        lcd.print("Acheter des tickets");
        digitalWrite(2, HIGH);
        digitalWrite(3, HIGH);
        delay(1000);
        digitalWrite(2, LOW);
        digitalWrite(3, LOW);
      } else {
        digitalWrite(3,HIGH);
        delay(10);
        digitalWrite(3,LOW);
        digitalWrite(4, HIGH);
        delay(1000);
        digitalWrite(4, LOW);
        lcd.setCursor(1, 2);
        lcd.print("Il vous reste :");
        lcd.setCursor(2, 4);
        lcd.print(tickets);
        lcd.print(" trajets ! ");
      }
    }

    delay(2000);
    lcd.clear();
    lcd.setCursor(1, 6);
    lcd.print("Bonjour");
    lcd.setCursor(2, 1);
    lcd.print("Passer votre carte");
  }
}
