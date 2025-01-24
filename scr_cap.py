from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import datetime
import os


options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get("** your web streaming url **")

base_options = python.BaseOptions(model_asset_path='cat2.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5)
detector = vision.ObjectDetector.create_from_options(options)

while True:
    sleep(1)
    now = datetime.datetime.now()
    file_name = "scr_pictures\inputs\sc_%s.png" % now.strftime("%Y%m%d%H%M%S")
    driver.save_screenshot(file_name)
    try:
        image = mp.Image.create_from_file(file_name)
        base_file_name = os.path.basename(file_name)

        detection_result = detector.detect(image)
        if len(detection_result.detections) > 0 and \
                detection_result.detections[0].categories is not None:
            for item in detection_result.detections[0].categories:
                if 'cat' in item.category_name or 'tabby' in item.category_name:
                    print(item.category_name)
                    driver.save_screenshot(base_file_name)
                    break
    except Exception as e:
        print(f"{e}")
    finally:
        os.remove(file_name)