# NLP_Basic

## 초기세팅

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from tensorflow.keras.datasets import imdb ## 자연어 처리를 위한 DB
from konlpy.tag import Twitter #한글 언어 패키지
from konlpy.tag import Okt
from konlpy.tag import Kkma 
from konlpy.tag import Twitter
from pprint import pprint
import nltk ## 영어, 일반적인 언어 패키지
from nltk.classify.scikitlearn import SklearnClassifier
from wordcloud import WordCloud, STOPWORDS 
from gensim import corpora, models #일반적인 자언어 패키지
import numpy  as np
from PIL import Image
from wordcloud import ImageColorGenerator
import glob
import re
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
%matplotlib inline
```

```bash
pip install gensim #문제없이 설치 가능   (단어를 벡터로 할때)
pip install konlpy # 윈도우에서 설치시 의존성 문제 발생할수 있음 (한국어 형태소)
pip install wordcloud # 윈도우에서 설치시 의존성 문제 발생할수 있음 (단어 시각화)
pip install jpype1 (리눅스에서) #konlpy 의 의존적인 라이브러리
conda install -c conda-forge jpype1(윈도우)
------------------------- 문제 없이 설치됨
pip 설치시 permission 에러 발생하면 뒤에--user 적어주면됨
```



각각의 캐릭터의 분포도를 구해서 특정 코드의 빈도수를 계산한다.

```python
x_train[0] # 0~54620 값들이 있다  # ko_str
print(np.where(x_train[0] >0)) ## np.where 을 사용하여 0 삭제, 이값들은 인덱스 값들이다.
index = np.where(x_train[0] >0)
data = x_train[0]
print(data[[32,46,44163]])
print(data[index]) ## for 문을 사용하지 않고 슬라이싱을 통해서 값 호출
```

```python
#X = np.array([[-1, -1], [3, 2]])
#Y = np.array([1,  2])

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
Y = np.array(['r','r','r','b','b','b'])


color = [ 'red' if y == 'r' else 'blue' for y in Y]

plt.scatter(X[:, 0], X[:, 1], color=color)

t = np.array([[-0.8, -1]])

plt.scatter(t[:,0], t[:,1], color='yellow')
```

![image-20200207110950942](image/image-20200207110950942.png)

```python
# 학습하기 --- (*6)
clf = GaussianNB() 
clf.fit(x_train, y_train)
y_pred = clf.predict([count_codePoint('안녕')])
print(y_pred)
------------------
['ko']
```

```python
# 평가 전용 데이터 준비하기
ko_test_str = '안녕 어디야' ##### ㅁㅇㅁㄴ자음으로 만 적으면 일본어로 인식하는 단점이있다
ja_test_str = 'こんにちは'
en_test_str = 'Hello'
x_test = [count_codePoint(en_test_str),count_codePoint(ja_test_str),count_codePoint(ko_test_str)]
y_test = ['en', 'ja', 'ko']

# 평가하기 --- (*7)
y_pred = clf.predict(x_test)
print(y_pred)
print("정답률 = " , accuracy_score(y_test, y_pred))
```



다량의 데이터로 학습시켜 보기

```python
# 학습 데이터 준비하기 --- (*1)
x_train = []
y_train = []
for file in glob.glob('./language/train/*.txt'):
    # 언어 정보를 추출하고 레이블로 지정하기 --- (*2)
    print(file)
    y_train.append(file[17:19]) ## [17:19] 이거는 파일 이름이 ko,es,en 등으로 되어있어서 파일이름을 슬라이싱 하는 것이다.
    
    # 파일 내부의 문자열을 모두 추출한 뒤 빈도 배열로 변환한 뒤 입력 데이터로 사용하기 --- (*3)
    file_str = ''
    for line in open(file, 'r', encoding='UTF8'):
        file_str = file_str + line
    x_train.append(count_codePoint(file_str))
```

```python
# 학습하기
clf = GaussianNB() 
clf.fit(x_train, y_train)
```

```python
# 출력
y_pred = clf.predict([count_codePoint('Großkatzen')])
print(y_pred)
-------------------------
['de']
```



## 단어 빈도수 기반 자연어 처리

```python
corpus = [ 'you know i want your love',
         'i like you',
         'what should i do',
         'what']
