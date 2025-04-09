#include <Arduino.h>

int a = 0;

void setup()
{
  Serial.begin(9600);
  Serial.println("Starting");
}

void loop()
{
  for (int i = 0; i < 1024; i++)
  {
    String send = String("");
    send += String(i) + "|0|0|0|0|0|0|0|0|0|0|0";
    Serial.println(send);
    delay(100);
  }

  for (int i = 1024; i > 0; i--)
  {
    String send = String("");
    send += String(i) + "|0|0|0|0|0|0|0|0|0|0|0";
    Serial.println(send);
    delay(100);
  }

}
