


def execute(**args):

    condition = args['condition']
    alias     = args['alias']
    db        = args['db']
    table     = db['data']

    print(table.find(alias=alias))

    #print('observer: %s' % (args))
