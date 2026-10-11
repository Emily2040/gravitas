# モジュール 07 - サブエージェント

## 目的

専門エージェントを用意する方法、2026 年 10 月時点でのサブエージェント関連ツールの引数、本プラグインに同梱しているエージェント、役割ごとに使うモデルをまとめたモジュールです。`invoke_subagent` または `define_subagent` を初めて呼び出す前に、`08-delegation.md` とあわせて読み込んでください。

## 専門エージェントを用意する 3 つの方法

| 方法 | 呼び出し方 | 書き込み権限 | 用途 |
| :--- | :--- | :--- | :--- |
| 同梱エージェント | `invoke_subagent` の `TypeName` に `gravitas-*` エージェントを指定 | エージェントファイルの `tools` リストで固定 | 観察・判断・批評を担うすべての役割 |
| その場で定義 | `define_subagent` で定義し、その名前を指定して `invoke_subagent` を呼ぶ | `enable_write_tools` の true / false で指定 | 本プラグインが同梱していない専門エージェント |
| 組み込みの `self` | `invoke_subagent` で `TypeName: "self"` を指定 | 親と同じツール | ユーザーが選んだモデルとツールのまま進めるべき実装作業。agy 1.2.9 でモデルが一覧に挙げたもので、このスキルではまだ試していない |

書き込みをさせてはいけない役割には、同梱エージェントを優先して使います。同梱エージェントが読み取り専用なのはファイルに書かれたツールリストによるものなので、サブエージェントが指示を守るかどうかには左右されません。

## ツール宣言

以下は、2026-09-24 に agy 1.2.9 上でモデル自身が持つツール宣言を読み出し、デスクトップ版 2.17.0 の `language_server.exe` に含まれる文字列と突き合わせたものです。CLI が 1.2.15 から 1.2.16 に上がった 2026-10-03 には、`define_subagent` 以外をあらためて読み出し、内容が一致することを確かめました。このスキルの旧版では宣言に存在しないフィールドを記載してしまったことがあるため、アップデート後は宣言を確認し直してください。

| ツール | 引数 |
| :--- | :--- |
| `invoke_subagent` | `Subagents`（配列）。各要素には `TypeName`、`Role`（2〜5 語の肩書き）、`Prompt` を指定し、この 3 つはすべて必須。これに加えて `Model`（`inherit`、`flash_lite`、`flash`、`pro`。既定値は `inherit`）と `Workspace`（`inherit`、`branch`、`share`。既定値は `inherit`）を受け付ける |
| `define_subagent` | `name`、`description`、`system_prompt`、`enable_write_tools`（ファイル編集とコマンド）、`enable_mcp_tools`、`enable_subagent_tools` |
| `manage_subagents` | `Action` に `list`、`kill`、`kill_all` のいずれかを指定。`kill` のときは `ConversationIds` も渡す |
| `send_message` | `Recipient`（サブエージェントの会話 ID）と `Message` |
| `schedule` | 一回限りのタイマーなら `DurationSeconds`、cron なら `CronExpression` を指定し、あわせて `Prompt` を渡す。`TimerCondition` は `never`（既定値）、`any`、または送信者 ID（その送信者からメッセージが届くとタイマーが取り消される）。`IsDaemon` と `MaxIterations` は cron 向けの指定。呼び出しはすぐに戻り、取り消すには `manage_task` に `kill` とタスク ID を渡す |

並行実行させるには、1 つの `Subagents` 配列に複数の要素を入れます。起動したサブエージェントにはそれぞれ専用の会話 ID と、トランスクリプトを指す `logAbsoluteUri` が割り当てられます。サブエージェントが `send_message` を呼ばずに終了した場合は、送信者 `system` のメッセージで最後の返答が届きます。この返答を待つときは、`TimerCondition: "any"` を指定した `schedule` タイマーをセットしてからターンを終えてください。サブエージェントの ID に紐づけたタイマーはこの `system` メッセージでは取り消されず、タイマーを置かなければヘッドレス実行はターンの終了とともに終わって結果が失われるためです。動作を確認済みのパターンは `08-delegation.md` にあります。

