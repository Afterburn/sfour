import logging
from jinja2 import Environment, FileSystemLoader

import emailutils



#https://pythonhosted.org/feedparser/


logger = logging.getLogger()
env    = Environment()

def execute(db, **args):
    email   = None
    message = None

    if 'message' in args:
        message = args['message']
   
    if 'notify' in args:
        if 'email' in args['notify']:
            email = args['notify']['email']
    
    # Notify on anything new
    #if 'new' in args and args['new'] == True:
    #    logging.debug('notification: %s' % args)
    #    msg = env.from_string(args['message'])
    #    print(msg.render(args['entry']))

    
    # emailutils is being imported from main.py's location. (I think)
    # if email is not True, then it won't bother looking at global_cfg
    if message and email:
   
        print(args['email_settings'])
        emailutils.send_email(to=args['email_settings']['to'],
                              from_=args['email_settings']['from'],
                              subject=args['email_settings']['subject'],
                              body=message)



