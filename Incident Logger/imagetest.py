import cv2

image = cv2.imread('/home/ubuntu/cdp/Application/cdp/media/Aron.jpg')
headers = {'time': '2020-06-19 20:08:59.337114'}
cv2.imwrite('Images/'+str(headers['time'])+'.jpg', image)