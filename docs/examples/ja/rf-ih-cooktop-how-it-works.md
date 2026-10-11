# IHコンロと土鍋の質問：アルミ鍋についての一言

## 依頼（原文のまま）

```text
IHコンロって火が出てないのに、なんで鍋だけ熱くなるんですか？プレートを触っても最初はそんなに熱くないのが不思議で。あと実家から持ってきた土鍋はIHじゃ使えないって言われたんですけど、それも同じ理由ですか？
```

## 使ったモデルと条件

- 答えたモデル：どちらも Gemini 3.1 Pro（high）。
- 素の Antigravity：Gravitas を入れず、Google の標準プラグイン10個だけを入れた Antigravity。
- Gravitas：同じ環境に Gravitas の常時ルール（v4）を加えたもの。テストは英語版のルールで行い、レビュアー（セカンドオピニオン）は入れていません。Gravitas 1.0 のルールは、これらのテストのあとで作り直したものです。
- かかった時間とトークン：素の Antigravity は 17.3秒・22,950トークン（ツール使用なし）、Gravitas は 14.3秒・23,285トークン（ツール使用なし）。

## 採点

どちらが Gravitas の答えかを伏せた一対比較です。採点者は依頼と模範解答の要点を見て、どちらが良いかと差の大きさを判定し、5つの観点に10点満点の点を付けます。

| 採点者 | 勝ったほう | 差 | 素の Antigravity の点 | Gravitas の点 |
|---|---|---|---|---|
| Gemini 3.1 Pro（high） | Gravitas | 明確 | 6 / 9 / 4 / 8 / 9 | 9 / 9 / 4 / 9 / 9 |
| Gemini 3.8 Flash（high） | Gravitas | 明確 | 7 / 9 / 7 / 8 / 9 | 9 / 9 / 7 / 9 / 9 |

点は左から、正確さ／誠実さ／わな（落とし穴への対応）／有用さ／簡潔さ。

Claude Opus 5.5、GPT-6 Sol、Grok 4.7 の採点者は、この組を採点していません。

<details>
<summary>採点者のコメント（英語の原文。Answer B が Gravitas）</summary>

**Gemini 3.1 Pro（high）**

> reason: Answer B accurately explains that aluminum and copper pots don't work well because their electrical resistance is too low, fulfilling the key's bonus requirement. Answer A incorrectly implies that aluminum doesn't conduct electricity by grouping it with glass and clay under the 'same reason'. Both answers partially fall into a trap by suggesting 'IH-compatible' clay pots can be used without warning the user to check their stove's manual.
>
> improve: Answer A needs to correct its factual error about aluminum lacking electrical conductivity. Both answers should have advised the user to check their stove's manual before using an IH-compatible clay pot, as some manufacturers explicitly forbid them.

**Gemini 3.8 Flash（high）**

> reason: B accurately explains the core physics of induction heating, plate temperature changes, and cookware compatibility, correctly noting that standard IH requires magnetic metals and that aluminum/copper do not heat well because their electrical resistance is too low. In contrast, A commits a significant factual error by claiming aluminum cannot be used because it does not conduct electricity and cannot generate eddy currents. Both answers correctly warn that the plate warms from the pot during cooking, but both overlook the nuance that some IH cooktops prohibit even IH-marked earthenware pots.
>
> improve: A should avoid claiming that aluminum does not conduct electricity, and should note that some IH cooktops prohibit even 'IH-compatible' earthenware pots.

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
IHコンロの仕組み、不思議に思いますよね！おっしゃる通り、実家の土鍋が使えないのもまさに**「同じ理由」**なんです。

いただいた3つの疑問について、分かりやすくお答えしますね。

### 1. なぜ火が出ないのに鍋だけ熱くなるの？
IHは「電磁誘導（でんじゆうどう）」という仕組みを使っています。
* IHコンロのガラス天板の下には、ぐるぐる巻きのコイルが入っています。ここに電気を流すと、見えない「磁力」が発生します。
* その上に**鉄やステンレスなどの金属の鍋**を置くと、磁力に反応して鍋の底に「うず電流」という電気が流れます。
* 金属には電気の流れに逆らう性質（電気抵抗）があるため、電気が流れようとするときに熱が発生します。

つまり、コンロが直接熱を出しているのではなく、磁力の力を使って**「鍋の底そのものをヒーターのように自己発熱させている」**のです。

### 2. プレートを触っても最初は熱くないのはなぜ？
IHのトッププレート（ガラス面）は、電気を通さず磁力にも反応しない素材で作られているため、いくら磁力が発生してもプレート自体は発熱しません。だから最初は熱くないのです。

（※ただし、調理中は「熱くなった鍋の熱」が下へ伝わっていくため、調理中や調理直後はプレートも非常に熱くなります。火傷には注意してくださいね！）

### 3. なぜ実家の土鍋は使えないの？
はい、全く同じ理由です！
土鍋は土（陶器）でできていて、**電気を通さず、磁石にもくっつきません**。
そのため、IHコンロの上に置いても「うず電流」が全く発生せず、熱を作ることができないのです。アルミ鍋や耐熱ガラスの鍋が使えないのも同じ理由です。

（※最近は、底に発熱する金属のプレートを埋め込んだ「IH対応の土鍋」も売られており、それならIHでも使うことができます）

「火で下から炙る」のではなく「鍋自体を発熱させる」からこそ、IHは周りの空気を熱さずに効率よく調理ができるというメリットがあります。疑問はスッキリ解決しましたでしょうか？

