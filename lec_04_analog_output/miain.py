from machine import Pin, PWM
import time

# Set up PWM on pin 16
pwm = PWM(Pin(16))
pwm.freq(1000)  # 1kHz PWM frequency

# Function to simulate analog output (0 to 3.3V)
def analog_out(voltage):
    max_voltage = 3.3
    if voltage < 0:
        voltage = 0
    elif voltage > max_voltage:
        voltage = max_voltage

    duty_u16 = int((voltage / max_voltage) * 65535)
    pwm.duty_u16(duty_u16)
    print(f"Voltage set to: {voltage:.2f}V (Duty: {duty_u16})")

# Main loop to get voltage input from user
while True:
    try:
        user_input = input("Enter voltage between 0 and 3.3V: ")
        voltage = float(user_input)
        analog_out(voltage)
    except ValueError:
        print("Invalid input! Please enter a number between 0 and 3.3.")
    time.sleep(0.1)
