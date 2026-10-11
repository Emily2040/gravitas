#!/bin/bash
# Gravitas installer for macOS. Double-click this file. It needs no Python and no agy.
#
# It copies dist/LANGUAGE/gravitas to the folder Antigravity loads plugins from,
# ~/.gemini/config/plugins/gravitas, in three steps, so that a failure at any point leaves the Mac
# as it was:
#   1. Copy into a new folder named for the date and time inside ~/.gemini/gravitas-backups, the
#      folder scripts/install.py uses too, and check the copy there.
#   2. Move any copy already installed, then the bare skill beta 1 installed at
#      ~/.gemini/config/skills/gravitas, into that backup folder.
#   3. Move the new copy into place. If step 2 or 3 fails, whatever was moved is moved back.
# Then beta 1's hook goes: its gravitas-always-on entry is taken out of ~/.gemini/config/hooks.json,
# with a copy of the file kept in the backup folder, and the script it ran is moved there.
# "Remove Gravitas" moves all of these into a backup folder. Nothing is deleted except this
# installer's own temporary copy.
#
# scripts/build_dist.py writes dist/ with install.py's own code, so this installs the same files
# as "python3 scripts/install.py LANGUAGE" with no options. The default choice follows the macOS
# language; GRAVITAS_LANG=en, zh-CN, ja or ko overrides it, which the tests use.
#
# hooks.json is edited with JavaScript for Automation (osascript -l JavaScript), which every Mac
# has; where it is missing or fails, the entry is reported instead of removed.
#
# Written for the bash 3.2 that ships with macOS. Keep LF line endings and the executable bit
# (git update-index --chmod=+x), or a double-click will not run it.

HERE="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)"
GEMINI="$HOME/.gemini"
CONFIG="$GEMINI/config"
PLUGINS="$CONFIG/plugins"
DEST="$PLUGINS/gravitas"
OLDSKILL="$CONFIG/skills/gravitas"
HOOKS="$CONFIG/hooks.json"
HOOKPY="$CONFIG/scripts/gravitas_always_on.py"
BACKUPS="$GEMINI/gravitas-backups"
RELEASES="https://github.com/Emily2040/gravitas/releases"
BACKUP=""
NEW=""
MOVED_PLUGIN=""
MOVED_SKILL=""
KEPT=""
RESTOREFAIL=""
HOOKDONE=""
HOOKNOTE=""
RC=0

say() { printf '%s\n' "$1"; }

# The language macOS shows its menus in, else the terminal's locale.
ui_language() {
  local l="${GRAVITAS_LANG:-}"
  if [ -z "$l" ] && command -v defaults >/dev/null 2>&1; then
    l="$(defaults read -g AppleLanguages 2>/dev/null | sed -n 2p | tr -d ' ",')"
  fi
  [ -n "$l" ] || l="${LC_ALL:-${LC_MESSAGES:-${LANG:-en}}}"
  case "$l" in
    zh*) echo zh-CN ;;
    ja*) echo ja ;;
    ko*) echo ko ;;
    *) echo en ;;
  esac
}

