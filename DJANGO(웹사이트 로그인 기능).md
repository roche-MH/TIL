# DJANGO(웹사이트 로그인 기능)



<<DJANGO>>

FLASK 는 단순하지만(웹서버 + 파이썬코드 실행 가능), 매번 서버에 요청할 때 마다 코드를 실행하는데 이것은 프로세스를 생성한다는 것이고 프로그램에게 부담을 주는 업무임

동시에 많은 사람이 접속하는 웹사이트에서는 문제가 발생할 수 있음



MVC&MTV

* Model : 안전하게 데이터를 저장(데이터를 모델링하는 부분)
* View: 데이터를 적절하게 유저에게 보여줌(사용자에게 내용을 어떻게 보여줄지에 대한 내용)
* Control / Template : 사용자의 입력과 이벤트에 반응하여 Model과 View를 업데이트

![image-20200213183602879](C:\Users\Student\Desktop\typora\image\image-20200213183602879.png)

Flask 와 는 다르게 내부적인 구조가 많이 있다.

![image-20200213183644679](C:\Users\Student\Desktop\typora\image\image-20200213183644679.png)

static 파일들을 서버에서 운영하기에는 아파치 등 전통적인 서버 툴을 이용하는 것이 훨씬 안정적이고 효율적 실제 서비스는 Flask 하나만, 또는 Django 하나만을 이용하는 것은 없음

Service side 작업은 아파치를 통해서 동작시키고 나머지는 flask/django 를 활용하는 방식

django는 -project와 app을 생성해서 코드 작성

- 프로젝트 생성 : $django-admin startproject tutorial
- app 생성 : $./manage.pt startapp ommunity



설치

```python
$pip install django
$django-admin ##  입력시 명령어를 확인할수 있다.(help 와 동일)
```

명령어로 프로젝트 생성

```python
$django-admin startproject mysite_200213 ##명령어를 친 폴더에서 생성
```

mysite_200213 폴더에는 기본적인 설정 값들이 작성된 코드들이 있다.



flask와 다르게 우리가 아무런 코드를 작성하지 않아도 '기본적인'(실행은 되는)사이트가 있음

해당 폴더로 위치하고 명령어 입력

![image-20200213184056751](C:\Users\Student\Desktop\typora\image\image-20200213184056751.png)

![image-20200213184109998](C:\Users\Student\Desktop\typora\image\image-20200213184109998.png)

기본 포트는 8000번으로 초기 세팅 없이 웹 페이지 접속시에 아래와 같은 페이지가 나온다.

![image-20200213184134031](C:\Users\Student\Desktop\typora\image\image-20200213184134031.png)

웹페이지를 생성하기 위해서는 app을 생성해 줘야 한다(cmd 로 이동해서 명령어를 쳐주면 기본적인것들 자동생성)

```bash
$python manage.py startapp myapp
```

![image-20200213184256605](C:\Users\Student\Desktop\typora\image\image-20200213184256605.png)

실제적으로 flask에서 index.html 과 같이 작동하는 곳은 views 파일이다.

views파일에서 아래와 같이 def index 대한 코드를 짜준다.

![image-20200213184423423](C:\Users\Student\Desktop\typora\image\image-20200213184423423.png)

그다음 urls.py 를 봐야 되는데 처음에 myapp은 urls 가 없고 mysite 에만 있음

![image-20200213184554403](C:\Users\Student\Desktop\typora\image\image-20200213184554403.png)

이기능으로 localhost:8000/admin 으로 들어가면 아래와 같이 나온다.

![image-20200213184625381](C:\Users\Student\Desktop\typora\image\image-20200213184625381.png)

myapp 에서 코드를 작성할 예정이기때문에 myapp 폴더에 urls를 복사해주고

기존 urls에는 다음과 같이 적어준다. (mysite.urls)

![image-20200213184732623](C:\Users\Student\Desktop\typora\image\image-20200213184732623.png)

(myapp.urls)

![image-20200213184815423](C:\Users\Student\Desktop\typora\image\image-20200213184815423.png)

views 에 존재하는 index함수를 선언해준다.