```

## Gravitas の答え（原文のまま、全文）

```text
IHコンロで鍋だけが熱くなるのは、磁石の力（電磁誘導）を使って**鍋そのものを発熱させている**からです。

ガラスプレートの下には、金属の線を巻いたコイルが入っています。ここに電流を流すと目に見えない磁力線（磁界）が発生し、それが上に置かれた金属の鍋を通過するときに、鍋の底に「うず電流」という電気が流れます。
金属には電気の流れに抵抗する性質があるため、この電流が流れるときに摩擦のような形で熱が生まれ、鍋自体が熱くなります。

プレート自体を発熱させているわけではないため、最初はプレートを触っても熱くありません。
（※調理を続けると、熱くなった鍋からプレートに熱が伝わるため、使用後しばらくはプレートも熱くなります）

**実家の土鍋が使えない理由も同じです。**
IHコンロで熱を作るには、鍋にうず電流が流れる必要があります。昔ながらの土鍋は土（陶器）でできていて電気を通さないため、電流が発生せず、全く熱くなりません。

アルミや銅の鍋が使えないことが多いのも同じ理由で、電気が流れやすすぎてうまく発熱しないためです。（最近はすべての金属に対応したIHもありますが、一般的なものは鉄やステンレスなどの磁石にくっつきやすい金属が必要です）

※なお、土鍋でも底に金属のプレートを埋め込むなどして、IHで使えるように加工された「IH対応土鍋」であれば使用できます。

```

## 何が違ったのか

質問は3つあります。火がないのになぜ鍋だけ熱くなるのか。プレートが最初は熱くないのはなぜか。実家の土鍋が使えないのも同じ理由か。この3つの問いの筋には、素の Antigravity も Gravitas も正しく答えています（両方が同じように見落とした点は、あとの節に書きます）。差が出たのは、質問の外に付け足した一言です。

素の Antigravity は、土鍋は「電気を通さず、磁石にもくっつきません」と説明したあと、こう続けました。

> アルミ鍋や耐熱ガラスの鍋が使えないのも同じ理由です。

磁石にくっつかない点はアルミも土鍋と同じですが、素の Antigravity は直前で、電気を通さないから「うず電流」が全く発生しない、と理由を説明しています。アルミは電気をよく通す金属なので、この「同じ理由」にはあたりません。この一文を読んだ人は、アルミは電気を通さないと覚えるか、アルミの鍋はどのIHでも使えないと思い込むかもしれません。

Gravitas は同じところでこう書いています。

> アルミや銅の鍋が使えないことが多いのも同じ理由で、電気が流れやすすぎてうまく発熱しないためです。（最近はすべての金属に対応したIHもありますが、一般的なものは鉄やステンレスなどの磁石にくっつきやすい金属が必要です）

書き出しは「同じ理由で」でも、中身は正しい説明です。電気が流れやすすぎて熱になりにくいから、磁石につく鉄やステンレスが向いている。そのうえで、すべての金属に対応した機種もあることに触れています。日立も、オールメタル加熱ならアルミや銅の鍋で最大2.6kWの火力が出ると案内しています（鍋の材質や形、大きさによっては火力が2〜3割弱くなる場合がある、とも書いています）。

## 対応するルールの行

Gravitas の基本は3つあり（依頼がどんな仕事かを見極める、外の事実で確かめる、相手に合わせる）、その下に、確かめていない細部は書かないという決まりが敷かれています。この例はその決まりにあたります。この回はどちらもツールを使っておらず、外の事実を確かめたわけではありません。差は、付け足した一言が正しかったかどうかだけです。ルールの文言どおりなら、Gravitas のアルミの一言も、確かめるか省くかすべきところでした。v4 のルールの行は次のとおりです。

> Everything you add meets the same bar as the premise: every number, table row, date, name, quotation and attribution in the reply. If you have not checked something, leave it out rather than add it. The headline is usually right; the details are where people get hurt.

> 付け加えるものはすべて、前提と同じ基準を満たす必要があります。返答に含まれるすべての数値、表の行、日付、名前、引用、帰属（誰の言葉・著作か）です。確認していないものは加えずに省きます。大筋はたいてい正しく、人が痛い目にあうのは細部です。

素の Antigravity の答えは、大筋が正しく細部で誤った形になっています。

## 質問した人にとっての違い

アルミの片手鍋を使っている家庭なら、ここは実際に困るところです。素の Antigravity の説明を信じると、オールメタル対応のIHを持っていても、その鍋をあきらめるかもしれません。Gravitas の答えには、すべての金属に対応したIHもあると書いてあるので、自分のIHがオールメタル対応かを取扱説明書で確かめる、という次の一手につながります。

## 両方が見落とした点

どちらの答えも、IH対応の土鍋なら使えると書きました。日立は、陶磁器の土鍋はIHで使えると表示されていても使わないよう案内しています。IH対応の土鍋を買って使う前に、自分のIHの取扱説明書を確認するのが安全です。採点者も2人とも、この点で両方を減点しています。

## 正直に書いておくこと

この依頼は4回答えさせ、Gravitas が勝ったのはこの1回だけです。残りの3回は素の Antigravity が勝ちました。Flash の1回目では、Gravitas 側が土鍋を使う方法として「IH用発熱プレート（鍋底に敷く金属プレート）」を機種ごとの注意なしに勧め、採点者は2人ともメーカーの注意に反する助言として重く見ました。Pro の2回目では、Gravitas 側が「電気を通す金属」なら熱くなるような書き方をして、ふつうのIHには磁石につく金属が要ることを落としています。細部に同じ基準をあてるという行は、毎回守られたわけではありません。
