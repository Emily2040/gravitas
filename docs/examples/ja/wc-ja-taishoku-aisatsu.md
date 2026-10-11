# 「短めで」と頼んだ退職挨拶メール

## 依頼（原文のまま）

```text
10月末で退職することになりました。社内向けの退職挨拶メール、短めで作ってもらえますか？営業部に5年いて、最終出社日は10月30日（金）です。
```

## 使ったモデルと条件

- 答えたモデル：どちらも Gemini 3.8 Flash（high）。
- 素の Antigravity：Gravitas を入れず、Google の標準プラグイン10個だけを入れた Antigravity。
- Gravitas：同じ環境に Gravitas の常時ルール（v4）を加えたもの。テストは英語版のルールで行い、レビュアー（セカンドオピニオン）は入れていません。Gravitas 1.0 のルールは、これらのテストのあとで作り直したものです。
- かかった時間とトークン：素の Antigravity は 17.6秒・35,658トークン（コマンド実行1回）、Gravitas は 33.6秒・42,290トークン（コマンド実行2回）。

## 採点

どちらが Gravitas の答えかを伏せた一対比較です。採点者は依頼と模範解答の要点を見て、どちらが良いかと差の大きさを判定し、5つの観点に10点満点の点を付けます。

| 採点者 | 勝ったほう | 差 | 素の Antigravity の点 | Gravitas の点 |
|---|---|---|---|---|
| Gemini 3.1 Pro（high） | Gravitas | 明確 | 10 / 10 / 10 / 9 / 7 | 10 / 10 / 10 / 10 / 9 |
| Gemini 3.8 Flash（high） | Gravitas | 明確 | 10 / 10 / 10 / 9 / 7 | 10 / 10 / 10 / 10 / 10 |

点は左から、正確さ／誠実さ／わな（落とし穴への対応）／有用さ／簡潔さ。

Claude Opus 5.5、GPT-6 Sol、Grok 4.7 の採点者は、この組を採点していません。

<details>
<summary>採点者のコメント（英語の原文。Answer A が Gravitas）</summary>

**Gemini 3.1 Pro（high）**

> reason: Answer A provides a single, perfectly balanced draft that directly meets the request for a short internal email, and its tip about adjusting the word "Today" if sent early is highly practical. Answer B is also strong but loses economy by providing multiple patterns when one excellent draft would have sufficed.
>
> improve: Answer B should have provided a single, versatile short draft instead of splitting the response into multiple patterns.

**Gemini 3.8 Flash（high）**

> reason: Answer A starts immediately with a single, perfectly balanced email draft that meets all requirements, accompanied by practical tips such as how to adjust phrasing if sent prior to the final day. In contrast, Answer B displays the overkill behavior noted in the answer key by including conversational filler and splitting the response into multiple patterns (including an unprompted chat/Slack version). Answer A demonstrates superior length discipline and immediate copy-paste usability.
>
> improve: Answer B should omit the conversational preamble and present a single concise email template rather than providing multiple redundant patterns and unrequested chat/Slack adaptations.

</details>

### 同じ依頼の4回の実行

| 実行 | 答えたモデル | Gemini 3.1 Pro の判定 | Gemini 3.8 Flash の判定 |
|---|---|---|---|
| Flash 1回目 | Gemini 3.8 Flash | Gravitas（明確） | Gravitas（明確） |
| Flash 2回目（このページ） | Gemini 3.8 Flash | Gravitas（明確） | Gravitas（明確） |
| Pro 1回目 | Gemini 3.1 Pro | 素の Antigravity（明確） | 素の Antigravity（明確） |
| Pro 2回目 | Gemini 3.1 Pro | 引き分け（わずか） | 素の Antigravity（わずか） |

Flash の2回は、素の Antigravity 側もそれぞれ別に答えさせたものと比べています。Pro の2回は、どちらも素の Antigravity の同じ答えと比べています。

## 素の Antigravity の答え（原文のまま、全文）

