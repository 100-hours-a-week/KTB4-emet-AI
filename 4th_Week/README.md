# 4주차 회고록

## 설명
Colab의 모든 코드는 셀순서대로 실행되도록 코드를 만들었습니다. 
실행은 위에서 아래로 순서대로 실행만 하면 됩니다.
아래는 해당 과제에 사용한 데이터셋과 데이터셋 분할, 모델구성을 정리했습니다.
4번 과제의 원본 데이터셋과 증강 데이터셋 각각 동일한 모델로 학습했을때의 성능 비교는 7번 과제에서 CNN으로 진행했습니다.

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
     - 설명: 흰바탕에 원,삼각형,사각형으로 구성된 심플한 도형 이미지
     - 형태: 이미지 데이터셋(
     - 수: 도형 300EA(각 도형 균일 수량)
     - 사용된 과제번호: 4,7

### 데이터 전처리
  - 1. programming_books_mlp.scv
     - 레이블(클래스) 선택    
       - '카테고리'
         - 5개 클래스
           ~~~
           {0:'C,' 1:'C#', 2:'C++', 3:'Java', 4:'Python'}
           ~~~
       - '대출가능'
         - 이진 분류 가능
           ~~~
           {0:불가능,1:가능}
           ~~~
       - '인기도'
         - 3개 클래스
           ~~~
           {0:비인기,1:보통,2:인기}
           ~~~   
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
      ~~~
      # labels.npy
      {0: 원, 1: 삼각형, 2: 사각형}
      ~~~
    - 증강 : 90도 회전, 좌우반전, 상하반전 사용
      -> 300EA에서 1200EA로 증가

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
        - 레이블: 도형이름 정수형
      
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

## 개선한점
일부 모델 평가에서 테스트 데이터셋의 예측값과 실제값을 직접 확인하기 위해 레이블인코더를 사용. 
~~~
from sklearn.preprocessing import LabelEncoder
# 레이블 인코더 생성
le = LabelEncoder()
# 인코딩: C++ -> 2
y = le.fit_transform(y)
# 디코딩: 2 -> C++
le.inverse_transform()
~~~

## 회고
과제 4번의 경우 과제7에서 같은 구조의 CNN에 적용해서 학습했으나 예상한바와 다르게 모델의 테스트 결과는 원본데이터셋이 증강한 데이터셋보다 결과가 좋았다. 학습률(lr)을 변경하면서 진행했음에도 결과는 바뀌지 않았다. 하지만 대체적으로 epoch에 따른 Loss 감소율은 증강데이터셋이 더 높았으며, 그에 따라 최종 Loss도 증강 데이터셋이 낮았다. 이런 결과는 증강을 하긴했지만 과적합으로 예상된다. 과적합이라 생각한 이유는 해당 이미지 데이터들이 흰바탕에 원, 사각형, 삼각형 도형이 존재하는 심플한 이미지이다. 그래서 내가 시도한 90 회전과 상하뒤집기,좌우뒤집기는 동일하거나 비슷한 이미지를 생성할 가능성이 높다. 그래서 증강한 데이터셋이 원본 데이터셋보다 많더라도 오히려 심플해서 중복 이미지를 만들었을 가능성이 있다. 그래서 위와 같은 결과가 나온걸로 예상된다.
