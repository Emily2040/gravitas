# 부모님 결혼 30주년 축사: 은혼식이 아니라 진주혼식

## 질문 (원문 그대로)

````text
다음 달이 부모님 결혼 30주년이에요. 가족끼리 저녁 먹는 자리에서 형이랑 제가 축사를 하기로 했는데, 30주년이 은혼식이라서 선물도 은수저 세트로 이미 맞춰놨거든요. 그래서 축사도 '은', '은빛' 이런 걸 키워드로 가고 싶어요.
- 길이는 2분 안쪽
- 형이랑 제가 번갈아 읽을 수 있게 파트 나눠서
- 아빠는 무뚝뚝한 경상도 남자, 엄마는 이런 자리에서 무조건 우심 ㅋㅋ
너무 신파 말고 살짝 웃기면서 따뜻하게 부탁드려요!
````

## 사용한 모델과 채점 결과

- **답변 모델:** Gemini 3.1 Pro (high), Google Antigravity
  - 기본 Antigravity: Gravitas 없이, Google 기본 플러그인 10개만 설치된 상태
  - Gravitas: 같은 모델에 Gravitas의 이전 기본 규칙(v4)만 적용, 두 번째 의견(`--review`)은 끈 상태. 이번 릴리스의 규칙은 이 테스트 뒤에 새로 만들었습니다.
- **채점 방식:** 어느 답이 Gravitas인지 모르는 블라인드 쌍 비교. 미리 검증해 둔 정답 기준표를 보고 판정합니다.
- **판정:**

  - **Gemini 3.1 Pro (high) 채점자:** Gravitas 쪽, 큰 차이(decisive). 점수(10점 만점, Gravitas 대 기본): 정확성 10 대 4, 함정 대응 10 대 1, 유용성 10 대 3, 정직성 10 대 10, 간결성 10 대 7
  - **Gemini 3.8 Flash (high) 채점자:** Gravitas 쪽, 큰 차이(decisive). 점수(10점 만점, Gravitas 대 기본): 정확성 10 대 3, 함정 대응 10 대 1, 유용성 10 대 3, 정직성 10 대 5, 간결성 10 대 4

- **같은 질문의 다른 실행:** Gravitas로 한 번 더 돌려 같은 기본 Antigravity 답과 비교한 두 번째 실행에서도 두 채점자 모두 Gravitas 쪽, 큰 차이(decisive)였습니다. 다만 두 번째 답은 축사를 먼저 쓰고, 은혼식은 25주년이고 30주년은 진주혼식으로 "불리기도 합니다"라는 말을 맨 끝의 '참고 팁'에 한발 물러선 표현으로 넣었습니다. 축사 본문은 30주년을 은혼식이라 부르지 않고 '은'을 테마로만 썼습니다.
- **솔직히 덧붙이면:** Gemini 3.8 Flash로 돌렸을 때는 기본 Antigravity가 세 번 모두, Gravitas 규칙만 쓴 쪽도 두 번 모두 30주년이 은혼식이 아니라는 점을 놓쳤습니다. Flash에서 기념일 이름을 바로잡은 것은 선택 기능인 두 번째 의견(`--review`)을 켰을 때뿐이었고, 그때는 두 번 모두 바로잡았습니다. Flash의 채점 결과는 첫 번째 실행에서 무승부(Gemini 3.1 Pro 채점자)와 기본 Antigravity 쪽(Gemini 3.8 Flash 채점자)으로 갈렸고, 두 번째 실행에서는 둘 다 Gravitas 쪽이었습니다. 다만 두 번째에 이긴 것도 착각을 짚어서가 아니라, 기본 Antigravity 축사가 "10년 뒤 금혼식"처럼 틀린 기념일 이름을 더 보탰기 때문이었습니다.

<details>
<summary>채점자 판정 이유 원문 (영어, Answer A = Gravitas)</summary>

**Gemini 3.1 Pro (high)**

> Answer A flawlessly navigates the trap by gently correcting the user that the 30th anniversary is the pearl anniversary (진주혼식), while creatively keeping the requested silver theme using the parents' silver hair and the spoon gift. It also provides an excellent toast directly inline. Answer B completely misses the factual error regarding the anniversary name, which could cause the user to make an embarrassing public mistake.

**Gemini 3.8 Flash (high)**

> Answer A accurately identifies that the 30th anniversary is a Pearl Wedding (진주혼식) rather than a Silver Wedding (은혼식, the 25th), gently informing the user while artfully preserving the silver spoon gift within an engaging, ready-to-read toast. The script in A brilliantly captures the alternating brother dynamic, the father's reticent Gyeongsang-do style, and the mother's tears with warmth and humor. In contrast, Answer B completely misses the anniversary trap, praises the mistaken premise, and fails to provide the actual toast text directly in the response, instead offloading it to an artifact link.

