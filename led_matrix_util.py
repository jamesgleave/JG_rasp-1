"""Utilities for the led library"""
import subprocess


def shutdown():
    subprocess.call(["sudo", "poweroff"])


def clamp(n, min_n, max_n):
    """Limits the range of n between min_n and max_n"""
    return max(min(max_n, n), min_n)


def change_matrix_options(matrix_options, **kwargs):
    print(kwargs.get("name"), kwargs.get("not real"))
    options = matrix_options
    try:
        if kwargs.get("led_gpio_mapping") is not None:
            options.hardware_mapping = kwargs.get("led_gpio_mapping")
        if kwargs.get("led_pwm_dither_bits") is not None:
            options.led_pwm_dither_bits = kwargs.get("led_pwm_dither_bits")
        if kwargs.get("hardware_mapping") is not None:
            options.hardware_mapping = kwargs.get("hardware_mapping")
        if kwargs.get("multiplexing") is not None:
            options.multiplexing = kwargs.get("multiplexing")
        if kwargs.get("pwm_bits") is not None:
            options.pwm_bits = kwargs.get("pwm_bits")
        if kwargs.get("brightness") is not None:
            brightness = kwargs.get("brightness")
            if brightness > 99 or brightness < 0:
                print("Brightness value received was not a percentage.\n It has been clamped between 0 and 100.")
            brightness = clamp(brightness, 0, 100)
            options.brightness = brightness
        if kwargs.get("pwm_lsb_nanoseconds") is not None:
            options.pwm_lsb_nanoseconds = kwargs.get("pwm_lsb_nanoseconds")
        if kwargs.get("led_rgb_sequence") is not None:
            options.led_rgb_sequence = kwargs.get("led_rgb_sequence")
        if kwargs.get("led_show_refresh"):
            options.show_refresh_rate = 1
        if kwargs.get("led_slowdown_gpio") is not None:
            options.gpio_slowdown = kwargs.get("led_slowdown_gpio")
        if kwargs.get("led_scan_mode") is not None:
            options.led_scan_mode = kwargs.get("led_scan_mode")
        if kwargs.get("led_daemon") is not None:
            options.led_daemon = kwargs.get("led_daemon")

    except Exception:
        led_matrix_help()
        raise UserWarning("There was an error processing these commands")


def led_matrix_help():
    print("HELP:")
    print("pwm_bits=<1..11> default is 11 -> Higher values lead to higher color range")
    print("brightness=<percent> default is 100")
    print("led_show_refresh Shows refresh rate of the led panel")
    print("led_scan_mode=<0..1> 0 = progressive; 1 = interlaced (Default: 0) -> 1 looks better with low refresh rate")
    print("pwm_lsb_nanoseconds PWM Nanoseconds for LSB (Default: 130) -> lower results in (maybe) more ghosting")
    print("led_pwm_dither_bits Time dithering of lower bits (Default: 0) -> higher refresh rate but lower brightness")
    print("led_slowdown_gpio=<0..2> Needed for faster Pis and/or slower panels (Default: 1) -> for pi3 2 may be needed")
    print("led_daemon If this is set, the program puts itself into the background (running as 'daemon'). "
          "You might want this if started from an init script at boot-time.")
