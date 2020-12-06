COLORS = {
    # BGR Pattern ,\
    'BLUE' : (255,0,0),\
    'GREEN' : (0,255,0),\
    'RED' : (0,0,255),\
    'YELLOW' : (0,255,255),\
    'BLACK' : (0,0,0),\
    'WHITE' : (255,255,255),\
}

GeneralSettings = {
    'MinFreeDisk' : 500.0,\
    'useImShow' : False,\
    'clientIP' : 'localhost' ,\
    'serverIP' : 'localhost',\
}

DBSettings = {
    'MySQLDBName': 'cdp2',\
    'MySQLDBUsername': 'sty',\
    'MySQLDBPassword': 'Sty@2018',\
}

RabbitMQSettings = {
    'Port' : 5672,\
    #'LocalHostName': 'rabbitmq',\
    'RemoteUsername' : 'sty',\
    'RemotePassword' : 'sty@2018',\
    'LocalHostName': 'localhost',\
    'LocalUsername' : 'sty',\
    'LocalPassword' : 'sty@2018',        
}

MailSettings ={
    'SMTPServer' : 'mail.shyenatechyarns.com',\
    'SMTPPort' : 465,\
    'SenderEmail' : 'support@shyenatechyarns.com',\
    'SenderPassword' : 'passwordis$$',\
    # 'ReceiverEmailID': ['sachin@drhm.co.in', 'chiefengineer@drhm.co.in', 'v.gujarathi777@gmail.com']
    'ReceiverEmail' : ['v.gujarathi777@gmail.com'],\
    'DeveloperEmail' : ['v.gujarathi777@gmail.com', 'shjoshi6357@gmail.com']
}