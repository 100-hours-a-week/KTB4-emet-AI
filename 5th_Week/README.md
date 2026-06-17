# 5주차 회고록

## 설명
  - Resnet50과 VGG16의 모델 구성을 불러와서(가중치X) 레이어를 재구성해서 생성하고 학습하여 모델을 테스트하고 두 모델의 성능을 비교합니다.
  - 그 후, 두 모델의 하이퍼파라미터인 학습률('lr')과 배치사이즈('batch_size')를 그리드 서치와 랜덤 서치를 진행해서 서치 전후 모델 성능을 확입합니다.
  
### Dataset
#### 과제 1~4
- images_360.npy & labels_360.npy
설명: 다색 바탕에 원,삼각형,사각형으로 구성된 도형 이미지
형태: 이미지 데이터셋
수: 도형 1200EA(각 도형 균일 수량)
훈련,테스트 비율: 8:2

### 모델 설계
과제1: Resnet50 전이 모델
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
~~~
        < 원본 구성(models.vgg16) >                ->          < MyVGG16 >
----------------------------------------------------------------------------------------------------
features:                                             base_model.features:
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
[17] Conv2d(256→512)                                  self.feature:
[18] ReLU                                             [0]  Conv2d(256→256,)
[19] Conv2d(512→512)                                  [1]  ReLU
[20] ReLU                                             [2]  MaxPool2d
[21] Conv2d(512→512)                                  [3]  Conv2d(256→256)
[22] ReLU                                             [4]  ReLU
[23] MaxPool2d                                        [5]  Conv2d(256→256)
[24] Conv2d(512→512)                                  [6]  ReLU
[25] ReLU                                             [7]  MaxPool2d
[26] Conv2d(512→512)                                  
[27] ReLU                                             
[28] Conv2d(512→512)
[29] ReLU
[30] MaxPool2d

AdaptiveAvgPool2d(output=(7,7))                       AdaptiveAvgPool2d(output=(7,7))

classifier:                                           self.classifier:
[0] Linear(25088→4096)                                [0] Linear(12544→4096)
[1] ReLU                                              [1] ReLU
[2] Dropout(0.5)                                      [2] Dropout(0.4)
[3] Linear(4096→4096)                                 [3] Linear(4096→1024)
[4] ReLU                                              [4] ReLU
[5] Dropout(0.5)                                      [5] Dropout(0.4)
[6] Linear(4096→1000)                                 [6] Linear(1024→1024)
                                                      [7] ReLU
                                                      [8] Dropout(0.4)
                                                      [9] Linear(1024→num_classes)
                                                      
~~~


## 결과
- 모델 성능 비교
  - epoch:10, lr: 0.01
  - **Resnet50 Test Accuracy: 99.58%   |   VGG16 Test Accuracy 33.33%**
<img width="576" height="438" alt="image" src="https://github.com/user-attachments/assets/6ab19bde-a488-4d2c-857f-99ece1a771e9" />


- 그리드 서치와 랜덤 서치
  - 그리드 서치
    - 범위 설정
      - 'lr': [0.01, 0.001],
      - 'batch_size': [20, 30]
    - 모델 결과
      - Resnet50  : 'lr:0.01', 'batch_size:20'인 상태에서 accuracy 100.00%
      - VGG16: 'lr:0.01', 'batch_size:20'인 상태에서 accuracy 33.33%
  - 랜덤 서치
    - 범위 설정
      - 'lr': [0.01, 0.001],
      - 'batch_size': [20, 30]
    - 모델 결과
      - Resnet50  : 'lr:0.0083...', 'batch_size:30'인 상태에서 accuracy 100.00%
      - VGG16: 'lr:0.0089...', 'batch_size:54'인 상태에서 accuracy 33.33%

## 개선한점
### 전이 모델 설계(코랩 GPU 메모리 한계)
- 설계 이유: 두 전이 모델의 학습과 그 이후 최적 하이퍼마라미터 검색의 그리드 서치와 랜덤 서치에서 GPU메모리 초과가 발생했습니다. 이를 해결하기 위해 모델의 연산수를 감소시키는 방향으로 레이어를 재구성했습니다.그 결과 torchsummary의 summary 함수를 통해 Resnet50은 약 80MB, VGG16은 약 320MB 감소 시켰습니다.
  
### sklearn.model_selection
- 사이킷런의 최적 하이퍼파라미터 검색 모듈
- 사용이유: 교재에서는 텐서플로우 방식으로 모델을 작성해서 그리드서치와 랜덤서치에서 tensorflow.keras의 각 라이브러리를 사용했습니다. 하지만 경험을 쌓기위한 이유로 파이토치 방식으로 모델을 생성하고 그리드서치와 랜덤서치를 사용했습니다. 이를 위해 sklearn.model_selection의 GridSearchCV와 RandomizedSearchCV를 사용했습니다.
  
### skorch.NeuralNetClassifier
- 파이토치모델을 사이킷런과 동일방식으로 훈련하고 사이킷런과 사용할 수 있게 래핑 해주는 클래스
- 사용이유: klearn.model_selection을 사용하기위해서는 사이킷런 방식의 fit()함수가 필요하지만 파이토치방식에서는 존재하지 않습니다. 해결책으로 학습때처럼 반복문을 사용하거나, 별도의 방법을 찾아야했습니다. 그래서 파이토치 모델을 래핑하는 skorch.NeuralNetClassifier를 찾아 사용했습니다. 아래코드 블럭은 사용 방법입니다.
~~~
# 설치
! pip install skorch

# 임포트
from skorch import NeuralNetClassifier

# 모델 래핑
model_wrapped = NeuralNetClassifier(
    module=base_model,
    module__num_classes=num_classes,  # module__: base_model의 인자 num_classes값 설정 
    criterion=nn.CrossEntropyLoss,    # 손실함수 설정
    optimizer=torch.optim.Adam,       # 옵티마이저 설정 
    max_epochs=10,                    # 최대 에포크 수   
    device=device,                    # cpu,gpu 할당(gpu할당함)
    verbose=0,                        # 콘솔에서 출력되는 정보량
)
~~~


## 회고
Resnet50과 VGG16의 레이어 구성만 가지고와서 신겨망 깊이를 더 깊게 시도할려했으나, 최적 하이퍼파라미터 서치단계에서 코랩의 GPU 메모리 부족에러가 발생해서 모델의 연산량을 축소하는 방향으로 진행했습니다. Resnet50의 수정모델은 테스트에서 99.99%의 정확도가 나오면 오히려 모델이 과적합됬다고 여겨졌습니다. 반대로 VGG16은 원본 모델보다 약740MB에서 약420MB로 감소하면서 연산량이 반이상 감소해서 테스트에서 33.33%의 정확도가 나왔습니다. 그리드 서치와 랜덤서치를 진행했음에도 두 모델의 정확도 결과는 처음에 세팅한 하이퍼파라미터의 테스트 결과와 차이가 없었습니다. 이를 통해 전이모델의 레이어 구성만을 사용해서 모델 경량화는 좀 더 신중하게 구성해야하며, 원본 모델들의 학습-검증 데이터셋과 비교해도 데이터의 양 차이는 심하다보니 데이터셋도 충분히 준비해야함을 느꼈습니다. 


