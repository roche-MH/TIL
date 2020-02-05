# 챗봇활용(크롤링 연동)

[https://search.naver.com/search.naver?query=부산광역시날씨](https://search.naver.com/search.naver?query=부산광역시날씨)



**날씨 정보 네이버에서 크롤링하기**

```python
def getWeather(city):
    url = "https://search.naver.com/search.naver?query="
    url = url + urllib.parse.quote_plus(city + '날씨')
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    temp = bs.findAll('span','todaytemp')
    do = bs.findAll('span','blind')
    desc = bs.findAll('p','cast_txt')
    return  {"temp":temp[0].text, "desc":desc[0].text, "city":city}
    #return print(f"현재 {city} 날씨는 {temp[0].text}˚미세먼지는 {desc[0].text}")
```

```python
asd=getWeather("제주")
print(f"현재 {asd['city']} 날씨는 {asd['temp']}˚미세먼지는 {asd['desc']}")
-----------------------------------------------------------------------------------------
현재 제주 날씨는 0˚미세먼지는 흐림, 어제보다 4˚ 낮아요
```

**챗봇과 연동하기**

```PYTHON
def get_answer(text, sessionId):
    data_send = {
        'query': text, 'sessionId': sessionId,
        'lang': 'ko', 'timezone' : 'Asia/Seoul'
    }
    data_header = { ## 헤더에 키와 json 파일 
        'Authorization': 'Bearer d7b1fe5197d24ddaa9cd5198bf2a3a56',
        'Content-Type': 'application/json; charset=utf-8'
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'
    res = requests.post(dialogflow_url, data=json.dumps(data_send), headers=data_header)
    if res.status_code == requests.codes.ok: ## 200일경우에 딕셔너리 형태로 리턴해줌
       return res.json()    
    return {}
```

```python
while True:
    txt = input("User")
    dict = get_answer(txt, 'user01')
    answer = dict['result']['fulfillment']['speech']

    #if dict['result']['metadata']['intentName'] == 'weather' and dict['result']['actionIncomplete'] == False:
    #    date = dict['result']['parameters']['date']
    #    geo_city = dict['result']['parameters']['geo-city']
    #    print("날씨", date, geo_city)
    if dict['result']['metadata']['intentName'] == 'order2':
        price = {'짜장면':5000, '짬뽕':3000, '탕수육':10000}
        params = dict['result']['parameters']['food_number']  ## food_number 는 json에서 안보여도 entitiy 명으로 설정
        print(params)
        output = [ food.get("number-integer",1) * price[food["food1"]] for food in params ]
        print("총 금액은 : ", sum(output))
    elif dict['result']['metadata']['intentName'] == 'weather' and dict['result']['actionIncomplete'] == False:
        date = dict['result']['parameters']['date']
        geo_city = dict['result']['parameters']['geo-city']
        info = getWeather(geo_city)
        print(f"현재 {info['city']} 날씨는 {info['temp']}˚미세먼지는 {info['desc']}")
        
    elif txt=='종료':
        break
    else:
        print('bot' + answer)
        
-----------------------------------------------------------------------------------------
User천안 날씨 알려줘
bot날짜를 알려주세요
User오늘
현재 천안시 날씨는 -5˚미세먼지는 맑음, 어제보다 8˚ 낮아요       
```



***지식 봇 만들기***

```python
word = '김연아'
url = "https://search.naver.com/search.naver?where=kdic&query="
url = url + urllib.parse.quote_plus(word)
bs = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

do = bs.select('p.txt_box')
def getQuery(word):
    url = "https://search.naver.com/search.naver?where=kdic&query="
    url = url + urllib.parse.quote_plus(word)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    do = bs.select('p.txt_box')
    return [i.text for i in do] 

print(getQuery('김연아'))

검색한 내용이 나오고
```

dialog 에서 query 라는 intent를 하나 만들어준다. (질문은 은/는/이/가 정도로 만들어준다.) 엔티티는 any로 만들어준다.

![image-20200205141516111](image/image-20200205141516111.png)

답변도 알맞게 만들어주고 챗봇과 연동되는 코드를 작성

```python
while True:
    txt = input("User")
    dict = get_answer(txt, 'user01')
    answer = dict['result']['fulfillment']['speech']
    intentName = dict['result']['metadata']['intentName']
    
    if intentName == 'query':
        word = dict['result']['parameters']['any']
        print(getQuery(word))
    elif intentName == 'order2':
        price = {'짜장면':5000, '짬뽕':3000, '탕수육':10000}
        params = dict['result']['parameters']['food_number']  ## food_number 는 json에서 안보여도 entitiy 명으로 설정
        print(params)
        output = [ food.get("number-integer",1) * price[food["food1"]] for food in params ]
        print("총 금액은 : ", sum(output))
    elif intentName == 'weather' and dict['result']['actionIncomplete'] == False:
        date = dict['result']['parameters']['date']
        geo_city = dict['result']['parameters']['geo-city']
        info = getWeather(geo_city)
        print(f"현재 {info['city']} 날씨는 {info['temp']}˚미세먼지는 {info['desc']}")
        
    elif txt=='종료':
        break
    else:
        print('bot' + answer)
----------------------------------------------------------------------------------------- 
User안녕
bot안녕!
User쿼리가 뭐야?
쿼리 (query)는 다음을 가리킨다. 질의어: 정보 수집에 대한 요청에 쓰이는 컴퓨터 언어 웹 검색 쿼리 제이쿼리(jQuery)
User날씨는?
bot날짜를 알려주세요
User날씨가 뭐야
‘오늘 날씨가 어떻지?’ 아침에 일어나자마자 창문을 활짝 열고 날씨가 어떤지 살펴본 적은 없나요? 이처럼 날씨는 우리의 일상생활과 밀접하게 관련되어 있어요.날씨는... 
User오늘 날씨가 어떻지?
bot지역을 알려주세요
User서울
현재 서울특별시 날씨는 -5˚미세먼지는 맑음, 어제보다 9˚ 낮아요
User바보는 뭐야?
이 도시는 신(新) 바보로서, 로마 황제 아우구스투스 때에 재건되었다. 바나바와 바울은 1차 선교여행 때 이곳에서 복음 사역을 훼방하는 유대인 마술사 엘루마의 눈을 멀게 했고, 그 기적을 목격한 로마 총독... 
User너는 바보
bot죄송해요. 다시 들려 주실래요?
```



# 구글 TTS 와 챗봇 연동 하기

pip install gtts 로 anaconda 에서 설치해준다.

```python
## 로컬 폴더에 저장
from gtts import gTTS
text = "오늘은 비가오고 내일도 비가오고 모래도 비가 온다고 한다."
tts = gTTS(text=text, lang='ko')
tts.save("output.mp3")
```

```python
import IPython.display as ipd
ipd.display(ipd.Audio('output.mp3', autoplay=True)) #디스플레이를 하면 지워지지않고 유지
```

```python
while True:
    txt = input("User")
    dict = get_answer(txt, 'user01')
    answer = dict['result']['fulfillment']['speech']
    intentName = dict['result']['metadata']['intentName']
    
    if intentName == 'query':
        word = dict['result']['parameters']['any']
        text = getQuery(word)
        tts = gTTS(text=text, lang='ko')
        tts.save("output.mp3")
        ipd.display(ipd.Audio('output.mp3', autoplay=True))
        print(getQuery(word))
    elif intentName == 'order2':
        price = {'짜장면':5000, '짬뽕':3000, '탕수육':10000}
        params = dict['result']['parameters']['food_number']  ## food_number 는 json에서 안보여도 entitiy 명으로 설정
        print(params)
        output = [ food.get("number-integer",1) * price[food["food1"]] for food in params ]
        print("총 금액은 : ", sum(output))
    elif intentName == 'weather' and dict['result']['actionIncomplete'] == False:
        date = dict['result']['parameters']['date']
        geo_city = dict['result']['parameters']['geo-city']
        info = getWeather(geo_city)
        print(f"현재 {info['city']} 날씨는 {info['temp']}˚미세먼지는 {info['desc']}")
        
    elif txt=='종료':
        break
    else:
        print('bot' + answer)
```

![image-20200205145026863](image/image-20200205145026863.png)



# jupyter notebook 에 챗봇 띄우기

```python
from IPython.core.display import HTML
HTML(
"""    
    <iframe
    allow="microphone;"
    width="350"
    height="430"
    src="https://console.dialogflow.com/api-client/demo/embedded/LMH-CHATBOT">
</iframe>"""
)
```

![image-20200205151140723](image/image-20200205151140723.png)



### Fulfillment 개요

dialogflow 에이전트가 의도에 따라 비즈니스 로직을 호출

dialogflow의 자연어 처리로 추출한 정보를 사용하여 동적 응답 생성





# Flask 웹개발

from flask import Flask

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "hello--------dadadasdsadsad"

@app.route('/abc')
def home2():
    return 'test~~~~'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True) #debug 가능하도록 해줌
