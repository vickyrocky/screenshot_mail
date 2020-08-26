import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import pyautogui
import time
import pyttsx3
import getpass
import pathlib
import datetime
import yaml

"""
username = input("Please enter email username:\n")
pwd = getpass.getpass("Please enter email password:\n")
receiver = input("Please enter email id of receiver:\n")
"""

with open("config.yml", 'r') as p:
	try:
		data = yaml.safe_load(p)
	except yaml.YAMLError as exc:
		print(exc)

def speak(bolo):
	try:
		engine = pyttsx3.init()
		engine.say(bolo)
		engine.runAndWait()
		engine.stop()
	except Exception as e:
		print(e)
		
def send_mail(ImgFileName):
	try:
		img_data = open(ImgFileName, 'rb').read()
		print("Reading image.")
		msg = MIMEMultipart()
		msg['Subject'] = 'Screenshot'
		msg['From'] = data['username']
		msg['To'] = data['receiver']
		text = MIMEText(os.path.basename(ImgFileName))
		msg.attach(text)
		image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
		msg.attach(image)
		print("Added image and content.")
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(data['username'], data['pwd'])
		s.sendmail(msg['From'], msg['To'], msg.as_string())
		print("Mail sent.")
		s.quit()
	except Exception as e:
		print(e)

def main():
	while True:
		current_time = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p").split()
		current_hour = current_time[4].split(":")[0]
		current_clock = current_time[4].split(":")[1][-2:]
		print(current_hour, current_clock)
		if int(current_hour) == 3 and current_clock == 'PM':
			i=1
			while i<45:
				try:
					pyautogui.screenshot(str(pathlib.Path(__file__).parent.absolute())+r'\question'+str(i)+r'.jpg')
					print("Screenshot taken.")
				except Exception as e:
					print(e)
				send_mail(str(pathlib.Path(__file__).parent.absolute())+r'\question'+str(i)+r'.jpg')
				speak("Next")
				time.sleep(2)
				i+=1

if __name__ == "__main__":
	main()
