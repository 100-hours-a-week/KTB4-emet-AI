# 4주차 회고록
## Abstact

## 설명

### Dataset
모든 데이터는 Claude(Pro)와 순수 대화로만 통해서 합성데이터 생성
<종류> 
  - 1. programming_books_mlp.scv
     - 설명: 프로그래밍 공부 서적에 대한 정보 데이터셋
     - 형태: 텍스트 데이터셋()
     - 수: 서적 500EA
     - 컬럼: 제목,저자,카테고리,판매가격,'난이도',출판연도,대출가능,인기도
     - 사용된 과제번호: 1,2,3
 -  2. images.npy & labels.npy (dataset_images.zip)
     - 설명: 원,삼각형,사각형으로 구성된 도형 이미지
     - 형태: 이미지 데이터셋()
     - 수: 도형 300EA(각 도형 균일 수량)
     - 사용된 과제번호: 4,

### 데이터 전처리
  - 1. programming_books_mlp.scv
     - 레이블(클래스) 선택    
       - '카테고리'
         -  
       - '대출가능'
         - 이진 분류 가능
       - '인기도'
         - 3개 클래스     
     - '제목','저자' 제거
       - 둘다 string 형태
       - '제목'의 특성을 '카테고리'가 가짐
       - '저자' 중복되는 수가 희소하다, 저자에 대한 추가 정보가 없다.
     - '난이도' 직접 정수화 매핑
       - value는 우선순위를 가짐으로 다음과 같이 매핑함
         ~~~
         {'입문': 0,'초급': 1,'중급': 2,'고급': 3,'전문가': 4}
         ~~~   
  - 2. images.npy & labels.npy (dataset_images.zip)
    - 레이블(클래스) 선택
     - labels.npy의 정수 번호(다각형 종류 의미)
    - 증강 : 90도 회전, 좌우반전, 상하반전 사용

### 학습-검증-테스트 데이터셋 분할
  - 분리 비율: 학습 80%, 테스트 20%
    - 1. programming_books_mlp.scv
      - 과제 1,2
        - 레이블: '카테고리'
      - 과제 3
        - 레이블: '대출가능'
        - 원핫인코딩: '카테고리'
        - 데이터정규화 사용O
      - 과제 6
        - 레이블: '인기도'
        - 원핫인코딩: '카테고리'
        - 데이터정규화 사용O
     - 2. images.npy & labels.npy (dataset_images.zip) 
      
### 모델 설계
  - 과제 2: K-NN
    - 구현: `sklearn.neighbors`의 `KNeighborsClassifier` 사용
    - 파라미터 세팅
      ```
      k: 5
      ```
        
  - 과제 3: Perceptron
    - 구현: 직접 Class 설계
    - 파라미터 세팅   
      ```
      weight: 랜덤, bias: 0.1, learning_rate: 0.1, epochs: 20
      ```
      
  - 과제 3: SVM
    - 구현: `sklearn.svm`의 `SVC` 사용
   
  - 과제 3: Random Forest
    - 구현: `sklearn.ensemble`의 `RandomForestClassifier` 사용
    - 파라미터 세팅    
      ```
      n_estimators: 100, max_depth: 5
      ```
      
  - 과제 3: Naive Bayes
    - 구현: `sklearn.naive_bayes`의 `GaussianNB` 사용
      
  - 과제 6: MLP
    - 구현: 직접 Class 설계
    - 구성
      input -> 퍼셉트론1 -> sigmoid -> 퍼셉트론2 -> Relu -> output
    - 파라미터 세팅   
      ```
      w1: 랜덤 벡터(입력 크기), w2: 랜덤 스칼라, b1: 랜덤 스칼라, b2: 랜덤 벡터(레이블 수),
      num_classes:레이블 수, lr:0.1 , epochs: 20
      ```
      
  - 과제 7: CNN
    - 구현: 직접 Class 설계
    - 구성
      input -> conv1 -> MaxPool ->  conv2 -> MaxPool ->  conv3 -> MaxPool ->  Flatten -> FC1 ->  FC2 -> output
    - 파라미터 세팅   
      ```
      conv1:{ch:3->32, kernel:3, padding:1}
      conv2:{ch:32->64, kernel:3, padding:1}
      conv3:{ch:64->128, kernel:3, padding:1}
      MaxPool:{kernel:2, stride:2}
      fc1:{ch:128*8*8->256}
      fc2:{ch:256->레이블 수}
      num_classes:레이블 수, lr:0.001 , epochs: 10
      loss func: 크로스엔트로피
      Optimizer: Adam
      ```






  
### 모델 
