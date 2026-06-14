# 5주차 회고록

## 설명

### Dataset
#### 과제 1~4
- 데이터  

#### 과제 5
- 말뭉치 데이터(korean_chatbot_data: 챗봇 트레이닝용 문답 페어)
- 출처: Korpora: Korean Corpora Archives[https://github.com/ko-nlp/Korpora]
  - 오픈소스 파이썬 패키지

### 모델 설계
과제1: Resnet50 전이 모델
- 깊은 층을 가진 Resnet50은 기본적으로 학습시간이 길다. 그래서 학습시간을 감소시키기위해 아래와 같이 구성했다.
- (layer1~layer4는) 각각 연속적인 층조합을 가진 복합층이다.
~~~
        < 원본 구성(models.resnet50) >          ->            < MyResNet50 >        
------------------------------------------------------------------------------------------------    
[0] conv1                                             [0] conv1  
[1] bn1                                               [1] bn1   
[2] relu                                              [2] relu   
[3] maxpool                                           [3] maxpool  
[4] layer1                                            [4] layer1  
[5] layer2                                            [5] layer2  
[6] layer3                                            [6] layer3  
[7] layer4                                            [7] avgpool    
[8] avgpool                                           [8] fc1(1024->512)
[9] fc(2048->1000)                                    [9] fc2(512->256)
                                                      [10]fc3(256->num_class)                                                                  
~~~

과제2: VGG16 전이 모델
- 깊은 층을 가진 Resnet50은 기본적으로 학습시간이 길다. 그래서 학습시간을 감소시키기위해 아래와 같이 구성했다.
~~~
        < 원본 구성(models.vgg16) >                ->          < MyVGG16 >
----------------------------------------------------------------------------------------------------
features:                                             features:
[0]  Conv2d(3→64)                                     [0]  Conv2d(3→64)
[1]  ReLU                                             [1]  ReLU
[2]  Conv2d(64→64)                                    [2]  Conv2d(64→64)
[3]  ReLU                                             [3]  ReLU
[4]  MaxPool2d                                        [4]  MaxPool2d
[5]  Conv2d(64→128)                                   [5]  Conv2d(64→128)
[6]  ReLU                                             [6]  ReLU
[7]  Conv2d(128→128)                                  [7]  Conv2d(128→128)
[8]  ReLU                                             [8]  ReLU
[9]  MaxPool2d                                        [9]  MaxPool2d
[10] Conv2d(128→256)                                  [10] Conv2d(128→256)
[11] ReLU                                             [11] ReLU
[12] Conv2d(256→256)                                  [12] Conv2d(256→256)
[13] ReLU                                             [13] ReLU
[14] Conv2d(256→256)                                  [14] Conv2d(256→256)
[15] ReLU                                             [15] ReLU
[16] MaxPool2d                                        [16] MaxPool2d
[17] Conv2d(256→512)                                  [17] Conv2d(256→256)  ┐
[18] ReLU                                             [18] ReLU             │ self.feature
[19] Conv2d(512→512)                                  [19] MaxPool2d        │
[20] ReLU                                             [20] Conv2d(256→256)  │
[21] Conv2d(512→512)                                  [21] ReLU             │
[22] ReLU                                             [22] MaxPool2d        ┘
[23] MaxPool2d
[24] Conv2d(512→512)                                  self.classifier:
[25] ReLU                                             [0] Linear(12544→4096)         
[26] Conv2d(512→512)                                  [1] ReLU                       
[27] ReLU                                             [2] Dropout(0.5)                
[28] Conv2d(512→512)                                  [3] Linear(4096→4096)          
[29] ReLU                                             [4] ReLU                       
[30] MaxPool2d                                        [5] Dropout(0.5)               
                                                      [6] Linear(4096→num_classes)   
classifier:
[0] Linear(25088→4096)
[1] ReLU
[2] Dropout(0.5)
[3] Linear(4096→4096)
[4] ReLU
[5] Dropout(0.5)
[6] Linear(4096→1000)
~~~

과제4: VGG16 전이 모델





## 개선한점
1. sklearn의 라이브러리 사용
   - 교재에서는 tensorflow.keras의 각 라이브러리를 사용했으나 이는 , 저는 공식 문서를 확인해서 sklearn 라이브러리를 사용해봤습니다. 


## 회고
