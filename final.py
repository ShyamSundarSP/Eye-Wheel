#All the imports go here
import numpy as np
import cv2
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

#Initializing the face and eye cascade classifiers from xml files
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
    
	def do_GET(self):
		self._set_headers()
		self.wfile.write(bytes(str(k), "utf-8"))
        
def run(server_class=HTTPServer, handler_class=S, port=8080):
	server_address = ('192.168.190.210', port)
	httpd = server_class(server_address, handler_class)
	httpd.serve_forever()

if __name__ == "__main__":
	from threading import Thread
	Thread(target=run).start()

def Threshold(point,min,max,r):
	if point < min:
		return "Left"
	elif min < point < max:
		return "Centre"
	elif point > max:
		return "Right"
	elif r==1:
		return "Blink"

#Starting the video capture
cap = cv2.VideoCapture(0)
ret,img = cap.read()
blink_count = 0  
start_time = time.time()
cnt=2
while(1):
	ret,img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray,5,1,1)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200))
	eyes = eye_cascade.detectMultiScale(gray)
	if eyes == ():
		if (time.time()-start_time>=5):
			k=Threshold(0,0,0,1)
			cnt+=1
			print(k)

			
	if cnt%2==0:	
		for (ex,ey,ew,eh) in eyes:
			a = int(ew/3)
			b = int(eh/3)
			cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
			cv2.line(img, (ex+a,ey), ((ex+a,ey+eh)), (0,0,255),1)
			cv2.line(img, (ex+2*a,ey), ((ex+2*a,ey+eh)), (0,0,255),1)
			cv2.line(img, (ex,ey+b), ((ex+ew,ey+b)), (0,0,255),1) 
			cv2.line(img, (ex,ey+2*b), ((ex+ew,ey+2*b)), (0,0,255),1)
			cv2.line(img, (ex+ew,ey), ((ex,ey+eh)), (0,0,255),1)
			roi_gray2 = gray[ey:ey+eh, ex:ex+ew]
			roi_color2 = img[ey:ey+eh, ex:ex+ew]
			circles = cv2.HoughCircles(roi_gray2, cv2.HOUGH_GRADIENT, 1, 200, param1=200, param2=1, minRadius=10, maxRadius=10)
			try:
				for i in circles[0,:]:
					cv2.circle(roi_color2,(i[0],i[1]),i[2],(255,255,255),1)
					cv2.circle(roi_color2,(i[0],i[1]),1,(255,255,255),1)
					k=Threshold(i[1],35,48,0)
					print(i[1],k)
			except Exception as e:
				print(e)
		else:
			if eyes is None:
				print("B")
	cv2.imshow('img',img)
	if cv2.waitKey(1) == 27: 
		break 
cap.release()
cv2.destroyAllWindows()