text() {
  case "$1" in
  en)
    M_HEAD="Gravitas installer"
    M_INTRO="This adds Gravitas to Antigravity. Nothing else on this Mac is changed."
    M_ASK="What would you like to do?"
    M_OPT5="Remove Gravitas"
    M_LANGNOTE="Choose the language you read most easily. Whichever you choose, Antigravity keeps answering in the language you write to it."
    M_PROMPT="Type a number and press Return. If you are not sure, just press Return (that chooses ${DEF})."
    M_CANCEL="To stop without changing anything, close this window."
    M_BAD="Please type a number from 1 to 5."
    M_STOPPED="Stopped. Nothing was changed."
    M_ALONE1="This installer needs the rest of Gravitas next to it, so nothing was changed."
    M_ALONE2="Double-click the Gravitas ZIP file in your Downloads folder to unzip it, then double-click Install Gravitas (Mac) in the folder that appears. If you downloaded only this one file, download all of Gravitas from this page instead:"
    M_INCOMPLETE="This download of Gravitas is incomplete, so nothing was changed. Download it again from this page:"
    M_NOACCESS1="macOS did not let Terminal read the Gravitas folder, so nothing was changed."
    M_NOACCESS2="Open System Settings, click Privacy & Security, then Files & Folders. Under Terminal, turn on Downloads Folder. Then double-click the installer again."
    M_COPYING="Copying Gravitas..."
    M_CHECKING="Checking the copied files..."
    M_MOVING="Moving your old copy of Gravitas into the backup folder..."
    M_INSTALLED="Done. Gravitas is installed in:"
    M_KEPT="Your old Gravitas files are kept in:"
    M_FINDER="Finder hides this folder. To open it, choose Go > Go to Folder in Finder (Shift-Command-G) and paste the path above."
    M_HOOKDONE="The old beta 1 hook, gravitas-always-on, is gone too. A copy of the hooks.json it was in is kept in that folder."
    M_RESTART="Now restart Antigravity so it picks up the change:"
    M_RESTART1="  1. If Antigravity is running, click its icon in the menu bar at the top right of the screen and choose Quit. If its window is in front, Command-Q does the same."
    M_RESTART2="  2. Open Antigravity again from your Applications folder."
    M_REMOVED="Done. Gravitas is removed from Antigravity. Its files were moved to:"
    M_DELETEOK="You can delete that folder whenever you like."
    M_NOTHING="Gravitas is not installed on this Mac, so there was nothing to remove."
    M_ERRBACKUP="The backup folder could not be made, so nothing was changed. It goes inside:"
    M_ERRCOPY="Copying Gravitas failed, so nothing was changed. Check that your Mac has free disk space, then run this installer again."
    M_ERRCHECK="Some files did not copy correctly, so nothing was changed. Run this installer again."
    M_ERRMOVE="This folder could not be moved, so nothing was changed:"
    M_OWNER="It may belong to another user account, for example after an earlier install with sudo. The Gravitas page on GitHub explains how to fix that."
    M_ERRPLACE="Gravitas could not be put into this folder, so nothing was changed:"
    M_ERRRESTORE="Something that was moved could not be put back. It is in:"
    M_HOOK1="Note: Gravitas beta 1 left a hook named gravitas-always-on in this file, and it could not be removed for you:"
    M_HOOK2="It still runs on every request. The Gravitas page on GitHub explains how to remove it."
    M_KEY="Press any key to finish. You can then close this Terminal window."
    ;;
  zh-CN)
    M_HEAD="Gravitas 安装程序"
    M_INTRO="本程序会把 Gravitas 装进 Antigravity，这台 Mac 上的其他内容一概不动。"
    M_ASK="你想做什么？"
    M_OPT5="卸载 Gravitas"
    M_LANGNOTE="选你看着最习惯的语言就行。不管选哪种，Antigravity 都会用你提问时用的语言来回答。"
    M_PROMPT="输入编号后按 Return 键。拿不准的话，直接按 Return 键就行（会选 ${DEF}）。"
    M_CANCEL="如果不想继续，直接关掉这个窗口，什么都不会改动。"
    M_BAD="请输入 1 到 5 之间的数字。"
    M_STOPPED="已停止，没有做任何改动。"
    M_ALONE1="Gravitas 的其余文件不在这个安装程序旁边，所以没有做任何改动。"
    M_ALONE2="请在“下载”文件夹里连按 Gravitas 的 ZIP 文件把它解压，然后在出现的文件夹里连按 Install Gravitas (Mac)。如果你只下载了这一个文件，请到下面这个页面下载完整的 Gravitas："
    M_INCOMPLETE="这份 Gravitas 没有下载完整，所以没有做任何改动。请到下面这个页面重新下载："
    M_NOACCESS1="macOS 没有允许“终端”读取 Gravitas 文件夹，所以没有做任何改动。"
    M_NOACCESS2="请打开“系统设置”，依次点按“隐私与安全性”和“文件与文件夹”，在“终端”下面打开“下载”文件夹的开关，然后重新连按安装程序。"
    M_COPYING="正在复制 Gravitas……"
    M_CHECKING="正在核对复制的文件……"
    M_MOVING="正在把旧版 Gravitas 移到备份文件夹……"
    M_INSTALLED="完成，Gravitas 已安装到："
    M_KEPT="旧版 Gravitas 的文件保存在："
    M_FINDER="访达默认不显示这个文件夹。要打开它，请在访达里选取“前往”>“前往文件夹”（Shift-Command-G），然后粘贴上面的路径。"
    M_HOOKDONE="beta 1 留下的旧钩子 gravitas-always-on 也已清除，原来那份 hooks.json 在上面这个文件夹里留了备份。"
    M_RESTART="最后重启一下 Antigravity，让改动生效："
    M_RESTART1="  1. 如果 Antigravity 正在运行，点按屏幕右上角菜单栏里的 Antigravity 图标，选择 Quit（菜单只有英文）。如果它的窗口在最前面，按 Command-Q 也可以。"
    M_RESTART2="  2. 再从“应用程序”文件夹重新打开 Antigravity。"
    M_REMOVED="完成，Gravitas 已从 Antigravity 卸载，文件移到了："
    M_DELETEOK="这个文件夹随时可以删除。"
    M_NOTHING="这台 Mac 上没有安装 Gravitas，不需要卸载。"
    M_ERRBACKUP="无法创建备份文件夹，所以没有做任何改动。备份文件夹应建在："
    M_ERRCOPY="复制 Gravitas 失败，所以没有做任何改动。请确认 Mac 的磁盘还有空间，再重新运行本安装程序。"
    M_ERRCHECK="有些文件没有正确复制，所以没有做任何改动。请重新运行本安装程序。"
    M_ERRMOVE="下面这个文件夹无法移动，所以没有做任何改动："
    M_OWNER="它可能属于另一个用户帐户，比如以前用 sudo 安装过。解决方法请看 GitHub 上 Gravitas 页面的说明。"
    M_ERRPLACE="Gravitas 没能放进下面这个文件夹，所以没有做任何改动："
    M_ERRRESTORE="有些已移走的文件没能放回原处，它们现在在："
    M_HOOK1="提示：Gravitas beta 1 在下面这个文件里留下了一个叫 gravitas-always-on 的钩子，没能替你自动清除："
    M_HOOK2="它在你每次提问时都会运行。清除方法请看 GitHub 上 Gravitas 页面的说明。"
    M_KEY="按任意键结束，然后就可以关闭这个“终端”窗口了。"
    ;;
  ja)
    M_HEAD="Gravitas インストーラ"
    M_INTRO="Antigravity に Gravitas を追加します。この Mac のほかの部分は変更しません。"
    M_ASK="実行する操作を選んでください。"
    M_OPT5="Gravitas をアンインストール"
    M_LANGNOTE="いちばん読みやすい言語を選んでください。どれを選んでも、Antigravity はあなたが書いた言語で返事をします。"
    M_PROMPT="番号を入力して Return キーを押してください。迷ったら、そのまま Return キーを押せば大丈夫です（${DEF} が選ばれます）。"
    M_CANCEL="何も変更せずにやめるときは、このウインドウを閉じてください。"
    M_BAD="1 から 5 までの番号を入力してください。"
    M_STOPPED="中止しました。何も変更していません。"
    M_ALONE1="このインストーラと同じ場所に Gravitas のほかのファイルがないため、何も変更していません。"
    M_ALONE2="「ダウンロード」フォルダにある Gravitas の ZIP ファイルをダブルクリックして展開し、現れたフォルダの中の Install Gravitas (Mac) をダブルクリックしてください。このファイルだけをダウンロードした場合は、代わりに次のページから Gravitas 一式をダウンロードしてください。"
    M_INCOMPLETE="ダウンロードした Gravitas の一部が欠けているため、何も変更していません。次のページからもう一度ダウンロードしてください。"
    M_NOACCESS1="macOS がターミナルに Gravitas のフォルダの読み取りを許可しなかったため、何も変更していません。"
    M_NOACCESS2="「システム設定」を開き、「プライバシーとセキュリティ」、「ファイルとフォルダ」の順にクリックして、「ターミナル」の下の「ダウンロードフォルダ」をオンにしてください。そのあと、もう一度インストーラをダブルクリックしてください。"
    M_COPYING="Gravitas をコピーしています…"
    M_CHECKING="コピーしたファイルを確認しています…"
    M_MOVING="以前の Gravitas をバックアップ用フォルダへ移しています…"
    M_INSTALLED="完了しました。Gravitas を次の場所にインストールしました。"
    M_KEPT="以前の Gravitas のファイルは次の場所に保管してあります。"
    M_FINDER="このフォルダは Finder には表示されません。開くには、Finder の「移動」メニューから「フォルダへ移動」（Shift + Command + G）を選び、上のパスを貼り付けてください。"
    M_HOOKDONE="beta 1 の古いフック gravitas-always-on も削除しました。それが書かれていた hooks.json のコピーは、上のフォルダに保管してあります。"
    M_RESTART="最後に Antigravity を再起動して、変更を反映させてください。"
    M_RESTART1="  1. Antigravity が動いている場合は、画面右上のメニューバーにある Antigravity のアイコンをクリックして Quit を選びます（メニューは英語で表示されます）。ウインドウが手前にあるときは Command + Q でも終了できます。"
    M_RESTART2="  2. 「アプリケーション」フォルダから Antigravity をもう一度開きます。"
    M_REMOVED="完了しました。Antigravity から Gravitas をアンインストールし、ファイルを次の場所に移しました。"
    M_DELETEOK="このフォルダはいつ削除してもかまいません。"
    M_NOTHING="この Mac には Gravitas がインストールされていないため、アンインストールするものはありません。"
    M_ERRBACKUP="バックアップ用フォルダを作成できなかったため、何も変更していません。作成先は次の場所です。"
    M_ERRCOPY="Gravitas のコピーに失敗したため、何も変更していません。Mac のディスクに空きがあるか確認してから、もう一度このインストーラを実行してください。"
    M_ERRCHECK="一部のファイルが正しくコピーされなかったため、何も変更していません。もう一度このインストーラを実行してください。"
    M_ERRMOVE="次のフォルダを移動できなかったため、何も変更していません。"
    M_OWNER="このフォルダは、ほかのユーザアカウントの所有になっている可能性があります（以前 sudo でインストールした場合など）。直し方は GitHub の Gravitas のページで説明しています。"
    M_ERRPLACE="Gravitas を次のフォルダに置けなかったため、何も変更していません。"
    M_ERRRESTORE="移動したものの一部を元に戻せませんでした。次の場所にあります。"
    M_HOOK1="補足：Gravitas beta 1 が次のファイルに残したフック gravitas-always-on を、自動では削除できませんでした。"
    M_HOOK2="このフックは依頼のたびに動きます。削除のしかたは GitHub の Gravitas のページで説明しています。"
    M_KEY="何かキーを押すと終了します。そのあと、このターミナルのウインドウを閉じてかまいません。"
    ;;
  ko)
    M_HEAD="Gravitas 설치 프로그램"
    M_INTRO="Antigravity에 Gravitas를 추가합니다. 이 Mac의 다른 부분은 건드리지 않습니다."
    M_ASK="원하는 작업을 선택하세요."
    M_OPT5="Gravitas 제거"
    M_LANGNOTE="가장 편하게 읽히는 언어를 고르세요. 어떤 언어를 고르든 Antigravity는 사용자가 쓴 언어로 답합니다."
    M_PROMPT="번호를 입력하고 Return 키를 누르세요. 잘 모르겠으면 그냥 Return 키만 누르면 됩니다(${DEF}번이 선택됩니다)."
    M_CANCEL="아무것도 바꾸지 않고 그만두려면 이 창을 닫으세요."
    M_BAD="1부터 5까지의 번호 중 하나를 입력하세요."
    M_STOPPED="중단했습니다. 아무것도 바꾸지 않았습니다."
    M_ALONE1="이 설치 프로그램과 같은 폴더에 Gravitas의 나머지 파일이 없어서 아무것도 바꾸지 않았습니다."
    M_ALONE2="다운로드 폴더에 있는 Gravitas ZIP 파일을 이중 클릭해 압축을 풀고, 나타난 폴더에서 Install Gravitas (Mac)을 이중 클릭하세요. 이 파일 하나만 내려받았다면, 대신 아래 페이지에서 Gravitas 전체를 내려받으세요."
    M_INCOMPLETE="내려받은 Gravitas에 빠진 파일이 있어서 아무것도 바꾸지 않았습니다. 아래 페이지에서 다시 내려받으세요."
    M_NOACCESS1="macOS가 터미널에 Gravitas 폴더를 읽을 권한을 주지 않아 아무것도 바꾸지 않았습니다."
    M_NOACCESS2="시스템 설정을 열고 개인정보 보호 및 보안, 파일 및 폴더를 차례로 클릭한 다음, 터미널 아래의 다운로드 폴더를 켜세요. 그런 다음 설치 프로그램을 다시 이중 클릭하세요."
    M_COPYING="Gravitas를 복사하는 중..."
    M_CHECKING="복사한 파일을 확인하는 중..."
    M_MOVING="이전 Gravitas를 백업 폴더로 옮기는 중..."
    M_INSTALLED="완료되었습니다. Gravitas가 다음 위치에 설치되었습니다."
    M_KEPT="이전 Gravitas 파일은 다음 위치에 보관해 두었습니다."
    M_FINDER="이 폴더는 Finder에 보이지 않습니다. 열려면 Finder에서 이동 > 폴더로 이동(Shift-Command-G)을 선택하고 위 경로를 붙여 넣으세요."
    M_HOOKDONE="beta 1의 이전 훅 gravitas-always-on도 지웠습니다. 이 훅이 들어 있던 hooks.json의 사본은 위 폴더에 보관해 두었습니다."
    M_RESTART="이제 Antigravity를 다시 시작해야 변경 사항이 적용됩니다."
    M_RESTART1="  1. Antigravity가 실행 중이라면 화면 오른쪽 위 메뉴 막대에서 Antigravity 아이콘을 클릭하고 Quit을 선택하세요(메뉴는 영어로만 나옵니다). 창이 맨 앞에 있을 때는 Command-Q를 눌러도 됩니다."
    M_RESTART2="  2. 응용 프로그램 폴더에서 Antigravity를 다시 여세요."
    M_REMOVED="완료되었습니다. Antigravity에서 Gravitas를 제거하고, 파일은 다음 위치로 옮겼습니다."
    M_DELETEOK="이 폴더는 언제 지워도 괜찮습니다."
    M_NOTHING="이 Mac에는 Gravitas가 설치되어 있지 않아 제거할 것이 없습니다."
    M_ERRBACKUP="백업 폴더를 만들지 못해 아무것도 바꾸지 않았습니다. 백업 폴더는 다음 위치에 만들어집니다."
    M_ERRCOPY="Gravitas를 복사하지 못해 아무것도 바꾸지 않았습니다. Mac의 디스크 공간이 남아 있는지 확인한 뒤 이 설치 프로그램을 다시 실행하세요."
    M_ERRCHECK="일부 파일이 제대로 복사되지 않아 아무것도 바꾸지 않았습니다. 이 설치 프로그램을 다시 실행하세요."
    M_ERRMOVE="다음 폴더를 옮기지 못해 아무것도 바꾸지 않았습니다."
    M_OWNER="이 폴더가 다른 사용자 계정의 소유일 수 있습니다(예: 예전에 sudo로 설치한 경우). 해결 방법은 GitHub의 Gravitas 페이지에 나와 있습니다."
    M_ERRPLACE="Gravitas를 다음 폴더에 넣지 못해 아무것도 바꾸지 않았습니다."
    M_ERRRESTORE="옮겼던 파일 일부를 원래 자리로 되돌리지 못했습니다. 지금은 다음 위치에 있습니다."
    M_HOOK1="참고: Gravitas beta 1이 다음 파일에 남긴 훅 gravitas-always-on을 자동으로 지우지 못했습니다."
    M_HOOK2="이 훅은 요청할 때마다 실행됩니다. 지우는 방법은 GitHub의 Gravitas 페이지에 나와 있습니다."
    M_KEY="아무 키나 누르면 끝납니다. 그다음 이 터미널 창을 닫아도 됩니다."
    ;;
  esac
}

