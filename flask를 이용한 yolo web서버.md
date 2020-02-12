# Flask Web 서버

## 딕셔너리로 image 갤러리 구현하기

```python
from flask import Flask, render_template, request
app = Flask(__name__)


listData = [{"id":0, "img":"book2.jpg", "title":"책데이터" },
            {"id":1, "img":"dog.jpg", "title":"개 영상 테스트" },
            {"id":2, "img":"single.jpeg", "title":"사람 이미지 테스트" }
            ]


@app.route('/')
def index():
    return render_template('home.html', title="my home page")

@app.route('/image')
def image(): 
    return render_template('image.html', listData=listData)

@app.route('/view')   # /view?id=0
def view():    
    id = request.args.get("id")
    return render_template('view.html', s = listData[int(id)] )

@app.route('/fileUpload', methods = ['POST'])
def fileUpload():
    f = request.files['file1']
    f.save("./static/" + f.filename)
    title = request.form.get("title")
    return f'{f.filename}  - 제목{title} :  파일 업로드 성공!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
```

메인이 있는 폴더에 templates, static 이라는 폴더를 만들어주고

templates 에 home.html, image.html, view.html 을 만들어 준다.



## home.html

```python
<font color=red><h1> {{title}} </h1> </font>
fwejifwe    fjiwef  한글
```

## image.html

```pyhton
Yolo image 갤러리  <br>

<head>
       <meta charset = "utf-8"> 
       <meta name="viewport" content="width=device-width, initial-scale=1.0">  ### meta 2줄은 모바일 접속시 모바일 크기로 접속
</head>
<form action = "/fileUpload" method = "POST" enctype = "multipart/form-data">      
     <input type = "file" name = "file1" accept="image/*" capture="camera"/> <br>
     제목 :<input type=text name=title>
     <input type = "submit" value="전송"/>     
</form>

<table>
    {% for s  in  listData  %}     
    <tr>        
           <td> <a href=/view?id={{s.id}}> <img src="/static/{{s.img}}" width=30 >  </a>  </td>
           <td> {{s.title}}    </td>
    </tr>    
    {% endfor %}
</table>
```

![image-20200212135617486](C:\Users\Student\Desktop\typora\image\image-20200212135617486.png)

## view.html

```python
<font size=20> {{s.title}}   </font>  <br>
<img src=/static/{{s.img}} >  

<a href=/image> 목록으로 </a>
```

![image-20200212135702236](C:\Users\Student\Desktop\typora\image\image-20200212135702236.png)

### nogrok 활용하여 모바일 접속

![image-20200212135747617](C:\Users\Student\Desktop\typora\image\image-20200212135747617.png)

## 올렸을때 다시 홈으로 자동으로 돌아가게 하기



```html
<script>
    alert("업로드가 성공했습니다.")

    window.location.href = "/image"
</script>
```

![image-20200212152113111](C:\Users\Student\Desktop\typora\image\image-20200212152113111.png)

기존 코드에 적용

```python
from flask import Flask, render_template, request
app = Flask(__name__)

listData = [{"id":0,"img":"book2.jpg", "title":"책데이터" },
        {"id":1,"img":"dog.jpg", "title":"개 영상 테스트" },
        {"id":2,"img":"single.jpeg", "title":"사람 이미지 테스트" }
        ]

@app.route('/')
def index():
    return render_template('home.html', title="my home page")

@app.route('/image')
def image():    
    return render_template('image.html', listData=listData)

@app.route('/view')  #/view?id=0
def view():
    id = request.args.get("id")
    return render_template('view.html', s=listData[int(id)])

@app.route('/fileUpload', methods = ['GET','POST'])
def fileUpload():
    if request.method == 'POST':
        f = request.files['file1']
        f.save("./static/" + f.filename)
        title = request.form.get("title")
        id = len(listData)
        listData.append({"id":id,"img":f.filename,"title":title})

        html = """
<script>
    alert("업로드가 성공했습니다.")

    window.location.href = "/image"
</script>
        """

        return html

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000, debug=True)
```

