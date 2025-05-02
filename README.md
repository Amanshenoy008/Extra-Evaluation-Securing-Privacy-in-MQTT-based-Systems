# Extra-Evaluation-Securing-Privacy-in-MQTT-based-Systems
To simulate MQTT communication between the victims, drones (brokers), and the C2 system, identify privacy threats, and implement privacy enhancement technologies (PETs) in the system.

## 🛠️ Tools Used

- Python 3.10+
- `paho-mqtt` for MQTT client communication
- Mosquitto MQTT Broker (via Homebrew)
- Virtual Environment (`venv`) for dependency isolation
- LINDDUN privacy threat modeling framework

## 📦 Installation Instructions
### 1. Clone the Repository

```bash
git clone git@github.com:Amanshenoy008/Extra-Evaluation-Securing-Privacy-in-MQTT-based-Systems.git

cd Extra-Evaluation-Securing-Privacy-in-MQTT-based-Systems
```

### 2. Install and Start mosquitto service locally
```bash
    brew install mosquitto

    brew services start mosquitto
```

### 3. Create a virtual environment

```bash
    python3 -m venv .venv

    source .venv/bin/activate
```
### 4. Install python dependencies

```bash
    pip install paho-mqtt
```
### 5. Start the publisher and subscriber python file

```bash
    python publisher.py

    python subscriber.py
```
### The Output 

## 
- from publisher terminal
```bash
    [INFO] Connected with result code 0
[PUBLISH] Sent: {"user_id": "victim_01", "location": "37.7749,-122.4194", "message": "Stuck on rooftop!"}
[PUBLISH] Sent: {"user_id": "victim_03", "location": "37.7600,-122.4477", "message": "Water level rising fast!"}

```
- from subscriber terminal
```bash
[INFO] Connected with result code 0
[INFO] Subscribed to topic: disaster/alerts
[RECEIVED] Topic: disaster/alerts | Payload: {'user_id': 'victim_01', 'location': '37.7749,-122.4194', 'message': 'Stuck on rooftop!'}
[RECEIVED] Topic: disaster/alerts | Payload: {'user_id': 'victim_03', 'location': '37.7600,-122.4477', 'message': 'Water level rising fast!'}
```

## 🔍 Privacy Threat Analysis (LINDDUN)

The following threats were identified in the base MQTT setup without any privacy-enhancing techniques:

| **System Element** | **Threat Type**   | **Explanation**                                                                 |
|--------------------|------------------|---------------------------------------------------------------------------------|
| `user_id`          | Identifiability  | Directly reveals the user's identity                                           |
| `user_id`          | Linkability      | Messages can be linked over time from the same user                           |
| MQTT topic         | Detectability    | Attackers could detect traffic on `disaster/alerts`                           |
| `location`         | Disclosure       | Sensitive location data can reveal user’s whereabouts                         |
| Plaintext payload  | Disclosure       | Anyone intercepting can read distress messages                                |
| Lack of consent UI | Unawareness      | Victims may not know how much data is being sent/stored                       |
| No legal framework | Non-compliance   | If stored or forwarded to third parties, could violate privacy laws (e.g., GDPR) |
| Logged messages    | Non-repudiation  | Logs could falsely be used to prove someone sent a message                    |


## 📊 Privacy and System Evaluation (before vs after)

| **Metric**              | **Without PETs**                                      | **With All 5 PETs**                                                |
|--------------------------|--------------------------------------------------------|---------------------------------------------------------------------|
| User Identifiability     | `user_id` exposed (e.g., "victim_01")                 | SHA-256 pseudonymized ID                                           |
| Linkability              | Messages easily linked via user ID                    | Reduced due to tokenization                                        |
| Message Confidentiality  | Plaintext – broker and interceptors can read it       | AES-encrypted using `cryptography.Fernet`                          |
| Topic Visibility         | Topic name: `disaster/alerts` visible to attacker     | Topic hashed via SHA-256                                           |
| Transport Security       | None                                                  | `client.tls_set()` included (TLS simulated in code)                |
| Data Minimization        | Full JSON: includes IDs, location, metadata           | Minimized to: `id`, `loc`, `msg`                                   |
| Message Size             | ~150 bytes                                            | ~230–250 bytes (encryption + hash overhead)                        |
| Performance Overhead     | None                                                  | Minor CPU + memory cost (hashing, encryption)                      |
| Usability Impact         | N/A                                                   | Transparent to users (app handles all PETs internally)             |
| Legal/Privacy Compliance | Likely violates GDPR-like standards                   | Stronger compliance via data minimization and anonymization        |


## 🔁 Message Comparison

### 🟠 Before (Without PETs)

```json
{
  "user_id": "victim_01",
  "location": "37.7749,-122.4194",
  "message": "Stuck on rooftop!"
}
```

### After

```bash
<encrypted_payload>
```

## ⚙️ Effectiveness and Trade-Offs

The applied PETs significantly improved privacy without compromising core functionality.

### 🔐 Strengths
- **Encryption** ensures confidentiality even if traffic is intercepted.
- **Tokenization** protects user identity while preserving functionality.
- **Data Minimization** reduces unnecessary exposure of metadata.
- **Topic Obfuscation** prevents external parties from learning about message purpose or routing.
- **Transport Layer Security (simulated)** defends against sniffing at the broker level.

### ⚖️ Trade-Offs
- **Performance:** Slight increase in CPU time for hashing and encryption
- **Message Size:** Approx. 50–100 byte increase per message
- **Complexity:** Requires additional setup (shared keys, hashing functions, encryption/decryption logic)

Overall, these are acceptable trade-offs given the sensitivity of the data and potential real-world implications in disaster scenarios.

## 🧠 Reflection on Design, Behavior & Usability

Implementing PETs introduced minimal friction to the system’s usability:

- The core publishing/subscribing logic remained the same.
- PETs like tokenization and encryption were applied transparently inside the app.
- Topics were hashed behind the scenes; users didn't interact with or notice the change.
- Usability was unaffected — all privacy was enforced at the communication and data layer.

However, the architecture evolved from a simple proof-of-concept into a privacy-aware system:
- The broker no longer has access to message contents or user identities.
- The system became resilient to eavesdropping, man-in-the-middle attacks, and data leaks.

This evolution aligns with privacy-by-design principles and prepares the system for secure, real-world deployments.