finish() {
  say ""
  say "$M_KEY"
  read -r -s -n 1 _ 2>/dev/null || true
  exit "$RC"
}

# A new folder for this run, named for the date and time when it is made. mkdir without -p fails
# when the folder exists, so another run in the same second, even one at the same moment, gets its own.
make_backup() {
  [ -z "$BACKUP" ] || return 0
  local stamp try n=1
  stamp="$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$BACKUPS" 2>/dev/null || return 1
  try="$BACKUPS/$stamp"
  until mkdir "$try" 2>/dev/null; do
    n=$((n + 1))
    [ "$n" -le 99 ] || return 1
    try="$BACKUPS/$stamp-$n"
  done
  BACKUP="$try"
}

# Deletes this run's own unused copy, then the backup folder if nothing was put in it, then the
# backups folder if that left it empty. rmdir removes only an empty folder. What the messages say
# was kept follows KEPT, not whether the folder is still there.
tidy() {
  [ -z "$NEW" ] || [ ! -d "$NEW" ] || rm -rf "$NEW"
  NEW=""
  if [ -n "$BACKUP" ]; then
    rmdir "$BACKUP" 2>/dev/null
    [ -d "$BACKUP" ] || BACKUP=""
  fi
  rmdir "$BACKUPS" 2>/dev/null
  return 0
}

