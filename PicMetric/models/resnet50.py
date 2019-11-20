import numpy as np

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

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


def resnet(img_path):
    resnet_model = ResNet50(input_shape=(224, 224, 3),weights='imagenet')
    predictions = resnet_model.predict(process_img_to_array(img_path))
    raw = decode_predictions(predictions, top=3)[0]
    preds = {tup[1]:str(tup[2]) for tup in raw}
    return preds