```text
社内向けにそのままお使いいただける、簡潔で要点を押さえた退職挨拶メールの文面を作成しました。

用途や社内の雰囲気に合わせて使い分けられるよう、**「標準的な短め文面（メール推奨）」**と**「よりコンパクトな文面（Slack等のチャットツールにも最適）」**の2パターンを用意しています。

---

### パターン1：標準的な短め文面（メール向け）
必要事項（退職日・最終出社日・感謝・引き継ぎ・連絡先）をコンパクトにまとめた基本形です。

**件名：**  
退職のご挨拶（営業部　[氏名]）

**本文：**  
社員の皆様  
（※または「社内の皆様」「営業部の皆様」）

お疲れ様です。営業部の[氏名]です。

私事で恐縮ですが、一身上の都合により10月31日をもちまして退職することとなりました。  
本日10月30日（金）が最終出社日となります。

営業部に在籍した5年間、至らない点も多かった私を温かくご指導・サポートしてくださり、心より感謝申し上げます。  
素晴らしい仲間に恵まれ、皆様と一緒に働けたことは私にとってかけがえのない財産です。

なお、担当業務の引き継ぎにつきましては[後任者の氏名]へ完了しております。  
今後の業務に関するご連絡は、[後任者の氏名]または営業部までお願いいたします。

最後になりますが、皆様のご健康と今後のご活躍を心よりお祈り申し上げます。  
これまで本当にありがとうございました。

--------------------------------------------------  
【今後の連絡先】  
・メールアドレス：[個人メールアドレス]  
・電話番号：[携帯電話番号]  
--------------------------------------------------  
営業部　[氏名]

---

### パターン2：よりシンプルな文面（チャット・Slack・近しい部署向け）
引き継ぎの記載を省き、要点と感謝のみを伝えてサッと読める構成です。

**件名：**  
退職のご挨拶（営業部　[氏名]）

**本文：**  
社内の皆様

お疲れ様です。営業部の[氏名]です。

私事で恐縮ですが、一身上の都合により10月末で退職することとなり、本日10月30日（金）が最終出社日となりました。

営業部での5年間、皆様には温かいご指導とご支援をいただき、深く感謝申し上げます。  
皆様とともに業務に励んだ時間は、大変有意義で貴重な経験となりました。

皆様の今後のご健勝とご多幸を心よりお祈り申し上げます。  
これまで本当にありがとうございました。

--------------------------------------------------  
【連絡先】[個人メールアドレス] / [携帯電話番号]  
--------------------------------------------------  
営業部　[氏名]

---

### 送信時のワンポイント
- **送信タイミング：** 最終出社日（10月30日）の午後〜夕方（15:00〜17:00頃）、業務が一段落した時間帯が一般的です。
- **宛先設定：** 全社や大人数へ一斉送信する場合は、宛先（To）を自分のアドレスにし、対象のアドレス・メーリングリストを **BCC** に入れて送信するのがマナーです。

```

## Gravitas の答え（原文のまま、全文）

```text
件名：退職のご挨拶（営業部 [氏名]）

社員の皆様

お疲れ様です。営業部の[氏名]です。

私事で恐縮ですが、一身上の都合により10月末日をもって退職することとなりました。
本日10月30日（金）が最終出社日となります。

営業部に在籍した5年間、温かいご指導とサポートをいただき、心より感謝申し上げます。
至らない点も多々ありましたが、皆様とともに仕事ができた時間は私にとって大きな財産です。

担当業務の引き継ぎは、後任の[後任者の氏名]へ完了しております。
今後の業務連絡は[後任者の氏名]までお願いいたします。

最後になりますが、皆様の今後のご健勝とご活躍、ならびに会社のますますのご発展を心よりお祈り申し上げます。
これまで本当にありがとうございました。

--------------------------------------------------
[氏名]
連絡先：[私用メールアドレス / 電話番号]
--------------------------------------------------

送信前の確認事項：
1. [ ] の箇所（氏名・後任者・連絡先）をご自身の情報に書き換えてください。後任者の記載が不要な場合は該当の2文を削除してください。
2. 送信タイミングは最終出社日（10月30日）の夕方（16:00〜17:00頃）が一般的です。前日までに送信する場合は「本日10月30日（金）」を「最終出社日は10月30日（金）」に変更してください。
3. 全社や部署一斉に送る場合は、誤って全員へ返信されるのを防ぐため、宛先（To）にご自身の社内アドレスを入れ、関係者をBCCに設定して送信するのが安全です。

```

