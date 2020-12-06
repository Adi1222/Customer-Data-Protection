'''
This is the main script file for Rabbit MQ

### WORKING
 - Provides link to RabbitMQ Servers to other scripts
 - Establishes connection
 - Creates a channel
 

### FRAMEWORKS
1. Message Queue - Rabbit MQ

### AUTHORS
Varun Gujarathi, Saurabh Joshi, Ankit Kumar Singh, Ankit Aglawe
(Shyena Tech Yarns)

### CREATED
28th March 2020
'''
#--------------------------------------------------------------------------------------------

# libraries
import pika
import os

# import developer scripts
import configs
#--------------------------------------------------------------------------------------------

# variables
localConnectionStatus = 1
localMQChannel = None
localMQConnection = None
localDeclaredQueues = []

remoteConnectionStatus = 0
remoteMQChannel = None
remoteMQConnection = None
remoteCredentials = pika.PlainCredentials(configs.RabbitMQSettings['RemoteUsername'],configs.RabbitMQSettings['RemotePassword'])
localCredentials = pika.PlainCredentials(configs.RabbitMQSettings['LocalUsername'],configs.RabbitMQSettings['LocalPassword'])
#--------------------------------------------------------------------------------------------

# Local Rabbit MQ

def localIsConnected():
    '''
    This function checks if complete connection to local Rabbit MQ Server is available i.e. pika connection is established --> pika channel is opened. 
    In the function I have used representation of the status of connection using numbers, description of which is given below \n
    1: RMQ Server available but pika not connected \n
    2: Pika is connected, but channel is not opened \n
    3: Pika channel is open and we are good to send/receive data
    '''
    
    global localConnectionStatus, localMQChannel, localMQConnection

    if localConnectionStatus == 1:  
             
        if localPikaConnect():
            localConnectionStatus = 2
        else:
            pass

    if localConnectionStatus == 2:
        # open pika channel 
        if localPikaChannelOpen():
            # channel opened
            localConnectionStatus = 3
        else:
            if localMQConnection.is_open:
                # queue connection is available but channel is not open
                localConnectionStatus = 2
            else:
                # queue connection is not available
                localConnectionStatus = 1    

    if localConnectionStatus == 3:
        if localMQChannel.is_open:
            return True
        else:
            localConnectionStatus = 2
            localDeclaredQueues = []
            return False
        
    return False              

def localPikaConnect():
    '''
        #### @brief\n
        Check whether local MQ connection is established or not
        If not then it creates one

        #### @params\n
        None
    
        #### @return\n
        Boolean
    '''
    global localConnectionStatus, localMQChannel, localMQConnection, remoteCredentials

    try:
        localMQConnection = pika.BlockingConnection(pika.ConnectionParameters(host=configs.RabbitMQSettings['LocalHostName'],credentials=localCredentials))
    except Exception as exception:
        print('localPikaConnect ERROR:', exception)
        return False

    if localMQConnection.is_open:
        return True
    else:
        return False    

def localPikaChannelOpen():
    '''
        #### @brief\n
        Check whether local MQ channel is opened or not
        If not then it creates one

        #### @params\n
        None
    
        #### @return\n
        Boolean
    '''
    global localConnectionStatus, localMQChannel, localMQConnection

    try:
        localMQChannel = localMQConnection.channel()
    except Exception as exception:
        print('localPikaChannelOpen ERROR:', exception)
        return False

    if localMQChannel.is_open:
        return True
    else:
        return False

def localBasicGet(localQueueName):
    '''
        #### @brief\n
        Returns the next frame and its headers from Local Rabbit MQ

        #### @params\n
        localQueueName - Name of the local Rabbit MQ queue from which data is to be pulled
    
        #### @return\n
        Tuple - (method, properties, body)
    '''
    if localQueueName not in localDeclaredQueues:
        localQueueDeclare(localQueueName)
    return localMQChannel.basic_get(queue=localQueueName, auto_ack=True)

def localBasicPublish(localExchange, localRoutingKey, body, headers):
    '''
        #### @brief\n
        Publishes the body and its headers to Local Rabbit MQ

        #### @params\n
        localExchange - Name of the local Rabbit MQ queue's exchange to which data is to be published
    
        #### @return\n
        None
    '''
    if localRoutingKey not in localDeclaredQueues:
        localQueueDeclare(localRoutingKey)

    return localMQChannel.basic_publish(exchange=localExchange, routing_key=localRoutingKey, body=body, properties=pika.BasicProperties(headers=headers))