there() { [ -e "$1" ] || [ -L "$1" ]; }

# Puts back what this run moved, last moved first. Something that cannot go back stays in the
# backup folder, and RESTOREFAIL makes fail say where.
rollback() {
  if [ -n "$MOVED_SKILL" ]; then
    there "$OLDSKILL" || mv "$BACKUP/skills-gravitas" "$OLDSKILL" 2>/dev/null
    ! there "$BACKUP/skills-gravitas" || RESTOREFAIL=1
  fi
  if [ -n "$MOVED_PLUGIN" ]; then
    there "$DEST" || mv "$BACKUP/gravitas" "$DEST" 2>/dev/null
    ! there "$BACKUP/gravitas" || RESTOREFAIL=1
  fi
  MOVED_SKILL=""
  MOVED_PLUGIN=""
  tidy
}

# Prints the messages given, then where anything that could not be put back is, and stops.
fail() {
  say ""
  for m in "$@"; do say "$m"; done
  if [ -n "$RESTOREFAIL" ]; then
    say "$M_ERRRESTORE"
    say "      $BACKUP"
  fi
  RC=1
  finish
}

# Moves $1 into the backup folder as $2. On failure puts back what was moved and stops.
move_in() {
  if ! mv "$1" "$BACKUP/$2" 2>/dev/null || there "$1"; then
    rollback
    fail "$M_ERRMOVE" "      $1" "$M_OWNER"
  fi
}

