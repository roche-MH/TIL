# ajax 비동기식 웹페이지

## ajax 의 장단점

* ajax의 장점
  * 웹페이지의 속도 향상
  * 서버의 처리가 완료 될때 까지 기다리지 않고 처리 가능하다
  * 서버에서 DATA만 전송하면 되므로 전체적인 코딩의 양이 줄어든다.
  * 기존 웹에서는 불가능했던 다양한 UI를 가능하게 해준다. 사진 공유 사이트 Flickr의 경우 사진의 제목이나 태그를 페이지 리로드 없이 수정할수 있다.
* ajax의 단점
  * 히스토리 관리가 안된다. (보안에 좀 더 신경을 써야한다.)
  * 연속으로 데이터를 요청하면 서버 부하가 증가할수 있다.
  * XMLhttpRequest를 통해 통신을 하는 경우사용자에게 아무런 진행 정보가 주어지지 않는다. 그래서 아직 요청이 완료되지 않았는데 사용자가 페이지를 떠나거나 오작동할 우려가 발생하게 된다.



**Jquery와의 시너지**

Ajax하면 Jquery에 대한 설명을 빼놓을 수 없습니다. 일반 Javascript만으로 Ajax를 하게되면 코딩량도 많아지고 브라우저별로 구현방법이 다른 단점이 있는데 jquery를 이용하면 더 적은 코딩량과 동일한 코딩방법으로 대부분의 브라우저에서 같은 동작을 할 수 있게 됩니다. jquery ajax를 사용하면, HTTP Get방식과 HTTP Post방식 모두를 사용하여 원격 서버로부터 데이터를 요청할 수 있습니다. Jquery는 Ajax처럼 JavaScript의 라이브러리 중 하나인데 자바스크립트를 좀 더 사용하기 쉽게 패키징화 시켜놓은 것입니다. Jquery에대한 내용은 추후에 포스팅하겠습니다



urls.py

```pyhton
urlpatterns = [
    path('', views.index),
    path('ajaxdel',views.ajaxdel),
    path('ajaxget',views.ajaxget),
]
```



jquery ajax 연습(serverside) 삭제기능 만들기

```python
def ajaxdel(request):
    pk = request.GET.get("pk") # 특정 게시물 찾고
    board = models.Board.objects.get(pk=pk) #DB내 PK 값을 가진 필드 추출
    board.delete() #DB 에서 내용 삭제

    return JsonResponse({'error':'0'})
```

```python
def ajaxget(request):
    page = request.GET.get("page",1)
    data = models.Board.objects.all().filter(category='common')
    p= Paginator(datas,3) #한페이지에 몇개씩 보여줄꺼냐
    subs = p.page(page)

    datas = {"datas": [{"pk":i.pk,"title":i.title,'cnt':i.cnt} for i in subs] }
    return JsonResponse(datas)
    ## 같은 표현
    #     page = request.GET.get("page",1)
    #data = models.Board.objects.all().filter(category='common')
    # page = int(page)
    # subs = datas[(page-1)*3:(page)*3]
```



#  Json 파일 전달

json 은 딕셔너리 형태로 데이터를 전달해야 되는데 DB에 있는 내용들을 딕셔너리로 만들어 주는 연습이 필요하다.

```python
from myboard import models

datas = models.Board.objects.all().filter(category='common')
print(datas)
--------------------------------
<board: 자동차 검출 43343>,<Board: 3123123>, <Board: 123123>
```

```python
ex) 딕셔너리로 만들어주기
data = []
for i in s:
    print({"s":i.age,"hobby":i.hobby,'name':i.name})
    
datas = {"datas": [{"s":i.age,"hobby":i.hobby,'name':i.name} for i in s] }
```



## Jquery 실습

ADD 클릭시 추가 되도록

```python
<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
<script src="http://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>


<button id="btnadd">ADD</button>


<div id="view">
    <div id="item">
    <a href=list?id=4> <span id=title>제목</span></a>
    조회수<span id=cnt>5</span>
    <br>
    </div>
</div>

<script>
    //$("#view").append("<a href=fefefe>데이터2<br></a>")
    //$("#view").append("<a href=fefefe>데이터2<br></a>")
    item = $("#item").clone()
    $("#title").html("제목1")
    $("#cnt").text("10")
    $("#view").append(item)


    $("#btnadd").click( function() {
        item = $("#item").clone()
        $("#view").append(item)
    });
</script>


```

![image-20200220134823766](C:\Users\Student\Desktop\typora\image2\image-20200220134823766.png)