stn = " ".join(corpus)
stn = stn.split(' ')
print(stn)

freq = {}
for i in stn:
    freq[i] = freq.get(i,0)+1
    
print(freq)
-------------------------------------
['you', 'know', 'i', 'want', 'your', 'love', 'i', 'like', 'you', 'what', 'should', 'i', 'do', 'what', 'should', 'should', 'what']
{'you': 2, 'know': 1, 'i': 3, 'want': 1, 'your': 1, 'love': 1, 'like': 1, 'what': 3, 'should': 3, 'do': 1}
```

```py
vector = CountVectorizer() 
tf = vector.fit_transform(corpus) ## 원핫인코딩을 해주는 함수
print(tf)
print(tf.toarray()) ## 단어수에 따라 1를 표현하는데 단어길이가 1개인경우 0으로처리
					## 값은 vocabulary_ 인덱스로 확인
-----------------------------------------------------
  (0, 7)	1
  (0, 1)	1
  (0, 5)	1
  (0, 8)	1
  (0, 3)	1
  (1, 7)	1
  (1, 2)	1
  (2, 6)	1
  (2, 4)	1
  (2, 0)	1
  (3, 6)	1
  (3, 4)	1
  (4, 6)	1
  (4, 4)	1
[[0 1 0 1 0 1 0 1 1]
 [0 0 1 0 0 0 0 1 0]
 [1 0 0 0 1 0 1 0 0]
 [0 0 0 0 1 0 1 0 0]
 [0 0 0 0 1 0 1 0 0]]
```

```python
print(vector.vocabulary_) # 각 단어의 인덱스가 어떻게 부여되었는지 보여준다.
{'you': 7, 'know': 1, 'want': 5, 'your': 8, 'love': 3, 'like': 2, 'what': 6, 'should': 4, 'do': 0}

```

단어를 벡터화 시키면 유사도의 거리와 분포를 구할수 있다.

```python
words = vector.get_feature_names() # 순서대로 정렬되어있음
for word in words: print(word)

print('===============')    
for key in vector.vocabulary_: # 순서는 랜덤으로 지정되어있다.
    print(key)
    
