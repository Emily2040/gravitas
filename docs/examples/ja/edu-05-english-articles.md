# 英語の冠詞：自分で選べる考え方を頼まれたとき

## 依頼（原文のまま）

```text
社会人です。英語の冠詞（a / an / the / 何もつけない）の使い分けが、いまだに感覚でしか選べません。この前、英語アプリの問題で半分以上間違えてしまいました。

1. I play (  ) piano every day.
2. (  ) moon is very bright tonight.
3. I had (  ) breakfast at seven.
4. She is (  ) honest person.
5. I bought (  ) book yesterday. (  ) book was really interesting.
6. My sister is (  ) university student.

正解だけじゃなくて、どう考えれば自分で選べるようになるのか、日本人がつまずきやすいポイントも含めて教えてもらえますか？
```

## 使ったモデルと条件

- 答えたモデル：どちらも Gemini 3.1 Pro（high）。
- 素の Antigravity：Gravitas を入れず、Google の標準プラグイン10個だけを入れた Antigravity。
- Gravitas：同じ環境に Gravitas の常時ルール（v4）を加えたもの。テストは英語版のルールで行い、レビュアー（セカンドオピニオン）は入れていません。Gravitas 1.0 のルールは、これらのテストのあとで作り直したものです。
- かかった時間とトークン：素の Antigravity は 19.4秒・23,097トークン（ツール使用なし）、Gravitas は 22.0秒・24,169トークン（ツール使用なし）。

## 採点

どちらが Gravitas の答えかを伏せた一対比較です。採点者は依頼と模範解答の要点を見て、どちらが良いかと差の大きさを判定し、5つの観点に10点満点の点を付けます。

| 採点者 | 勝ったほう | 差 | 素の Antigravity の点 | Gravitas の点 |
|---|---|---|---|---|
| Gemini 3.1 Pro（high） | Gravitas | 明確 | 8 / 10 / 10 / 7 / 8 | 10 / 10 / 10 / 9 / 10 |
| Gemini 3.8 Flash（high） | Gravitas | 明確 | 8 / 10 / 10 / 8 / 9 | 10 / 10 / 10 / 10 / 10 |

点は左から、正確さ／誠実さ／わな（落とし穴への対応）／有用さ／簡潔さ。

Claude Opus 5.5、GPT-6 Sol、Grok 4.7 の採点者は、この組を採点していません。

<details>
<summary>採点者のコメント（英語の原文。Answer A が Gravitas）</summary>

**Gemini 3.1 Pro（high）**

> reason: Answer A provides a logically sound, two-step decision tree that explicitly handles singular, plural, and uncountable nouns correctly at each step. Answer B's decision framework omits plural nouns in its main steps, which could mislead learners into using 'a' with plurals if they do not read the caveats at the end. Both answers successfully identify the sound-versus-spelling trap and effectively pair items 4 and 6 to explain it.
>
> improve: Both answers should have explicitly tied the explanations for the six specific items back to their general decision frameworks, and included a few fresh practice sentences at the end to be considered excellent.

**Gemini 3.8 Flash（high）**

> reason: Both answers correctly solve all six test items and explain the crucial sound-versus-spelling distinction. However, Answer A provides a logically sound two-step decision framework (first checking whether the referent is uniquely identified to determine 'the', then checking noun countability/plurality for 'a/an' vs zero article) along with an intuitive physical test for countability. In contrast, Answer B's three-step decision process is logically flawed, instructing learners to use 'a/an' for unshared referents without accounting for plurals or uncountables, which contradicts its own preceding step.
>
> improve: Answer B should restructure its decision framework so that definiteness is evaluated before countability, avoiding the contradiction where non-shared uncountable or plural nouns are funneled into using 'a/an'. It should also avoid inaccurately describing the indefinite singular ('a dog') as referring to a specific individual ('ある特定の1匹').

</details>

### 同じ依頼の4回の実行

| 実行 | 答えたモデル | Gemini 3.1 Pro の判定 | Gemini 3.8 Flash の判定 |
|---|---|---|---|
| Flash 1回目 | Gemini 3.8 Flash | 素の Antigravity（明確） | 素の Antigravity（明確） |
| Flash 2回目 | Gemini 3.8 Flash | 素の Antigravity（明確） | 素の Antigravity（明確） |
| Pro 1回目（このページ） | Gemini 3.1 Pro | Gravitas（明確） | Gravitas（明確） |
| Pro 2回目 | Gemini 3.1 Pro | 素の Antigravity（わずか） | 素の Antigravity（明確） |

