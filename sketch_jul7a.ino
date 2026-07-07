#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define LED_PIN 8 

MFRC522 rfid(SS_PIN, RST_PIN);

// Сюди впишіть UID вашої карти, який ви дізналися раніше
// Наприклад: 0A 1B 2C 3D
byte allowedUID[] = {0x74, 0xC8, 0x43, 0x1D};

void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(LED_PIN, OUTPUT);
  Serial.println("Система готова. Очікую на авторизовану карту...");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  // Перевірка: чи співпадає UID карти з дозволеним
  bool isAuthorized = true;
  for (byte i = 0; i < 4; i++) {
    if (rfid.uid.uidByte[i] != allowedUID[i]) {
      isAuthorized = false;
      break;
    }
  }

  if (isAuthorized) {
    Serial.println("Доступ дозволено! Відкриваю.");
    digitalWrite(LED_PIN, HIGH);
    delay(3000);
    digitalWrite(LED_PIN, LOW);
  } else {
    Serial.println("Доступ заборонено! Карта невідома.");
    // Можна блимнути світлодіодом 3 рази для помилки
    for(int i=0; i<6; i++){
        digitalWrite(LED_PIN, HIGH); delay(200);
        digitalWrite(LED_PIN, LOW); delay(200);
    }
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}