while True:
    operator = ""
    value1 = 0
    value2 = 0
    pressed = ""
    while not (pressed == "+" or pressed == "-" or pressed == "*" or pressed == "/" or pressed == "reset"):
        pressed = input().strip()
        try:
            if not (pressed == "+" or pressed == "-" or pressed == "*" or pressed == "/" or pressed == "reset"):
                value1 *= 10
                value1 += int(pressed)
            else:
                pass
        except:
            print("Not a number")
            pass
    if pressed != "reset":
        operator = pressed
    while pressed != "=" and pressed != "reset":
        pressed = input().strip()
        try:
            if pressed != "=" and pressed != "reset":
                value2 *= 10
                value2 += int(pressed)
            else:
                pass
        except:
            print("Not a number")
            pass
    if pressed == "=":
        if operator == "+":
            print(value1 + value2)
        elif operator == "-":
            print(value1 - value2)
        elif operator == "*":
            print(value1 * value2)
        elif operator == "/":
            print(value1 / value2)