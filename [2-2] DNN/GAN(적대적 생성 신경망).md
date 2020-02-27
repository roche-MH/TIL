# GAN(적대적 생성 신경망)

**생성자 네트워크** : 랜덤 벡터(잠재 공간의 무작위한 포인트)를 입력으로 받아 이를 합성된 이미지로 디코딩한다.

**판별자 네트워크**: 이미지(실제 또는 합성 이미지)를 입력으로 받아 훈련 세트에서 온 이미지인지, 생성자 네트워크가 만든 이미지인지 판별



* 생성자 네트워크는 판별자 네트워크를 속이도록 훈련한다.
* 실제 이미지와 구분할수 없는 인공적인 이미지를 만들어 판별자 네트워크가 두 이미지를 동일하게 보도록 만든다.
* 판별자 네트워크는 생성된 이미지가 실제인지 판별하는 기준을 설정하면서 생성자의 능력 향상에 적응해 간다.
* 훈련이 끝나면 생성자는 입력 공간에 있는 어떤 포인트를 그럴듯한 이미지로 변환한다.
* VAE와 달리 잠재 공간은 의미 있는 구조를 보장하지 않는다.

![gan](https://pathmind.com/images/wiki/gan_schema.png)

[단점]

* GAN은 최적화의 최솟값이 고정되지 않은 시스템이다.
* 보통 경사 하강법은 고정된 손실 공간에서 언덕을 내려오는 방법인데 GAN에서 언덕을 내려오는 매 단계가 조금씩 전체 공간을 바꾼다.
* 최적화 광정이 최솟값을 찾는 것이 아니라 두 힘 간의 평형점을 찾는 다이나믹 시스템이다.
* GAN은 훈련하기가 어렵고 GAN을 만들기위해서는 모델 구조와 훈련 파라미터를 주의 깊게 많이 조정해야 한다.



## GAN(DCGAN) 구현 방법

CIFAR10 데이터 셋 사용

1. generator 네트워크(생성자)는 (latent_dim,) 크기의 벡터를 (32,32,3) 크기의 이미지로 매핑한다.
2. discriminator 네트워크는 (32,32,3) 크기의 이미지가 진짜일 확률을 추정하여 이진 값으로 매핑한다.
3. 생성자와 판별자를 연결하는 GAN 네트워크를 만든다. gan(x) = discriminator(generator(x)) 이다., 이 gan네트워크는 잠재 공간의 벡터를 판별자의 평가로 매핑한다.
4. 즉 판별자는 생성자가 잠재 공간의 벡터를 디코딩한 것이 얼마나 현실적인지 평가한다.
5. "진짜"/"가짜" 레이블과 함께 진짜 이미지와 가짜 이미지 샘플을 사용하여 판별자를 훈련한다. 일반적인 이미지 분류 모델을 훈련하는 것과 동일하다.
6. 생성자를 훈련하려면 gan 모델의 손실에 대한 생성자 가중치의 그래디언트를 사용한다. 이 말은 매 단계마다 생성자에 의해 디코딩된 이미지를 판별자가 "진짜"로 분류하도록 만드는 방향으로 생성자의 가중치를 이동한다는 뜻이다. 다른 말로 하면 판별자를 속이도록 생성자를 훈련한다.



## 훈련방법

* 생성자의 마지막 활성화로 다른 종류의 모델에서 널리 사용하는 sigmoid 대신 tanh함수를 사용한다.
* 균등 분포가 아니고 정규 분포(가우시안 분포)를 사용하여 잠재 공간ㅇ네서 포인트를 샘플링한다.
* 무작위성은 모델을 견고하게 만든다. GAN훈련은 동적 평형을 만들기 때문에 여러 방식으로 갇힐 가능성이 높습니다. 훈련하는 동안 무작위성을 주입하는 ;이를 방지하는데 도움이 됩니다. 무작위성은 두가지 방법으로 주입합니다. 판별자에 드롭아웃을 사용하거나 판별자를 위해 레이블에 랜덤 노이즈를 추가합니다.
* 희소한 그래디언트는 GAN 훈련을 방해할수 있습니다. 딥러닝에서 희소는 종종 바람직한 현상이지만 GAN에서는 그렇지 않습니다. 그래디언트를 희소하게 만들수 있는 것은 최대풀링 연산과 ReLU 활성화 두가징 입니다. 최대 풀링 대신 스트라이드 합성곱을 사용하여 다운 샘플링을 하는 것이 좋습니다. 또 ReLU활성화 대신 LeakyReLU층을 사용한다. RELU와 비슷하지만 음수의 활성화 값을 조급 허용학디 때문에 희소가 조금 완화된다.



## 생성자 네트워크 

먼저 벡터(훈련하는 동안 잠재 공간에서 무작위로 샘플링 된다)를 이미지로 변환하는 generator 모델을 만든다. GAN에서 발생하는 많은문제중 하나는 생성자가 노이즈 같은 이미지를 생성하는 데서 멈추는 것이다. 판별자와 생성자 양쪽에 모두 드롭아웃을 사용하는 것이 해결 방법이 될수 있다.

```python
import keras
from keras import layers
import numpy as np

latent_dim = 32
height=32
width = 32
channels = 3

generator_input = keras.Input(shape=(latent_dim,))

#### 입력을 16 * 16 크기의 채널 128개를 가진 특성 맵으로 변환한다.
x=layers.Dense(128* 16* 16)(generator_input)
x=layers.LeakyReLU()(x)
x=layers.Reshape((16,16,128))(x)

x=layers.Conv2D(256,5,padding='same')(x)
x=layers.LeakyReLU()(x)

x = layers.Conv2DTranspose(256,4,strides=2, padding='same')(x)
x=layers.LeakyReLU()(x)

x=layers.conv2D(256,5,padding='same')(x)
x=layers.LeakyReLU()(x)
x=layers.Conv2D(256,5,padding='same')(x)
x=layers.LeakyReLU()(x)

### 32 * 32 크기 (CIFAR10 이미지 크기)의 1개 채널을 가진 특성 맵을 생성한다.
x = layers.Conv2D(channels, 7, activation='tanh', padding='same')(x)
generator = keras.models.Model(generator_input, x)
generator.summary()
```



## 판별자

후보 이미지(진짜 또는 가짜) 를 입력으로 받고 2개의 클래스로 분류하는 discriminator 모델을 만든다.

```python
discriminator_input = layers.Input(shape=(height,width, channels))
x= layers.Conv2D(128,3)(discriminator_input)
x= layers.LeakyReLu()(x)
x=layers.Conv2D(128, 4, strides=2)(x)
x= layers.LeakyReLu()(x)
x=layers.Conv2D(128, 4, strides=2)(x)
x= layers.LeakyReLu()(x)
x=layers.Conv2D(128, 4, strides=2)(x)
x= layers.LeakyReLu()(x)
x= layers.Flatten()(x)

x= layers.Dropout(0.4)(x)
x= layers.Dense(1, activation='sigmoid')(x)
discriminator = keras.models.Model(discriminator_input,x)
discriminator.summary()
```





## 적대적 네트워크

생성자와 판별자를 연결하여 GAN을 설정한다. 훈련할 때 생성자가 판별자를 속이는 능력이 커지도록 학습한다. 이 모델은 잠재 공간의 포인트를"진짜" 또는 "가짜"의 분류결정으로 변환합니다. 훈련에 사용되는 타깃 레이블은 항상 "진짜 이미지" 이다. gan을 훈련하는 것은 discriminator가 가짜 이미지를 보았을때 진짜라고 예측하도록 하기 위해 generator의 가중치를 업데이트 하는 것이다. 훈련하는 동안 판별자를 동결(학습하지 않도록) 하는 것이 아주 중요하다. gan을 훈련할 때 가중치가 업데이트 되지 않는다. **판별자의 가중치가 훈련하는 동안 업데이트되면 판별자는 항상"진짜"를 예측하도록 훈련된다. 이렇게 되면 안됨!**



```python
discriminator.trainable = False ## 판별자의 가중치가 훈련되지 않도록 설정한다(gan 모델에만 적용된다.)

gan_input = keras.input(shape=(latent_dim,)
gan_output = discriminator(generator(gan_input))
gan = keras.models.Model(gan_input, gan_output)
                       
gan_optimizer = keras.optimizers.RMSprop(lr=0.0004, clipvalue=1.0, decay = 1e-8)
gan.compile(optimizer=gan_optimizer, loss='binary_crossenrtropy')
```



## DCGAN 훈련 방법

매 반복마다 다음을 수행

1)	잠재 공간에서 무작위로 포인트를 뽀는다(랜덤 노이즈)

