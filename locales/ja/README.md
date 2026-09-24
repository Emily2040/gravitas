# Gravitas

[English](https://github.com/Emily2040/gravitas/blob/main/README.md) · [简体中文](https://github.com/Emily2040/gravitas/blob/main/README.zh-CN.md) · **日本語** · [한국어](https://github.com/Emily2040/gravitas/blob/main/README.ko.md)

これは、インストーラーがプラグインの中に置いた README の写しです。テスト結果とほかのスキルとの比較を含む完全版は [GitHub](https://github.com/Emily2040/gravitas) にあり、ベータの間は非公開です。

## 第 1 部：いまインストールしたもの

Gravitas は、Antigravity のエージェントに、「終わりました」と言う前に自分の仕事を証明させます。

AI のエージェントは、仕事の簡単な部分を確かめて問題がないと判断し、仕事全体に問題がないと報告することがあります。テストで一番多かった間違いは、開いてもいない資料を読んだとエージェントが言うことでした。Gravitas はエージェントに三つの習慣を身につけさせます。

1. どうして知っているのかを言う。すべての主張にラベルが付きます。自分で見た、実行した、読んだ（該当する一行はこれ）、あるいは自分で考えた、覚えていた、のどれかです。
2. 確かめやすい隣のものではなく、本物を確かめる。
3. ほかの誰かに崩させる。別の検査役のエージェントが間違いや抜けを探します。検査役には、ファイルを編集するツールがありません。

たとえば、10,000 人に 1 人がかかる病気の「精度 99%」の検査で陽性が出たなら、その病気である確率は 99% だ、という主張を確認するよう求められたとき、Gravitas は違うと答えました。本当の数字はおよそ 102 人に 1 人です。計算の過程を示し、計算した数字ごとに、あなたが自分で実行できるコマンドを添えました。

間違えると代償のある仕事では、自分から働き始めます。監査、デバッグ、多くのファイルにまたがる変更、デザインの作業、調査、法律、医学、数学、お金、歴史です。ちょっとした質問には、すぐに答えます。

確かめた答えは、すぐに出す答えより時間がかかり、プランも多く使います。上の例では約 100 秒、小さなプロジェクトの完全な監査では約 6 分でした。モデルを賢くすることも、誰にも確かめられないものを確かめることもできません。照らし合わせるものが何もないときは、その主張に推論というラベルを付けます。これはプライベートベータで、Windows 11 と Google の Gemini モデルでテストしました。

止めるには `agy plugin disable gravitas` を実行します。Antigravity がドキュメントに載せている、プラグイン用のコマンドです。もう一度有効にするには `agy plugin enable gravitas` を実行します。問題を報告するときは、作者の [GitHub プロフィール](https://github.com/Emily2040) にあるリンクを使ってください。

## 第 2 部：このフォルダの中身

```text
plugin.json                  manifest: the name and description Antigravity lists
rules/AGENTS.md              always-on rule: when to load the skill, and three rules that hold while it is in use
agents/                      eight agents with fixed tool lists
skills/gravitas/SKILL.md     the router; it loads references/00-orchestrator.md
skills/gravitas/references/  fourteen modules, each 100 lines or fewer so one view_file call reads it whole
skills/gravitas/schemas/     the finding and verdict records subagents return
skills/gravitas/scripts/     ledger.py, provenance_check.py, check_skills.py, slopcheck.py
skills/gravitas/examples/    a gate suite that goes red on the scene it was built from
```

実行はこう進みます。ルールは常に読み込まれています。条件に合うタスクでは、エージェントがスキルを開き、スキルがオーケストレーターに振り分けます。オーケストレーターは、些細な質問には直接答えます。そうでなければタスクの記録を書き、ファンアウト、票、停止の数字が決まった規模（quick、standard、full、exhaustive）を選び、読み込むモジュールを指定します。作業リストは実際のツールで作り、専門役は絶対パスと返却スキーマを持ってファンアウトし、結論を支える主張は独立した検証に回り、網羅性の批評役が一度も確かめられなかったものを挙げ、報告は発見を層と欠落とともに順位付けします。

| 層 | 必ず起きていなければならないこと |
| :--- | :--- |
| `observed` | 成果物そのものを調べ、ラベルがその名前を挙げている |
| `executed` | ツールが実行されて値を返し、ラベルがコマンドまたはクエリと、その戻り値を示している |
| `read` | 出典を取得し、ラベルが URL またはパスを挙げて一行を引用している |
| `inferred` | 推論または記憶。欄を埋められないものすべて |

どのエージェントも、ファイルを編集するツールを持っていません。チェッカーはコマンドを実行でき、審査中の仕事を決して変えないよう指示されています。文章の編集役は、編集した文章を書き込まずに返します。

| エージェント | 役割 | ツール |
| :--- | :--- | :--- |
| `gravitas-scout` | ファイル、ルート、シンボル、出典の場所を探す | `list_dir`、`find_by_name`、`grep_search`、`view_file` |
| `gravitas-reader` | 名指しされたファイルや URL についての問いに答え、行を引用する | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content` |
| `gravitas-finder` | 作業リストを対象に、ひとつの種類の欠陥を探す | 読み取り役のツールと `search_web` |
| `gravitas-checker` | 独立した検証をひとつ走らせる | `view_file`、`run_command` |
| `gravitas-refuter` | ひとつの主張の反証を試み、確信がなければ反証済みとする | `view_file`、`grep_search`、`read_url_content`、`search_web` |
| `gravitas-visual-critic` | ソースを見ていない閲覧者としてスクリーンショットを判断する | `view_file` |
| `gravitas-completeness-critic` | 探されず、開かれず、走らされず、検証されなかったものを挙げる | `view_file`、`list_dir`、`grep_search`、`find_by_name` |
| `gravitas-prose-editor` | 草稿を文章の基準に合わせて直す | `view_file` |

スクリプトはこのフォルダから実行します。`--latest` は最新の会話を対象に確かめます。会話の ID は、`~/.gemini/antigravity-cli/brain/` の下のフォルダ名か、`agy -p --output-format json` の出力にある `conversation_id` です。

```bash
python skills/gravitas/scripts/check_skills.py          # validate every skill, agent, rule and plugin under ~/.gemini/config
python skills/gravitas/scripts/provenance_check.py <answer> --latest   # check evidence labels against the transcript
python skills/gravitas/scripts/ledger.py --help         # bookkeeping for fan-outs: dedupe, votes, dry rounds
python skills/gravitas/scripts/slopcheck.py <files>     # structural markers of generated prose; --strict fails on any flag
```

これまでのテストでわかったこと。ベータ 2 のテストで得た回答に対して、出所チェッカーは、出典を開いていた法律の回答の 6 つのラベルすべてを通し、一度も開いていない引用を不合格にしました。完全な監査のテストケースは、仕込んだ三つの欠陥をすべて見つけました。Antigravity 単体とのきれいな比較はまだありません。そのベンチマークが次の仕事です。

限界について。方法の大半は、モデルに従うよう求める指示です。ツールリストと 4 つのスクリプトが機械的な部分で、スクリプトはエージェントが実行するよう指示されたときに走ります。テストは Windows 11 上の agy 1.2.9 で行いました。使い方に影響するプラットフォームの振る舞いは `skills/gravitas/references/13-platform.md` にあります。特に大事なのは二点です。ヘッドレスの `agy -p` の実行には、明示的な権限の付与か、`~/.gemini/antigravity-cli/settings.json` の `toolPermission` の設定が必要です。そして CLI は、リポジトリ自身の `.agents/` フォルダを、そのリポジトリを `--add-dir` で渡したときしか読みません。このプラグインがグローバルにインストールされるのは、そのためです。

バージョン 1.0.0-beta.2 · MIT · 作者 [Iamemily2050](https://github.com/Emily2040)
