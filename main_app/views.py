from django.shortcuts import render
from django.http import HttpResponse
#import types
from django.core.files.storage import FileSystemStorage
from .models import encrypted_data
from django.contrib.auth.models import User, auth
from django.db.models import Q

#for DES
from Crypto.Cipher import DES

#For AES
from Crypto.Cipher import AES
from Crypto import Random
import binascii
import base64
import unittest
import os

#for random name for image saving
import random
import string
# Create your views here.
def index(request):
    return render(request,'index.html')


def Encrypt_and_send(request):
    letters=string.ascii_letters
    random_saveas = ''.join(random.choice(letters) for i in range(8))
    #print(random_saveas)
    #key_changed =  base64.b64encode(key)
    users_details=User.objects.all()
    return render(request,'Encrypt_and_send.html',{'users_details':users_details,'random_saveas':random_saveas})#,'key':key,'key_changed':key_changed

def Encrypt_and_download(request):
	letters=string.ascii_letters
	random_saveas = ''.join(random.choice(letters) for i in range(8))	
    
    #print(random_saveas)
	#users_details=User.objects.all()
	return render(request,'Encrypt_and_download.html',{'random_saveas':random_saveas})
    
def decbtn(request):
    return render(request,'Decrypt.html')


# using Q objects, F objects , 
def sent(request):
	user_firstname= str
	if request.user.is_authenticated:
		#print(User.objects.get(username='pbchandra3'))
		user_username=request.user.username
		#print(request.user.username)
		test=encrypted_data.objects.filter(sendby=user_username).order_by('-id')
		#test2=encrypted_data.objects.filter(Q(Q(secret_key=8) | Q(secret_key=22) & Q(msg='jp}~ivi(m(vmml(|w(jm(ni{|'))).query
        
		return render(request,'items.html',{'test':test})
	else:
		#print("else")
		return render(request,'index.html')

def received(request):
	user_firstname= str
	if request.user.is_authenticated:
		#print(User.objects.get(username='pbchandra3'))
		user_username=request.user.username
		#print(request.ufser.username)
		test=encrypted_data.objects.filter(sendto=user_username).order_by('-id')
		#test=encrypted_data.objects.filter(Q(Q(secret_key=8) | Q(secret_key=22) & Q(msg='jp}~ivi(m(vmml(|w(jm(ni{|'))).query
		return render(request,'items.html',{'test':test})
	else:
		#print("else")
		return render(request,'index.html')

def user_decrypt(request):
	test_id=request.POST['p_id']
	test=encrypted_data.objects.filter(Q(id=test_id))
	return render(request,'user_decrypt.html',{'test': test})

#stegnography actual code

from PIL import Image


def stringToBinary(data):
#ord('a') = 97; ord returns unicode(ascii) value of given char
#format(ord(i), '08b') changes unicode to 8 bit binay
		binary_data = []
		for i in data:
			binary_data.append(format(ord(i), '08b'))
		return binary_data


