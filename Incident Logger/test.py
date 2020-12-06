import mysql.connector
from mysql.connector import Error
import cv2
import numpy as np

import configs

try:
    dbConnection = mysql.connector.connect(host='localhost',
                                         database=configs.DBSettings['MySQLDBName'],
                                         user=configs.DBSettings['MySQLDBUsername'],
                                         password=configs.DBSettings['MySQLDBPassword'])
    dbCursor = dbConnection.cursor()
except Error as e:
    print("Error while connecting to MySQL", e)


headers = {'camID': 'INF-YASH-LAP', 'time': '2020-06-19 20:09:08.599523', 'tampering': 0, 'multiple_person': 0, 'not_looking': 0, 'unknown': 0, 'mobile': 1}
tampered = headers['tampering']
mobileDetected = headers['mobile']
multiplePeople = headers['multiple_person']
unidentifiedPerson = headers['unknown']
unattended = headers['not_looking']
macID = headers['camID']
agentID = 1
timestamp = str(headers['time'][2:4] + headers['time'][5:7] + headers['time'][8:10])

img_counter = 1
imagePath = '../Application/cdp/media/'+str(img_counter)+'.jpg'


dbCursor.execute('INSERT INTO Incident (category, incident_date, incident_img, created_on, created_by, modified_on, modified_by, agent_id, mac_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', ('Mobile Detected', str(timestamp), imagePath, str(timestamp), '-', str(timestamp), '-', int(agentID), str(macID)))
dbConnection.commit()