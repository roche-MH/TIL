# django DB(ORM)

sql 데이터 베이스를 조작하는 언어

sql의 특징

DBMS 제작 회사와 독립적임

다른 시스템으로의 이식성이 좋음

표준이 계속 발전함

대화식 언어임

클라이언트/서버 구조 지원함



표준 SQL과 각 회사의 SQL

* 많은 회사가 되도록 표준 sql을 준수하려고 노력하지만 각 회사의 DBMS마다 특징이 있기 때문에 현실적으로 완전히 통일 되기는 어려움
* 각 회사의 제품은 모두 표준 SQL을 공통으로 사용



c, python, r , bash 등 일반 언어는 절차적 언어이고 SQL은 선언적 언어이다.

절차적언어는 how2how

선언적 언어는 선언으로 인해 값을 불러옴 ex) select * from db;





select 문 형식

select select_expr

[from table_references]

[where where_condition]

[group by {col_name | expr | position}]

[having]

[orderby]



## django dblite 관리자 계정 만들기

mysite 페이지에 가서 

```python
python manage.py createsuperuser 해주면 유저가 생기고
```

127.0.0.1:8000/admin 으로 들어가서 설정한 아이디 패스워드를 쳐서 들어가면 된다.

user 에 들어가면 계정 정보

![image-20200217104646488](C:\Users\Student\Desktop\typora\image2\image-20200217104646488.png)



home으로 들어가보면 여러가지 user 의 정보를 볼수도 있고 권한도 설정해 줄수 있다. sql grant

![image-20200217104724544](C:\Users\Student\Desktop\typora\image2\image-20200217104724544.png)

user 에서 유저를 추가할수 있는데 기본생성시 일반 유저로 생성된다.

![image-20200217104923183](C:\Users\Student\Desktop\typora\image2\image-20200217104923183.png)

## db 쿼리로 데이터 관리하기

sqlite browser 다운 받아서 db 접속

![image-20200217105214871](C:\Users\Student\Desktop\typora\image2\image-20200217105214871.png)

![image-20200217110322901](C:\Users\Student\Desktop\typora\image2\image-20200217110322901.png)



### table 만들어주기

```python
CREATE TABLE userTBL -- 회원 테이블 
( userID CHAR(8) NOT NULL PRIMARY KEY, -- 사용자 아이디(PK) 
  userName VARCHAR(10) NOT NULL, -- 이름 
  birthYear INT NOT NULL, -- 출생 연도 
  addr CHAR(2) NOT NULL, -- 지역(경기, 서울, 경남 식으로 2글자만 입력) 
  mobile1 CHAR(3), -- 휴대폰의 국번(011, 016, 017, 018, 019, 010 등) 
  mobile2 CHAR(8), -- 휴대폰의 나머지 번호(하이픈 제외) 
  height SMALLINT, -- 키 
  mDate DATE -- 회원 가입일
);
CREATE TABLE buyTBL -- 구매 테이블 
( num INTEGER   PRIMARY KEY AUTOINCREMENT, 
  userID CHAR(8) NOT NULL, -- 아이디(FK) 
  prodName CHAR(6) NOT NULL, -- 물품 
  groupName CHAR(4), -- 분류 
  price INT NOT NULL, -- 단가 
  amount SMALLINT NOT NULL, -- 수량 
  FOREIGN KEY (userID) REFERENCES userTBL (userID)
);

```

```python
INSERT into userTBL VALUES('KHD','강호동',1970,'경북','011','22222222', 182, '2007-07-07')
```

데이터 삽입 한 결과

![image-20200217112604595](C:\Users\Student\Desktop\typora\image2\image-20200217112604595.png)

```python
INSERT into buyTBL VALUES(NULL, 'fef','운동화',NULL,30,2) ##error 발생

#FOREIGN KEY (userID) REFERENCES userTBL (userID) 키로 userid 값을 외래키로 매칭시켜놔서 불가능

# 일부만 맵핑 시키려면 () 로 컬럼명을 적어준다.
INSERT into buyTBL (userID, prodName, price, amount) VALUES('KHD','운동화',30,2)
num 은 auto_increment 로 자동 생성이 되야 하는데 dblite 에서 실행이 잘 안되서 값을 넣어줌

INSERT into buyTBL (num,userID, prodName, price, amount) VALUES(1,'KHD','운동화',30,2)
```



데이터 인설트 

