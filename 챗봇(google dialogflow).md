# 챗봇(google dialogflow)

### 챗봇 기능(웹 챗봇, 구글 듀플렉스)



greeting message

intent classification(의도분류) & Enti

slot Filing prompt ( 부족한 정보 재질의)

slot Filing Answer(재질의 응답)

API Query (API 질의)

result speaking

[사이트](www.dialogflow.com)  > create new agent > 이름 설정 > default language (ko) > create

상단 위쪽 Try it now 에서 질의 가능

메뉴 intents 에서 default intents 에서 초기 설정 값을 볼수 있다.

데이터양이 없으면 룰 베이스 기반이고 데이터가 많아져야지만 학습후에 인식한다.



## intents 만들기

create intents > training phrases 에서 질의 > Responses 에서 응답

ntt 생성 ( 사용자 정의 ntt , system ntt 두개로 분류)



**system ntt** : sys.date(날짜) , sys.geo-city(지역) 

날짜랑 지역을 바꿔도 구글에서 인식한 곳으로 데이터 인식되어 답변 할수 있다.



#### 응답

질의 값을 가져올때 $parameter-name 으로 적으면 하면 질의 했던 값을 가져온다.

$date $geo-city 날씨는 좋아



**error**

[empty response] 가 발생하면 parameter 를 인식하지 못한것으로 콘솔로 가서 디버깅을 해봐야 한다.

해결 Action and parameters 에서 requred 를 클릭하고 prompts 에서 slot Filing prompt ( 부족한 정보 재질의) 를 설정할수 있다.  (질의시 빠진 부분을 질의하고 값을 저장한다. )

ex ) 날짜를 알려주세요 : 오늘 -> 지역을 알려주세요 : 부산 -> 2020-02-04T12:00:00+09:00 부산광역시 날씨는 좋아 이렇게 나온다.

### 계층구조를 갖는 intents 만들기

시나리오 (3개의 인텐트가 필요하고 각 인텐트가 계층 구조를 가지고 있어야 한다.) 질문과 답변이 1개의 인텐트

U:  메뉴판 주세요

B:  어떤음식을 주문 하실건가요?

​		U: 짜장면 주세요.

​		B: 짜장면 주문 접수 할까요?

​		U:  네 | 맞아요 | 옙 | 넵 | 응 | 어

​		B: 짜장면 주문 접수가 완료되었습니다.



orderfood 인스턴스

![image-20200204133107281](C:\Users\Student\Desktop\typora\image\image-20200204133107281.png)

![image-20200204133135069](C:\Users\Student\Desktop\typora\image\image-20200204133135069.png)

생성하고 intents 에서 add follow-up intent 를 클릭

![image-20200204133240027](C:\Users\Student\Desktop\typora\image\image-20200204133240027.png)

![image-20200204133320276](C:\Users\Student\Desktop\typora\image\image-20200204133320276.png)

orderfood-2 를 클릭해서 주문하는 내용을 넣는다.

![image-20200204133559665](C:\Users\Student\AppData\Roaming\Typora\typora-user-images\image-20200204133559665.png)

****

![image-20200204133804111](C:\Users\Student\Desktop\typora\image\image-20200204133804111.png)

![image-20200204135403941](C:\Users\Student\Desktop\typora\image\image-20200204135403941.png)



yes 부분에 $food 로 처음 오더 변수를 불러오려고 할때 불러올수 없다. 

그럴때는 #orderfood-2-followup  에 있는 food 변수를 가져와서 불러내야 한다.

 ![image-20200204134923830](C:\Users\Student\Desktop\typora\image\image-20200204134923830.png)



음식이 여러번 나올 경우 리스트를 체크 하면 여러개의 값을 여러번 불러올수 있도록 해줌

![image-20200204141711471](C:\Users\Student\Desktop\typora\image\image-20200204141711471.png)

![image-20200204141926407](C:\Users\Student\Desktop\typora\image\image-20200204141926407.png)



**최상단 intents에 action 을 만들어주고 최 하단에서 불어오기**

![image-20200204143018338](C:\Users\Student\Desktop\typora\image\image-20200204143018338.png)



최하단 Contexts 에 추가

![](C:\Users\Student\Desktop\typora\image\image-20200204143527336.png)

text response 에 

#orderfood-2-followup.name 으로 내용추가



**복합 ENTITY**