### 이미지 업로드시 업로드가 성공했다고 나온후 메인으로 복귀

### 함수로 표현

```python
from flask import Flask, render_template, request
app = Flask(__name__)

listData = [{"id":0,"img":"book2.jpg", "title":"책데이터" },
        {"id":1,"img":"dog.jpg", "title":"개 영상 테스트" },
        {"id":2,"img":"single.jpeg", "title":"사람 이미지 테스트" }
        ]

@app.route('/')
def index():
    return render_template('home.html', title="my home page")

@app.route('/image')
def image():    
    return render_template('image.html', listData=listData)

@app.route('/view')  #/view?id=0
def view():
    id = request.args.get("id")
    return render_template('view.html', s=listData[int(id)])

def goURL(msg,url):
    html = """
<script>
    alert(@msg)

    window.location.href = "@url"
</script>
"""
	html = html.replace(html, "@msg", msg)
	html = html.replace(html, "@url", url)
	return html

@app.route('/fileUpload', methods = ['GET','POST'])
def fileUpload():
    if request.method == 'POST':
        f = request.files['file1']
        f.save("./static/" + f.filename)
        title = request.form.get("title")
        id = len(listData)
        listData.append({"id":id,"img":f.filename,"title":title})

        return goURL("업로드가 성공했습니다.","/ image")

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000, debug=True)
```

## 삭제 추가 다 적용

```python
from flask import Flask, render_template, request
app = Flask(__name__)


listData = [{"id":0, "img":"book2.jpg", "title":"책데이터" },
            {"id":1, "img":"dog.jpg", "title":"개 영상 테스트" },
            {"id":2, "img":"single.jpeg", "title":"사람 이미지 테스트" }
            ]

@app.route('/')
def index():
    return render_template('home.html', title="my home page")

@app.route('/image')
def image(): 
    return render_template('image.html', listData=listData)

@app.route('/view')   # /view?id=0
def view():    
    id = request.args.get("id")
    return render_template('view.html', s = listData[int(id)] )


def goURL(msg, url) :
   html = """        
<script>    
      alert("@msg");        
      window.location.href = "@url";
</script>
    """
   
   html = html.replace("@msg", msg)
   html = html.replace("@url", url)
   return html    

@app.route('/fileUpload', methods = ['POST'])
def fileUpload():
    f = request.files['file1']
    f.save("./static/" + f.filename)
    title = request.form.get("title")    
    
    id = listData[len(listData)-1]["id"] + 1    
    listData.append({"id":id, "img":f.filename, "title":title})    
    return goURL("업로드가 성공했습니다.",  "/image")

@app.route('/deleteimage')  # /deleteage?id=0
def deleteimage():        
    idx = -1
    id = int(request.args.get("id"))   
    for i in range(len(listData)) :
        if id == listData[i]["id"] :
            idx = i            
    if idx >= 0 : del listData[idx]                
        
    return goURL("자료를 삭제했습니다.",  "/image")



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000, debug=True)
```

## image.html

```python
Yolo image 갤러리  <br>

<form action = "/fileUpload" method = "POST"
       enctype = "multipart/form-data">      
     <input type = "file" name = "file1" /> <br>
     제목 :<input type=text name=title>
     <input type = "submit" value="전송"/>     
</form>

<table>
    {% for s  in  listData  %}     
    <tr>        
           <td> <a href=/view?id={{s.id}}> <img src="/static/{{s.img}}" width=30 >  </a>  </td>
           <td> {{s.title}}    </td>
           <td> <a href=/deleteimage?id={{s.id}}>삭제</a> </td>
    </tr>    
    {% endfor %}
</table>

```



![image-20200212161948843](C:\Users\Student\Desktop\typora\image\image-20200212161948843.png)

![image-20200212162004827](C:\Users\Student\Desktop\typora\image\image-20200212162004827.png)

![image-20200212162027800](C:\Users\Student\Desktop\typora\image\image-20200212162027800.png)

![image-20200212162046018](C:\Users\Student\Desktop\typora\image\image-20200212162046018.png)

