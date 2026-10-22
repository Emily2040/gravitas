## DeepSeek Harness で使うとき

このスキルは Google Antigravity 向けに書かれています。DeepSeek Harness（DSH）でも使い方は同じで、ツール名だけを次のように読み替えます。

| モジュールの記載 | DSH での名前 |
| --- | --- |
| `view_file` | `read` |
| `list_dir`、`find_by_name` | `glob` |
| `grep_search` | `grep` |
| `run_command` | Windows では `pwsh`、それ以外では `bash` |
| `read_url_content`、`search_web` | `web_fetch`、`web_search` |
| `invoke_subagent` で `gravitas-*` エージェントを起動 | `gravitas_inspect` に `agent_preset` を指定（下記） |
| `invoke_subagent` で `TypeName: "self"` | `subagent` ツール |
| `define_subagent`、`Workspace: "branch"` | DSH にはありません |
| `Model: "flash"` または `"pro"` | `gravitas_inspect` は親エージェントのモデルを使います。ツールが `provider` と `model` を受け付ける場合に限り、別のモデルを選べます |

### 検査役の起動

1. 必要な役割のファイルを読みます。`AGENTS_DIR` には `gravitas-scout.md`、`gravitas-reader.md`、`gravitas-finder.md`、`gravitas-checker.md`、`gravitas-refuter.md`、`gravitas-visual-critic.md`、`gravitas-completeness-critic.md`、`gravitas-prose-editor.md` があります。
2. `gravitas_inspect` を呼び、次の三つを渡します。
   - `description`：3〜5 語の短い説明
   - `prompt`：役割ファイルのヘッダー以降の本文、続けて作業内容（確かめる主張、対象ファイル、問い）
   - `agent_preset`：
     - `gravitas-checker` はチェッカー専用です。コマンドを実行できます。Antigravity と同じく、レビュー対象を変更しないことはツールによる制限ではなく、役割上の決まりです。
     - それ以外の役割はすべて `gravitas-inspector` です。ファイルの読み取り、ワークスペースの検索、ウェブの利用ができ、ファイルを書いたり編集したりするツールはありません。
3. 呼び出しはすぐに検査役の ID を返し、結果は後から完了通知として届きます。互いに独立した検査役はまとめて起動し、すべての通知を受け取ってから判断します。

ビジュアル批評役は `read_image` で画像を読みますが、画像入力に対応したモデル経路でしか使えません。テキストのみの経路では、視覚チェックは実行していないと明記します。

### Antigravity との違い

- モジュール `13-platform.md` は Antigravity のバージョンと制約を扱っています。DSH では一般的な教訓だけを参考にしてください。
- モジュール `15-harness-probing.md` はそのまま当てはまります。頼りにする DSH の動作は、信じる前に確かめます。
- 検査役には常時適用ルールが届きますが、スキルは読み込めません。Gravitas のどちらのプリセットにもスキルツールがないためです。検査役に必要なモジュールの要点は、役割ファイルの後に続けて `prompt` に書きます。検査役はまず自分の役割ファイルに従います。
- `scripts/provenance_check.py` は Antigravity の会話記録しか読めず、DSH では検査役のツール操作を見る手段もありません。`gravitas_inspect` が返すのは検査役の id だけで、完了通知に入っているのはその回答だけです。そのため `01-evidence.md`、`02-evidence-traps.md`、`08-delegation.md` の出典確認は、DSH では手作業で行います。自分の回答のラベルは、自分が実際に行ったツール呼び出しと一つずつ照らし合わせます。検査役の重要な主張に頼る前に、その出典を自分で開くか、そのコマンドを自分で実行します。自分で確かめ直していない主張は、ラベルが何であれ `inferred` です。
- ヘッドレス実行（`dsh-headless` バンドル）には agent-presets サービスがないため、読み込まれるのはこのルールとスキルだけで、`gravitas_inspect` はありません。その場合は `subagent` ツールで検査役を起動し、役割ファイルの本文を作業内容の前に置きます。このツールはファイルを書けるので、読み取り専用はツールによる制限ではなく、役割上の決まりです。