```python
<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
<script src="http://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>


<button id="btnadd">ADD</button>


<div id="view">
    <div id="item">
    <a href=list?id=4> <span id=title>제목</span></a>
    조회수<span id=cnt>5</span>
    <br>
    </div>
</div>

<script>
    //$("#view").append("<a href=fefefe>데이터2<br></a>")
    //$("#view").append("<a href=fefefe>데이터2<br></a>")
    item = $("#item").clone()
    $("#title",item).html("제목1")// ,item을 안하면 전체 문서중에서 title을 찾아야 되는데 ,item으로 해주면 item안에서만 title를 찾는다.
    $("#cnt",item).text("10") // 복사한 item 안에서 cnt id 를 찾는다
    $("#view").append(item)

    var index =0;

    $("#btnadd").click( function() {
        item = $("#item").clone()
        $("#title",item).html("제목" + index)
        $("#cnt",item).text("10")
        $("#view").append(item)
        index++
    });
</script>


```

![image-20200220135647380](C:\Users\Student\Desktop\typora\image2\image-20200220135647380.png)

초기값 숨기기

```python
<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
<script src="http://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>


<button id="btnadd">ADD</button>


<div id="view">
    <div id="item">
    <a href=list?id=4> <span id=title>제목~!</span></a>
    조회수<span id=cnt>0</span>
    <br>
    </div>
</div>

<script>
    //$("#view").append("<a href=fefefe>데이터2<br></a>")
    //$("#view").append("<a href=fefefe>데이터2<br></a>")

    $("#item").hide() // 처음 디폴트 값을 숨길수 있게 해서 아무것도 없고 추가 누를때 생긴다.

    item = $("#item").clone()
    $("#title",item).html("제목1")// ,item을 안하면 전체 문서중에서 title을 찾아야 되는데 ,item으로 해주면 item안에서만 title를 찾는다.
    $("#cnt",item).text("10") // 복사한 item 안에서 cnt id 를 찾는다
    $("#view").append(item)

    var index =0;

    $("#btnadd").click( function() {
        item = $("#item").clone()
        item.show() // 추가시 item.show() 를 안해주면 hide 파일을 상속받아 추가하는거기 때문에 값이 안보여져서 show()를 해줘야 한다.
        $("#title",item).html("제목" + index)
        $("#cnt",item).text("10")
        $("#view").append(item)
        index++
    });
</script>


```



![image-20200220140108529](C:\Users\Student\Desktop\typora\image2\image-20200220140108529.png)

```python

    $("#btnadd").click( function() {
    
        json = {'datas': [{'s': 50, 'hobby': 'ㅇㅁㅇ', 'name': '김유신'},{'s': 29, 'hobby': '피겨스케이팅', 'name': '김연아'},{'s': 30, 'hobby': 'MC', 'name': '김제동'}]}

        console.log(json.datas[0].name);
        console.log(json.datas[1].name);


        item = $("#item").clone()
        item.show() // 추가시 item.show() 를 안해주면 hide 파일을 상속받아 추가하는거기 때문에 값이 안보여져서 show()를 해줘야 한다.
        $("#title",item).html("제목" + index)
        $("#cnt",item).text("1");
        $("#view").append(item);
        index++;
    });
```

![image-20200220142458185](C:\Users\Student\Desktop\typora\image2\image-20200220142458185.png)

```python
   $("#btnadd").click( function() {
    
        json = {'datas': [{'s': 50, 'hobby': 'ㅇㅁㅇ', 'name': '김유신'},{'s': 29, 'hobby': '피겨스케이팅', 'name': '김연아'},{'s': 30, 'hobby': 'MC', 'name': '김제동'}]}
        for (i=0; i< json.datas.length; i++){
            //console.log(json.datas[i].name);
            item = $("#item").clone()
            item.show() // 추가시 item.show() 를 안해주면 hide 파일을 상속받아 추가하는거기 때문에 값이 안보여져서 show()를 해줘야 한다.
            $("#title",item).html(json.datas[i].name + "뉴스")
            $("#cnt",item).text(json.datas[i].s);
            $("#view").append(item);

        }
    });
</script>
```

![image-20200220143102258](C:\Users\Student\Desktop\typora\image2\image-20200220143102258.png)

page 별로 값 넘기기

## JQuery 프로그램

![img](C:\Users\Student\Desktop\typora\image2\i7-mGjAbfTiMBIiSv2CEWeYVP24RIECmQowkAFK_x5-ZUaAgh96lEpCxdSOky0R6hB1Og71N7Ss2W4fnb1jjAheuZB1tLGSVUBffhP2X71mfP8wcXCcVA5HP-QfWB651Lp9anpupNUPRAkpdxg)

