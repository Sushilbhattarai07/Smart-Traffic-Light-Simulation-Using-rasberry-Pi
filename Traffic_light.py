import RPi.GPIO as GPIO 
import time
import os
from threading import Thread, Event

# ---------------- GPIO SETUP ----------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RED = 23
YELLOW = 27
GREEN = 22
EMG_LED = 24
BUTTON_PED = 17
BUTTON_EMG = 25

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(EMG_LED, GPIO.OUT)

GPIO.setup(BUTTON_PED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_EMG, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ---------------- EVENTS ----------------
ped_event = Event()
emg_event = Event()

# ---------------- HELPERS ----------------
def all_off():
    GPIO.output(RED, False)
    GPIO.output(YELLOW, False)
    GPIO.output(GREEN, False)
    GPIO.output(EMG_LED, False)


def log(msg):
    print("[" + time.strftime('%H:%M:%S') + "] " + msg)


def set_priority(level):
    try:
        if level == 'high':
            os.nice(-10)
        elif level == 'medium':
            os.nice(0)
        elif level == 'low':
            os.nice(10)
    except PermissionError:
        log("Run with sudo to change priority")


# ---------------- TRAFFIC LIGHT LOGIC ----------------
def traffic_light():
    set_priority('low')

    while True:

        # EMERGENCY MODE
        if emg_event.is_set():
            log("EMERGENCY MODE")
            all_off()
            GPIO.output(RED, True)
            GPIO.output(EMG_LED, True)
            time.sleep(5)
            emg_event.clear()
            continue

        # PEDESTRIAN MODE
        if ped_event.is_set():
            log("Pedestrian crossing")
            all_off()
            GPIO.output(YELLOW, True)
            time.sleep(3)

            all_off()
            GPIO.output(RED, True)
            time.sleep(5)

            ped_event.clear()
            continue

        # NORMAL CYCLE
        log("GREEN - Traffic moving")
        all_off()
        GPIO.output(GREEN, True)
        time.sleep(10)

        if emg_event.is_set() or ped_event.is_set():
            continue

        log("YELLOW - Slow down")
        all_off()
        GPIO.output(YELLOW, True)
        time.sleep(3)

        if emg_event.is_set() or ped_event.is_set():
            continue

        log("RED - Stop")
        all_off()
        GPIO.output(RED, True)
        time.sleep(5)


# ---------------- BUTTON HANDLERS ----------------
def pedestrian_button():
    set_priority('medium')
    while True:
        if GPIO.input(BUTTON_PED) == 0:
            time.sleep(0.05)
            if GPIO.input(BUTTON_PED) == 0:
                log("Pedestrian button pressed")
                ped_event.set()
                while GPIO.input(BUTTON_PED) == 0:
                    time.sleep(0.1)
        time.sleep(0.05)


def emergency_button():
    set_priority('high')
    while True:
        if GPIO.input(BUTTON_EMG) == 0:
            time.sleep(0.05)
            if GPIO.input(BUTTON_EMG) == 0:
                log("EMERGENCY button pressed")
                emg_event.set()
                while GPIO.input(BUTTON_EMG) == 0:
                    time.sleep(0.1)
        time.sleep(0.05)


# ---------------- THREAD START ----------------
t1 = Thread(target=traffic_light, daemon=True)
t2 = Thread(target=pedestrian_button, daemon=True)
t3 = Thread(target=emergency_button, daemon=True)

log("Starting system...")

all_off()

t1.start()
t2.start()
t3.start()

# ---------------- MAIN LOOP ----------------
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    log("Shutting down...")
    all_off()
    GPIO.cleanup()
    log("Clean exit")
