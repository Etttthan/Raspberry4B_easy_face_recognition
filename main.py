# -*- coding: utf-8 -*-

import smtplib
import RPi.GPIO as GPIO

# 导入face_recogntion模块，可用命令安装 pip install face_recognition
import face_recognition
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from picamera import PiCamera
from time import sleep

# 导入pil模块 ，可用命令安装 apt-get install python-Imaging
from PIL import Image
from PIL import ImageDraw

#GPIO口设置:BOARD 模式
#蜂鸣器对io口占用错误忽略：setwarnings(False)
#红外阈值Infrared
Infrared=38
address_gpio = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(Infrared,GPIO.IN)
GPIO.setup(address_gpio, GPIO.OUT)

while 1 :
    
    
    #Buzzer Setting: silent in HIGH
    GPIO.output(address_gpio, GPIO.HIGH)

    #traffic light GREEN
    print("GREEN")
    sec = 10
    while sec !=0 :
        sleep(1)
        sec=sec-1
        print('GREEN countdown:%d'%sec)
        
    #traffic light RED  
    print("RED")
    
    sec = 30
    while sec !=0:
        print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" No illegal pedestrians")
        if(GPIO.input(Infrared)==True):
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" Illegal pedestrians detected")
            start=time.time()
            #camera settings:
            #necessary exposure time: >2s
            camera = PiCamera()
            camera.start_preview()
            sleep(2)
            camera.capture('/home/pi/find_face/cam_out.jpg')
            camera.stop_preview()
            camera.close()
            
            # 将jpg文件加载到numpy 数组中
            image = face_recognition.load_image_file("/home/pi/find_face/cam_out.jpg")
            
            # 使用默认的给予HOG模型查找图像中所有人脸
            # 这个方法已经相当准确了，但还是不如CNN模型那么准确，因为没有使用GPU加速
            # 另请参见: find_faces_in_picture_cnn.py
            face_locations = face_recognition.face_locations(image)

            # 使用CNN模型
            #face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

            # 打印：我从图片中找到了 多少 张人脸
            print("I found {} face(s) in this photograph.".format(len(face_locations)))

            pil_image = Image.fromarray(image)
            # 循环找到的所有人脸
            d = ImageDraw.Draw(pil_image)
            for face_location in face_locations:
                    # 打印每张脸的位置信息
                    top, right, bottom, left = face_location
                    # print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right)) 
            # 指定人脸的位置信息，然后显示人脸图片
                    face_image = image[top:bottom, left:right]
                    d.rectangle((right, top, left, bottom), fill = None, outline = (150,0,0,128), width = 5)
            #保存图片，裁减图片
            if(len(face_locations)!=0):
                pil_image.save("/home/pi/find_face/face_out_without_crop.jpg")
                pil_image.crop((left, top, right, bottom)).save("/home/pi/find_face/face_out.jpg")
                
                #蜂鸣器响
                GPIO.output(address_gpio, GPIO.LOW)
                end=time.time()
            
                print('face detectRunning time: %s Seconds'%(end-start))
            if(len(face_locations)!=0):
                #Send face.jpg to email
                message = MIMEMultipart()   # 邮件主体

                sender = "qq_id @qq.com"
                receivers = ["qq_id @qq.com", "qq_id @qq.com"]

                # 邮件加入文本内容
                text = '<img src="cid:0">'   # html文本引入id为0的图片
                my_text = """
                <p> 该人员涉嫌闯红灯</p>
                """
                text = my_text + text
                m_text = MIMEText(text, 'html', 'utf-8')
                message.attach(m_text)

                # 邮件加入图片
                m_img = MIMEBase('image', 'jpg')
                m_img.add_header('Content-Disposition', 'attachment')
                m_img.add_header('Content-ID', '<0>')   # 设置图片id为0
                f = open("/home/pi/find_face/face_out.jpg", "rb")   # 读取本地图片
                m_img.set_payload(f.read())
                encoders.encode_base64(m_img)
                message.attach(m_img)

                # 设置发送信息
                message['From'] = Header('闯红灯行人抓拍摄像系统', 'utf-8')   # 邮件发送者名字
                message['To'] = Header('闯红灯违法抓拍', 'utf-8')   # 邮件接收者名字
                message['Subject'] = Header('违法行人照片', 'utf-8')   # 邮件主题

                mail = smtplib.SMTP()
                mail.connect("smtp.qq.com")   # 连接 qq 邮箱
                mail.login("qq_id @qq.com", "xxxxxxxxx")   # 账号和授权码

                mail.sendmail("qq_id @qq.com", ["qq_id @qq.com"], message.as_string())   # 发送账号、接收账号和邮件信息
                print("Email sent!")
                GPIO.output(address_gpio, GPIO.HIGH)
            
            sec = 15
            while sec !=0 :
                sleep(1)
                sec=sec-1
                print('RED countdown:%d'%sec)
        else:
            print('RED countdown:%d'%sec)
            sec = sec -1
            sleep(1)
    
