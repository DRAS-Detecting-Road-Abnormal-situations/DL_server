import time
from absl import app, flags, logging
from absl.flags import FLAGS
import cv2
import tensorflow as tf
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images
from yolov3_tf2.utils import draw_outputs
from firebase_admin import messaging
import requests
flags.DEFINE_string('classes', './data/labels/classes.names', 'path to classes file')
flags.DEFINE_string('weights', './weights/yolov3.tf',
                    'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_string('video', './data/video/test_1.mp4',
                    'path to video file or number for webcam)')
flags.DEFINE_string('output', './output/', 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_integer('num_classes', 1, 'number of classes in the model')


def main(_argv):
   
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    if FLAGS.tiny:
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
    else:
        yolo = YoloV3(classes=FLAGS.num_classes)

    yolo.load_weights(FLAGS.weights)
    logging.info('weights loaded')

    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]
    logging.info('classes loaded')

    times = []

    try:
        vid = cv2.VideoCapture(int(FLAGS.video))
    except:
        vid = cv2.VideoCapture(FLAGS.video)

    out = None

    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))
    fps = 0.0
    count = 0

    num = 1
    tmp = 0
    log_1 = "True"
    while True:
        _, img = vid.read()
       
        if img is None:
            logging.warning("Empty Frame")
            time.sleep(0.1)
            count+=1
            if count < 3:
                continue
            else: 
                break


        img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        img_in = tf.expand_dims(img_in, 0)
        img_in = transform_images(img_in, FLAGS.size)

        t1 = time.time()
        boxes, scores, classes, nums = yolo.predict(img_in)
        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        #print(fps, scores)
        print("FPS: {:.2f}".format(fps))
        #img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
        img = cv2.putText(img, "FPS: {:.2f}".format(fps), (0, 30),
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
        log = "False"
        
        if scores[0][0] > 0.7 and log_1 == "True":
            log = "True"
            name = FLAGS.output + 'output' + str(num) + '.jpg'
            print('---------'+name)
            cv2.imwrite(FLAGS.output + 'output' + str(num) + '.jpg', img)
            print(log)
            print('output saved to: {}'.format(FLAGS.output + 'output' + str(num) + '.jpg'))
            num = num + 1
            if num > 4: 
                num = 1
            log_1 = "False"
            image_url = 'C:/workspace/yolov3/yolov3_object_detections'+ str(name)
            send_post(image_url,name)
        else :
            log = "False"
            print(log)
            tmp += 1
            if tmp > 40 :
                log_1 = "True"
                tmp = 0
            
        if FLAGS.output:
            out.write(img)
        cv2.imshow('output', img)
        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()

def send_to_firebase_cloud_messaging(url,type):
    # This registration token comes from the client FCM SDKs.
    registration_token = 'cHXdiCBkUFM:APA91bFI01-x0KnqCSSJRCh7iD-50rprDalwsom5nhdcHCDomm9XLc7m9rJAR-OsRJzFLJ-YctQUsfTs6um_wO4yb476s6b_frfVPom94_CwJoo7JwKG1iOdbmBg4MrmV-PwCQOTLUC-'

    # See documentation on defining a message payload.
    if(type =='acc'):
        message = messaging.Message(
        notification=messaging.Notification(
            title='알림입니다.',
            body='주변에 교통사고가 났습니다. 조심하세요',
            image= url,
        ),
        token=registration_token,
        data={'case':'accidnet', 'cctv_id':'서울역'},
        )
def send_post(image_url, image_name):
    url = "http://127.0.0.1:8000/push_server/image/"
    files = {
        'image': open(image_url, 'rb')
        }
    data = {
        'name' : image_name
    }
    response = requests.request("POST", url, files=files, data = data)
    print(response)
    # Response is a message ID string.
    print('Successfully sent message:', response)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
