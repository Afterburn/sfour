import random



def execute(plugins, db):
    value = {'test':random.randrange(0,1000)}

    echo = plugins('echo')

    if echo:
        echo.execute(plugins, db, value)

    else:
        print('cant echo')