## html로 이미지 입력받아 yolo 실행하기

### web.py

```python
from flask import Flask, render_template, request
import yolo
import time
app = Flask(__name__)


listData = [{"id":0, "img":"book2.jpg", "title":"책데이터" },
            {"id":1, "img":"dog.jpg", "title":"개 영상 테스트" },
            {"id":2, "img":"single.jpeg", "title":"사람 이미지 테스트" }
            ]

@app.route('/')
def index():
    return render_template('home.html', title="my home page")

@app.route('/image')
def image(): 
    return render_template('image.html', listData=listData)

@app.route('/view')   # /view?id=0
def view():    
    id = request.args.get("id")
    return render_template('view.html', s = listData[int(id)] )


def goURL(msg, url) :
   html = """        
<script>    
      alert("@msg");        
      window.location.href = "@url";
</script>
    """
   
   html = html.replace("@msg", msg)
   html = html.replace("@url", url)
   return html    

@app.route('/fileUpload', methods = ['POST'])
def fileUpload():
    f = request.files['file1']
    f.save("./static/" + f.filename)
    title = request.form.get("title")    
    
    id = listData[len(listData)-1]["id"] + 1    
    listData.append({"id":id, "img":f.filename, "title":title})   
    yolo.detectObject("./static/"+f.filename)
    time.sleep(1)
    return goURL("업로드가 성공했습니다.",  "/image")

@app.route('/deleteimage')  # /deleteage?id=0
def deleteimage():        
    idx = -1
    id = int(request.args.get("id"))   
    for i in range(len(listData)) :
        if id == listData[i]["id"] :
            idx = i            
    if idx >= 0 : del listData[idx]                
        
    return goURL("자료를 삭제했습니다.",  "/image")



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000, debug=True)
```

### yolo.py

```python
import cv2 as cv
import argparse
import numpy as np

confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 416       #Width of network's input image
inpHeight = 416      #Height of network's input image

# Load names of classes
classesFile = "coco.names"
classes = None
with open(classesFile, 'rt') as f:

    classes = f.read().rstrip('\n').split('\n')
# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(frame, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    
    label = '%.2f' % conf
        
    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame, classIds[i], confidences[i], left, top, left + width, top + height)  
        
        
def detectObject(filename) :
    frame = cv.imread(filename)
    blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    postprocess(frame, outs)
    cv.imwrite(filename, frame)   
    return filename
```

### image.html

```python
Yolo image 갤러리  <br>

<form action = "/fileUpload" method = "POST"
       enctype = "multipart/form-data">      
     <input type = "file" name = "file1" /> <br>
     제목 :<input type=text name=title>
     <select name=algorithm>
            <option value=0>YOLO</option>
            <option value=1>Face Detection</option>
     </select>
     <input type = "submit" value="전송"/>     
</form>

<table>
    {% for s  in  listData  %}     
    <tr>        
           <td> <a href=/view?id={{s.id}}> <img src="/static/{{s.img}}" width=30 >  </a>  </td>
           <td> {{s.title}}    </td>
           <td> <a href=/deleteimage?id={{s.id}}>삭제</a> </td>
    </tr>    
    {% endfor %}
</table>

```

### view.html

``` python
<font size=20> {{s.title}}   </font>  <br>
<img src=/static/{{s.img}} >  

<a href=/image> 목록으로 </a>
```

![image-20200212173056309](C:\Users\Student\Desktop\typora\image\image-20200212173056309.png)

## face Detection, yolo 중에 선택하여 적용하기

![image-20200212184412211](C:\Users\Student\Desktop\typora\image\image-20200212184412211.png)

### web.py