```python
INSERT INTO userTBL VALUES ('KHD', '강호동', 1970, '경북', '011', '2222', 182, '2007-7-7');
INSERT INTO userTBL VALUES ('KKJ', '김국진', 1965, '서울', '019', '33333333', 171, '2009-9-9');
INSERT INTO userTBL VALUES ('KYM', '김용만', 1967, '서울', '010', '44444444', 177, '2015-5-5');
INSERT INTO userTBL VALUES ('KJD', '김제동', 1974, '경남', NULL , NULL, 173, '2013-3-3');
INSERT INTO userTBL VALUES ('NHS', '남희석', 1971, '충남', '016', '66666666', 180, '2017-4-4');
INSERT INTO userTBL VALUES ('SDY', '신동엽', 1971, '경기', NULL, NULL, 176, '2008-10-10');
INSERT INTO userTBL VALUES ('LHJ', '이휘재', 1972, '경기', '011', '88888888', 180, '2006-4-4');
INSERT INTO userTBL VALUES ('LKK', '이경규', 1960, '경남', '018', '99999999', 170, '2004-12-12');
INSERT INTO userTBL VALUES ('PSH', '박수홍', 1970, '서울', '010', '00000000', 183, '2012-5-5');

INSERT INTO buyTBL VALUES (NULL, 'KHD', '운동화', NULL, 30, 2);
INSERT INTO buyTBL VALUES (NULL, 'KHD', '노트북', '전자', 1000, 1);
INSERT INTO buyTBL VALUES (NULL, 'KYM', '모니터', '전자', 200, 1);
INSERT INTO buyTBL VALUES (NULL, 'PSH', '모니터', '전자', 200, 5);
INSERT INTO buyTBL VALUES (NULL, 'KHD', '청바지', '의류', 50, 3);
INSERT INTO buyTBL VALUES (NULL, 'PSH', '메모리', '전자', 80, 10);
INSERT INTO buyTBL VALUES (NULL, 'KJD', '책', '서적', 15, 5);
INSERT INTO buyTBL VALUES (NULL, 'LHJ', '책', '서적', 15, 2);
INSERT INTO buyTBL VALUES (NULL, 'LHJ', '청바지', '의류', 50, 1);
INSERT INTO buyTBL VALUES (NULL, 'PSH', '운동화', NULL, 30, 2);
INSERT INTO buyTBL VALUES (NULL, 'LHJ', '책', '서적', 15, 1);
INSERT INTO buyTBL VALUES (NULL, 'PSH', '운동화', NULL, 30, 2);
```



## 조인

테이블의 행의 개수 * 행의 개수 한 값만 큼 출력이 되는데 이거는 외부 조인이라 하고 NULL 값이 존재

```python
select count(*) from userTBL, buyTBL
------------------------
108개  -> user 9 * buy 12
```



내부조인(두 테이블간 컬럼이 같은 값을 기준으로 조인한다, 이 테이블은 bt가 ut의 외래키기 때문에 적용가능)

```python
select * from userTBL as ut, buyTBL as bt
where ut.useriD=bt.userID
```

유저별 합계 구하기

```python
select addr, u.userid, username, sum(amount), sum(amount * price) as total from buyTBL as b,userTBL as u
where b.userID=u.userID
group by addr
having total > 170
order by total desc
```





# ORM(object Relation Model)

django ORM

![image-20200217134305574](C:\Users\Student\Desktop\typora\image2\image-20200217134305574.png)

![image-20200217134540306](C:\Users\Student\Desktop\typora\image2\image-20200217134540306.png)



ORM을 사용하기 위해서는 INSTALLED_APPS(mysite/settings.py)부분에 이름을 넣어주어야 한다.



-model 클래스 생성

class Post(models.Model)

-admin.py 수정

from django.contrib import admin

from .models import Post

admin.site.register(Post)



-DB 변경 사항 반영

python manage.py makemigrations myapp (어떤한 변경사항이 만들어졌는지에 대해서만 수집)

python manage.py migrate(수집한 내용에 대해서 DB 에 적용하는게 migrate)



### 설정