`invoke_subagent` の宣言には、ユーザーが別のモデルを求めない限り `Model` を `inherit` にするよう、モデルに向けた指示が書かれています。下のモデル振り分け表に載っている役割については、本プラグインをインストールしたこと自体が、この「別のモデルを求める」意思表示にあたります。

## カスタムエージェントのファイル

カスタムエージェントは、YAML フロントマター付きの Markdown ファイルです。フロントマターでエージェントを設定し、本文がそのエージェントのシステムプロンプトになります。

```markdown
---
name: "gravitas-refuter"
description: "Attempts to refute one specific claim. Defaults to refuted when uncertain."
tools:
  - view_file
  - grep_search
  - read_url_content
  - search_web
model: "pro"
mainAgent: false
subagent: true
inheritCustomizations: false
inheritMcp: false
---

You are a refuter. ...
```

| キー | 意味 |
| :--- | :--- |
| `name`、`description` | エージェントの識別情報と、親がサブエージェントを選ぶときに読む説明文 |
| `tools` | エージェントが呼び出せるツール。それ以外のツールは持たない |
| `model` | `inherit`、`flash`、`pro` のいずれか |
| `mainAgent`、`subagent` | メインエージェントとして選べるかどうかと、`invoke_subagent` から起動できるかどうか |
| `commandExecutionPolicy` | シェル実行のポリシー。`off`、`auto`、`eager`、`sandbox` のいずれか |
| `skills`、`plugins`、`mcpServers`、`rules`、`hooks`、`agents` | このエージェントに付けるカスタマイズ |
| `inheritCustomizations`、`inheritMcp` | ユーザーのスキル・ルール・プラグインを引き継ぐかどうかと、ユーザーの MCP サーバーを使えるようにするかどうか |
| `excludeDefaultComponents` | ドキュメント上は、既定のプロンプトセクションとツールを外すとされている。agy 1.2.9 では、指定しても追加で外れるものはなかった（未解決の issue #1015） |

キー名は、デスクトップ版 2.17.0 の `language_server.exe` に YAML タグとして含まれていることを確認しました。意味の説明はカスタムサブエージェントのドキュメントに基づいています。`inheritMcp` はドキュメントに記載がなく、意味は本スキルでのテストで確かめたものです。バイナリには `enabledTools`、`disabledTools`、`hidden`、`background` も含まれていますが、いずれも未検証で、使っていません。

`tools` リストに書いたものがツールセットのすべてになるわけではありません。agy 1.2.9 では、`view_file` だけを列挙して `inheritCustomizations: false` にしたエージェントにも、本人の申告によればツール宣言に `send_message`、`call_mcp_tool`、`list_resources`、`read_resource`、`manage_task` が含まれていました。`call_mcp_tool` からは接続中のすべての MCP サーバーを呼び出せるため、批評役を読み取り専用といえるのは、それらのサーバーがすべて読み取り専用の場合に限られます。`inheritMcp: false` を加えると `call_mcp_tool` は消えましたが、さらに `excludeDefaultComponents: true` を重ねても何も変わりませんでした。同梱エージェントはすべて、2 つの継承フラグをどちらも false にしています。

カスタムエージェントは、`~/.gemini/config/agents/` と、プラグイン内の `agents/` から検出されます。2026-09-24 に agy 1.2.9 で確認したところ、`agy agents` はグローバルに置いたエージェントを一覧に表示した一方、プラグイン内のエージェントは表示しませんでした。ただしモデルからはどちらも見えており、名前を挙げることもできました。ワークスペースの `.agents/agents/` に置いたエージェントは、`--add-dir` でリポジトリを渡したときにしか検出されませんでした。