do
know
like
love
should
want
what
you
your
===============
you
know
want
your
love
like
what
should
do    
```



* TF-IDF
    * TF: 현재 문서에서 단어 A가 나타난 횟수(단어빈도수)  
    * DF: 단어가 나타난 문서의 수( 다른 문서에서 언급횟수)
    * 특정 단어의 상대적인 빈도를 나타내주는 값
    * 값이 클 수록 내 문서에만 많이 언급되는 단어(=다른 문서에서는 잘 언급 안됨)
    * 값이 작을수록 다른 문서에 잘 언급하는 단어를 의미(=현재 문서와 관련없음)
    

 IDF 는 특정 문서에서 언급이 높을 경우에 높다. (DF 와 반비례)

![image-20200207141701538](image/image-20200207141701538.png)



## konlpy

# https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype
#에러 발생시 위 사이트 에 들어가서 jpype1-0.7.1-cp37 다운
#jpype1 uninstall 한다음
#pip install --upgrade pip
#pip install JPype1‑0.7.0‑cp35‑cp35m‑win_amd64.whl
#pip install jpype1-0.7..파일
#pip install konlpy
#시스템 환경설에서 변수 설정에 JAVA_HOME 추가해주어야 한다.



```python
okt = Okt()
malist = okt.pos("아버지 가방에 들어가신다.", norm=True, stem=True) 
print(malist)
----------------------------------------------------------------
[('아버지', 'Noun'), ('가방', 'Noun'), ('에', 'Josa'), ('들어가다', 'Verb'), ('.', 'Punctuation')]
```



```python
print(okt.nouns(u'을지로 3가역 주변 첨단빌딩숲 사이에 자리 잡은 커피집')) ## 명사만 추출
print(okt.nouns('짜장면 2개 짬뽕 3개 탕수육 한개 주세요'))
print(okt.pos('짜장면 2개 짬뽕 3개 탕수육 한개 주세요'))
print(okt.pos(u'이것도 되나요 ㅋㅋ'))
print(okt.pos(u'이것도 되나요 ㅋㅋ', norm=True,stem=True))
--------------------------------------------------------------------
['을지로', '역', '주변', '첨단', '빌딩', '숲', '사이', '자리', '커피집']
['짜장면', '개', '짬뽕', '개', '탕수육']
[('짜장면', 'Noun'), ('2', 'Number'), ('개', 'Noun'), ('짬뽕', 'Noun'), ('3', 'Number'), ('개', 'Noun'), ('탕수육', 'Noun'), ('한개', 'Modifier'), ('주세요', 'Verb')]
[('이', 'Determiner'), ('것', 'Noun'), ('도', 'Josa'), ('되나요', 'Verb'), ('ㅋㅋ', 'KoreanParticle')]
[('이', 'Determiner'), ('것', 'Noun'), ('도', 'Josa'), ('되다', 'Verb'), ('ㅋㅋ', 'KoreanParticle')]
```

```python
kkma = Kkma()
#문장분리
print('kkma 문장분리 : ', kkma.sentences('안녕하세요. 반갑습니다. 저는 인공지능 입니다.'))
#명사 추출
print('kkma 명사만 추출 : ', kkma.nouns('안녕하세요. 반갑습니다. 저는 인공지능 입니다.'))
-------------------------------------------------------------
kkma 문장분리 :  ['안녕하세요.', '반갑습니다.', '저는 인공지능 입니다.']
kkma 명사만 추출 :  ['안녕', '저', '인공', '인공지능', '지능']
```

```python
print('kkma 문장분리 : ', kkma.nouns('짜장면 2개 짬뽕 3개 탕수육 한개 주세요'))
print('okt 명사만 추출 : ', okt.nouns('짜장면 2개 짬뽕 3개 탕수육 한개 주세요'))
------------------------------------------------------------------------
kkma 문장분리 :  ['짜장면', '2', '2개', '개', '짬뽕', '3', '3개', '개', '탕수육']
okt 명사만 추출 :  ['짜장면', '개', '짬뽕', '개', '탕수육']
```

Okt 형태소 분석기

okt=okt()

-  객체생성

okt.morphs()

* 텍스트를 형태소 단위로 나눈다. 옵션은 norm과 stem이 있다.
* norm은 normalize의 약자로 문장을 정규화 하는 역할
* stem은 각 단어에서 어간을 추출하는 기능

okt.nouns()

* 텍스트에서 명사만 뽑아낸다.

okt.phrases()

* 텍스트에서 어절을 뽑아낸다.

okt.pos()

* 각 품사를 태깅하는 역할
* 품사를 태깅한다는 것은 주어진 텍스트를 형태소 단위로 나누고, 나눠진 각 형태소를 그에 해당하는 품사와 함께 리스트화 하는 것을 의미한다.

# RNN

word embedding

- 빈도수 기반 표현은 단어간 의미차를 표현할 수 없음
- 단어 자체 의미 자체를 다차원 공간에서 벡터화 필요
  - 단어들 사이의 유사도  측정가능
  - 단어들 간의 평균, 및 연산을 통해 추론 가능

continuous bag of words

​	주변에 있는 단어들을 가지고, 중간에 있는 단어들을 예측하는 방법

​	the fat cat sat on the mat

​	{"the","fat","cat","on","the","mat"}으로부터 context sat 을 예측

윈도우 슬라이딩을 통해 데이터 셋 생성

![image-20200210114402938](image/image-20200210114402938.png)

![image-20200210114439741](image/image-20200210114439741.png)

컬럼벡터로 인풋이 들어가기 때문에 디멘젼이 열이 아닌 행이라고 생각하면 된다.



![image-20200210132502070](image/image-20200210132502070.png)

![image-20200210132650838](image/image-20200210132650838.png)

projection(mapping)













## wordcloud

```python
pip install wordcloud
text = "coffee phone phone phone phone phone phone phone phone phone cat dog dog"
wordcloud = WordCloud(max_font_size=100).generate(text)
fig = plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
```

![image-20200210112935182](image/image-20200210112935182.png)



# 네이버 영화 후기 분석

```python
#파일 읽기 함수. 첫줄 헤더를 제외하고 한 줄씩 읽어서 data 에 담아서 리턴 한다.
def read_data(filename):
    with open(filename, encoding='utf-8', mode='r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]   # header 제외
    return data

ratings_train = read_data('ratings_train.txt')
print(ratings_train[0])
------------------------------------------------
['9976970', '아 더빙.. 진짜 짜증나네요 목소리', '0'] [id, text, 감정분석 0or1 로 구성되있는 데이터]
```

```python
okt = Okt()

def tokens(doc):
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]
```

```python
tokens('아 더빙.. 진짜 짜증나네요 목소리')
--------------------------------------
['아/Exclamation',
 '더빙/Noun',
 '../Punctuation',
 '진짜/Noun',
 '짜증나다/Adjective',
 '목소리/Noun']
