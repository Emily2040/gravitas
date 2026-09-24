# モジュール 07 - サブエージェント

## 目的

このモジュールは、専門役の得方、2026 年 9 月時点でサブエージェント用ツールが受け取る引数、このプラグインに同梱のエージェント、そして各役割が使うモデルを扱います。最初の `invoke_subagent` または `define_subagent` の呼び出しの前に、`08-delegation.md` と一緒に読み込みます。

## 専門役を得る三つの方法

| 経路 | 方法 | 書き込み権限 | 用途 |
| :--- | :--- | :--- | :--- |
| 同梱のエージェント | `TypeName` を `gravitas-*` のエージェントにして `invoke_subagent` | エージェントファイルの `tools` リストで固定 | 観察、判断、批評のすべての役割 |
| その場での定義 | `define_subagent` のあと、新しい名前で `invoke_subagent` | `enable_write_tools` の true か false | このプラグインが同梱していない専門役 |
| 組み込みの `self` | `TypeName: "self"` で `invoke_subagent` | 親と同じツール | ユーザーが選んだモデルとツールで行うべき実装。agy 1.2.9 でモデルが一覧に挙げたもので、このスキルとはまだ試していない |

書いてはいけない役割には、同梱のエージェントを優先します。読み取り専用であることはファイルのツールリストから来るので、サブエージェントが指示に従うかどうかに左右されません。

## ツールの宣言

2026-09-24 に agy 1.2.9 でモデル自身が受け取ったツール宣言を読み出し、デスクトップ 2.17.0 の `language_server.exe` の文字列と照合したものです。このスキルの以前の版は宣言にないフィールドを記載していたので、更新後は確認し直してください。

| ツール | 引数 |
| :--- | :--- |
| `invoke_subagent` | `Subagents`：配列。各項目は必須の `TypeName`、`Role`（2〜5 語の肩書き）、`Prompt` と、`Model`（`inherit`、`flash_lite`、`flash`、`pro`、既定は `inherit`）、`Workspace`（`inherit`、`branch`、`share`、既定は `inherit`）を受け取ります |
| `define_subagent` | `name`、`description`、`system_prompt`、`enable_write_tools`（ファイル編集とコマンド）、`enable_mcp_tools`、`enable_subagent_tools` |
| `manage_subagents` | `Action`：`list`、`kill`、`kill_all`。`kill` には `ConversationIds` を付けます |
| `send_message` | `Recipient`（サブエージェントの会話 ID）と `Message` |

並行実行は、ひとつの `Subagents` 配列に複数の項目を入れることで得られます。起動した各サブエージェントは固有の会話 ID と、そのトランスクリプトを指す `logAbsoluteUri` を持ち、終わるとメッセージを返します。対話セッションではポーリングは不要です。ヘッドレス実行では、すべての子が終わるまでツール呼び出しを続けます（`08-delegation.md`）。

`invoke_subagent` の宣言は、ユーザーが別のモデルを求めない限り `Model` を `inherit` にするようモデルに指示しています。このプラグインをインストールすることが、下のルーティング表の役割についてのその要求にあたります。

## カスタムエージェントのファイル

カスタムエージェントは YAML のフロントマターを持つ Markdown ファイルです。フロントマターがエージェントを設定し、本文がシステムプロンプトになります。

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
| `name`、`description` | 識別と、親がサブエージェントを選ぶときに読む文 |
| `tools` | エージェントが呼べるツール。それ以外はない |
| `model` | `inherit`、`flash`、`pro` |
| `mainAgent`、`subagent` | メインエージェントとして選べるか、`invoke_subagent` で起動できるか |
| `commandExecutionPolicy` | シェルの方針：`off`、`auto`、`eager`、`sandbox` |
| `skills`、`plugins`、`mcpServers`、`rules`、`hooks`、`agents` | このエージェントに付けるカスタマイズ |
| `inheritCustomizations`、`inheritMcp` | ユーザーのスキル、ルール、プラグインを引き継ぐか、ユーザーの MCP サーバーを得るか |
| `excludeDefaultComponents` | 既定のプロンプト部分とツールを外すと説明されているが、agy 1.2.9 ではそれ以上何も外れなかった（open issue #1015） |

