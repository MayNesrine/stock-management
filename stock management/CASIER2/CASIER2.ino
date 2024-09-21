#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Servo.h>

const char* ssid = "SSID_WIFI";
const char* password = "PASSWORD";

const int greenLedPin = 5; 

const int redLedPin = 4; 
const int servoPin = 12;                         // replace with servo pin
Servo servo;
bool drawerOpen = false;

IPAddress ip(192, 168, 137, 100); // Adresse IP statique de votre ESP8266
IPAddress gateway(192, 168, 137, 1); // Adresse IP de votre passerelle
IPAddress subnet(255, 255, 255, 0); // Masque de sous-réseau

WiFiServer server(8080);

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(greenLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  digitalWrite(greenLedPin, LOW); 
  digitalWrite(redLedPin, LOW);  
  servo.attach(servoPin);
  servo.write(0);
  // Configuration de l'interface WiFi avec une adresse IP statique
  WiFi.config(ip, gateway, subnet);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }

  Serial.println("");
  Serial.println("WiFi connecté");
  Serial.println("Adresse IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  Serial.println("Nouvelle connexion");
  while (!client.available()) {
    delay(1);
  }

  String command = client.readStringUntil('\r');
  Serial.println("Requête reçue : " + command);

  if (command.indexOf("ouvrir_tiroir") != -1) {
    // Ouvrir le tiroir
    digitalWrite(greenLedPin, HIGH);
    servo.write(90);
    drawerOpen = true;
    Serial.println("Commande pour ouvrir le tiroir reçue !");
  } else if (command.indexOf("fermer_tiroir") != -1) {
    // Fermer le tiroir si ouvert
    if (drawerOpen) {
      digitalWrite(greenLedPin, LOW);
      servo.write(0);
      drawerOpen = false;
      Serial.println("Commande pour fermer le tiroir reçue !");
    } else {
      Serial.println("Le tiroir est déjà fermé.");
    }
  } else if (command.indexOf("manque_de_stock") != -1) {
    // Clignoter la LED rouge
    for (int i = 0; i < 5; i++) { // Clignote la LED rouge 5 fois
      digitalWrite(redLedPin, HIGH); // Allumer la LED rouge
      delay(500); // Attendre 500 ms
      digitalWrite(redLedPin, LOW); // Éteindre la LED rouge
      delay(500); // Attendre 500 ms
    }
    Serial.println("Commande pour signaler un manque de stock reçue !");
  } else {
    Serial.println("Commande inconnue");
  }

  client.flush();
  delay(1);
  Serial.println("Client déconnecté");
}