이렇게 하면 루트 페이지('/')에 대한 url - 함수가 매핑된다.

127.0.0.1:8000으로 들어가면 아까와 다르게 views 파일에서 정의한 Main Screen is here 이라는 문구를 볼수 있다.

![image-20200213185013521](C:\Users\Student\Desktop\typora\image\image-20200213185013521.png)

여기서 볼수있는게 flask는 서버가 실행될 때 모든 코드를 다시 실행하는데(변수 선언 등등)

django는 변화된 부분만 하기 때문에 빨라보이는 것처럼 느껴진다.

함수 url 추가해서 제대로 되는지 확인해본다.

(views.py)

```python
def index(request):
    return HttpResponse("Main Screen is here")

def test(request):
    return HttpResponse("Test Screen is here")
```

(urls.py)

```python
from . import views
urlpatterns = [
    path('',views.index),
    path('test',views.test),
]
```

![image-20200213185302712](C:\Users\Student\Desktop\typora\image\image-20200213185302712.png)



루트페이지 지정 (chroot) mysite.urls.py

![image-20200213185402008](C:\Users\Student\Desktop\typora\image\image-20200213185402008.png)

myapp.urls 이부분을 변경해주면 변경한 부분으로 / 디렉터리가 생성된다.

ex) path('***',include('myapp.urls')) 여기 **** 부분을 aaa로 입력하면

웹브라우저에서 접속할 때 이제 루트페이지가 /에서 /aaa 로 된다.



view.py는 controller + view 의 기능을 모두 담당한다.

flask에서 사용하던 문법과 동일하지만 전달하는 방식에만 차이가 있음

test 페이지에 render()를 이용해서 코드 수정 myapp.views

![image-20200213185623711](C:\Users\Student\Desktop\typora\image\image-20200213185623711.png)

![image-20200213185642542](C:\Users\Student\Desktop\typora\image\image-20200213185642542.png)

template.html 파일이 필요한경우 루트 디렉토리에 template라고 폴더를 생성한후 template.html이라는

파일을 만들어 준다.



그리고 mysite , settings.py 에서 54번째 TEMPLATES 에서 DIRS 부분을 채워준다.

![image-20200213185819658](C:\Users\Student\Desktop\typora\image\image-20200213185819658.png)



template.html에 값을 전달하고, 그 값을 받아서 출력해보는것

![image-20200213185916272](C:\Users\Student\Desktop\typora\image\image-20200213185916272.png)

![image-20200213185931745](C:\Users\Student\Desktop\typora\image\image-20200213185931745.png)





## 로그인 페이지 만들기

이미지 디렉토리 만들기 mysite 전 루트 디렉토리에서 static 이라는 파일을 만든후 이미지를 만들어준다.

그리고 mysite > settings.py 에서 마지막 줄에 보면 STATIC_URL = '/static' 이라고 있는데 그 밑에 적어준다.(나중에 static을 통해서 얼굴 로그인 진행)

![image-20200213192201527](../../AppData/Roaming/Typora/typora-user-images/image-20200213192201527.png)



그리고 static 폴더에 가서 login.html 파일을 만들어 준다.

```python
<form action=/login method="GET">

    id <input type=text name=id> <br>
    pw <input type=password name=pwd> <br>
    <input type=submit name="로그인"> <br>    
    
</form>
```

![image-20200213113935008](C:\Users\Student\Desktop\typora\image-20200213113935008.png)



기본적으로 static 에 로그인 페이지를 만들어주는건 보안상 매우 위험하기 때문에 보편적으로는 

template 파일에 login.html 을 만들어준다음

```python
<form action=/login method="GET">

    id <input type=text name=id> <br>
    pw <input type=password name=pwd> <br>
    <input type=submit name="로그인"> <br>    
    
</form>
```

views.py 이랑 urls.py 에서 추가해준다.

```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request): # flask에서 request와 동일한 기능을 해주는 것
    return HttpResponse("Main Screen is here")

def test(request) :
    data = {"s":{"img":"test.png"}, "list":[1,2,3,4,5]}
    return render(request, 'template.html',data)

def login(request):
    return render(request, 'login.html') <== 이부분
```