# JavaScript for Automation: takes the gravitas-always-on entry out of the hooks.json named by its
# argument and writes the file back the way scripts/install.py writes it (Python's json.dump with
# indent=2, then a newline), in one atomic write. Prints removed, or absent when there is no such
# entry at the top level; throws, so osascript exits 1, when it cannot.
read -r -d '' HOOK_JS <<'JS'
function run(argv) {
  ObjC.import("Foundation");
  var path = argv[0];
  var text = ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(path, $.NSUTF8StringEncoding, null));
  if (typeof text !== "string") throw new Error("cannot read " + path);
  if (text.charCodeAt(0) === 0xFEFF) text = text.slice(1);
  var data = JSON.parse(text);
  if (data === null || typeof data !== "object" || Array.isArray(data)) throw new Error("not a JSON object");
  if (!Object.prototype.hasOwnProperty.call(data, "gravitas-always-on")) return "absent";
  delete data["gravitas-always-on"];
  var out = JSON.stringify(data, null, 2).replace(/[\u007f-\uffff]/g, function (c) {
    return "\\u" + ("000" + c.charCodeAt(0).toString(16)).slice(-4);
  }) + "\n";
  if (!$(out).writeToFileAtomicallyEncodingError(path, true, $.NSUTF8StringEncoding, null)) {
    throw new Error("cannot write " + path);
  }
  return "removed";
}
JS

