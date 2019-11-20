from imageai.Detection import ObjectDetection

#make sure you download the weights!
#wget https://github.com/pjreddie/darknet/blob/master/data/dog.jpg?raw=true https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5


detector = ObjectDetection()
model_path = "yolo.h5"
input_path = "dog.jpg"
output_path = "new_dog.jpg"

detector.setModelTypeAsYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()
detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)

for eachItem in detection:
    print(eachItem["name"] , " : ", eachItem["percentage_probability"])