(mysite > settings.py)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', ## 나중에 oracle, mysql로 변경하여 사용가능
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```



```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp', # 폴더명 추가
]
```

myapp > models.py

```python
from django.utils import timezone
# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    hobby = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.userid} / {self.name} / {self.age}" #테이블로 변환된다.
```

python manage.py makemigrations myapp -> 매번 만들어줄수 없으니까 migration에서 이력관리를 통해 매번 만들지 않는다.



model 등록은 admin.py 에 가서 해야 한다.

```python
from myapp.models import User #myapp폴더에 models.py에서 User Class 를 불러와라
# Register your models here.
admin.site.register(User)   # Register(대문자로 하면 에러 발생)
```

등록이 다 되면 docs 로 나가서 python manage.py makemigrations myapp 이걸 하면 migrations 폴더에 py 파일이 생긴다. 

* makemigrations 는 DB에 저장되는 값이 아니기 때문에 make만 하고 값을 확인하려 하면 error 발생
* migrate 까지 해줘야 한다.



![image-20200217142356624](C:\Users\Student\Desktop\typora\image2\image-20200217142356624.png)

![image-20200217143052723](C:\Users\Student\Desktop\typora\image2\image-20200217143052723.png)

만들고 admin 페이지로 들어가면 DB가 만들어 진것을 확인

![image-20200217142520256](C:\Users\Student\Desktop\typora\image2\image-20200217142520256.png)

+ADD 를 눌러서 값을 넣어준다.

![image-20200217143118778](C:\Users\Student\Desktop\typora\image2\image-20200217143118778.png)

![image-20200217143201379](C:\Users\Student\Desktop\typora\image2\image-20200217143201379.png)

되면 DB내 적용된 값을 확인할 수 있다.



python manage.py shell

![image-20200217143911646](C:\Users\Student\Desktop\typora\image2\image-20200217143911646.png)

파이썬 기본 쉘 커맨드로 django 관련 페키지 같은 것들이 미리 임폴트 되어 있어서  DB 를 관리하기에 편하다.



SQL 과 동일하게 jango가 제공하는 객체기반 핸들링 문법이 있다.

```python
from myapp.models import User 을 해줘야됨
```



![image-20200217144115887](C:\Users\Student\Desktop\typora\image2\image-20200217144115887.png)

User.objects.all()  =  select* from user

문법도 가능

![image-20200217144308305](C:\Users\Student\Desktop\typora\image2\image-20200217144308305.png)

나이만 출력하려면 각 컬럼명을 넣어주면 값을 받을수 있다.

```python
for i in datas: print(i.age)
-----------------------------
50
27
```

### Insert

```python
u = User(userid='lee',name='이순신',age=65, hobby='봉사')
u.save() ## 인설트
```

![image-20200217144834164](C:\Users\Student\Desktop\typora\image2\image-20200217144834164.png)

### update

![image-20200217145028365](C:\Users\Student\Desktop\typora\image2\image-20200217145028365.png)

### delete

![image-20200217145300154](C:\Users\Student\Desktop\typora\image2\image-20200217145300154.png)

### 

## jupyter notebook django 연동

```python
pip install django==2.0
pip install django-extensions
```

```python
#settings.py 에서 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', <--- 추가해준다.
    'myapp',
]
```

```python
python manage.py shell_plus --notebook
```

jupyter notebook 웹페이지가 열리게 된다.



열때 django shell-plus 로 열어줘야 장고 패키지들을 사용할수 있다.

![image-20200217151933027](C:\Users\Student\Desktop\typora\image2\image-20200217151933027.png)

## ![image-20200217152113329](C:\Users\Student\Desktop\typora\image2\image-20200217152113329.png)



## Model Manager

* **Model Manager**
  * .objects
* 데이터베이스 질의 인터페이스를 제공
* 디폴트 Manager로서 모델클래스.objects가 제공된다.
* Model Manager를 통해 해당 모델 클래스의 DB데이터를 추가, 조회, 수정,삭제(CRUD)가 가능하다.



* **QuerySet**
* SQL을 생성해주는 인터페이스
* .objects.all()
* objects.create():
* chaining을 지원
* connection 모듈을 통해 queryset으로 만들어진 실제 sql문을 shell에서 확인
  * .objects.filter(title_icontaions='1').filter(title_endswith='3')



```python
from django.db import connection
ModelCls.objects.all().order_by('-id')[:10]
connection.queries[-1] #가장 마지막에 실행된 커리 값을 반환
```



### filter

```python
from myapp.models import User
q=User.objects.all()
q.filter(age=50) ## q =User dB 데이터, 에서 age가 50인 값 출력
---------------------
q.filter(q.age<50) 이렇게 하면 에러 발생 (NAME)value 값으로 규칙에 어긋남
q.filter(age__gte=50) 이렇게 해줘야 50보다 같거나 큰사람 출력 가능