# Beta 1's hook: an entry named gravitas-always-on in hooks.json, and the script it runs. If the
# entry cannot be taken out, it stays, the script it runs stays with it, and hook_note says so.
retire_hook() {
  if [ -f "$HOOKS" ] && grep -q "gravitas-always-on" "$HOOKS" 2>/dev/null; then
    local said=""
    if command -v osascript >/dev/null 2>&1 && make_backup && cp -p "$HOOKS" "$BACKUP/hooks.json" 2>/dev/null; then
      said="$(osascript -l JavaScript -e "$HOOK_JS" "$HOOKS" 2>/dev/null)"
    fi
    if [ "$said" = removed ]; then
      HOOKDONE=1
      KEPT=1
    else
      [ -z "$BACKUP" ] || rm -f "$BACKUP/hooks.json"  # this run's own copy of a file left unchanged
      # absent: the name is only inside another hook's text, so there is no entry to take out
      if [ "$said" != absent ]; then
        HOOKNOTE=1
        return 0
      fi
    fi
  fi
  if there "$HOOKPY" && make_backup && mv "$HOOKPY" "$BACKUP/gravitas_always_on.py" 2>/dev/null; then
    KEPT=1
  fi
  return 0
}

hook_note() {
  [ -n "$HOOKNOTE" ] || return 0
  say ""
  say "$M_HOOK1"
  say "      $HOOKS"
  say "$M_HOOK2"
}