def localQueueDeclare(queueName):
    localMQChannel.queue_declare(queue=queueName, durable=True)
    localDeclaredQueues.append(queueName)
#--------------------------------------------------------------------------------------------

# Remote Rabbit MQ

def remoteIsConnected(remoteIP=configs.GeneralSettings['clientIP']):
    '''
    This function checks if complete connection to Rabbit MQ Server is available i.e. 
    server in known --> pika connection is established --> pika channel is opened. 
    In the function I have used representation of the status of connection using numbers, 
    description of which is given below \n
    
    0: Remote not available \n
    1: Remote available but pika not connected \n
    2: Pika is connected, but channel is not opened \n
    3: Pika channel is open and we are good to receive data
    '''
    
    global remoteConnectionStatus, remoteMQChannel, remoteMQConnection
    
    #print('Checking server')
    if remoteConnectionStatus == 0:
        # server not available, connect to server
        if remoteAvailable(remoteIP):
            remoteConnectionStatus = 1
        else:
            remoteConnectionStatus = 0

    if remoteConnectionStatus == 1:  
        # server available       
        if remotePikaConnect(remoteIP):
            remoteConnectionStatus = 2
        else:
            if remoteAvailable(remoteIP):
                remoteConnectionStatus = 1
            else:
                remoteConnectionStatus = 0

    if remoteConnectionStatus == 2:
        # open pika channel 
        if remotePikaChannelOpen():
            # channel opened
            remoteConnectionStatus = 3
        else:
            if remoteMQConnection.is_open:
                # queue connection is available but channel is not open
                remoteConnectionStatus = 2
            else:
                # queue connection is not available
                remoteConnectionStatus = 1    

    if remoteConnectionStatus == 3:
        if remoteMQChannel.is_open:
            return True
        else:
            remoteConnectionStatus = 2
            return False
        
    return False              

def remoteAvailable(remoteIP):
    '''
        #### @brief\n
        Check whether remote device is available or not, by ping

        #### @params\n
        None
    
        #### @return\n
        Boolean
    '''
    global remoteCredentials, remoteMQConnection, remoteMQChannel
    ''' Checks if network is connected to server'''

    try:
        # try ping to remote IP with timeout as 1 sec
        if remoteIP == '127.0.0.1':
            return True
            
        response = os.system("ping -c 1 -w 1 " + remoteIP)
        if response == 0:
            return True
        else:
            return False    
    
    except Exception as exception:
        print('remoteAvailable ERROR:',exception)
        return False 

def remotePikaConnect(remoteIP):
    '''
        #### @brief\n
        Check whether remote MQ connection is established or not
        If not then it creates one

        #### @params\n
        None
    
        #### @return\n
        Boolean
    '''
    global remoteCredentials, remoteMQConnection, remoteMQChannel
    try:
        if remoteIP == "127.0.0.1":
            remoteMQConnection = pika.BlockingConnection(pika.ConnectionParameters(host=remoteIP))
        else:
            remoteMQConnection = pika.BlockingConnection(pika.ConnectionParameters(host=remoteIP, credentials=remoteCredentials))
    except Exception as exception:
        print('remotePikaConnect ERROR:', exception)
        return False

    if remoteMQConnection.is_open:
        return True
    else:
        return False    

def remotePikaChannelOpen():
    '''
        #### @brief\n
        Check whether remote MQ channel is opened or not
        If not then it creates one

        #### @params\n
        None
    
        #### @return\n
        Boolean
    '''
    global remoteCredentials, remoteMQConnection, remoteMQChannel
    try:
        remoteMQChannel = remoteMQConnection.channel()
    except Exception as exception:
        print('remotePikaChannelOpen ERROR:', exception)
        return False

    if remoteMQChannel.is_open:
        return True
    else:
        return False

def remoteBasicGet(remoteQueueName):
    '''
        #### @brief\n
        Returns the next frame and its headers from remote Rabbit MQ

        #### @params\n
        localQueueName - Name of the remote Rabbit MQ queue from which data is to be pulled
    
        #### @return\n
        Tuple - (method, properties, body)
    '''
    return remoteMQChannel.basic_get(queue=remoteQueueName, auto_ack=True)