キー名はデスクトップ 2.17.0 の `language_server.exe` 内の YAML タグとして確認し、意味はカスタムサブエージェントのドキュメントから取りました。`inheritMcp` はドキュメントにはなく、ここで試しました。バイナリには `enabledTools`、`disabledTools`、`hidden`、`background` もありますが、未検証で使っていません。

`tools` リストがツールセットのすべてではありません。agy 1.2.9 では、`view_file` だけを挙げて `inheritCustomizations: false` にしたエージェントも、自分の宣言についての本人の説明によれば `send_message`、`call_mcp_tool`、`list_resources`、`read_resource`、`manage_task` を持っていました。`call_mcp_tool` は接続中のすべての MCP サーバーに届くので、批評役が読み取り専用なのは、それらがすべて読み取り専用である場合だけです。`inheritMcp: false` を加えると `call_mcp_tool` が消え、さらに `excludeDefaultComponents: true` を加えても何も変わりませんでした。同梱のエージェントはすべて、二つの継承フラグを false にしています。

カスタムエージェントは `~/.gemini/config/agents/` と、プラグイン内の `agents/` から検出されます。2026-09-24 の agy 1.2.9 では、`agy agents` はグローバルのエージェントを表示し、プラグイン内のものは表示しませんでしたが、モデルはどちらも見て名前を挙げられました。ワークスペースの `.agents/agents/` のエージェントは、リポジトリを `--add-dir` で渡したときだけ検出されました。

注意が二つあります。ドキュメントは、`tools` の未対応や綴り違いのツール名がサブエージェントを停止させるおそれがあると警告しているので、`scripts/check_skills.py` がすべての名前を既知の一覧と照合します。また agy 1.2.7 以降、`find_by_name`、`grep_search`、`list_dir` は既定のツールセットから外れており、カスタムエージェントはそれらを挙げたときだけ使えます。

## 同梱のロスター

| エージェント | 役割 | ツール | モデル | 書き込み |
| :--- | :--- | :--- | :--- | :--- |
| `gravitas-scout` | ファイル、ルート、シンボル、出典の場所を探す。パスと行範囲だけを返す | `list_dir`、`find_by_name`、`grep_search`、`view_file` | flash | なし |
| `gravitas-reader` | 限られたファイルや URL について具体的な問いに答え、依拠した行を引用する | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content` | flash | なし |
| `gravitas-finder` | 与えられた作業リストで、ひとつの種類の欠陥を探すか、ひとつの角度から探す | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content`、`search_web` | flash | なし |
| `gravitas-checker` | 独立した検証をひとつ走らせる：数値評価、テスト、再計算、クエリ | `view_file`、`run_command` | flash | 役割の規定で作業用ファイルのみ |
| `gravitas-refuter` | ひとつの主張の反証を試み、確信がなければ反証済みとする | `view_file`、`grep_search`、`read_url_content`、`search_web` | pro | なし |
| `gravitas-visual-critic` | ソースを見ていない閲覧者として取得画像を判断する | `view_file` | pro | なし |
| `gravitas-completeness-critic` | 台帳を読み、探されず、開かれず、走らされず、検証されなかったものを挙げる | `view_file`、`list_dir`、`grep_search`、`find_by_name` | pro | なし |
| `gravitas-prose-editor` | 草稿を文章の基準に合わせて直し、直した文章を返す | `view_file` | pro | なし |

`gravitas-checker` はコマンドラインを持つ唯一の検証役なので、読み取り専用であることはツールの制限ではなく役割の規定です。範囲を狭く保ち、その結果が結論を支えるときはトランスクリプトを読みます。

実装は親か、`Model: "inherit"` の `self` に任せます。そうすればファイルを変える作業にはユーザーが選んだモデルが使われます。

## モデルの振り分け

| 作業 | モデル |
| :--- | :--- |
| 機械的な抽出、ファイルの仕分け、一覧作成 | `flash_lite` |
| 偵察、読み取り、探索、検証 | `flash` |
| 反証、批評、審査、最終的な統合 | `pro` |
| ファイルを書くものすべて | `inherit` |

ファイルの仕分けに `pro` の料金を払うのは無駄です。視覚批評を `flash_lite` で走らせると、その役割が存在する理由である判断力を捨てることになります。書き込む役割の既定が `inherit` なのは、ユーザーが選んだモデルを黙って格下げするのは、ユーザーがしていない決定だからです。