urls

```python
from django.urls import path
from . import views  # from 다음에는 폴더 명이 오는데 .이니까 current 폴더를 의미

urlpatterns = [
    path('', views.index), #current 폴더 안에 있는 views 파일을 읽어오는데, views 파일 안에 index() 함수
    path('test', views.test),
    path('login', views.login),
]
```



login.html 에서 받은 값을 login(request) 에서 처리를 하는 가설을 정한다.

1. id 와 pw 가 동일 할 경우 접속 성공
2. 접속시 세션 유지
3. 접속후 로그아웃 기능 



구현

view.py

```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
def login(request):
    id = request.GET["id"]
    pwd = request.get["pwd"]
    if id ==pwd:
        request.session["user"] =id #session을 유저마다 다른값을 주어서 접속시에 유지할수 있도록
        #session을 만들었을경우 아래에서 DB관리에서 보이듯이 DB에서 명령어로 테이블을 새로 만들어줘야한다.
        return redirect("/service") #접속 성공시 /service 페이지로 넘어감
    return redirect("/static/login.html")

def logout(request):
    request.session["user"] ="" # session 초기화 시켜서 다시 로그인 할수 있도록
    return redirect("/static/login.html")

def service(req): #이부분은 값을 받아오는 곳이라 request 그냥 변수명이라 생각하면된다.
    if req.session.get("user","") == "":
        return redirect("/static/login.html") #로그인 안했을 경우 service 페이지 접근 거부
   html = "Main Service<br>" + req.session.get("user") + "님 감사합니다.  <a href=/logout>로그아웃하기</a>" 
    return HttpResponse(html)
```

urls.py

```python
from django.urls import path
from . import views  # from 다음에는 폴더 명이 오는데 .이니까 current 폴더를 의미

urlpatterns = [
    path('', views.index), #current 폴더 안에 있는 views 파일을 읽어오는데, views 파일 안에 index() 함수
    path('test', views.test),
    path('login', views.login),
    path('logout', views.logout),
    path('service', views.service),
    path('uploadimage', views.uploadimage),
]
```

login.html

```python
<form action=/login method="GET">

    id <input type=text name=id> <br>
    pw <input type=password name=pwd> <br>
    <input type=submit name="로그인"> <br>

</form>
<!-- 처리는 폼단위로 되기 때문에 서로 간의 연동 연관은 무시해도 된다.-->
<form action = "/uploadimage" method = "POST"
       enctype = "multipart/form-data">
     <input type ="file" name = "file1" /> <br>
      <input type=submit name="얼굴인증">  
     <!--<select name=algorithm>
         <option value=0>YOLO</option>
         <option value=1>face detection</option>
     </select>-->
        
    
</form>
```



***보안문제***

service 웹페이지를 접속할경우 로그인 된 상태나 안된상태 둘다 접속이 가능하기 때문에

세션값을 만들어줘서 로그인 성공시 세션값을 받아 저장하고 로그아웃시 세션값을 초기화 하는 형태로 구성



**세션-쿠키** : 둘다 키벨류 값으로 구성되어 있는데 쿠키는 사용자가 가지고 있는거고 세션은 서버에서 관리하고 있는 것

```python
def service(req): ## 로그인을 했는지 안했는지를 따져서 분리를 해주어야 한다.
    if req.session.get("user", "") == "" :# get 했을때 user 값이 없을경우 default ""  session 은 글로벌 변수도 아니고 지역변수도 아닌 중간 값
        return redirect("/static/login.html")
    html = "Main Service<br>" + req.session.get("user") + "님 감사합니다." 
    return HttpResponse(html)
```



**DB 관리** (DB 테이블 등 필요한게 있을경우 아래 명령어를 치면 자동으로 생성해준다.) mysql 기반

python manage.py migrate 

![image-20200213142624568](C:\Users\Student\Desktop\typora\image-20200213142624568.png)

초기 서비스 페이지 접속 시도시 로그인 페이지로 넘어가고

![image-20200213142802639](C:\Users\Student\Desktop\typora\image-20200213142802639.png)