def pixel_modification(pix, data):

	binary_data = stringToBinary(data)
	lendata = len(binary_data)
	imdata = iter(pix) 
	##The iter() function creates an object which can be iterated one element at a time.
	for i in range(lendata):
		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (binary_data[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (binary_data[i][j] == '1' and pix[j] % 2 == 0):
				pix[j] += 1
					

		# Delimiter :- Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means the message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def data_embedding(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)
	for pixel in pixel_modification(newimg.getdata(), data):
		# inserting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1
# Encode data into image
def encryptanddownload(request):
	uploaded_file = request.FILES["nrmlimg"]
	fs=FileSystemStorage()
	fs.save(uploaded_file.name,uploaded_file)
	THIS_FOLDER = r"C:\Users\hp\Projects\mtech_project\media"
	path = os.path.join(THIS_FOLDER, uploaded_file.name)
	img = uploaded_file.name
	image = Image.open(path, 'r')
	data = request.POST["msg"]
	if (len(data) == 0):
		raise ValueError('Data is empty')

	cryptographic_algorithm=request.POST["cryptographic_algorithm"]
	
	if cryptographic_algorithm =='1':
		secret_key=request.POST["secret_key"]        
		data=ceasar_encrypt(data,secret_key)
	
	if cryptographic_algorithm =='2':
		secret_key=request.POST["secret_key_des"]
		secret_key=secret_key.encode("utf8")
		data=append_space(data,64)				        
		data=data.encode("utf8")
		data=encrypt(data,secret_key)
		data = base64.b64encode(data)
		data=data.decode('utf-8')
				
	
	newimg = image.copy()
	data_embedding(newimg, data)

	name = request.POST["saveasname"]
	extenstion = request.POST["extension"]
	new_img_name = name+extenstion
	THIS_FOLDER = r'C:\Users\hp\Projects\mtech_project\static\encryptedimgs'
	#print(path2)
	path2 = os.path.join(THIS_FOLDER, new_img_name)
	newimg.save(path2, str(new_img_name.split(".")[1].upper()))
	
	return render(request,'results.html',{'test':new_img_name,'filename':new_img_name})
# Encode data into image
def encryptandsend(request):
	uploaded_file = request.FILES["nrmlimg"]
	fs=FileSystemStorage()
	fs.save(uploaded_file.name,uploaded_file)
	path = r'C:\Users\hp\Projects\mtech_project\media\\'+ uploaded_file.name;
	img = uploaded_file.name
	image = Image.open(path, 'r')

	data = request.POST["msg"]
	sendby = request.POST["sendby"]
	sendto = request.POST["sendto"]
	if (len(data) == 0):
		raise ValueError('Data is empty')
	
	cryptographic_algorithm=request.POST["cryptographic_algorithm"]

	if cryptographic_algorithm =='low':
		secret_key=''	
	
	if cryptographic_algorithm =='medium':
		secret_key=request.POST["secret_key_ceasar"]
		data=ceasar_encrypt(data,secret_key)
	if cryptographic_algorithm =='high':
		secret_key=request.POST["secret_key_des"]
		secret_key=secret_key.encode("utf8")
		data=append_space(data,64)				        
		data=data.encode("utf8")
		data=encrypt(data,secret_key)
		data = base64.b64encode(data)
		data=data.decode('utf-8')
	if cryptographic_algorithm =='vhigh':
		secret_key=Random.new().read(16)
		data=append_space(data,128)				        
		data=data.encode("utf8")
		data=encrypt_aes(data,secret_key)
		data = base64.b64encode(data)
		data=data.decode('utf-8')
	newimg = image.copy()
	data_embedding(newimg, data)

	name = request.POST["saveasname"]
	extenstion = request.POST["extension"]
	new_img_name = name+extenstion
	path = r'C:\Users\hp\Projects\mtech_project\static\encryptedimgs\\'+new_img_name;
	
	newimg.save(path, str(new_img_name.split(".")[1].upper()))
	posting = encrypted_data(sendby=sendby,sendto=sendto,nrmlimg=uploaded_file.name,msg='Never search here for data you won\'t get anything',sensitivity=cryptographic_algorithm,secret_key=secret_key,encryimg=new_img_name)
	posting.save()
	return render(request,'results.html',{'test':new_img_name,'filename':new_img_name})

#direct decryption 
def decryption(request):
    uploaded_file = request.FILES["stignoimg"]
    fs=FileSystemStorage()
    fs.save(uploaded_file.name,uploaded_file)
    img = r'C:\Users\hp\Projects\mtech_project\media\\'+ uploaded_file.name
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        cryptographic_algorithm=request.POST["cryptographic_algorithm"]
        secret_key=request.POST["secret_key"]
        plain_text=''
        if (pixels[-1] % 2 != 0):
            if cryptographic_algorithm == '0':
                plain_text = data            
            if cryptographic_algorithm == '1':
                plain_text=ceasar_decrypt(data,secret_key)
            if cryptographic_algorithm == '2':
                secret_key=request.POST["secret_key_des"]
                secret_key=secret_key.encode("utf8")
                data= data.encode('utf-8')
                data = base64.b64decode(data)												
                plain_text = decrypt(data,secret_key)
                plain_text = remove_space(plain_text,64)
                             
            return render(request,'results2.html',{'result': plain_text})



def userdecryption(request):
    uploaded_file = request.POST["stignoimg"]

    img = r'C:\Users\hp\Projects\mtech_project\static\encryptedimgs' + "\\"+uploaded_file
	
    image = Image.open(img, 'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        cryptographic_algorithm=request.POST["cryptographic_algorithm"]
        secret_key=request.POST["secret_key"]
        if (pixels[-1] % 2 != 0):
            if cryptographic_algorithm == 'low':
                plain_text = data            
            if cryptographic_algorithm =='medium':
                plain_text=ceasar_decrypt(data,secret_key)
			#DES
            if cryptographic_algorithm == 'high':
                secret_key=request.POST["secret_key_des"]
                secret_key=secret_key[2:-1]				
                secret_key=secret_key.encode("utf8")
                data= data.encode('utf-8')
                data = base64.b64decode(data)												
                plain_text = decrypt(data,secret_key)
                plain_text = remove_space(plain_text,64)
                #AES				
            if cryptographic_algorithm == 'vhigh':
                test_id=request.POST['p_id'] 
                test=encrypted_data.objects.filter(Q(id=test_id))   
                for t in test:
                    key=t.secret_key
                secret_key=eval(key)				
                data= data.encode('utf-8')
                data = base64.b64decode(data)												
                plain_text = decrypt_aes(data,secret_key)
                plain_text = remove_space(plain_text,128)				
            					                
            return render(request,'results2.html',{'result': plain_text})



#cryptography
#ceaser cipher

def ceasar_encrypt(plain_text,key):
    cipher_text=''
    for char in plain_text:
        char = ord(char)+ int(key)#gets the ascii value of string and add's key to it
        cipher_text=cipher_text+chr(char)
    return cipher_text

def ceasar_decrypt(cipher_text,key):
    plain_text=''
    for char in cipher_text:
        char = ord(char) - int(key)#gets the ascii value of string & substracts key from it
        plain_text = plain_text+chr(char)
    return plain_text
	
#DES

def encrypt(plaintext, key):
    des = DES.new(key, DES.MODE_ECB)
    return des.encrypt(plaintext)

def decrypt(ciphertext, key):
    des = DES.new(key, DES.MODE_ECB)
    return des.decrypt(ciphertext).decode('UTF-8')

#AES

def encrypt_aes(plaintext, key):
    des = AES.new(key, AES.MODE_ECB)
    return des.encrypt(plaintext)

def decrypt_aes(ciphertext, key):
    des = AES.new(key, AES.MODE_ECB)
    return des.decrypt(ciphertext).decode('UTF-8')


#for adding removig padding
def append_space(str, blocksize):
    length = blocksize - (len(str) % blocksize)
    padding = '*'*length
    return str + padding

def remove_space(str, blocksize):
    temp = 0 
    for c in str[::-1]: 
        if c == '*':
            temp += 1
        else:
            break
    str = str[:-temp]
    return str