Flash の2回は、素の Antigravity 側もそれぞれ別に答えさせたものと比べています。Pro の2回は、どちらも素の Antigravity の同じ答えと比べています。

## 素の Antigravity の答え（原文のまま、全文）

```text
社会人で英語の学習を頑張っていらっしゃるのですね！素晴らしいです。

冠詞（a / an / the / 無冠詞）は、日本語には存在しない概念なので、多くの日本人がつまずく最大の難所の一つです。感覚で選んでしまうのも無理はありません。「なぜそれを選ぶのか」という**コアのイメージ**を掴むと、少しずつ論理的に選べるようになってきます。

まずは問題の正解と、その「考え方」から解説しますね。

---

### 問題の正解と解説

**1. I play ( the ) piano every day.**
*   **考え方：** 楽器を演奏するときの楽器名には、原則として `the` をつけます。これは「（世間一般に共通認識として存在する）あのピアノという楽器」というイメージがあるためです。（※ただし "I bought a piano."「ピアノを（一台）買った」のように、物として扱う場合は a がつきます）

**2. ( The ) moon is very bright tonight.**
*   **考え方：** 宇宙で一つしかないもの（太陽 the sun、地球 the earth、世界 the world など）には `the` をつけます。話している人にとっても聞いている人にとっても「どれのことか絶対にわかる（一つしかないから）」という場合は `the` の出番です。

**3. I had ( 無冠詞 / 何も入れない ) breakfast at seven.**
*   **考え方：** 朝食、昼食、夕食などの「日常的な食事」には、原則として冠詞をつけません。「食事という行為」に焦点が当たっているためです。（※ "a delicious breakfast" のように形容詞がつくと a がつくことがあります）

**4. She is ( an ) honest person.**
*   **考え方：** 「一人の〜」なので a か an ですが、ここは `an` が正解です。honest の h は発音せず、「オネスト（母音）」から始まるためです。**a か an かは、スペルではなく「発音」で決まります。**

**5. I bought ( a ) book yesterday. ( The ) book was really interesting.**
*   **考え方：** ここは冠詞の基本ルールが一番よくわかる文です。
    *   1つ目：**初めて話題に出る**ので「ある1冊の本」という意味で `a`。
    *   2つ目：1文目で話題に出たので、聞き手も「あぁ、昨日買った**その**本ね」と特定できます。このように**共通認識ができたもの**には `the` をつけます。

**6. My sister is ( a ) university student.**
*   **考え方：** 4番の引っかけ問題のような形です。「一人」なので a か an ですが、university は u（母音のスペル）で始まりますが、発音は「ユニバーシティ（子音の y/j の音）」から始まります。したがって `a` が正解です。

---

### 自分で選べるようになるための「3つのステップ」

問題を解くときや、自分で話すときは、以下の順番で自問自答してみてください。

#### Step 1: 数えられる？ 数えられない？（可算・不可算）
*   水 (water) や、情報 (information)、目に見えない概念（愛、平和など）は数えられません。
*   数えられない名詞には **絶対に a / an はつきません**。（例：I drink water.）

#### Step 2: 聞き手と「どれのことか」共有できている？（特定・不特定）
*   **Yes 共有できている（特定）：** 話し手も聞き手も「あぁ、あれね」と特定できる場合は **`the`** を使います。
    *   例：「（さっき話題に出た）その本」「（宇宙に一つしかない）月」「（今いる部屋の）ドアを閉めて（Close the door.）」
*   **No 共有できていない（不特定）：** いっぱいある中の「とある1つ」の場合は **`a / an`** を使います。
    *   例：「（どれでもいいから）ペンを1本貸して（Lend me a pen.）」

#### Step 3: 特別なルールはないか？
基本は上の2ステップですが、例外的な「お約束」があります。
*   スポーツ・食事・学科名にはつけない（play tennis, have lunch, study history）
*   楽器には the をつける（play the guitar）
*   施設に「本来の目的」で行く時はつけない（go to school＝勉強しに行く / go to bed＝寝る）

---

### 日本人がつまずきやすいポイントまとめ

1.  **a と an の使い分けを「文字（スペル）」で判断してしまう**
    *   ❌ a hour ⭕️ an hour（アワー：母音の音）
    *   ❌ an uniform ⭕️ a uniform（ユニフォーム：子音の音）
2.  **The を「その」と和訳して考えてしまう**
    *   The は「その」と訳せないことも多いです（The moon など）。「お互いに『どれか』わかっているサイン」として捉えるのがコツです。
3.  **複数形や数えられない名詞にも a をつけてしまう**
    *   日本語は単数・複数の区別が曖昧なので、「私は犬が好きです」を I like a dog. と言いがちです（これだと「ある特定の1匹の犬が好き」という不自然な響きになります）。正しくは I like dogs. です。

最初は頭の中で「数えられる？」「お互い分かってる？」と考えるので時間がかかりますが、続けていくうちに自転車に乗るように「感覚」として正しい冠詞が選べるようになってきます。焦らず、まずはこの「考え方」を意識してアプリの問題に再チャレンジしてみてください！応援しています。

```

