import random



def execute(plugins):
    return_value = {'test':random.randrange(0,1000)}

    echo = plugins('echo')

    if echo:
        echo.execute(plugins, return_value)

    else:
        print(dir(echo))
