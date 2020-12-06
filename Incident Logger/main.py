import mysql.connector
from mysql.connector import Error
import cv2
import numpy as np
from datetime import datetime

from RabbitMQManager import RabbitMQManager as RMQ
import configs

try:
    dbConnection = mysql.connector.connect(host='localhost',
                                         database=configs.DBSettings['MySQLDBName'],
                                         user=configs.DBSettings['MySQLDBUsername'],
                                         password=configs.DBSettings['MySQLDBPassword'])
    dbCursor = dbConnection.cursor()
except Error as e:
    print("Error while connecting to MySQL", e)

img_counter = 0

if __name__ == "__main__":
    # pull from RMQ and send to database
    while True:
        if RMQ.localIsConnected():

            # get the next frame and its headers
            try:
                method, properties, body = RMQ.localBasicGet('EMP') 
            except Exception as exception:
                print('Queue RMQ.GET ERROR:', exception)
                method = False

            if method:
                # get headers from Rabbit MQ
                timestamp = str(properties.headers['time'][2:4] + properties.headers['time'][5:7] + properties.headers['time'][8:10])
                tampered = properties.headers['tampering']
                mobileDetected = properties.headers['mobile']
                multiplePeople = properties.headers['multiple_person']
                unidentifiedPerson = properties.headers['unknown']
                unattended = properties.headers['not_looking']
                macID = properties.headers['camID']
                agentID = 1

                # print('SELECT id FROM Agent WHERE mac_id='+str(properties.headers['camID']))    
                # dbCursor.execute('SELECT id FROM Agent WHERE mac_id="'+str(properties.headers['camID'])+'"')
                # records = dbCursor.fetchall()
                # print(records)
                # if records == [] or records[0][0] == None:
                #     agentID = -1
                # else:
                #     agentID = records[0][0]


                # decode image 
                image = cv2.imdecode(np.fromstring(body, np.uint8), cv2.IMREAD_COLOR)
                imagePath = 'Images/'+str(datetime.now().strftime("%x %X.%f"))+'.jpg'


                print(properties.headers)
                print('agent_id:',agentID)
                
                # deteremine which violation occured
                if tampered == 1:
                    dbCursor.execute('INSERT INTO Incident (category, incident_date, incident_img, created_on, created_by, modified_on, modified_by, agent_id, mac_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', ('Camera Tampered', str(timestamp), imagePath, str(timestamp), '-', str(timestamp), '-', int(agentID), str(macID)))
                    dbConnection.commit()
                    # save image in filesystem
                    cv2.imwrite(imagePath, image)

                if mobileDetected == 1:
                    dbCursor.execute('INSERT INTO Incident (category, incident_date, incident_img, created_on, created_by, modified_on, modified_by, agent_id, mac_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', ('Mobile Detected', str(timestamp), imagePath, str(timestamp), '-', str(timestamp), '-', int(agentID), str(macID)))
                    dbConnection.commit()
                    # save image in filesystem
                    cv2.imwrite(imagePath, image)

                if multiplePeople == 1:
                    dbCursor.execute('INSERT INTO Incident (category, incident_date, incident_img, created_on, created_by, modified_on, modified_by, agent_id, mac_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', ('Multiple People', str(timestamp), imagePath, str(timestamp), '-', str(timestamp), '-', int(agentID), str(macID)))
                    dbConnection.commit() 
                    # save image in filesystem
                    cv2.imwrite(imagePath, image)   

                if unidentifiedPerson == 1:  
                    dbCursor.execute('INSERT INTO Incident (category, incident_date, incident_img, created_on, created_by, modified_on, modified_by, agent_id, mac_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', ('Unidentified Person', str(timestamp), imagePath, str(timestamp), '-', str(timestamp), '-', int(agentID), str(macID)))
                    dbConnection.commit()
                    # save image in filesystem
                    cv2.imwrite(imagePath, image)

                if unattended == 1:  
                    dbCursor.execute('INSERT INTO Incident (category, incident_date, incident_img, created_on, created_by, modified_on, modified_by, agent_id, mac_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', ('Unattended Session', str(timestamp), imagePath, str(timestamp), '-', str(timestamp), '-', int(agentID), str(macID)))    
                    dbConnection.commit()
                    # save image in filesystem
                    cv2.imwrite(imagePath, image)

                img_counter += 1

