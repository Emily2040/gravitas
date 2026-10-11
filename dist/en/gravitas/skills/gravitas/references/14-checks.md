# Module 14 - Language Checks

## Purpose

Some forms are counted, and a model miscounts them while sounding sure: the tones of a 绝句, the morae of a haiku, the syllables of a 시조, the zeros in 1.5 crore written as 万. Six scripts in `scripts/checks/` do the counting. They need Python 3.8 or later and nothing else, and their data ships with them.

Run each one by its full path inside the installed plugin, `<home>/.gemini/config/plugins/gravitas/skills/gravitas/scripts/checks/<script>`. The examples below shorten the path. Running a script needs `run_command`, which a headless run at default settings refuses (`13-platform.md`). When no command can run, apply the same rules by hand and record in the coverage section that the script did not run.

## When To Run Each Check

| Script | Run It When | Give It |
| :--- | :--- | :--- |
| `pingze_check.py` | You write or review a 绝句 or 律诗 | The poem in simplified characters; `--scheme xinyun` when the person asked for 中华新韵 |
| `couplet_check.py` | You write or review a 对联, 春联 or 开业联 | The 上联 and 下联 as two arguments, `--hengpi`, and `--require` for characters that must be embedded |
| `mora_count.py` | You write or review a haiku, tanka or senryu | A kana reading of each line, written for the check only |
| `sijo_check.py` | You write or review a 평시조 | The three 장, with each 음보 marked by `\|` in a check copy |
| `num_units.py` | An amount moves between 万, 亿, 億, 兆, 만, 억, 조, lakh, crore and million, or a 人民币 大写 or Korean 공문 amount is written | Digits with units, such as `4.8万` or `1.5 crore` |
| `locale_dates.py` | Dates are written for zh-CN, ja or ko readers, or a date is given in 和暦 | An ISO date for `show`, or a language and the text for `lint` |

```bash
python scripts/checks/pingze_check.py "秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。"
python scripts/checks/couplet_check.py 知味停车香满座 闻香下马客盈门 --hengpi 宾至如归 --require 知味
python scripts/checks/mora_count.py haiku ふるいけや かわずとびこむ みずのおと
python scripts/checks/sijo_check.py "이 몸이|죽고 죽어|일백 번|고쳐 죽어" "백골이|진토되어|넋이라도|있고 없고" "임 향한|일편단심이야|가실 줄이|있으랴"
python scripts/checks/num_units.py same "1.5 crore" "1500万" "15,000,000"
python scripts/checks/locale_dates.py lint ko "퇴사일(2026.9.30)로부터 14일"
```

Each script also takes `--json` for a ledger record, and `--help`.

## Reading The Output

The first line is the verdict, and it can be quoted as it stands: `PASS`, `FAIL` or `ERROR`. Lines starting `- ` under a `FAIL` name the line, position or value and the rule it breaks. Lines starting `note:` never fail anything; they name what the script could not judge.

| Exit | Verdict | What To Do |
| :--- | :--- | :--- |
| 0 | `PASS` | Read the notes, then keep the text |
| 1 | `FAIL` | Fix each named problem and run the script again, until it passes or the remaining problem is deliberate and you can say why |
| 2 | `ERROR` | The input needs fixing: kanji left in a mora reading, Latin letters in a 음보, or a number or date the script cannot read |

In the report file or ledger, label a result `executed` and give the command that ran with it (`01-evidence.md`); the reply carries no tier label. `parse`, `show`, `daxie` and `ko-amount` in `num_units.py`, and `show` in `locale_dates.py`, only convert: they print the forms and exit 0.

## What Each Verdict Covers

Chinese verse is judged by one rhyme system at a time. `pingshui` (平水韵, the default) counts 入声 characters such as 国, 白, 一 and 十 as 仄; `xinyun` (中华新韵) reads them in Mandarin, where they are 平. So a poem written to 平水韵 can fail 中华新韵 on its inner tones, and 窗 and 霜 rhyme in 中华新韵 but not in 平水韵. Check against the system the person asked for, and say in the reply which one the poem follows.