restart_note() {
  say ""
  say "$M_RESTART"
  say "$M_RESTART1"
  say "$M_RESTART2"
}

UI="$(ui_language)"
case "$UI" in
  zh-CN) DEF=2 ;;
  ja) DEF=3 ;;
  ko) DEF=4 ;;
  *) DEF=1 ;;
esac
text "$UI"

# Terminal may not be allowed to read the Downloads folder (System Settings, Privacy & Security).
if ! ls "$HERE" >/dev/null 2>&1; then
  RC=1
  say ""
  say "$M_NOACCESS1"
  say "$M_NOACCESS2"
  finish
fi
# A download of the source without dist/ is incomplete; this file on its own is not.
if [ ! -f "$HERE/dist/en/gravitas/plugin.json" ]; then
  RC=1
  say ""
  if [ -d "$HERE/dist" ] || [ -f "$HERE/plugin/plugin.json" ]; then
    say "$M_INCOMPLETE"
  else
    say "$M_ALONE1"
    say "$M_ALONE2"
  fi
  say "      $RELEASES"
  finish
fi

say ""
say "$M_HEAD"
say ""
say "$M_INTRO"
say ""
say "$M_ASK"
say ""
say "    1  Install Gravitas in English"
say "    2  安装 Gravitas（简体中文版）"
say "    3  日本語版の Gravitas をインストール"
say "    4  한국어판 Gravitas 설치"
say "    5  $M_OPT5"
say ""
say "$M_LANGNOTE"
say ""

# Empty input takes the default. Full-width digits and spaces, which a Chinese, Japanese or Korean
# input method may type, count too. The end of input (Control-D) stops without changing anything,
# and a last answer with no newline after it still counts.
PICK=""
while [ -z "$PICK" ]; do
  say "$M_PROMPT"
  say "$M_CANCEL"
  printf '> '
  CHOICE=""
  if ! IFS= read -r CHOICE && [ -z "$CHOICE" ]; then
    say ""
    say "$M_STOPPED"
    RC=1
    finish
  fi
  CHOICE="${CHOICE//[[:space:]]/}"
  CHOICE="${CHOICE//　/}"
  case "$CHOICE" in
    "") PICK="$DEF" ;;
    1|１) PICK=1 ;;
    2|２) PICK=2 ;;
    3|３) PICK=3 ;;
    4|４) PICK=4 ;;
    5|５) PICK=5 ;;
    *) say "$M_BAD" ;;
  esac
done

