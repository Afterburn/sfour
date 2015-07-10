


def execute(**args):

    condition = args['condition']
    alias     = args['alias']
    db        = args['db']
    table     = db['data']


    if condition == 'any_value':
        result = list(table.find(alias=alias)


    