```python
from flask import Flask, render_template, request
import yolo, agegender
import time
app = Flask(__name__)


listData = [{"id":0, "img":"book2.jpg", "title":"책데이터" },
            {"id":1, "img":"dog.jpg", "title":"개 영상 테스트" },
            {"id":2, "img":"single.jpeg", "title":"사람 이미지 테스트" }
            ]

@app.route('/')
def index():
    return render_template('home.html', title="my home page")

@app.route('/image')
def image(): 
    return render_template('image.html', listData=listData)

@app.route('/view')   # /view?id=0
def view():    
    id = request.args.get("id")
    return render_template('view.html', s = listData[int(id)] )


def goURL(msg, url) :
   html = """        
<script>    
      alert("@msg");        
      window.location.href = "@url";
</script>
    """
   
   html = html.replace("@msg", msg)
   html = html.replace("@url", url)
   return html    

@app.route('/fileUpload', methods = ['POST'])
def fileUpload():
    f = request.files['file1']
    f.save("./static/" + f.filename)
    title = request.form.get("title")   

    checkbox = int(request.form.get("algorithm"))

    if checkbox == 1:
        id = listData[len(listData)-1]["id"] + 1    
        listData.append({"id":id, "img":f.filename, "title":title})   
        yolo.detectObject("./static/"+f.filename)
        time.sleep(1)
        return goURL("업로드가 성공했습니다.",  "/image")
    elif checkbox == 0:
        id = listData[len(listData)-1]["id"] + 1    
        listData.append({"id":id, "img":f.filename, "title":title})   
        agegender.objectT("./static/"+f.filename)
        time.sleep(1)
        return goURL("업로드가 성공했습니다.",  "/image")

@app.route('/deleteimage')  # /deleteage?id=0
def deleteimage():        
    idx = -1
    id = int(request.args.get("id"))   
    for i in range(len(listData)) :
        if id == listData[i]["id"] :
            idx = i            
    if idx >= 0 : del listData[idx]                
        
    return goURL("자료를 삭제했습니다.",  "/image")



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000, debug=True)
```

### yolo.py

```python
import cv2 as cv
import argparse
import numpy as np

confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 416       #Width of network's input image
inpHeight = 416      #Height of network's input image

# Load names of classes
classesFile = "coco.names"
classes = None
with open(classesFile, 'rt') as f:

    classes = f.read().rstrip('\n').split('\n')
# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(frame, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    
    label = '%.2f' % conf
        
    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame, classIds[i], confidences[i], left, top, left + width, top + height)  
        
        
def detectObject(filename) :
    frame = cv.imread(filename)
    blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    postprocess(frame, outs)
    cv.imwrite(filename, frame)   
    return filename
```

### image.html

```python
Yolo image 갤러리  <br>

<form action = "/fileUpload" method = "POST"
       enctype = "multipart/form-data">      
     <input type = "file" name = "file1" /> <br>
     제목 :<input type=text name=title>
     <select name='algorithm'>
            <option value=1>YOLO</option>
            <option value=0>Face Detection</option>
     </select>
     <input type = "submit" value="전송"/>     
</form>

<table>
    {% for s  in  listData  %}     
    <tr>        
           <td> <a href=/view?id={{s.id}}> <img src="/static/{{s.img}}" width=30 >  </a>  </td>
           <td> {{s.title}}    </td>
           <td> <a href=/deleteimage?id={{s.id}}>삭제</a> </td>
    </tr>    
    {% endfor %}
</table>


```

### agegender.py

```python
import cv2 as cv
import math
import time
import argparse

_input= ""

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"         # 받아야함
 
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"  # 받아야함

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

ageNet = cv.dnn.readNet(ageModel, ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
faceNet = cv.dnn.readNet(faceModel, faceProto)

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

def objectT(filename):
    cap = cv.VideoCapture("./static/"+filename)
    padding = 100
    hasFrame, frame = cap.read()

    frameFace, bboxes = getFaceBox(faceNet, frame)

    for bbox in bboxes:
            # print(bbox)
            face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
    
            blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
    
            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]    
            label = "{},{}".format(gender, age)
            cv.putText(frameFace, label, (bbox[0], bbox[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
            cv.imwrite("./static/"+filename, frameFace)
    return filename
```

![image-20200212184813405](C:\Users\Student\Desktop\typora\image\image-20200212184813405.png)