注意点が 2 つあります。まず、`tools` にマッピングされていないツール名や綴りを誤ったツール名があると、サブエージェントがハングすることがある、とドキュメントで警告されています。そのため `scripts/check_skills.py` で、すべてのツール名を既知の一覧と照合しています。次に、agy 1.2.7 以降は `find_by_name`、`grep_search`、`list_dir` が既定のツールセットから外れており、カスタムエージェントがこれらを使えるのは `tools` に列挙した場合だけです。

## 同梱エージェント一覧

| エージェント | 役割定義 | ツール | モデル | 書き込み |
| :--- | :--- | :--- | :--- | :--- |
| `gravitas-scout` | ファイル、ルート（routes）、シンボル、情報源の場所を特定する。返すのはパスと行範囲だけ | `list_dir`、`find_by_name`、`grep_search`、`view_file` | flash | なし |
| `gravitas-reader` | 範囲を限ったファイルや URL について具体的な質問に答え、根拠にした行を引用する | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content` | flash | なし |
| `gravitas-finder` | 渡された作業リスト全体を対象に、1 種類の欠陥に絞って洗い出すか、1 つの切り口に絞って調べる | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content`、`search_web` | flash | なし |
| `gravitas-checker` | 独立したチェックを 1 つ実行する（数値の評価、テスト、再計算、クエリ） | `view_file`、`run_command` | flash | 一時ファイルのみ（役割定義による） |
| `gravitas-refuter` | 1 つの主張の反証を試みる。確信が持てないときは「反証された」とする | `view_file`、`grep_search`、`read_url_content`、`search_web` | pro | なし |
| `gravitas-visual-critic` | ソースを見ていない閲覧者の立場でキャプチャを評価する | `view_file` | pro | なし |
| `gravitas-completeness-critic` | 台帳を読み、まだ検索していないもの・開いていないもの・実行していないもの・検証していないものを挙げる | `view_file`、`list_dir`、`grep_search`、`find_by_name` | pro | なし |
| `gravitas-prose-editor` | 下書きにこのスキルの文章基準（prose standard）を当てはめ、手を入れた文章を返す | `view_file` | pro | なし |
| `gravitas-reviewer` | 常時適用ルールの「セカンドオピニオン」として返答の下書きをレビューし、欠陥を最大 3 つ返す | `view_file`、`read_url_content`、`search_web`、`run_command` | pro | なし（役割定義による） |

`gravitas-checker` と `gravitas-reviewer` はコマンドラインを使えるので、この 2 つが読み取り専用なのはツールによる制限ではなく、役割定義上のルールです。チェッカーには狭い範囲だけを任せ、その結果に結論が依存するときはトランスクリプトまで読んでください。レビュアーはこのスキルのファンアウト用ではなく、ルールの「セカンドオピニオン」のためのエージェントで、その節を含むルールと一緒にしかインストールされません。そのルールを入れるには、インストール時に `--review` を指定します。実装作業は親が自分で行うか、`Model: "inherit"` を指定した `self` に任せます。こうすれば、ファイルを変更する作業にはユーザーが選んだモデルがそのまま使われます。

## モデルの振り分け

| 作業 | モデル |
| :--- | :--- |
| 機械的な抽出、ファイルの仕分け、一覧の作成 | `flash_lite` |
| 偵察役（scout）、読み取り役（reader）、探索役（finder）、チェッカー（checker） | `flash` |
| 反証役（refuter）、批評役（critic）、判定役（judge）、最終的な統合 | `pro` |
| ファイルを書き込む作業すべて | `inherit` |

ファイルの仕分けに `pro` を使うのはコストの無駄です。逆に、視覚批評役を `flash_lite` で動かせば、この役割の存在意義である判断力を捨てることになります。書き込みを伴う作業の既定値を `inherit` にしているのは、ユーザーが選んだモデルを黙って格下げすれば、ユーザー自身が下していない決定を勝手に下すことになるからです。
