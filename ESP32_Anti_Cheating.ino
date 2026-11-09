/*
  ESP32 WROOM - AI Anti-Cheating LED Indicator
  Commands received over USB serial:
    G = Green LED ON (face looking toward camera)
    R = Red LED ON   (head turned away / alert)
    N = Both LEDs OFF

  Wiring:
    GPIO 25 -> 220/330 ohm resistor -> Green LED anode (+)
    GPIO 26 -> 220/330 ohm resistor -> Red LED anode (+)
    Both LED cathodes (-) -> ESP32 GND
*/

#define GREEN_LED 25
#define RED_LED   26

char currentState = 'N';

void allLedsOff() {
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
}

void setIndicator(char command) {
  if (command == currentState) {
    return;
  }

  allLedsOff();

  if (command == 'G') {
    digitalWrite(GREEN_LED, HIGH);
    Serial.println("STATUS: CORRECT - GREEN LED ON");
    currentState = 'G';
  }
  else if (command == 'R') {
    digitalWrite(RED_LED, HIGH);
    Serial.println("STATUS: LOOKING AWAY - RED LED ON");
    currentState = 'R';
  }
  else if (command == 'N') {
    allLedsOff();
    Serial.println("STATUS: LEDs OFF");
    currentState = 'N';
  }
}

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  allLedsOff();

  Serial.begin(115200);
  delay(500);
  Serial.println("ESP32 ANTI-CHEATING INDICATOR READY");

  // Start in alert state until Python sends a valid status.
  setIndicator('R');
}

void loop() {
  while (Serial.available() > 0) {
    char received = (char)Serial.read();

    if (received == 'G' || received == 'R' || received == 'N') {
      setIndicator(received);
    }
  }
}
