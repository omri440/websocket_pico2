# 🚨 Smart Alarm System with WebSocket & Raspberry Pi Pico W

This project implements a real-time smart alarm system using a Raspberry Pi Pico W, with the following features:

- Motion detection via PIR sensor
- Temperature monitoring
- Real-time WebSocket-based communication to browser
- Control of two LEDs (green and red) remotely via WebSocket
- System status reporting (memory, temperature, sensor)

---

## 📦 Features

- 📡 Wi-Fi connection with Pico W
- 🌡️ Internal temperature sensor reading
- 🟢 LED control via browser (green/red toggle)
- 🕵️‍♂️ Motion detection via PIR sensor (WebSocket alert)
- 💬 Real-time memory and temperature monitoring
- 🔄 Supports remote arming/disarming of the alarm system

---

## 🧰 Hardware Requirements

- Raspberry Pi Pico W
- 1x PIR Motion Sensor
- 2x LEDs (optional: with resistors)
- Breadboard + jumper wires

### Wiring Summary:

| Component  | Pico GPIO Pin |
|------------|----------------|
| PIR sensor | GPIO13         |
| Red LED    | GPIO14         |
| Green LED  | GPIO15         |

> The PIR sensor must be connected to 3.3V and GND, with the output pin going to GPIO13.

---

## 📁 File Structure

