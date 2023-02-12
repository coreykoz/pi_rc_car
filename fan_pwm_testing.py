# https://github.com/Pioreactor/rpi_hardware_pwm

from rpi_hardware_pwm import HardwarePWM

pwm = HardwarePWM(pwm_channel=0, hz=60)
pwm.start(100) # full duty cycle

pwm.change_duty_cycle(10)
pwm.change_frequency(25_000)