`pingze_check.py` enforces the line count, 二四六分明, 粘 and 对, one 平声 rhyme group, 仄 endings on the lines that do not rhyme, 三平尾 and 孤平. It does not model 拗救, so a 拗 that a 救 offsets still shows as a problem, with a note saying so. A character with readings in both tones counts as either. A character missing from the table also counts as either, so it never fails a poem; it is named in a note, and when a rule reads it, a `PASS` names it in its first line as unchecked. Judge that character's tone by hand, and never change a character only to clear the note. A traditional character is the usual cause, so write the check copy in simplified characters; the table also keeps some classical variants (翦 and 谿 are in it, 剪 and 溪 are not), so a simplified copy does not always clear it.

`couplet_check.py` checks 平仄相对 only at positions 2, 4 and 6, which is the lenient reading. With the default `--scheme both` it reports a tone problem only when it fails under both systems, and a failure under one system is a note. Positions past 6 in a long couplet are not checked. It also fails a character that stands at the same position in both lines (同位重字), except a 虚词 such as 之, 而 or 不, which is a note; other 不规则重字 are notes, as in 知味停车香满座 / 闻香下马客盈门. A deliberate or requested 同位重字 can stay when you say why. When no system could judge a rule because a character is missing from the tables, the `PASS` line names it.

`mora_count.py` counts the reading you give it. The reading of a kanji is your claim, so a wrong reading gives a wrong count. A `FAIL` means 字余り or 字足らず: fix the line unless the 破調 is intended. It does not judge 季語 or 切れ字.

`sijo_check.py` counts syllables in the 음보 you marked, and the marking is a reading of the poem. Hard failures are the 장 and 음보 counts and the two 종장 rules; distance from 3·4·4·4 and a total outside 43 to 47 are notes.

`num_units.py same` is the check for a conversion you wrote: it passes only when every expression has the same value. A bare digit after a unit, as in `4万8`, is read as 48,000 and flagged as colloquial. After 零 the digits keep their written place (`4万零8` is 40,008). A 千 or 百 tail after 亿, 億, 억, 兆 or 조 with no 万 or 만, as in `3억 5천`, is read as spoken (350,000,000) and flagged with the written reading; 零 before it keeps the written reading. `daxie` handles whole yuan only. `ranges` applies GB/T 15835 to ranges joined by ～, a dash, 至 or 到: 13万～17万 and 15%到30%, not 13～17万 or 15到30%.

`locale_dates.py lint` knows a few patterns: a Korean dotted date without its last dot, with a leading zero, or with no space after the year or the month dot; a 和暦 year that contradicts the Western year beside it, 1年 written for an era's first year where prose writes 元年, a 和暦 date its era does not cover (平成元年1月5日 fell in 昭和), or 1月1日 written before 元旦; and a two-digit Chinese year before a month or before 出生, 毕业, 入学 or 入职. A `PASS` says only that none of those patterns appeared.

## What A PASS Does Not Show

Every check here is a count, and a count can pass while the piece fails (`05-acceptance.md`). A poem can hold every tone and still be flat, misuse an allusion or answer the wrong brief. A converted number can be exact and still be the wrong number. Read the piece as its reader would after the script passes.

## Data And Sources

`scripts/checks/data/pingshui.tsv` holds the 106 平水韵 groups from the zh.wikisource page 平水韻, revision 8264804, in its simplified rendering. The page carries the PD-old template; the file also carries Wikisource's CC BY-SA 4.0 terms, and its header records both. `scripts/checks/data/mandarin.tsv` holds Mandarin readings taken from pypinyin 0.55.0 (MIT, notice in the header), keeping a reading when pypinyin lists it first or its phrase dictionary uses it at least 3 times. `build_check_data.py`, in the repository's own scripts folder, rebuilds both files.
