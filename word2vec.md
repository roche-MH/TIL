# word2vec

```python
sentences = [
                ['this', 'is', 'a',   'good',      'product'],
                ['it',   'is', 'a',   'excellent', 'product'],
                ['it',   'is', 'a',   'bad',       'product'],
                ['that', 'is', 'the', 'worst',     'product']
            ]

# 문장을 이용하여 단어와 벡터를 생성한다.
model = Word2Vec(sentences, size=20, window=3, min_count=1)
(텍스트, 차원크기, window(중심단어 주변단어 개수), 최소한 단어가 1번이상 반복하는것만 인식)

# 단어벡터를 구한다.
word_vectors = model.wv
print(word_vectors)
----------------------------------
<gensim.models.keyedvectors.Word2VecKeyedVectors object at 0x00000215EC5FD208>

# this의 w값
print(word_vectors["this"])
print(word_vectors["the"])
-------------------------------
[ 0.01152619 -0.08421122  0.00649844 -0.07513636  0.06621818]
[ 0.0110632   0.01930176 -0.03931442  0.04428726 -0.03861976]
```

```python
## 단어들 간의 유사도
vocabs = word_vectors.vocab.keys()
print(vocabs)
------------------------------------
dict_keys(['this', 'is', 'a', 'good', 'product', 'it', 'excellent', 'bad', 'that', 'the', 'worst'])

model.similarity(w1='it',w2='this') (it과 this의 유사도)
-------------------------------------
-0.25251895 (유클리안 디스턴스로 두 단어간 cos0(거리) 가 계산된다) (-1~1 1이면 동일)
```

```python
지정한 문자와 가장 가까운 거리의 문자를 추출 
model.wv.most_similar('it', topn=2) (탑n 은 몇개 출력, 안적으면 전체 출력)
-------------------------------
[('excellent', 0.82203209400177), ('a', 0.4252210259437561)]
```

## 언어 시각화

```python
vocab = list(w2v_model.wv.vocab)
X = w2v_model[vocab]
tsne = TSNE(n_components=2) ## 고차원 데이터를 저차원으로 내려서 시각화해준다.
X_tsne = tsne.fit_transform(X[:300,:])# n**2 의 속도를 가지고 있기때문에 많으면 힘들다
```

```python
print(X_tsne.shape)
print(X_tsne)
--------------------------
(300, 2)
[[-3.16323996e+00  6.73234701e+00]
 [ 7.73720264e+00 -4.02564478e+00]
 [ 7.02186346e+00  1.16638098e+01]
 [ 4.47930765e+00 -1.40811510e+01]
 [-1.96423900e+00  1.17269478e+01]
 ...
```

```python
from matplotlib import font_manager, rc
import matplotlib as mpl
import matplotlib.pyplot as plt
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

mpl.rcParams['axes.unicode_minus'] = False

plt.scatter(X_tsne[:,0], X_tsne[:,1], c='red')


words = vocab[:100]    
for i, word in enumerate(words):
    plt.text(X_tsne[i,0], X_tsne[i,1 ], word, fontsize=8) 
plt.savefig('out.png', dpi=200)
```

![image-20200210153027422](C:\Users\Student\Desktop\typora\image\image-20200210153027422.png)

```python
group1 = w2v_model.wv.most_similar(tokens('예쁘다'), topn=30)
group1 = [w for ( w,  s )  in  group1 ]
X1 = w2v_model[group1]

group2 = w2v_model.wv.most_similar(tokens('못생겼다'), topn=30)
group2 = [w for ( w,  s )  in  group2 ]
X2 = w2v_model[group2]

X_tsne =tsne.fit_transform(np.vstack([X1, X2]))

label = np.hstack([0*np.ones(30), np.ones(30)  ])
c = [ 'red'  if l == 0  else 'blue'  for l in label ]


plt.scatter(X_tsne[:,0], X_tsne[:,1], color=c)

## 값을 할때 마다 그래프가 계속 바뀐다.
#2차원으로 값을 줄일때마다 값이 바뀜
# 범인 X_tsne 초기값이 랜덤하게 바뀌기 때문에 fit 값으로 주지 않고
# 시각화 할경우에만 사용한다.
```

![image-20200210161040500](C:\Users\Student\Desktop\typora\image\image-20200210161040500.png)

