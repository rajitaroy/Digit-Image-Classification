from django.db import models
from django.conf import settings
from PIL import Image 
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from tensorflow.keras.models import load_model 
import cv2, os
import numpy as np
import tensorflow as tf

# Create your models here.
class Digit(models.Model):
    image = models.ImageField(upload_to = 'images')
    result = models.CharField(max_length = 2, blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        print(self.image)
        img = Image.open(self.image)
        img_array = image.img_to_array(img)
        print(img_array)
        print(img_array.shape)
        new_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        dim = (28,28)
        resized = cv2.resize(new_img, dim, interpolation = cv2.INTER_AREA)
        print(resized.shape)

        ready = np.expand_dims(resized, axis = 2)
        ready = np.expand_dims(ready, axis = 0)
        print(ready.shape)
        
        try:
            file_model = os.path.join(settings.BASE_DIR, 'CNN_model.h5')
            graph = tf.compat.v1.get_default_graph()

            with graph.as_default():
                model = load_model(file_model)
                pred = np.argmax(model.predict(ready))
                self.result = str(pred)
                print(f'Classified as {pred}')
        
        except:
            print('Failed to classify')
            self.result = 'Failed to classify'

        return super().save(*args, **kwargs)