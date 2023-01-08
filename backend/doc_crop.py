import cv2
import numpy as np
import pytesseract
import re


def adhaar_read_data(text):
    res = text.split('\n')
    res = [r for r in res if r != '']
    name = res[res.index('To') + 2]
    contact = [r for r in res if len(r) == 10][0]
    print('res in list::', res)
    for i in range(len(res)):
        if "Your Aadhaar No" in res[i]:
            aadhar_num_index = i
            break;
    print('test:', res)
    return {
        "name": name,
        "contact": contact,
        "address": ','.join(res[res.index(name) + 1:res.index(contact)]),
        "aadhar number": res[aadhar_num_index + 1],
        "dob": re.compile(r'\d{2}\/\d{2}\/\d{4}').search(''.join(res)).group()
    }


def extract_doc(imagePath):
    img = cv2.imread(imagePath)
    denoised = cv2.fastNlMeansDenoising(img, h=7)
    grayImage = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
    grayImage = cv2.GaussianBlur(grayImage, (5, 5), 0)
    canny = cv2.Canny(grayImage, 0, 100)
    canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    kernel = np.ones((7, 7), np.uint8)
    canny = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=7)
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    img1 = img.copy();
    # Drawing a rectangle on copied image
    rect = cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Cropping the text block for giving input to OCR
    cropped = img1[y:y + h, x:x + w]
    strImg = pytesseract.image_to_string(cropped, lang='eng+Devanagari')
    return adhaar_read_data(strImg)




