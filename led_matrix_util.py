"""Utilities for the led library"""


def clamp(n, min_n, max_n):
    """Limits the range of n between min_n and max_n"""
    return max(min(max_n, n), min_n)


def change_matrix_options(matrix_options, **kwargs):
    print(kwargs.get("name"), kwargs.get("not real"))
    options = matrix_options
    try:
        if kwargs.get("led_gpio_mapping") is not None:
            options.hardware_mapping = kwargs.get("led_gpio_mapping")
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
        if  kwargs.get("led_slowdown_gpio") is not None:
            options.gpio_slowdown = kwargs.get("led_slowdown_gpio")
        if kwargs.get("led_no_hardware_pulse"):
            options.disable_hardware_pulsing = True
    except:
        raise UserWarning("There was an error processing these commands")