```

```python
#파일중에서 영화 리뷰 데이터만 담기
docs = []
for row in ratings_train:
    docs.append(row[1])
print(docs[:10])
-------------------------------------
['아 더빙.. 진짜 짜증나네요 목소리', '흠...포스터보고 초딩영화줄....오버연기조차 가볍지 않구나', '너무재밓었다그래서보는것을추천한다', '교도소 이야기구먼 ..솔직히 재미는 없다..평점 조정', '사이몬페그의 익살스런 연기가 돋보였던 영화!스파이더맨에서 늙어보이기만 했던 커스틴 던스트가 너무나도 이뻐보였다', '막 걸음마 뗀 3세부터 초등학교 1학년생인 8살용영화.ㅋㅋㅋ...별반개도 아까움.', '원작의 긴장감을 제대로 살려내지못했다.', '별 반개도 아깝다 욕나온다 이응경 길용우 연기생활이몇년인지..정말 발로해도 그것보단 낫겟다 납치.감금만반복반복..이드라마는 가족도없다 연기못하는사람만모엿네', '액션이 없는데도 재미 있는 몇안되는 영화', '왜케 평점이 낮은건데? 꽤 볼만한데.. 헐리우드식 화려함에만 너무 길들여져 있나?']
```

```python
data = [tokens(d) for d in  docs]
print(data[:10])
-----------------------------------
[['아/Exclamation', '더빙/Noun', '../Punctuation', '진짜/Noun', '짜증나다/Adjective', '목소리/Noun'], ['흠/Noun', '.../Punctuation', '포스터/Noun', '보고/Noun', '초딩/Noun', '영화/Noun', '줄/Noun', '..../Punctuation', '오버/Noun', '연기/Noun', '조차/Josa', '가볍다/Adjective', '않다/Verb'], ['너/Modifier', '무재/Noun', '밓었/Noun', '다그/Noun', '래서/Noun', '보다/Verb', '추천/Noun', '한/Josa', '다/Adverb'], ['교도소/Noun', '이야기/Noun', '구먼/Noun', '../Punctuation', '솔직하다/Adjective', '재미/Noun', '는/Josa', '없다/Adjective', '../Punctuation', '평점/Noun', '조정/Nou...
```

```python
w2v_model = word2vec.Word2Vec(data,size =100, window=3, min_count=2)
w2v_model.save('naver.model')
```

```python
vocabs = w2v_model.wv.vocab.keys()
print(vocabs)
-----------------------------------
/Josa', '가볍다/Adjective', '않다/Verb', '너/Modifier', '무재/Noun', '다그/Noun', '래서/Noun', '보다/Verb',...
```

```python
print(w2v_model.wv.most_similar(positive=tokens('남자 여배우'), negative=tokens('배우'), topn=1)) #
-----------------------------------------------------------
[('여자/Noun', 0.8314921855926514)]# 남자 여배우 - 배우 = 여자, 남자 - 배우 = 여자 - 여배우
```

```python
print(w2v_model.wv.most_similar(positive=tokens('정우성'),topn=1))
print(w2v_model.wv.most_similar(positive=tokens('짜증나'),topn=3))
-----------------------------------------------------------
[('김혜수/Noun', 0.9234626889228821)]
[('답답하다/Adjective', 0.7830038070678711), ('어이없다/Adjective', 0.7476608753204346), ('오글거리다/Verb', 0.7256500720977783)]
```

