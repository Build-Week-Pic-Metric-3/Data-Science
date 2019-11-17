import numpy as np

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model # This is the functional API
from skimage import io, transform

def process_img_path(img_path):
    "loads image at path and compresses to 224x224 pixels"
    return image.load_img(img_path, target_size=(224, 224))

def process_img_to_array(img_path):
    """processes an image into an array"""
    processed_img = process_img_path(img_path)
    x = image.img_to_array(processed_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    x = np.asarray(x).reshape(len(x),224,224,3)
    return x


def resnet_process(img_path):
    resnet = ResNet50(input_shape=(224, 224, 3),weights='imagenet')
    predictions = resnet.predict(process_img_to_array(img_path))
    preds = decode_predictions(predictions, top=3)[0]
    return preds