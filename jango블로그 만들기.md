# 블로그 만들기

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import Post
from django.views.generic import View
from django.contrib.auth import authenticate ## login 인증을 DB와 하기 위해서
from django.contrib.auth.models import User ## model에 저장된 사용자 정보 불러오기 위함
from django.forms import Form## 장고가 form ui 요소를 만들어줄수 있도록 11
from django.forms import CharField, Textarea ## 장고가 form ui 요소를 만들어줄수 있도록 22
```



python manage.py startapp blog 로 새로운 app을 만들어 준다.

views.py

```python
def index(request):
    return HttpResponse("ok")
```

urls.py

```python
from . import views
urlpatterns = [
    path('',views.index)
]
```

![image-20200218191125190](C:\Users\Student\Desktop\typora\image2\django DB(ORM).md)

### DB 연동하여 데이터 확인하기



models.py

```python
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()  # 글자수에 제한 없는 텍스트
    created_date = models.DateTimeField(
        default=timezone.now)  # 날짜와 시간
    published_date = models.DateTimeField(
        blank=True, null=True) #  필드가 폼에서 빈 채로 저장되는 것을 허용

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
```

admin.py

```python
from django.contrib import admin
from blog.models import Post
# Register your models here.
admin.site.register(Post)
```

**DB 생성**

```powershell
python manage.py makemigrations blog
python migrate
```

**데이터 등록**

![image-20200218191417431](C:\Users\Student\Desktop\typora\image2\image-20200218191417431.png)

views.py

```python
def list(request):
    data = Post.objects.all() # 모든 사용자 똑같이 데이터 다 보여주기
    username = request.session["username"]
    return render(request, "blog/list.html", {"data":data, "username":username})
```

urls.py

```python
path('list/',views.list, name="list"), 추가 (name 을 지정해주면 redirect시 name 값으로 호출 가능)
```



list.html

```python
{% extends 'blog/base.html' %}  # 베이스.html을 기본으로 쓰겠다.

{% block content %}

{%  for d in data %}
<a href="{% url 'detail' d.pk}"> {{d.title}} </a> <br>

{% endfor %}

{% endblock %}
```

base.html

```python
<font color="red"><h1>My blog</h1> </font><br>
{{username}}님 로그인 되셨습니다.<br>

{% block content %}
{% endblock %}


<br><br><br>
copy right..... <br>
서울특별시 ........
```

![image-20200218191849638](C:\Users\Student\Desktop\typora\image2\image-20200218191849638.png)

## views.py (유저별 데이터 보여주기)

```python
from django.contrib.auth.models import User
def list(request) :
    username = request.session["username"]
    user = User.objects.get(username=username) #사용자 id 가져오기
    data = Post.objects.all().filter(author=user)# id 가져와서 DB 필터링 하기
    context = {"data":data, "username":username}
    return render(request, "blog/list.html", context)
```

* User.objects.get 으로 DB내 사용자 목록을 불러오고 필터를 통해서 사용자에 따른 데이터 추출가능



## 로그인 페이지 만들기(view.generic사용)

### 객체의 제네릭뷰

* 장고의 제네릭 뷰는 데이터베이스 컨텐츠의 뷰를 보여줄때 장점이 많다.

* 또한 class로 묶기에 가독성이 좋고 간결해진다.



views.py

```python
from django.contrib.auth import authenticate
class LoginView(View) :
    def get(self, request):
        return render(request, "blog/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password) ##패스워드와 id를 DB에서 확인
        if user == None :
            return redirect("login") ## urls 파일에서 name로 정의된 값으로 간다.
        request.session["username"] = username # 로그인 했을때 누구인지를 저장하기 위해 세션값에 username을 저장한다.
        return redirect("list")
```

login.html

```python
<form action = "{% url 'login'%}"method=POST> <!--action을 상대경로로 표시하기 위해서는 url 이라는 값으로 정의한다.-->
    {% csrf_token %}
    id <input type=text name=username> <br>
    pw <input type=password name=password> <br>
    <input type=submit name="로그인"> 
    
</form>
```

urls.py

```python
path('login/', views.LoginView.as_view(), name="login"), #  .as_view() 를 통해서 generic view를 적용할 수 있다.
```

![image-20200218193400232](C:\Users\Student\Desktop\typora\image2\image-20200218193400232.png)

### 로그인 페이지를 완성함으로 로그인시에만 service 페이지에 접속할수 있게 되었다

### 데이터 추가 삭제

views.py

```python
from django.forms import Form
from django.forms import CharField, Textarea, ValidationError

class PostView(View) :
    def get(self, request):
        return render(request, "blog/edit.html")

    def post(self, request):

        title = request.POST.get("title")
        text = request.POST.get("text")
        username = request.session["username"]
        user = User.objects.get(username=username)
        Post.objects.create(title=title, text=text, author=user)
        return redirect("list")

class PostEditView(View) :
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(initial={'title': post.title, 'text': post.text})
        return render(request, "blog/edit.html", {"form":form, "pk":pk})

    def post(self, request, pk):
        form = PostForm(request.POST)
        if form.is_valid():#입력 받는 데이터가 모두 정상일때 True
            post = get_object_or_404(Post, pk=pk)
            post.title = form['title'].value()
            post.text = form['text'].value()
            post.publish()
            return redirect("list")
        return render(request, "blog/edit.html", {"form": form, "pk": pk})

def validator(value) :
    if len(value) < 5 : raise  ValidationError("길이가 너무 짧아요");
```

`get_object_or_404()`: 해당 모델의 기본 키(primary key) 값에 연결되는 특정 객체를 반환하거나 해당 record가 없을경우 `Http404`예외를 발생시킨다. 