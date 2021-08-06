import sys 
import numpy as np
import cv2
import os
# pip install git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api
from googletrans import Translator
# pip install wikipedia-api
import wikipediaapi

class Yolo:
    def __init__(self):
        # paths
        self.root = os.getcwd().replace('\\', '/') + '/'
        self.weight = self.root + 'YOLO/yolov3.weights'
        self.cfg = self.root + 'YOLO/yolov3.cfg.txt'
        self.coconames = self.root + 'YOLO/coco.names.txt'
        self.img = self.root + 'picture/' # img
    
    def run(self,image):
        try:
            print(image)
            self.img += image
            # value set
            pretrained_model = self.weight
            config = self.cfg
            # class_labels load
            class_labels = self.coconames
            classes = []
            with open(class_labels) as f:
                lines = f.readlines()
                f.close()
            classes = [line.rstrip() for line in lines]
            print(classes)

            # hold ---> if prediction under 0.9 ignore
            confThreshold = 0.7
            nmsThreshold = 0.7
            # load pre-model
            net = cv2.dnn.readNet(pretrained_model,config)
            # output layer value
            layer_names = net.getLayerNames()
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            # run
            r_img = cv2.imread(self.img) # read image
            use_img = cv2.resize(r_img,(500,500)) # resize image
            # create blob & prediction
            blob = cv2.dnn.blobFromImage(use_img, 1/255., (416,416),swapRB=True)
            net.setInput(blob) # use blob value for model input setting
            outs = net.forward(output_layers)

            h,w = use_img.shape[0], use_img.shape[1] # height and width 

            class_ids = []
            confidences = []
            boxes = []
            for out in outs :
                for detection in out :
                    # detection(85) = 4(bounding box coordinate value) 
                    #               + 1(confidence) 
                    #               + 80(class prediction value)
                    scores = detection[5:] # 80(class prediction value)
                    class_id = np.argmax(scores) # prediction label
                    confidence = scores[class_id]
                    if confidence > confThreshold:
                        # biggest prediction value
                        # bounding box center coordinate value and box size
                        cx = int(detection[0] * w)
                        cy = int(detection[1] * h)
                        w = int(detection[2] * w)
                        h = int(detection[3] * h)

                        # bounding box left&top coordinate
                        x = int(cx - w / 2)
                        y = int(cy - h / 2)

                        boxes.append([x, y, w, h])
                        # confidences append covert float confidence value
                        confidences.append(float(confidence)) 
                        class_ids.append(int(class_id))

            indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
            # prediction
            for i in indices : 
                i = i[0]
                x, y, w, h = boxes[i]
                label = f'{classes[class_ids[i]]}: {confidences[i]:.2}' # format output
                whsthis = classes[class_ids[i]] # prediction label 
            # visualization
                # color = (61,46,73) # color
                # cv2.rectangle(use_img, (x, y, w, h), color, 2) # draw retangle
                # cv2.putText(use_img, label, (x, y-10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
                # cv2.imshow('Color',use_img)
            #     cv2.waitKey()
            # cv2.destroyAllWindows()
            print(whsthis)

            # translation for ko
            translator = Translator(service_urls=['translate.googleapis.com'])
            ko_label = translator.translate(whsthis,src='en',dest='ko').text
            print(ko_label)

            # find label explanation in wiki
            wiki=wikipediaapi.Wikipedia('ko') # ko-wikipedia site setting
            page_py = wiki.page(ko_label) # search label
            title = page_py.title # title
            summary = page_py.summary # summary
            # processing for html
            r_summary = summary.replace('.','.<br>').strip()
            r_summary = "<li><a>"+r_summary+"</a></li>" 
            print(r_summary)

            # path for html
            img_name = os.path.basename(self.img)

            # html code 
            html_code = """ 
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Find!</title>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Hi+Melody&display=swap');
                    *{
                        margin:0;
                        padding:0;
                        box-sizing: border-box;
                        font-family: 'Hi Melody',cursive;
                    }
                    body{
                        background-image:linear-gradient(rgba(187, 169, 169, 0.61),rgba(255, 255, 255, 0.555)) ;
                        background-size:cover;
                    }
                    #main-wrapper{
                        margin: 10px auto;
                        width: 1700px;
                        height: 2000px;
                        background-image: url('../needfiles/tamplet.jpg');
            """
            html_code.replace('\n',' ')
            html2 = """ 
                        background-size: 1700px 2000px;
                        border-radius: 10px;
                        padding-top: 150px;
                        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.507);
                    }
                    img{
                        margin: 30px auto;
                        width: 300px;
                        height: 300px;
                        text-align:center;
                        display: block;
                        margin-bottom: 0px;
                        border: 3px solid rosybrown;
                        border-radius: 10px;
                    }
                    #subtitle{
                        margin: 0px auto;
                        text-align: center;
                        font-size: 55px;
                        color: white;
                        width: 300px;
                        height: 70px;
                        background-color:rgba(0, 0, 0, 0.884);
                        border-radius: 10px;
                    }
                    #summary{
                        margin: 10px auto;
                        padding: 5px 250px;
                        font-size: 25px;
                        margin-left: 150px;
                    }
                    @media screen and (max-width: 500px){
                        body{width:100%;height:auto;background-color: white;}
                        #main-wrapper{padding:10px;width:100%;height:auto;background-image: none;background-color:white;}
                        img{width: 90%;height:auto;margin: 10px auto;}
                        #summary{width:100%;height:auto;margin:auto;padding:10px;}
                    }
                </style>
            </head>
            <body>
                <div id="main-wrapper">
            """
            html2.replace('\w',' ')
            html_code += html2
            a = f'<img src="../picture/{img_name}"><h1 id = "subtitle">{ko_label}<h1><div id ="summary">{r_summary}<address><br>출처 : <a href="http://ko.wikipedia.org/wiki/{ko_label}">위키백과-{ko_label}</address></div>'
            html_code += a
            html_code += "</div></div></body></html>"
            
            # create folder
            if not os.path.isdir(self.root+'html') == True:
                os.mkdir(self.root+'html') 

            # create html
            filename = f'{whsthis}.html'
            with open(self.root+ 'html/' + filename,'w',encoding='UTF-8') as f :
                f.write(html_code)
                f.close()

        except UnboundLocalError:
            print("no whsthis")