```

웹 페이지 접속시 hello 를 띄우고

/abc 들어가면 test 를 띄워주게 된다.



기능

```python
@app.route('/s5/<name>')

def s6(name):

​	return "data=" + name
-----------------------------------
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    name = request.args.get("name")
    return "hello--------dadadasdsadsad" + name
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
    
-------------------------------------
http://127.0.0.1:6000/?name=wwwwwwwwwwwwwwwwwwww
    Web : hello--------dadadasdsadsadwwwwwwwwwwwwwwwwwwww   
        
## 2개 넣기
-------------------------------------
@app.route('/')
def home():
    name = request.args.get("name")
    item = request.args.get('item')
    return "hello--------dadadasdsadsad" + name + item
-------------------------------------
http://127.0.0.1:5000/?name=wwwwwwwwwwwwwwwwwwww&item=한글
```



Tip : Secure Tunnels

8시간동안 사설 ip를 공인 ip로 변환시켜 주는 프로그램 https://ngrok.com/download



cmd(ngrok가 있는 폴더로 가서) : ngrok http local포트번호

![image-20200205174437080](image/image-20200205174437080.png)

http://2e472ac2.ngrok.io/dialogflow 로 들어가면 내 로컬과 동일하다.





## dialogflow 와 웹서버 연동

dialogflow 에서 Fulfillment 로 가서 webhook 를 enable 시켜주고 url 에 ngrok 에서 받은 웹 주소를 입력한다. dialogflow 는 https 로만 통신이 가능하다.

![image-20200205174937407](image/image-20200205174937407.png)

intents  -> 특정 인스턴스만 서버에 가서 값을 가져오도록 설정

![image-20200205175105406](image/image-20200205175105406.png)