![image-20200204150944812](C:\Users\Student\AppData\Roaming\Typora\typora-user-images\image-20200204150944812.png)

복합 ENTITY 를 사용하지 않았을 경우에 음식과 수량이 따로따로 노는게 보인다.

그렇기 때문에 Entities 에서 새로 하나 만드는데 

![image-20200204151612613](C:\Users\Student\Desktop\typora\image\image-20200204151612613.png)

define synonyms 는 동음이의어 인데 복합 entitiy를 사용할때는 체크를 풀어준다.

@food:food1 에서 food1 값은 마음대로 지정해도 된다.

다시 order로 넘어와서 entitiy를 빼주고

![image-20200204151835261](C:\Users\Student\Desktop\typora\image\image-20200204151835261.png)

![image-20200204152047207](C:\Users\Student\Desktop\typora\image\image-20200204152047207.png)

food_number 는 json 형태로 파일을 받는다.

![image-20200204152207326](C:\Users\Student\Desktop\typora\image\image-20200204152207326.png)









## Entities

system.ntt 와 사용자.ntt 로 구분 된다.

system.ntt 는 구글에서 등록해 놓은 ntt 로 지역, 날짜 등등 이 있다.

사용자.ntt 는 사용자가 만드는 ntt







## integration (내가 만든 챗봇을 다른 프로그램과 연동)

**web demo** 를 누르면 웹 고유값 주소가 나온다. 수정으로 고유 값을 수정할수 있다. [주소](https://bot.dialogflow.com/LMH-CHATBOT)

모바일 접속 가능

facebook, skype, telegram 등등 연동가능





## Fulfillment

사용자가 요청한것을 서버에서 확인하고 다시 돌려주는것





## Event

대화의 문맥을 따라가는데 있어서 다시 돌아가거나 할때 점프해서 사용







## API 로 사용하기

chatbot 옆 톱니바퀴 눌르면 볼수 있다.

![image-20200204153209165](C:\Users\Student\Desktop\typora\image\image-20200204153209165.png)

``` python
import requests
import json
def get_answer(text, sessionId):
    data_send = {
        'query': text, 'sessionId': sessionId,
        'lang': 'ko', 'timezone' : 'Asia/Seoul'
    }
    data_header = {
        'Authorization': 'Bearer d7b1fe5197d24ddaa9cd5198bf2a3a56',
        'Content-Type': 'application/json; charset=utf-8'
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'
    res = requests.post(dialogflow_url, data=json.dumps(data_send), headers=data_header)
    if res.status_code == requests.codes.ok:
       return res.json()    
    return {}
a=input()
while(a!='종료'):
    dict = get_answer(a,'user01')
    answer = dict['result']['fulfillment']['speech']
    print("Bot:" + answer)
    a=input()
```



```
이모
Bot:주문하시게요?
맞아
Bot:마지막에 말씀을 잘 못 이해 한것 같아요.
이모
Bot:주문하시게요?
메뉴판
Bot:주문하시게요?
메뉴판좀줘
Bot:어떤 음식 주문하실건가요?
짜장면 3개 짬뽕 3개
Bot:짜장면 3, 짬뽕 3 개 확인이요
오케이! 종료
Bot:마지막에 말씀을 잘 못 이해 한것 같아요.
종료
```

api 호출시 조건걸기

*** ***

intentName 이 weather 이고 actionlncomplete 이 False(다 적용되는거) 일때 호출

``` python
dict = get_answer('짜장면 1개 짬뽕 3개 주세요', 'user01')
answer = dict['result']['fulfillment']['speech']

if dict['result']['metadata']['intentName'] == 'weather' and dict['result']['actionIncomplete'] == False:
    date = dict['result']['parameters']['date']
    geo_city = dict['result']['parameters']['geo-city']
    print("날씨", date, geo_city)
else:
    print("bot"+answer)
    
bot짜장면 1, 3 짬뽕 개 확인이요
```



금액 리턴하기

```python
dict = get_answer('짜장면 2개 짬뽕 3개','user01')
params = dict['result']['parameters']
if dict['result']['metadata']['intentName'] == 'order2':
    price = {'짜장면':5000, '짬뽕':3000, '탕수육':10000}
    params = dict['result']['parameters']['food_number']
    output = [ food.get("number-integer",1) * price[food["food1"]] for food in params ]
    print("총 금액은 : ", sum(output))

총 금액은 : 19000.0
```