q.filter(name='임명훈',age__gte=27)
q.filter(name='임명훈').filter(age__gte=27) #chaining 으로 임명훈에서 27을 추가로 필터링
q.filter(name__contains='김') # 문자를 포함하고 있을때 출력
q.filter(name__icontains='김') # ignore 의 약자로 대소문자 구별안할때
```



### filter (And, or 조건 사용)

from django.db.models import Q

.objects.all().filter(Q(조건필드1=조건값1) | Q(조건필드2=조건값2)) # or 조건

```python
q.filter(Q(age__gte=50) | Q(name__contains='임'))
-----------------
[<User: kim / 김유신 / 50>, <User: lim / 임명훈 / 27>]
```



### 정렬

queryset = queryset.order_by('field1') # 지정 필드 오름차순 요청

queryset = queryset.order_by('-field1') # 지정 필드 내림차순 요청 

queryset = queryset.order_by('field2', 'field3') # 1차기준, 2차기준



### insert

create문을 사용하여 필드 생성

new_post = Post.objects.create(author=User.objects.get(id=1), title='title', text='content')



### update

* Model Instance 속성을 변경하고, save 함수를 통해 저장
  * post_instance = Post.objects.get(id=66)
  *  post_instance.title = 'edit title' # title 수정
  *  post_instance.save()

*  QuerySet의 update 함수에 업데이트할 속성값을 지정하여 일괄 수정
  *  queryset = Post.objects.all() queryset.update(title='test title') # 일괄 update 요청



### delete

* Model Instance 속성을 변경하고, save 함수를 통해 저장 
  * post_instance = Post.objects.get(id=66) 
  * post_instance.delete()
*  QuerySet의 delete 함수에 업데이트할 속성값을 지정하여 일괄 삭제
  * queryset = Post.objects.all()
  * queryset.delete() # 일괄 delete 요청



### 데이터 베이스 목록 웹에 출력하여 검색 기능 구현 하기

views.py

```python
from myapp.models import User
def listuser(request):
    q=request.GET.get("q","")

    if q == "":
        data = User.objects.all()
    else:
        data = User.objects.all().filter(name__contains=q)
    return render(request, 'myapp/template2.html', {"data":data})
```

urls.py

```python
path('listuser', views.listuser),
```

admin.py

```python
from django.contrib import admin
from myapp.models import User
# Register your models here.
admin.site.register(User)
```

apps.py

```python
from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'
```

tempaltes > myapp>template.html

```python
user List<br>

{% for i in data %}

    이름 {{i.name}} 나이 {{i.age}} <br>

{% endfor %}

<form action="">
    <input type="text" name="q">
    <input type="submit" value ="검색">

</form>
```

![image-20200217163245694](C:\Users\Student\Desktop\typora\image2\image-20200217163245694.png)

없으면 DB 전체 데이터 불러오고 이름에 들어가는 글자 중 아무거나 치면 출력된다.

![image-20200217163933644](C:\Users\Student\Desktop\typora\image2\image-20200217163933644.png)

![image-20200217163945988](C:\Users\Student\Desktop\typora\image2\image-20200217163945988.png)



### DB 등록 및 출력 페이지로 보여주기

views.py

```python
def listuser(request):
    if request.method == "GET":
        userid = request.GET.get("userid","")
        if userid != "":
            User.objects.all().get(userid=userid).delete()
            redirect("/listuser")

        q=request.GET.get("q","")

        if q == "":
            data = User.objects.all()
            
        else:
            data = User.objects.all().filter(name__contains=q)
        return render(request, 'myapp/template2.html', {"data":data})
    else:
        userid = request.POST.get("userid","")
        name = request.POST.get("name","")
        age = request.POST.get("age","")
        hobby = request.POST.get("hobby","")
        u=User(userid=userid,name=name,age=age,hobby=hobby)
        u.save()
        return redirect("/listuser")
```

template2.html

```python
<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
<!--<script src="http://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
-->

user List<br>

{% for i in data %}

    이름 {{i.name}} 나이 {{i.age}} <a href="listuser?userid={{i.userid}}"> 삭제 </a> <br>

{% endfor %}

<form action="listuser">
    <input type="text" name="q">
    <input type="submit" value ="검색"> <br>

</form>
<button id="btuRun">추가</button>
<div id="layer">
<form action="listuser" method="POST">
    {% csrf_token %}
    아이디<input type="text" name="userid"><br>
    이름 <input type="text" name="name"><br>
    나이 <input type="text" name="age"><br>
    취미 <input type="text" name="hobby"><br>
    <input type="submit" value="Add">
</form>
</div>

<script>
    $("#layer").hide();
    $("#btuRun").click( function(){
        $("#layer").toggle()
    });
</script>
```

![image-20200217173945184](C:\Users\Student\Desktop\typora\image2\image-20200217173945184.png)

추가 버튼 누르면 DB 입력하는 공간이 생김

![image-20200217174015044](C:\Users\Student\Desktop\typora\image2\image-20200217174015044.png)

admin 페이지

![image-20200217174042115](C:\Users\Student\Desktop\typora\image2\image-20200217174042115.png)



