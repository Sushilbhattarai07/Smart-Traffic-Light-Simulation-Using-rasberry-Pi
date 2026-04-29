# Smart-Traffic-Light-Simulation-Using-rasberry-Pi
Smart Raspberry Pi traffic light system with pedestrian and emergency control using multithreading and GPIO in Python.
# 🚦 Raspberry Pi Traffic Light System (Smart Controller)

A Python-based smart traffic light simulation using Raspberry Pi GPIO pins.  
This system includes **traffic control, pedestrian crossing, and emergency override functionality** using multithreading.

---

##  Features

-  Automatic traffic light cycling (Green → Yellow → Red)
-  Pedestrian crossing button support
-  Emergency override system (highest priority)
-  Multithreaded design for real-time responsiveness
-  Button debounce handling for stable input
-  Safe GPIO cleanup on exit
-  Simple event-based control system

---

##  Hardware Requirements

- Raspberry Pi (any model with GPIO support)
- 3 × LEDs (Red, Yellow, Green)
- 1 × Emergency LED
- 2 × Push buttons
- Resistors (220Ω recommended)
- Breadboard & jumper wires

---

##  GPIO Pin Configuration

| Component        | GPIO Pin (BCM) |
|------------------|----------------|
| Red Light        | 23             |
| Yellow Light     | 27             |
| Green Light      | 22             |
| Emergency LED    | 24             |
| Pedestrian Button| 17             |
| Emergency Button | 25             |

---

##  Software Requirements

- Python 3
- RPi.GPIO library

Install GPIO library if needed:

```bash
pip install RPi.GPIO
