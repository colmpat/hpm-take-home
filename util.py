def to_celcius(kelvin):
    return kelvin - 273.15


def to_fahrenheit(kelvin):
    return kelvin * 9 / 5 - 459.67


# Convert the temperature to a string with no decimal places
def celc_str(celcius):
    return "{:.0f}C".format(celcius)


# Convert the temperature to a string with no decimal places
def fahr_str(fahrenheit):
    return "{:.0f}F".format(fahrenheit)
