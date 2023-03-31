import streamlit as st
import numpy as np
import pickle
from  PIL import Image, ImageEnhance
from tensorflow import keras
import cv2
import requests
import urllib.request

pipe = pickle.load(open('pipe.pkl','rb'))

st.title('Cat vs Dog Prediction')
option='select'
ctr=0
option = st.selectbox('How would you like to upload your pets photo?',('Online URL', 'Upload Local File'))
if option != 'select':
    if option == 'Online URL':
        url = st.text_input("Enter Image URL")
        if url:
            sub_str = "jpg"
            if sub_str in url:
                res = url[:url.index(sub_str) + len(sub_str)]
                url = str(res)
            f = open('onlinepic.jpg','wb')
            f.write(requests.get(url).content)
            f.close()
            new_image = Image.open('onlinepic.jpg')
            new_image = new_image.resize((256, 256))
            if st.button('Preview'):
                st.image(new_image)
                ctr+=1
            if st.button('Predict'):
                if ctr==0:
                    st.image(new_image)
                img1 = np.asarray(new_image)
                query = img1.reshape((1,256,256,3))
                ans = int(pipe.predict(query)[0])
                typ = ''
                if ans==0:
                    typ = 'a Cat'
                if ans==1:
                    typ = 'a Dog'
                st.title("The uploaded image is that of " + typ)

    if option == 'Upload Local File':
        file = st.file_uploader("Upload the image to be classified", type=["jpg", "png"])
        st.set_option('deprecation.showfileUploaderEncoding', False)
        if file:
            image = Image.open(file)
            new_image = image.resize((256, 256))
            if st.button('Predict'):
                st.image(new_image)
                img1 = np.asarray(new_image)
                query = img1.reshape((1,256,256,3))
                # test_img = cv2.resize(image,(256,256))
                # query = test_img.reshape((1,256,256,3))
                ans = int(pipe.predict(query)[0])
                typ = ''
                if ans==0:
                    typ = 'a Cat'
                if ans==1:
                    typ = 'a Doggo'
                st.title("The uploaded image is that of " + typ)
        else:
            st.text("Please upload an image file")
