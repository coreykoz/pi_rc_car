# https://github.com/Pioreactor/rpi_hardware_pwm <-- doesn't work

# Basics of Pulse-Width-Modulation (PWM)

# turns a digital signal into an analog signal by changing the timing of how long it stays on and off

# RPIO IS UMAINTAINED, USES DMA



import pigpio

pi = pigpio.pi()       # pi1 accesses the local Pi's GPIO


pi.hardware_PWM(18, 500, 630000) # 50Hz 25% dutycycle

pi.hardware_PWM(18, 500, 750000) # 2000Hz 75% dutycycle








from rpi_hardware_pwm import HardwarePWM

pwm = HardwarePWM(pwm_channel=1, hz=60)
pwm.start(100) # full duty cycle

pwm.change_duty_cycle(10)
pwm.change_frequency(25_000)