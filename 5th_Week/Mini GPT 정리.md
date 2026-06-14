# Mini GPT
- URL[https://colab.research.google.com/drive/1RQrM35MmBrgdTT_SNJKnVM9WjYgrEmNd?usp=sharing]
- 해당 문서는 위 URL에서 Mini GPT 코드 분석을 정리했습니다.
- 코드에 대해 개인주석으로 설명했습니다.
- 처음 접한 메소드, 모듈은 'Code' 항목 이후 개별 정리했습니다.

## Code

### Hyperparameters
~~~
block_size = 128     # 최대 문장 길이
n_embd = 256         # 임베딩 차원embedding dimension
n_head = 4           # 어텐션 헤드 attention heads
n_layer = 6          # transformer blocks
batch_size = 64
steps = 20000
lr = 1e-3
dropout = 0.2
device = (
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)
torch.manual_seed(1337)
~~~
### data

