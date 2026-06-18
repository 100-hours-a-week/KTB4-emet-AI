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

~~~
text = open("input.txt").read()
chars = sorted(set(text))
vocab_size = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda ids: "".join(itos[i] for i in ids)
data = torch.tensor(encode(text), dtype=torch.long)
n_train = int(0.9 * len(data))  # hold out the last 10% to measure overfitting
train_data, val_data = data[:n_train], data[n_train:]
~~~

### Self-Atteion
~~~
# 셀프 어텐션 역할을 하는 "CausalSelfAttention" 클래스
class CausalSelfAttention(nn.Module):
    """Multi-head scaled dot-product attention: softmax(QK^T / sqrt(d) + mask) V."""

    def __init__(self):
        super().__init__()
        self.qkv = nn.Linear(n_embd, 3 * n_embd)   # Q,K,V 한번에 계산하기 위한 레이어: 3분할을 위해서 출력크기 3 * n_embd설정
        self.proj = nn.Linear(n_embd, n_embd)      # 멀티헤드 어텐션 결과를 합친 후 최종 출력하는 레이어
        self.drop = nn.Dropout(dropout)

    def forward(self, x):
        B, T, C = x.shape            # B=배치크기, T=문장길이(시퀀스), C=임베딩차원 으로 분리
        head_dim = C // n_head       # 몫연산, head_dim=헤드당 차원

        # q, k, v 얻기 위해 텐서를 열방향으로  3등분
        ## self.qkv(x) = tensor[(B, T, 3*C)]
        ## 1차 변환: 텐서[B, T, C] -(차원 확장)-> 텐서[B, T, n_head, head_dim]
        q, k, v = self.qkv(x).chunk(3, dim=-1)    
        
   
        ## 2차 변환: 텐서[B, T, n_head, head_dim] -(1,2 차원 교환)-> [B, n_head, T, head_dim]로 변환
        ### 텐서를 각 헤드별로 병렬계산하기위해서
        q = q.view(B, T, n_head, head_dim).transpose(1, 2)
        k = k.view(B, T, n_head, head_dim).transpose(1, 2)
        v = v.view(B, T, n_head, head_dim).transpose(1, 2)

        # 어텐션 점수: q와 k전치행렬 내적곱 진행후, 스케일링
        ## q[B, n_head, T, head_dim] @ k[B, n_head, head_dim, T] -> [B, n_head, T, T]
        ## head_dim**0.5 로 몫연산: 계산 값 오버플로우 방지
        att = q @ k.transpose(-2, -1) / head_dim**0.5        

        # 좌측하단이 직각이며 True의 시작점인 삼각형(torch.tril) 마스크 생성
        ## 미래토큰을 볼수없고, 현재와 과거만 볼수있도록 강제함
        ### tensor([[True,  False, False, False],
        ###         [True,  True,  False, False],
        ###         [True,  True,  True,  False],
        ###         [True,  True,  True,  True ]])
        causal = torch.tril(torch.ones(T, T, dtype=torch.bool, device=x.device))

        # 위의 마스크를 반전시키고, True를 -inf로 변환
        ## softmax를 거치면 -inf는 0이되면서 미래토큰 완전 무시
        att = att.masked_fill(~causal, float("-inf"))        
        att = self.drop(F.softmax(att, dim=-1))

        out = att @ v                                        # (B, n_head, T, head_dim)
        out = out.transpose(1, 2).reshape(B, T, C)           # concat heads
        return self.drop(self.proj(out))
~~~

### Deocoder
~~~
# 트랜스포머의 디코더(셀프 어텐션 + 순전파) 역할을 하는 "Block"클래스
class Block(nn.Module):
    """Transformer decoder block: causal self-attention + feed-forward."""

    
    def __init__(self):
        super().__init__()                           
        self.ln1 = nn.LayerNorm(n_embd)            # 레이어 정규화1
        self.attn = CausalSelfAttention()          # 셀프 어센션
        self.ln2 = nn.LayerNorm(n_embd)            # 레이어 정규화2
        self.mlp = nn.Sequential(                  # 멀티 레이어 페셉트론
            nn.Linear(n_embd, 4 * n_embd),            ## 선형레이어1
            nn.GELU(),                                ## GELU(Gaussian Error Linear Unit)
            nn.Linear(4 * n_embd, n_embd),            ## 선형레이어2
            nn.Dropout(dropout),                      ## 드롭아웃
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x
~~~

### MiniGPT

#### Main Body

~~~
class MiniGPT(nn.Module):
    def __init__(self):
        super().__init__()
        ## 토큰 임베딩
        self.tok_emb = nn.Embedding(vocab_size, n_embd)
        ## 포지셔널 임베딩(인코딩)
        self.pos_emb = nn.Embedding(block_size, n_embd)

        self.blocks = nn.Sequential(*[Block() for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        T = idx.size(1)
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        x = self.ln_f(self.blocks(x))
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, vocab_size), targets.view(-1))
        return logits, loss
~~~

#### Train

~~~
def train(model):
    print(f"{sum(p.numel() for p in model.parameters()):,} parameters, device={device}")
    opt = torch.optim.AdamW(model.parameters(), lr=lr)

    for step in range(steps):
        x, y = get_batch()
        _, loss = model(x, y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 1000 == 0 or step == steps - 1:
            est = estimate_loss(model)
            print(f"step {step:5d}  train {est['train']:.3f}  val {est['val']:.3f}", flush=True)

    torch.save(model.state_dict(), "mini_gpt.pt")
    print("saved weights to mini_gpt.pt")

    model.eval()
    prompt = torch.zeros((1, 1), dtype=torch.long, device=device)  # start token
    print("\n--- sample ---")
    print(decode(model.generate(prompt, 500)[0].tolist()))
~~~

#### Predict

~~~
@torch.no_grad()
def estimate_loss(model):
    """Average loss over several batches, with dropout off."""
    model.eval()
    out = {s: sum(model(*get_batch(s))[1].item() for _ in range(20)) / 20
           for s in ("train", "val")}
    model.train()
    return out
~~~

-------------------------------------------------------------------------------------------------------------

~~~

class MiniGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block() for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        T = idx.size(1)
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        x = self.ln_f(self.blocks(x))
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, vocab_size), targets.view(-1))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, _ = self(idx[:, -block_size:])
            probs = F.softmax(logits[:, -1, :], dim=-1)
            idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
        return idx