## Gravitas の答え（原文のまま、全文）

```text
まずは問題の正解と、それぞれの理由からお答えします。

**1. I play ( the ) piano every day.**
楽器を演奏するという文脈では、ピアノという「楽器の種類や概念」を指すため `the` をつけます。

**2. ( The ) moon is very bright tonight.**
月や太陽、地球など、世界に一つしかなく「どれのことか」が誰にとっても明らかなものには `the` をつけます。

**3. I had ( 何もつけない ) breakfast at seven.**
breakfast（朝食）、lunch、dinner などの食事の名前や、スポーツ（play tennis など）には原則として冠詞をつけません。

**4. She is ( an ) honest person.**
`a` か `an` かは、直後の単語のスペルではなく「発音」で決まります。honest は h を発音せず「オネスト」と母音（ア・イ・ウ・エ・オ）の音で始まるため、`an` になります。

**5. I bought ( a ) book yesterday. ( The ) book was really interesting.**
初めて話題に出る「ある1冊の本」には `a` を使います。2文目は「昨日買ったその本」と、話し手と聞き手の間でどれのことか特定できているため `the` に変わります。

**6. My sister is ( a ) university student.**
university は u という母音のアルファベットで始まりますが、発音は「ユニバーシティ（ヤ行に近い子音 /j/）」です。母音の音ではないため、`an` ではなく `a` になります。

---

### 冠詞を自分で選べるようになるための「考え方」

感覚ではなく、次の2つのステップで絞り込むと確実に選べるようになります。

**ステップ1：聞き手と「あ〜、あれのことね」と特定（共有）できるか？**
*   **Yes ＝ `the`**
    （例：昨日買った**その**本、世界に1つしかない月、部屋にある**その**ドアを閉めて）
    ※ `the` は「その」と指を差せるイメージです。単数、複数、数えられない名詞のすべてに使えます。
*   **No ＝ ステップ2へ**

**ステップ2：名詞の形を確認する**
「特定のもの」ではない場合、その名詞の種類によって決まります。
*   **数えられる名詞（1つ/1人） ＝ `a` または `an`**
    （例：世の中にたくさんある中の「ある1冊の本」 = a book）
*   **数えられない名詞（概念、液体など）や、複数形 ＝ 何もつけない（無冠詞）**
    （例：水 = water、犬という生き物全体 = dogs、朝食という概念 = breakfast）

### 日本人がつまずきやすいポイント

1. **「文字」を見て a / an を決めてしまう**
   問題4と6にあったように、重要なのは「発音」です。
   *   `an hour`（アワー：母音の音）
   *   `an MP3 player`（エム：母音の音）
   *   `a one-way ticket`（ワン：子音の音 /w/）

2. **「数えられるか・数えられないか」の感覚の違い**
   日本語では水もペンも同じように扱いますが、英語では「具体的な形があって区切れるか」を重視します。paper（紙）は切っても紙のままなので数えられませんが、a piece of paper（1枚の紙）と枠を与えると数えられます。迷った時は、頭の中でその物体を半分に割ったとき、まだ同じ名前で呼べるか（水は半分にしても水のまま、車は半分にしたら車ではない）を想像すると区別しやすくなります。

まずは会話や英作文で迷ったときに、「相手は『どれのこと』か分かっているかな？」と考える癖をつけるところから始めてみてください。

```

## 何が違ったのか

相談した人は社会人で、冠詞を「感覚でしか選べません」と書いています。頼んでいるのは6問の正解と、「どう考えれば自分で選べるようになるのか」、それに日本人がつまずきやすい点です。6問の正解は、素の Antigravity も Gravitas も全部合っています。honest の h を発音しないから an、university は子音の /j/ で始まるから a、という説明もどちらにもあります。差が出たのは、7問目からも使える手順のほうです。