로그인 성공시 서비스 페이지로 넘어가게 된다.

![image-20200213142823216](C:\Users\Student\Desktop\typora\image-20200213142823216.png)

### 파일 업로드 하기

login.html

```python

<form action=/login method="GET">

    id <input type=text name=id> <br>
    pw <input type=password name=pwd> <br>
    <input type=submit name="로그인"> <br>

</form>
<!-- 처리는 폼단위로 되기 때문에 서로 간의 연동 연관은 무시해도 된다.-->
<form action = "/uploadimage" method = "POST"
       enctype = "multipart/form-data">
     <input type = "file" name = "file1" /> <br>
      <input type=submit name="얼굴인증">  
     <!--<select name=algorithm>
         <option value=0>YOLO</option>
         <option value=1>face detection</option>
     </select>-->
        
    
</form>
```

urls.py

```python
urlpatterns = [
    path('', views.index), #current 폴더 안에 있는 views 파일을 읽어오는데, views 파일 안에 index() 함수
    path('test', views.test),
    path('login', views.login),
    path('logout', views.logout),
    path('service', views.service),
    path('uploadimage', views.uploadimage),
]
```

view.py

```python
def uploadimage(req):
    return HttpResponse("ok")
```

이렇게만 했을 경우 CSFR 에러가 난다.

![image-20200213152800191](C:\Users\Student\Desktop\typora\image-20200213152800191.png)

CSFR 은 XSS와 조금 다른 기법으로 해커가 서버에 코드를 짜서 올렸을 경우 다른 사용자가 그걸 보고 눌렀을때

피해를 입는 기법



무시하기

```python
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def uploadimage(req):
    return HttpResponse("ok")
```

![image-20200213153100226](C:\Users\Student\Desktop\typora\image-20200213153100226.png)

파일업로드(views.py)

```python
from django.conf import settings
@csrf_exempt
def uploadimage(req):
    file = req.FILES['file1']
    filename = file._name
    fp = open(settings.BASE_DIR + "/static" + filname, "wb") 
    #BASE_DIR = settings.py 에 지정되어 있다.
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()
    html = "ok :" + "^^" + filename
    return HttpResponse(html)
```

파일 업로드가 되서 static 파일에 올라온다면 facedetection 을 통해서 웹으로 구현 해줄수가 있다.





## 이미지 로그인 기능 구현

(views.py)

```python
import facereco
@csrf_exempt
def uploadimage(req):
    file = req.FILES['file1']
    filename = file._name
    fp = open(settings.BASE_DIR + "/static" + filename, "wb")
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()
    ------------- 파일을 저장하는 코드

    result = facereco.facerecognition("known.bin","/static" + filename)
    if result[0] != "":
        request.sesstion["user"] = id
        return redirect("/service")
    return redirect("static/login.html")
	------------------- 모델을 불러와서 값을 확인함 모델은 이미지를 넣었을때 학습된 모델에서 그사람과 가장 거리가 가까운 얼굴의 이름을 출력해준다.
    
    
```

(facereco.py)

```python
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import matplotlib.pyplot as plt
import face_recognition
import os
from imutils import paths
import pickle

def facerecognition(model, file):
    data = pickle.loads(open(model, "rb").read())
    image = cv2.imread(file)

    boxes = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, boxes)
 
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {} 
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1 
            name = max(counts, key=counts.get)
        names.append(name)                             
    return names
```

위 코드가 이미지를 넣으면 이름을 출력할수 있게 하는 것이고 모델은 기존에 학습해 두었던 모델을 사용하였다.



**주의** 이미지 로그인 방식은 주의해야할 점이 있는데 face_recognition 은 python 3.6 에서 밖에 되지 않고

dlib 등과 같은 모듈을 따로 설치해주어야 한다.

따라서 방법을 사용시에는 python3.6으로 설정해주고 django 또한 3.6 버전에 맞춰서 설치가 되어야 실행이된다.

![image-20200213192011257](C:\Users\Student\Desktop\typora\image\image-20200213192011257.png)

![image-20200213192024791](C:\Users\Student\Desktop\typora\image\image-20200213192024791.png)