@torch.no_grad()
def estimate_loss(model):
    """Average loss over several batches, with dropout off."""
    model.eval()
    out = {s: sum(model(*get_batch(s))[1].item() for _ in range(20)) / 20
           for s in ("train", "val")}
    model.train()
    return out


def train(model):
    print(f"{sum(p.numel() for p in model.parameters()):,} parameters, device={device}")
    opt = torch.optim.AdamW(model.parameters(), lr=lr)

    for step in range(steps):
        x, y = get_batch()
        _, loss = model(x, y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 1000 == 0 or step == steps - 1:
            est = estimate_loss(model)
            print(f"step {step:5d}  train {est['train']:.3f}  val {est['val']:.3f}", flush=True)

    torch.save(model.state_dict(), "mini_gpt.pt")
    print("saved weights to mini_gpt.pt")

    model.eval()
    prompt = torch.zeros((1, 1), dtype=torch.long, device=device)  # start token
    print("\n--- sample ---")
    print(decode(model.generate(prompt, 500)[0].tolist()))


def chat(model):
    model.load_state_dict(torch.load("mini_gpt.pt", map_location=device))
    model.eval()
    print("Type a prompt and the model will continue it (empty line or Ctrl-D to quit).")
    while True:
        try:
            prompt = input("> ")
        except EOFError:
            break
        if not prompt:
            break
        # drop characters the corpus (and thus the vocab) doesn't contain
        ids = [stoi[c] for c in prompt if c in stoi]
        if not ids:
            print("(no characters from the prompt are in the vocabulary)")
            continue
        idx = torch.tensor([ids], dtype=torch.long, device=device)
        out = model.generate(idx, 200)[0].tolist()
        print(decode(out[len(ids):]))  # print only the continuation
~~~


## Module

### torch.nn

#### nn.Embedding(num_embeddings, embedding_dim)
- 기능: 입력 텐서를 다차원 텐서로 확장
- params
    - num_embeddings : 단어 사전 크기 (총 단어 수) 또는 문장 길이
    - embedding_dim  : 출력 벡터 크기 
  예)  
- 사용법
    - **토큰 임베딩**
        - 토큰화된 단어(인데스 번호)를 임베딩해서 벡터로 변환  
        - 예)
          tensor([3, 6]) # 단어 토큰
          -> nn.Embedding(num_embeddings=10,embedding_dim=4)
          -> tensor([[ 0.7890, -0.2345,  0.6789, -0.1234],    # 인덱스 3번 단어 벡터
                  [-0.4567,  0.8901, -0.3456,  0.7890]],      # 인덱스 6번 단어 벡터
                  grad_fn=<EmbeddingBackward0>)
    - **포지셔널 인코딩**
        - 위치 인덱스를 인코딩해서 벡터로 변환
        - 예)
          tensor([0, 1, 2, 3, 4])
          -> pos_embedding = nn.Embedding(num_embeddings=seq_len, embedding_dim=4)
          -> tensor([[-0.12,  0.56, -0.90,  0.34],   # 0번째 위치 벡터
                  [ 0.78, -0.23,  0.67, -0.12],   # 1번째 위치 벡터
                  [-0.45,  0.89, -0.34,  0.78],   # 2번째 위치 벡터
                  [ 0.12, -0.56,  0.90, -0.34],   # 3번째 위치 벡터
                  [-0.78,  0.23, -0.67,  0.12]],  # 4번째 위치 벡터
                  grad_fn=<EmbeddingBackward0>)
    

        - grad_fn=<EmbeddingBackward0> : 역전파 추적 정보(made by nn.Embedding 을 표시하는 태그)
            - grad_fn = gradient function (기울기 계산 함수)
            - Embedding = nn.Embedding 레이어를 통과했다
            - Backward = 역전파 시 이 함수로 기울기를 계산하겠다
            - 0 = 연산 순서 번호