if [ "$PICK" = 5 ]; then
  say ""
  if ! there "$DEST" && ! there "$OLDSKILL" && ! there "$HOOKPY" \
      && ! { [ -f "$HOOKS" ] && grep -q "gravitas-always-on" "$HOOKS" 2>/dev/null; }; then
    say "$M_NOTHING"
    finish
  fi
  make_backup || fail "$M_ERRBACKUP" "      $BACKUPS" "$M_OWNER"
  if there "$DEST"; then
    move_in "$DEST" gravitas
    MOVED_PLUGIN=1
    KEPT=1
  fi
  if there "$OLDSKILL"; then
    move_in "$OLDSKILL" skills-gravitas
    MOVED_SKILL=1
    KEPT=1
  fi
  retire_hook
  tidy
  if [ -n "$KEPT" ]; then
    say "$M_REMOVED"
    say "      $BACKUP"
    say "$M_FINDER"
    say "$M_DELETEOK"
  fi
  [ -z "$HOOKDONE" ] || say "$M_HOOKDONE"
  hook_note
  restart_note
  finish
fi

case "$PICK" in
  1) LANGDIR=en ;;
  2) LANGDIR=zh-CN ;;
  3) LANGDIR=ja ;;
  4) LANGDIR=ko ;;
esac
text "$LANGDIR"
SRC="$HERE/dist/$LANGDIR/gravitas"
if [ ! -f "$SRC/plugin.json" ]; then
  RC=1
  say ""
  say "$M_INCOMPLETE"
  say "      $RELEASES"
  finish
fi

# Step 1: copy into the backup folder and check the copy there. A download carries the quarantine
# mark onto every unzipped file, and cp copies it; the copy does not need it.
say ""
make_backup || fail "$M_ERRBACKUP" "      $BACKUPS" "$M_OWNER"
NEW="$BACKUP/gravitas-new"
say "$M_COPYING"
if ! cp -R "$SRC" "$NEW" 2>/dev/null; then
  tidy
  fail "$M_ERRCOPY"
fi
if command -v xattr >/dev/null 2>&1; then
  xattr -dr com.apple.quarantine "$NEW" 2>/dev/null
fi
say "$M_CHECKING"
if ! diff -r "$SRC" "$NEW" >/dev/null 2>&1 || [ ! -f "$NEW/plugin.json" ] \
    || [ ! -f "$NEW/rules/AGENTS.md" ] || [ ! -f "$NEW/skills/gravitas/SKILL.md" ]; then
  tidy
  fail "$M_ERRCHECK"
fi

# Step 3 will need leave to make a folder in plugins. That is tried now, before step 2 moves
# anything, under a name as unique as this run's backup folder.
mkdir -p "$PLUGINS" 2>/dev/null
TESTDIR="$PLUGINS/.gravitas-test-${BACKUP##*/}"
if ! mkdir "$TESTDIR" 2>/dev/null; then
  tidy
  fail "$M_ERRPLACE" "      $PLUGINS" "$M_OWNER"
fi
rmdir "$TESTDIR" 2>/dev/null

# Step 2: the installed plugin first, then beta 1's skill.
if there "$DEST"; then
  say "$M_MOVING"
  move_in "$DEST" gravitas
  MOVED_PLUGIN=1
  KEPT=1
fi
if there "$OLDSKILL"; then
  move_in "$OLDSKILL" skills-gravitas
  MOVED_SKILL=1
  KEPT=1
fi

# Step 3: a rename on the same disk. If another run put a plugin here meanwhile, mv either fails,
# leaving this copy where it was, or puts it inside the other as gravitas-new. Both are caught, and
# what was moved is put back.
if there "$DEST" || ! mv "$NEW" "$DEST" 2>/dev/null; then
  rollback
  fail "$M_ERRPLACE" "      $PLUGINS" "$M_OWNER"
fi
if there "$DEST/gravitas-new" || there "$NEW"; then
  there "$NEW" || mv "$DEST/gravitas-new" "$NEW" 2>/dev/null
  rollback
  fail "$M_ERRPLACE" "      $PLUGINS" "$M_OWNER"
fi
NEW=""

retire_hook
tidy
say ""
say "$M_INSTALLED"
say "      $DEST"
if [ -n "$KEPT" ]; then
  say "$M_KEPT"
  say "      $BACKUP"
  say "$M_FINDER"
fi
[ -z "$HOOKDONE" ] || say "$M_HOOKDONE"
hook_note
restart_note
finish
