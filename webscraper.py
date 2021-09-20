import os
import time
from _datetime import datetime
import smtplib
import pyderman as cdi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart



# Deschide un client de chrome si obtine screenshot-urile, returneaza lista numelor pozelor
def get_images():
    path = cdi.install(file_directory="c:\\data\\chromedriver\\", verbose=True, chmod=True, overwrite=False, version=None)

    chrome_options = Options()
    chrome_options.add_argument("headless")


    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get("http://46.97.49.199:55/")

    top = driver.find_element_by_tag_name("body")
    quality_indicators = driver.find_element_by_class_name("qualityfieldset.lessreducedtopbottompadding")
    gnss = driver.find_element_by_class_name("reducedtopbottompadding")
    logging = driver.find_element_by_id("fsdiskview")
    data_streams = driver.find_element_by_id("iocanvas") #"//fieldset[@class='reducedtopbottompadding'][3]"
    ntrip = driver.find_element_by_id("ntripcanvas")
    wifi = driver.find_element_by_id("wificanvas") #
    time.sleep(5)

    top.screenshot("top.png")
    quality_indicators.screenshot("quality_indicators.png")
    gnss.screenshot("gnss.png")
    data_streams.screenshot("data_streams.png")
    ntrip.screenshot("ntrip.png")
    wifi.screenshot("wifi.png")
    driver.quit()
    return ["top.png", "quality_indicators.png", "gnss.png", "data_streams.png", "ntrip.png", "wifi.png"]

# Adauga din lista de nume pozele propriu-zise in mail-ul ce urmeaza a fi scris
def add_image(root, images, id):
    img = open(images[id], 'rb')
    msgImage =  MIMEImage(img.read())
    img.close()
    os.remove(images[id])
    msgImage.add_header("Content-ID", "<image"+(str)(id+1)+">")
    root.attach(msgImage)

# Creeaza mail-ul
def generate_email(strFrom, strTo):
    root = MIMEMultipart('related')
    root['Subject'] = 'Septentrio Information @' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    root['From'] = strFrom
    root['To'] = strTo
    root.preamble = "====================================================="
    images = get_images()
    for i in range(len(images)):
        add_image(root, images, i)
    return root

# Face conexiunea la serverul SMTP si trimite mail-ul de la Expeditor: strFrom la Destinatar: strTo
def send_mail(strFrom, strTo):
    smtp = smtplib.SMTP_SSL('mail.roinspace.com')
    smtp.connect('mail.roinspace.com', port=465)
    # Credentiale de login pt SMTP
    smtp.login("andrei.zenoveiov@roinspace.com","c*P9.A{&Szp}")
    root = generate_email(strFrom, strTo)
    smtp.sendmail(strFrom, strTo, root.as_string())
    smtp.quit()

send_mail("andrei.zenoveiov@roinspace.com", "zenoveiovandrei@gmail.com")