2)	이 랜덤 노이즈를 사용하여 generator에서 이미지를 생성한다.

3) 	생성된 이미지와 진짜 이미지를 섞는다.

4) 	진짜와 가짜가 섞인 이미지와 이에 대응하는 타깃을 사용하여 discriminator를 훈련한다. 타깃은 "진짜(실제 이미지일 경우)" 또는 "가짜(생성된 이미지일 경우)"이다.

5)	잠재 공간에서 무작위로 새로운 포인트를 뽑습니다.

6)	이 랜덤 벡터를 사용하여 gan을 훈련한다. 모든 타깃은 "진짜"로 설정한다. 판별자가 생성된 이미지를 모두 "진짜 이미지"라고 예측하도록 생성자의 가중치를 업데이트 한다. (gan안에서 판별자는 동결되기 때문에 생성자만 업데이트 한다.)

결국 생성자는 판별자를 속이도록 훈련한다.

**구현**

```python
import os
from keras.preprocessing import image

(x_train, y_train), (_,_) = keras.datasets.cifar10.load_data()

x_train = x_train[y_train.flatten() = =6] # 개구리 이미지 선택

x_train = x_train.reshape(
	(x_train.shape[0],) + (height, width, channels)).astype('float32') / 255. # 데이터 정규화

iterations = 10000
batch_size = 20
save_dir = './datasets/gan_images/' ## 생성된 이미지를 저장할 위치를 지정
if not os.path.exists(save_dir)
	os.mkdir(save_dir)
    
start =0
for step in range(iterations):
    random_latent_vectors = np.random.normal(size=(batch_size, latent_dim)) ### 잠재공간에서 무작위로 포인트를 샘플링 한다.
    generated_images = generator.predict(random_latent_vectors) # 가짜 이미지를 디코딩한다.
    stop = start + batch_size
    real_images = x_train[start: stop]
    combined_images = np.concatenate([generated_images, real_images])
    labels = np.concatenate([np.ones((batch_size, 1)), np.zeros((batch_size, 1))])
    labels += 0.05 * np.random.rnadom(labels.shape) #레이블에 랜덤 노이즈를 추가한다. 중요!
    d_loss = discriminator.train_on_batch(combined_images, labels) #discriminator 를 훈련
    random_latent_vectors = np.random.normal(size=(batch_size, latent_dim))
    
    misleading_targets = np.zers((batch_size, 1)) ## 모두 "진짜 이미지" 라고 레이블을 만든다(사실 거짓)
    a_loss = gan.train_on_batch(random_latent_vectors, misleading_targets) # generator를 훈련(gan모델에서 discriminator의 가중치는 동결)
    
    start += batch_size
    if start > len(x_train) - batch_size:
        start =0
    if step % 100 == 0 : #중간중간 저장하고 그래프를 그린다.
        gan.save_weights('gan.h5') #모델 가중치 저장
        
        print('판별자 손실:', d_loss)
        print('적대적 손실:', a_loss)

        img = image.array_to_img(generated_images[0] * 255., scale=False)
        img.save(os.path.join(save_dir, 'generated_forg' + str(step) + '.png')) # 생성된 이미지 하나 저장
        img = image.array_to_img(real_images[0] * 255., scale=False)
        img.save(os.path.join(save_dir, 'real_forg' + str(step) + '.png')) # 비교를 위해 진짜 이미지 하나 저장

```



## TIP

훈련할때 적대적 손실이 크게 증가하는 것을 볼지도 모른다. 반면에 판별자의 손실은 0으로 향한다. 결국 판별자가 생성자를 압도할수 있다. 이런 경우 판별자의 학습률을 낮추고 판별자의 드롭아웃 비율을 높여서 시도해보자