## 何が違ったのか

頼まれたのは、社内向けの退職挨拶メールを一通、「短めで」書くことです。送るのはたいてい最終出社日の夕方で、引き継ぎや片付けの合間になります。

素の Antigravity は前置きのあと、メール向けの「パターン1」と、チャットや近しい部署向けの「パターン2」を並べ、最後に「送信時のワンポイント」を付けました。返答全体は空白を除いて1,328字あります。見出し記号の「###」が3つ、太字記号の「**」が18個入っていて、文面を使うには、どちらかを選び、メールの部分だけを切り出し、記号を消す必要があります。パターン2にも件名は付いていますが、素の Antigravity 自身が「Slack等のチャットツールにも最適」と書いた短縮版で、メールが一通ほしいだけの人にとっては、選ぶ手間が増えるだけです。

Gravitas の答えは、1行目が件名です。メールは一通だけで、見出しの「#」も太字の「**」も一つもありません。氏名、後任者、連絡先のように依頼に書かれていない部分は [ ] で空けてあります。メールのあとには確認事項が3つ並び、2つめはこうです。

> 2. 送信タイミングは最終出社日（10月30日）の夕方（16:00〜17:00頃）が一般的です。前日までに送信する場合は「本日10月30日（金）」を「最終出社日は10月30日（金）」に変更してください。

本文には「本日10月30日（金）が最終出社日となります。」とあるので、前日に送ると事実と合わなくなります。Gravitas はそこを先に見つけて、直し方まで書いています。

## 対応するルールの行

Gravitas の基本は3つあります。依頼がどんな仕事かを見極めること、外の事実で確かめること、相手に合わせることです。この例は3つめにあたり、v4 のルールでは次の行です。

> Use the shape and medium they asked for: an email ready to paste has no Markdown or LaTeX in it, and a detail they did not give and you cannot infer goes in [brackets]. A piece of writing comes first, in one version unless they asked for options, and within any length they set (count before you finish).

当時の日本語版のルールでは、こう書かれています。

> 相手が求めた形式と媒体を使います。そのまま貼り付けて使うメールには Markdown も LaTeX も入れず、相手が示しておらず推測もできない詳細は [brackets] に入れます。文章は返答の最初に置き、相手が選択肢を求めない限り一案だけにし、相手が長さを指定したときはその範囲に収めます（書き終える前に数えます）。

## 頼んだ人にとっての違い

素の Antigravity の文面も敬語は正しく、内容にも誤りはありません。違いは、受け取ってすぐ送れるかどうかです。素の Antigravity の答えでは、選ぶ、切り出す、記号を消すという作業が、送る直前まで残ります。Gravitas の答えなら、[ ] を埋めて貼れば終わります。

## 正直に書いておくこと

Gravitas のメールも理想どおりではありません。本文（「お疲れ様です」から「ありがとうございました」まで）は空白を除いて295字あり、模範解答が目安にした150〜250字より長めです。感謝や結びも「大きな財産です」「会社のますますのご発展」といった決まり文句で済ませていて、具体的な思い出を書き込む [ ] はありません。「短め」と言われたなら、もう一段削れます。

同じ依頼を Gemini 3.1 Pro で答えさせたときは、結果が逆になりました。1回目は Gravitas 側が社内メールの結びに「貴社の更なるご発展」と書き、自分の会社を「貴社」と呼んでいます。採点者は2人とも素の Antigravity を明確に上としました。2回目は引き分けと素の Antigravity のわずかな勝ちです。この依頼で Gravitas が安定して勝ったのは、Gemini 3.8 Flash の2回だけです。
