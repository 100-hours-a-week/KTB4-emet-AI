# 5주차 회고록

## 설명

### Dataset



### 모델 설계
과제1: Resnet50 전이 모델
- 깊은 층을 가진 Resnet50은 기본적으로 학습시간이 길다. 그래서 학습시간을 감소시키기위해서 마지막 3층을 제거한후 layer3의 출력 크기에 맞게 avgpool을 생성 및 연결하고,fc를 연결했다.

  
~~~
        <원본 구성(models.resnet50)>          ->            <MyResNet50>        
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

과제4: VGG16 전이 모델
- grid



## 개선한점
1. sklearn의 라이브러리 사용
   - 교재에서는 tensorflow.keras의 각 라이브러리를 사용했으나 이는 , 저는 공식 문서를 확인해서 sklearn 라이브러리를 사용해봤습니다. 


## 회고