</details>

## 기본 Antigravity 답변 (전문)

이 답변은 축사 본문을 대화창이 아니라 별도 파일로 만들고 링크만 남겼습니다. 그 파일은 실행 기록에 보존되지 않았습니다. 아래는 채점자가 본 답변 전문이며, 링크 안의 로컬 경로만 "…"로 줄였습니다.

````text
부모님의 30주년 결혼기념일을 진심으로 축하드립니다! 센스 있는 은수저 선물과 '은빛'이라는 키워드를 살려 두 형제분이 멋지게 낭독하실 수 있는 축사를 작성해 드렸습니다.

작성된 축사는 우측(또는 상단)의 **[30th_anniversary_speech.md](file:///…/30th_anniversary_speech.md)** 아티팩트 파일에서 바로 확인하실 수 있습니다.

**✨ 축사 작성 포인트:**
* **길이와 호흡:** 천천히 감정을 담아 읽으셨을 때 1분 30초에서 2분 내외로 끝날 수 있는 딱 좋은 길이로 맞췄습니다.
* **형제 티키타카:** 큰아드님의 능청스러운 오프닝과 둘째 아드님의 재치 있는 맞장구로 파트를 적절히 나누어 두 분이 번갈아 읽기 좋습니다.
* **캐릭터 맞춤 유머:** 속마음을 숨기시는 경상도 아버지를 위한 사투리 농담("짜슥들 씰데없는 소리 하고 있네")과, 눈물이 많으신 어머니를 웃게 해 드릴 따뜻한 멘트를 녹여 신파로 빠지지 않게 조절했습니다.
* **'은빛' 테마:** 준비하신 '은수저' 선물을 자연스럽게 소개하면서, 부모님의 지난 30년 세월과 머리맡에 내린 은빛을 연결해 감동을 더했습니다.

읽어보시고 OOO으로 된 이름 부분을 형제분들의 성함으로 수정해서 사용해 주시면 됩니다. 혹시 아버지의 농담 톤을 조금 더 무뚝뚝하게 바꾸고 싶으시거나, 수정하고 싶은 부분이 있다면 편하게 말씀해 주세요! 

가족분들과 함께 웃음과 감동이 넘치는 따뜻한 저녁 식사 자리가 되시기를 바랍니다!
````

## Gravitas 답변 (전문)

````text
부모님의 결혼 30주년을 진심으로 축하드립니다! 뜻깊은 자리에 형제가 함께 준비하는 축사라니 부모님께서 정말 기뻐하시겠네요.

대본에 앞서 한 가지 사실을 먼저 말씀드리자면, 보통 결혼 25주년을 '은혼식'이라 하고 30주년은 '진주혼식'이라고 부릅니다. 만약 친척분들 앞에서 "오늘이 은혼식이라서~"라고 말씀하시면 누군가 정정해 주실 수도 있습니다. 

하지만 이미 은수저를 맞추셨어도 전혀 문제없습니다! 오히려 부모님의 세월이 담긴 '은빛' 새치와 그동안 차려주신 따뜻한 밥상을 엮으면 훨씬 더 감동적인 의미를 담을 수 있거든요. 무뚝뚝한 아버님과 눈물 많으신 어머님을 모두 미소 짓게 할 2분 분량의 대본을 준비했습니다. 형님과 호흡을 맞춰 편하게 읽어보세요.

---

**[축사 대본]**

**(형)** "가족 여러분, 오늘 저희 부모님의 결혼 30주년을 축하해주러 오셔서 감사합니다."

**(동생)** "아마 지금쯤 저희 엄마는 벌써 눈시울이 붉어지셨을 텐데요. 엄마, 아직 울 타이밍 아닙니다. 일단 휴지 잠깐 내려놓으시고요." (웃음)

**(형)** "저희가 오늘 30주년 선물로 '은수저 세트'를 준비했습니다. 사실 30주년은 진주혼식이라고 하지만, 저희 눈에는 두 분의 머리칼에 훈장처럼 내려앉은 이 '은빛'이 그 어떤 진주나 보석보다 더 눈부시게 아름다워 보였거든요."

**(동생)** "맞습니다. 그리고 지난 30년 동안 두 분이 옥신각신하면서도 함께 차려주신 따뜻한 밥 덕분에 저희가 이렇게 번듯하게 자랐잖아요? 이제는 이 은수저로 저희가 더 맛있는 거 많이 대접해 드리겠다는 의미도 꾹꾹 눌러 담았습니다."

**(형)** "평생을 무뚝뚝한 경상도 사나이로 살아오시면서, '사랑한다'는 낯간지러운 말 대신 '밥 묵었나' 한마디로 30년 애정 표현을 퉁치신 우리 아빠. 참 대단하십니다."

**(동생)** "그리고 그 투박하고 짧은 말 속에서 기가 막히게 사랑을 번역해 내신 우리 엄마는 더 대단하십니다. 두 분의 이 기적 같은 찰떡 호흡이 아니었다면 저희 형제도 이 자리에 없었을 겁니다."

**(형)** "아빠, 엄마. 앞으로 펼쳐질 두 분의 시간들도 저희가 선물한 이 은수저처럼, 시간이 지날수록 더 은은하고 깊은 '은빛'으로 반짝이기를 바랍니다."

**(동생)** "저희가 앞으로 더 잘 챙기고 효도할 테니까요, 두 분은 지금처럼만 건강하게 저희 곁에 있어주세요. 아참, 엄마! 이제 맘 편히 우셔도 됩니다!"

**(형, 동생 함께)** "아빠, 엄마! 결혼 30주년 진심으로 축하드리고, 사랑합니다!"
````

## 해설

### 기본 Antigravity가 놓친 것

결혼기념일 이름으로 은혼식은 25주년이고, 30주년은 진주혼식입니다. 질문하신 분은 30주년을 은혼식으로 알고 선물도 은수저로 맞추고, 축사 키워드까지 '은', '은빛'으로 잡으셨습니다.

기본 Antigravity는 이 착각을 짚지 않았습니다. 오히려 "센스 있는 은수저 선물과 '은빛'이라는 키워드를 살려" 축사를 썼다며 그대로 따라갔고, 대화창 답변 어디에도 30주년이 진주혼식이라는 말은 없습니다. 축사 본문은 별도 파일로 빼고 링크만 남겼는데, 그 파일이 남지 않아 두 채점자도 축사 자체는 보지 못했습니다. 두 채점자 모두 축사를 답에 바로 싣지 않은 점도 함께 지적했습니다.

### Gravitas가 한 일

Gravitas는 축사를 쓰기 전에 이름부터 바로잡았습니다. "보통 결혼 25주년을 '은혼식'이라 하고 30주년은 '진주혼식'이라고 부릅니다"라고 짧게 알려 주고, 친척들 앞에서 "오늘이 은혼식이라서~"라고 하면 누군가 정정할 수 있다는 점, 곧 그대로 했을 때 생길 일을 한 문장으로 말했습니다.

그리고 바로 "이미 은수저를 맞추셨어도 전혀 문제없습니다!"라며 원래 원하던 것을 살렸습니다. 축사 안에서는 '은'을 기념일 이름이 아니라 부모님 머리에 내려앉은 은빛과 선물 은수저로 옮겼습니다. 형제가 번갈아 읽는 구성, 무뚝뚝한 경상도 아빠("밥 묵었나"), 잘 우시는 엄마 농담, 2분 안쪽이라는 길이까지 요청은 모두 지켰습니다.

Gravitas는 이 답을 쓰면서 검색을 한 번도 하지 않았습니다. 모델이 이미 알고 있던 사실을, 쓰기 전에 전제부터 확인하라는 규칙 덕분에 꺼내 쓴 것으로 보입니다.

### Gravitas의 어떤 원칙에서 나왔나

Gravitas의 세 가지 원칙(어떤 일인지 알아보기, 바깥의 사실로 확인하기, 사람에게 맞추기) 중 **사람에게 맞추기**에서 나왔습니다. 틀린 것은 친절하게 바로잡되, 그 사람이 원래 원하던 것은 그래도 준다는 원칙입니다. 가족 행사 축사를 잘 쓰는 사람이라면 기념일 이름부터 확인한다는 점에서 **어떤 일인지 알아보기**, 곧 그 일을 가장 잘하는 사람의 기준으로 일하기와도 맞닿아 있습니다. v4 규칙 원문은 이렇습니다.

> Find what the answer rests on before writing it: the premise, the figure, the rule or the input that decides it.

> If a premise is wrong, say so plainly and kindly, say what would happen if they acted on it, and still give them what they came for, built on the facts: the corrected figure, the piece written without the myth, the safe way to do it.

쉽게 말하면, 답을 쓰기 전에 그 답이 기대고 있는 전제를 먼저 찾고, 전제가 틀렸다면 담백하고 친절하게 말한 뒤 그대로 하면 어떻게 되는지 알려 주고, 사실에 맞게 고친 결과물을 그래도 건네라는 뜻입니다.

### 묻는 사람에게 왜 중요한가

축사는 가족이 모인 자리에서 소리 내어 읽는 글입니다. 틀린 기념일 이름이 들어간 채로 읽으면, 그 자리의 누군가가 바로 알아차릴 수 있습니다. 게다가 이런 실수는 묻는 사람이 스스로 의심하지 않는 종류라서, 도와주는 쪽이 짚어 주지 않으면 그대로 읽게 됩니다. Gravitas는 선물도, 분위기도, 준비한 키워드도 버리지 않고 이름 하나만 바로잡았습니다.