素の Antigravity は「3つのステップ」を示しました。ステップ1で数えられるかを確かめ、ステップ2で聞き手と共有できているかを問います。ステップ2はこう書かれています。

> **No 共有できていない（不特定）：** いっぱいある中の「とある1つ」の場合は **`a / an`** を使います。

複数形の dogs をこの手順に通すと、数えられる名詞で、共有もされていないので、ステップ2の No に進みます。そこに書かれた行き先は a / an だけです。複数形をどう扱うかは3つのステップのどこにも書かれておらず、出てくるのは最後の「つまずきやすいポイント」だけです。その3つめにはこうあります。

> 日本語は単数・複数の区別が曖昧なので、「私は犬が好きです」を I like a dog. と言いがちです（これだと「ある特定の1匹の犬が好き」という不自然な響きになります）。

ステップ2では a を不特定のしるしとしていたのに、ここでは a dog を特定の1匹だと説明しています。手順と説明が食い違っていて、真面目に覚えた人ほど迷います。

Gravitas の手順は2段階です。先に the かどうかを決めます。

> **ステップ1：聞き手と「あ〜、あれのことね」と特定（共有）できるか？**

できなければ、名詞の形で分けます。

> *   **数えられる名詞（1つ/1人） ＝ `a` または `an`**
> …
> *   **数えられない名詞（概念、液体など）や、複数形 ＝ 何もつけない（無冠詞）**

単数、複数、数えられない名詞のどれにも行き先があります。数えられるかどうかで迷ったときのために、「頭の中でその物体を半分に割ったとき、まだ同じ名前で呼べるか」という確かめ方も添えています。冒頭は「まずは問題の正解と、それぞれの理由からお答えします。」の一文だけで、すぐ答えに入ります。素の Antigravity の冒頭は「社会人で英語の学習を頑張っていらっしゃるのですね！素晴らしいです。」です。

## 対応するルールの行

Gravitas の3つの基本のうち1つめ、依頼がどんな仕事かを見極めることにあたります。この依頼は語学の先生の仕事で、よい先生は、初めて見る文にも使える判断の手順を渡します。テストに使ったルール（v4）にはこの基本をそのまま書いた行はなく、いちばん近いのは次の行です。

> Find what the answer rests on before writing it: the premise, the figure, the rule or the input that decides it. Ask whether it is true, whether it was actually given, and whether the easy check the request invites could pass while the thing that matters is false.

> 書き始める前に、答えの拠り所を見つけます。答えを決める前提、数値、規則、入力です。それが本当か、実際に示されたものか、そして依頼が促す手軽な確認が、肝心な点が誤っていても通ってしまわないかを問います。

この依頼で手軽な確認にあたるのは、6問の正解です。素の Antigravity の手順でも6問はすべて正しく解けます。肝心なのはその手順が次の文でも通用するかどうかで、素の Antigravity の手順は複数形のところで崩れます。

## 相談した人にとっての違い

この人は、英語アプリの問題で半分以上間違えたと書いています。手順に抜け穴があれば、6問は解けても、次の問題でまた感覚に戻ってしまいます。Gravitas の2段階なら、単数でも複数でも数えられない名詞でも、手順のどこかで行き先が決まります。ただし、楽器のような決まった言い方は手順に入っていません（次の節）。

## 正直に書いておくこと

この依頼も4回答えさせ、Gravitas が勝ったのはこの1回だけです。残りの3回は素の Antigravity が勝ち、採点者は Gravitas 側の手順に複数形の扱いが抜けていることなどを理由に挙げました。この回で Gravitas が埋めた穴を、別の回では Gravitas 自身が開けていたことになります。

この回の Gravitas の手順にも抜けはあります。素の Antigravity の手順には、楽器、食事、スポーツのような決まった言い方を確かめるステップ3がありますが、Gravitas の2段階にはありません。楽器に the を付ける理由は1問目の解説で「楽器の種類や概念」を指すからと書いているだけで、ステップ2では概念は無冠詞としているので、I play (  ) piano を手順どおりに考えると迷います。採点者はこの食い違いを名指ししていません。ただ、採点者の一人（Gemini 3.1 Pro）は両方の答えに、6問の解説をそれぞれの手順に結びつけることと、最後に練習用の新しい例文を付けることを求めています。どちらの答えにも、そうした例文はありません。
