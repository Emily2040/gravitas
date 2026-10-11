@echo off
rem Gravitas installer for Windows. Double-click this file. It needs no Python, no terminal and no agy.
rem
rem It copies dist\LANGUAGE\gravitas to the folder Antigravity loads plugins from,
rem %USERPROFILE%\.gemini\config\plugins\gravitas, in three steps, so that a failure at any point
rem leaves the computer as it was:
rem   1. Copy into a new folder named for the date and time inside %USERPROFILE%\.gemini\gravitas-backups,
rem      the folder scripts\install.py uses too, and check the copy there.
rem   2. Move any copy already installed, then the bare skill beta 1 installed at
rem      %USERPROFILE%\.gemini\config\skills\gravitas, into that backup folder.
rem   3. Move the new copy into place. If step 2 or 3 fails, whatever was moved is moved back.
rem Then beta 1's hook goes: its gravitas-always-on entry is taken out of
rem %USERPROFILE%\.gemini\config\hooks.json, with a copy of the file kept in the backup folder, and the
rem script it ran is moved there. "Remove Gravitas" moves all of these into a backup folder. Nothing is
rem deleted except this installer's own temporary copy.
rem
rem scripts\build_dist.py writes dist\ with install.py's own code, so this installs the same files
rem as "python scripts\install.py LANGUAGE" with no options. The default choice follows the Windows
rem display language; GRAVITAS_LANG=en, zh-CN, ja or ko overrides it, which the tests use.
rem
rem PowerShell, which every Windows 10 and 11 has, gives the display language and the date and time,
rem takes the download mark off the copied files, and edits hooks.json with the code at the end of
rem this file. Without PowerShell the install still works: the language comes from the registry, the
rem backup folder is named "backup", and a beta 1 hook entry is reported instead of removed.
rem
rem cmd reads this file in the console code page until chcp 65001 has run, so everything above that
rem line stays ASCII, and the file keeps CRLF line endings (see .gitattributes). Paths are always
rem quoted, and printed through :say, so spaces, brackets, ampersands and non-ASCII names are safe.
rem Messages contain no straight double quotes or percent signs, for the same reason.

setlocal EnableExtensions DisableDelayedExpansion
set "OLDCP="
for /f "tokens=*" %%A in ('chcp') do for %%B in (%%A) do set "OLDCP=%%B"
if defined OLDCP set "OLDCP=%OLDCP:.=%"
chcp 65001 >nul
title Gravitas

set "HERE=%~dp0"
set "GV_SELF=%~f0"
set "GEMINI=%USERPROFILE%\.gemini"
set "CONFIG=%GEMINI%\config"
set "PLUGINS=%CONFIG%\plugins"
set "DEST=%PLUGINS%\gravitas"
set "OLDSKILL=%CONFIG%\skills\gravitas"
set "HOOKS=%CONFIG%\hooks.json"
set "HOOKPY=%CONFIG%\scripts\gravitas_always_on.py"
set "BACKUPS=%GEMINI%\gravitas-backups"
set "RELEASES=https://github.com/Emily2040/gravitas/releases"
set "PSEXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
set "BACKUP="
set "NEW="
set "MOVED_PLUGIN="
set "MOVED_SKILL="
set "KEPT="
set "RESTOREFAIL="
set "HOOKDONE="
set "HOOKNOTE="
set "RC=0"

rem The display language: PowerShell's UI culture, else the language list in the registry.
set "UICULTURE="
if defined GRAVITAS_LANG set "UICULTURE=%GRAVITAS_LANG%"
if not defined UICULTURE for /f "usebackq delims=" %%A in (`%PSEXE% -NoLogo -NoProfile -NonInteractive -Command "[Globalization.CultureInfo]::CurrentUICulture.Name" 2^>nul`) do set "UICULTURE=%%A"
if not defined UICULTURE for /f "tokens=3" %%A in ('reg query "HKCU\Control Panel\Desktop" /v PreferredUILanguages 2^>nul') do set "UICULTURE=%%A"
if not defined UICULTURE for /f "tokens=3" %%A in ('reg query "HKCU\Control Panel\Desktop\MuiCached" /v MachinePreferredUILanguages 2^>nul') do set "UICULTURE=%%A"
if not defined UICULTURE set "UICULTURE=en"

set "UI=en"
if /i "%UICULTURE:~0,2%"=="zh" set "UI=zh-CN"
if /i "%UICULTURE:~0,2%"=="ja" set "UI=ja"
if /i "%UICULTURE:~0,2%"=="ko" set "UI=ko"
set "DEF=1"
if "%UI%"=="zh-CN" set "DEF=2"
if "%UI%"=="ja" set "DEF=3"
if "%UI%"=="ko" set "DEF=4"
call :text_%UI%

rem Started from inside the ZIP, Explorer copies this one file to a temporary folder, without dist.
if not exist "%HERE%dist\en\gravitas\plugin.json" goto no_dist

echo(
call :say M_HEAD
echo(
call :say M_INTRO
echo(
call :say M_ASK
echo(
echo     1  Install Gravitas in English
echo     2  安装 Gravitas（简体中文版）
echo     3  日本語版の Gravitas をインストール
echo     4  한국어판 Gravitas 설치
set "LINE=    5  %M_OPT5%"
call :say LINE
echo(
call :say M_LANGNOTE
echo(

:ask
call :say M_PROMPT
call :say M_CANCEL
set "CHOICE="
set /p "CHOICE=> "
call :parse
if not defined PICK call :say M_BAD
if not defined PICK goto ask
if "%PICK%"=="5" goto remove

set "LANGDIR=en"
if "%PICK%"=="2" set "LANGDIR=zh-CN"
if "%PICK%"=="3" set "LANGDIR=ja"
if "%PICK%"=="4" set "LANGDIR=ko"
call :text_%LANGDIR%
set "SRC=%HERE%dist\%LANGDIR%\gravitas"
if not exist "%SRC%\plugin.json" goto incomplete

rem Step 1: copy into the backup folder and check the copy there.
echo(
call :make_backup || goto err_backup
set "NEW=%BACKUP%\gravitas-new"
call :say M_COPYING
robocopy "%SRC%" "%NEW%" /E /R:2 /W:1 /NFL /NDL /NJH /NJS /NP >nul 2>&1
if errorlevel 8 goto err_copy
call :say M_CHECKING
rem Listing again copies nothing; exit code 0 means every file is there with the same size and time.
robocopy "%SRC%" "%NEW%" /E /L /R:0 /W:0 /NFL /NDL /NJH /NJS /NP >nul 2>&1
if errorlevel 1 goto err_check
if not exist "%NEW%\plugin.json" goto err_check
if not exist "%NEW%\rules\AGENTS.md" goto err_check
if not exist "%NEW%\skills\gravitas\SKILL.md" goto err_check
rem Files unzipped from a download that was not unblocked carry its mark, and robocopy copies it.
set "GV_PATH=%NEW%"
"%PSEXE%" -NoLogo -NoProfile -NonInteractive -Command "Get-ChildItem -LiteralPath $env:GV_PATH -Recurse -Force -File | Unblock-File" >nul 2>&1

rem Step 3 will need leave to make a folder in plugins. That is tried now, before step 2 moves
rem anything, under a name as unique as this run's backup folder.
if not exist "%PLUGINS%\" mkdir "%PLUGINS%" >nul 2>&1
for %%I in ("%BACKUP%") do set "TESTDIR=%PLUGINS%\.gravitas-test-%%~nxI"
mkdir "%TESTDIR%" >nul 2>&1 || goto err_place
rd "%TESTDIR%" >nul 2>&1

rem Step 2: move the installed plugin first, since a running Antigravity may hold it, then beta 1's skill.
if not exist "%DEST%" goto install_skill
call :say M_MOVING
move "%DEST%" "%BACKUP%\gravitas" >nul 2>&1
if exist "%DEST%" goto err_move
set "MOVED_PLUGIN=1"
set "KEPT=1"
:install_skill
if not exist "%OLDSKILL%" goto install_place
move "%OLDSKILL%" "%BACKUP%\skills-gravitas" >nul 2>&1
if exist "%OLDSKILL%" goto err_move
set "MOVED_SKILL=1"
set "KEPT=1"

rem Step 3: a rename on the same drive. If another run put a plugin here meanwhile, move either
rem fails, leaving this copy where it was, or puts it inside the other as gravitas-new. Both are
rem caught, and what was moved is put back.
:install_place
if exist "%DEST%" goto err_place
move "%NEW%" "%DEST%" >nul 2>&1
if exist "%DEST%\gravitas-new\" move "%DEST%\gravitas-new" "%NEW%" >nul 2>&1
if exist "%NEW%\" goto err_place
if exist "%DEST%\gravitas-new\" goto err_place
if not exist "%DEST%\plugin.json" goto err_place
set "NEW="

call :retire_hook
call :tidy
echo(
call :say M_INSTALLED
set "LINE=      %DEST%"
call :say LINE
if not defined KEPT goto install_told
call :say M_KEPT
set "LINE=      %BACKUP%"
call :say LINE
:install_told
if defined HOOKDONE call :say M_HOOKDONE
call :hook_note
call :restart_note
goto finish

:remove
echo(
set "FOUND="
if exist "%DEST%" set "FOUND=1"
if exist "%OLDSKILL%" set "FOUND=1"
if exist "%HOOKPY%" set "FOUND=1"
if exist "%HOOKS%" findstr /c:"gravitas-always-on" < "%HOOKS%" >nul 2>&1 && set "FOUND=1"
if not defined FOUND goto remove_none
call :make_backup || goto err_backup
if not exist "%DEST%" goto remove_skill
move "%DEST%" "%BACKUP%\gravitas" >nul 2>&1
if exist "%DEST%" goto err_move
set "MOVED_PLUGIN=1"
set "KEPT=1"
:remove_skill
if not exist "%OLDSKILL%" goto remove_hook
move "%OLDSKILL%" "%BACKUP%\skills-gravitas" >nul 2>&1
if exist "%OLDSKILL%" goto err_move
set "MOVED_SKILL=1"
set "KEPT=1"
:remove_hook
call :retire_hook
call :tidy
if not defined KEPT goto remove_told
call :say M_REMOVED
set "LINE=      %BACKUP%"
call :say LINE
call :say M_DELETEOK
:remove_told
if defined HOOKDONE call :say M_HOOKDONE
call :hook_note
call :restart_note
goto finish

:remove_none
call :say M_NOTHING
goto finish

:no_dist
rem A download of the source without dist\ is incomplete; this file on its own is not.
if exist "%HERE%dist\" goto incomplete
if exist "%HERE%plugin\plugin.json" goto incomplete
echo(
call :say M_ALONE1
call :say M_ALONE2
call :say M_ALONE3
set "LINE=      %RELEASES%"
call :say LINE
set "RC=1"
goto finish

:incomplete
echo(
call :say M_INCOMPLETE
set "LINE=      %RELEASES%"
call :say LINE
set "RC=1"
goto finish

:err_backup
echo(
call :say M_ERRBACKUP
set "LINE=      %BACKUPS%"
call :say LINE
goto fail

:err_copy
call :tidy
echo(
call :say M_ERRCOPY
goto fail

:err_check
call :tidy
echo(
call :say M_ERRCHECK
goto fail

:err_move
call :rollback
echo(
call :say M_ERRMOVE
call :say M_STILLRUNNING
goto fail

:err_place
call :rollback
echo(
call :say M_ERRPLACE
set "LINE=      %PLUGINS%"
call :say LINE
call :say M_AGAIN
goto fail

:fail
set "RC=1"
if not defined RESTOREFAIL goto finish
call :say M_ERRRESTORE
set "LINE=      %BACKUP%"
call :say LINE
goto finish

:finish
echo(
call :say M_KEY
pause >nul
if defined OLDCP chcp %OLDCP% >nul
endlocal & exit /b %RC%


rem ---- subroutines -------------------------------------------------------------------------------

:say
rem Prints the variable named by the argument exactly as it is, whatever characters it holds.
setlocal EnableDelayedExpansion
echo(!%~1!
endlocal
exit /b 0

:parse
rem Sets PICK to 1-5 from CHOICE, or leaves it empty. Empty input takes the default. Full-width
rem digits and spaces, which a Chinese, Japanese or Korean input method may type, count too.
rem Empty input and the end of piped input look the same to set /p, so both take the default.
setlocal EnableDelayedExpansion
set "C=!CHOICE!"
if defined C set "C=!C: =!"
if defined C set "C=!C:　=!"
set "P="
if not defined C set "P=%DEF%"
for %%N in (1 2 3 4 5) do if "!C!"=="%%N" set "P=%%N"
if "!C!"=="１" set "P=1"
if "!C!"=="２" set "P=2"
if "!C!"=="３" set "P=3"
if "!C!"=="４" set "P=4"
if "!C!"=="５" set "P=5"
endlocal & set "PICK=%P%"
exit /b 0

:make_backup
rem A new folder for this run, named for the date and time when it is made. mkdir fails when the
rem folder exists, so another run in the same second, even one at the same moment, gets its own.
rem That holds only when its parent exists already: making the parent too, two runs at once can
rem both succeed. So the backups folder is made first, on its own.
if defined BACKUP exit /b 0
set "STAMP="
for /f "usebackq delims=" %%A in (`%PSEXE% -NoLogo -NoProfile -NonInteractive -Command "Get-Date -Format yyyyMMdd-HHmmss" 2^>nul`) do set "STAMP=%%A"
if not defined STAMP set "STAMP=backup"
if not exist "%BACKUPS%\" mkdir "%BACKUPS%" >nul 2>&1
if not exist "%BACKUPS%\" exit /b 1
set "N=1"
set "TRY=%BACKUPS%\%STAMP%"
:make_backup_try
mkdir "%TRY%" >nul 2>&1 && goto make_backup_made
set /a N+=1
if %N% GTR 99 exit /b 1
set "TRY=%BACKUPS%\%STAMP%-%N%"
goto make_backup_try
:make_backup_made
set "BACKUP=%TRY%"
exit /b 0

:tidy
rem Deletes this run's own unused copy, then the backup folder if nothing was put in it, then the
rem backups folder if that left it empty. rd without /s removes only an empty folder. What the
rem messages say was kept follows KEPT, not whether the folder is still there.
if defined NEW if exist "%NEW%\" rd /s /q "%NEW%" >nul 2>&1
set "NEW="
if defined BACKUP rd "%BACKUP%" >nul 2>&1
rd "%BACKUPS%" >nul 2>&1
if defined BACKUP if not exist "%BACKUP%\" set "BACKUP="
exit /b 0

:rollback
rem Puts back what this run moved, last moved first. Something that cannot go back stays in the
rem backup folder, and RESTOREFAIL makes :fail say where.
if not defined MOVED_SKILL goto rollback_plugin
if not exist "%OLDSKILL%" move "%BACKUP%\skills-gravitas" "%OLDSKILL%" >nul 2>&1
if exist "%BACKUP%\skills-gravitas" set "RESTOREFAIL=1"
:rollback_plugin
if not defined MOVED_PLUGIN goto rollback_done
if not exist "%DEST%" move "%BACKUP%\gravitas" "%DEST%" >nul 2>&1
if exist "%BACKUP%\gravitas" set "RESTOREFAIL=1"
:rollback_done
set "MOVED_SKILL="
set "MOVED_PLUGIN="
call :tidy
exit /b 0

:retire_hook
rem Beta 1's hook: an entry named gravitas-always-on in hooks.json, and the script it runs. findstr
rem reads the file through cmd, which opens any path. The PowerShell at the end of this file takes
rem the entry out and keeps a copy of the file in the backup folder. If it cannot, the entry stays,
rem the script it runs stays with it, and HOOKNOTE makes :hook_note say so.
if not exist "%HOOKS%" goto retire_hook_script
findstr /c:"gravitas-always-on" < "%HOOKS%" >nul 2>&1 || goto retire_hook_script
call :make_backup || goto retire_hook_failed
set "GV_HOOKS=%HOOKS%"
set "GV_BACKUP=%BACKUP%"
"%PSEXE%" -NoLogo -NoProfile -NonInteractive -Command "$t = [IO.File]::ReadAllText($env:GV_SELF); & ([ScriptBlock]::Create($t.Substring($t.LastIndexOf('#GRAVITAS' + '-POWERSHELL'))))" >nul 2>&1
rem Exit 4: the name is only inside another hook's text, so there is no entry to take out.
if errorlevel 5 goto retire_hook_failed
if errorlevel 4 goto retire_hook_script
if errorlevel 1 goto retire_hook_failed
set "HOOKDONE=1"
set "KEPT=1"
:retire_hook_script
if not exist "%HOOKPY%" exit /b 0
call :make_backup || exit /b 0
move "%HOOKPY%" "%BACKUP%\gravitas_always_on.py" >nul 2>&1
if not exist "%HOOKPY%" set "KEPT=1"
exit /b 0
:retire_hook_failed
set "HOOKNOTE=1"
exit /b 0

:hook_note
if not defined HOOKNOTE exit /b 0
echo(
call :say M_HOOK1
set "LINE=      %HOOKS%"
call :say LINE
call :say M_HOOK2
exit /b 0

:restart_note
echo(
call :say M_RESTART
call :say M_RESTART1
call :say M_RESTART2
call :say M_RESTART3
exit /b 0


rem ---- text, written for each language ---------------------------------------------------------

:text_en
set "M_HEAD=Gravitas installer"
set "M_INTRO=This adds Gravitas to Antigravity. Nothing else on this computer is changed."
set "M_ASK=What would you like to do?"
set "M_OPT5=Remove Gravitas"
set "M_LANGNOTE=Choose the language you read most easily. Whichever you choose, Antigravity keeps answering in the language you write to it."
set "M_PROMPT=Type a number and press Enter. If you are not sure, just press Enter (that chooses %DEF%)."
set "M_CANCEL=To stop without changing anything, close this window."
set "M_BAD=Please type a number from 1 to 5."
set "M_ALONE1=This installer needs the rest of Gravitas next to it, so nothing was changed."
set "M_ALONE2=If you opened it from inside the ZIP: close this window, click Extract all at the top of the folder window and click Extract. If the folder that opens holds only one folder, open that one. Then double-click Install Gravitas (Windows)."
set "M_ALONE3=If you downloaded only this one file: download all of Gravitas from this page instead:"
set "M_INCOMPLETE=This download of Gravitas is incomplete, so nothing was changed. Download it again from this page:"
set "M_COPYING=Copying Gravitas..."
set "M_CHECKING=Checking the copied files..."
set "M_MOVING=Moving your old copy of Gravitas into the backup folder..."
set "M_INSTALLED=Done. Gravitas is installed in:"
set "M_KEPT=Your old Gravitas files are kept in:"
set "M_HOOKDONE=The old beta 1 hook, gravitas-always-on, is gone too. A copy of the hooks.json it was in is kept in that folder."
set "M_RESTART=Now restart Antigravity so it picks up the change:"
set "M_RESTART1=  1. If Antigravity is open, find its icon near the clock at the bottom right of the screen. If you do not see it, click the small ^ arrow there."
set "M_RESTART2=  2. Right-click the icon and choose Quit."
set "M_RESTART3=  3. Open Antigravity again from the Start menu."
set "M_REMOVED=Done. Gravitas is removed from Antigravity. Its files were moved to:"
set "M_DELETEOK=You can delete that folder whenever you like."
set "M_NOTHING=Gravitas is not installed on this computer, so there was nothing to remove."
set "M_ERRBACKUP=The backup folder could not be made, so nothing was changed. It goes inside:"
set "M_ERRCOPY=Copying Gravitas failed, so nothing was changed. Check that the disk is not full, then run this installer again."
set "M_ERRCHECK=Some files did not copy correctly, so nothing was changed. Run this installer again."
set "M_ERRMOVE=The Gravitas already on this computer could not be moved, so nothing was changed."
set "M_STILLRUNNING=Antigravity is probably still running. Quit it from its icon near the clock (right-click the icon, then choose Quit), and run this installer again."
set "M_ERRPLACE=Gravitas could not be put into this folder, so nothing was changed:"
set "M_AGAIN=Run this installer again."
set "M_ERRRESTORE=Something that was moved could not be put back. It is in:"
set "M_HOOK1=Note: Gravitas beta 1 left a hook named gravitas-always-on in this file, and it could not be removed for you:"
set "M_HOOK2=It still runs on every request. The Gravitas page on GitHub explains how to remove it."
set "M_KEY=Press any key to close this window."
exit /b 0

:text_zh-CN
set "M_HEAD=Gravitas 安装程序"
set "M_INTRO=本程序会把 Gravitas 装进 Antigravity，电脑上的其他内容一概不动。"
set "M_ASK=你想做什么？"
set "M_OPT5=卸载 Gravitas"
set "M_LANGNOTE=选你看着最习惯的语言就行。不管选哪种，Antigravity 都会用你提问时用的语言来回答。"
set "M_PROMPT=输入编号后按回车键。拿不准的话，直接按回车键就行（会选 %DEF%）。"
set "M_CANCEL=如果不想继续，直接关掉这个窗口，什么都不会改动。"
set "M_BAD=请输入 1 到 5 之间的数字。"
set "M_ALONE1=Gravitas 的其余文件不在这个安装程序旁边，所以没有做任何改动。"
set "M_ALONE2=如果你是在 ZIP 压缩包里直接打开的：先关掉这个窗口，单击文件夹窗口顶部的“全部解压缩”，再单击“提取”。打开的文件夹里如果只有一个文件夹，就先打开它，然后双击 Install Gravitas (Windows)。"
set "M_ALONE3=如果你只下载了这一个文件：请到下面这个页面下载完整的 Gravitas："
set "M_INCOMPLETE=这份 Gravitas 没有下载完整，所以没有做任何改动。请到下面这个页面重新下载："
set "M_COPYING=正在复制 Gravitas……"
set "M_CHECKING=正在核对复制的文件……"
set "M_MOVING=正在把旧版 Gravitas 移到备份文件夹……"
set "M_INSTALLED=完成，Gravitas 已安装到："
set "M_KEPT=旧版 Gravitas 的文件保存在："
set "M_HOOKDONE=beta 1 留下的旧钩子 gravitas-always-on 也已清除，原来那份 hooks.json 在上面这个文件夹里留了备份。"
set "M_RESTART=最后重启一下 Antigravity，让改动生效："
set "M_RESTART1=  1. 如果 Antigravity 开着，在屏幕右下角的时钟附近找到它的图标；找不到的话，单击那里的小箭头 ^。"
set "M_RESTART2=  2. 右键单击这个图标，选择 Quit（菜单只有英文）。"
set "M_RESTART3=  3. 再从“开始”菜单重新打开 Antigravity。"
set "M_REMOVED=完成，Gravitas 已从 Antigravity 卸载，文件移到了："
set "M_DELETEOK=这个文件夹随时可以删除。"
set "M_NOTHING=这台电脑上没有安装 Gravitas，不需要卸载。"
set "M_ERRBACKUP=无法创建备份文件夹，所以没有做任何改动。备份文件夹应建在："
set "M_ERRCOPY=复制 Gravitas 失败，所以没有做任何改动。请确认磁盘还有空间，再重新运行本安装程序。"
set "M_ERRCHECK=有些文件没有正确复制，所以没有做任何改动。请重新运行本安装程序。"
set "M_ERRMOVE=电脑上已有的 Gravitas 无法移动，所以没有做任何改动。"
set "M_STILLRUNNING=多半是 Antigravity 还在运行。请右键单击时钟附近的 Antigravity 图标，选择 Quit 退出，然后重新运行本安装程序。"
set "M_ERRPLACE=Gravitas 没能放进下面这个文件夹，所以没有做任何改动："
set "M_AGAIN=请重新运行本安装程序。"
set "M_ERRRESTORE=有些已移走的文件没能放回原处，它们现在在："
set "M_HOOK1=提示：Gravitas beta 1 在下面这个文件里留下了一个叫 gravitas-always-on 的钩子，没能替你自动清除："
set "M_HOOK2=它在你每次提问时都会运行。清除方法请看 GitHub 上 Gravitas 页面的说明。"
set "M_KEY=按任意键关闭此窗口。"
exit /b 0

:text_ja
set "M_HEAD=Gravitas インストーラー"
set "M_INTRO=Antigravity に Gravitas を追加します。このパソコンのほかの部分は変更しません。"
set "M_ASK=実行する操作を選んでください。"
set "M_OPT5=Gravitas をアンインストール"
set "M_LANGNOTE=いちばん読みやすい言語を選んでください。どれを選んでも、Antigravity はあなたが書いた言語で返事をします。"
set "M_PROMPT=番号を入力して Enter キーを押してください。迷ったら、そのまま Enter キーを押せば大丈夫です（%DEF% が選ばれます）。"
set "M_CANCEL=何も変更せずにやめるときは、このウィンドウを閉じてください。"
set "M_BAD=1 から 5 までの番号を入力してください。"
set "M_ALONE1=このインストーラーと同じ場所に Gravitas のほかのファイルがないため、何も変更していません。"
set "M_ALONE2=ZIP ファイルの中から開いた場合は、このウィンドウを閉じ、フォルダー ウィンドウ上部の［すべて展開］をクリックしてから［展開］をクリックします。開いたフォルダーの中にフォルダーが1つだけあるときは、まずそれを開きます。そのあと Install Gravitas (Windows) をダブルクリックしてください。"
set "M_ALONE3=このファイルだけをダウンロードした場合は、代わりに次のページから Gravitas 一式をダウンロードしてください。"
set "M_INCOMPLETE=ダウンロードした Gravitas の一部が欠けているため、何も変更していません。次のページからもう一度ダウンロードしてください。"
set "M_COPYING=Gravitas をコピーしています…"
set "M_CHECKING=コピーしたファイルを確認しています…"
set "M_MOVING=以前の Gravitas をバックアップ用フォルダーへ移しています…"
set "M_INSTALLED=完了しました。Gravitas を次の場所にインストールしました。"
set "M_KEPT=以前の Gravitas のファイルは次の場所に保管してあります。"
set "M_HOOKDONE=beta 1 の古いフック gravitas-always-on も削除しました。それが書かれていた hooks.json のコピーは、上のフォルダーに保管してあります。"
set "M_RESTART=最後に Antigravity を再起動して、変更を反映させてください。"
set "M_RESTART1=  1. Antigravity が開いている場合は、画面右下の時計の近くにあるアイコンを探します。見当たらないときは、そこにある小さな ^ をクリックします。"
set "M_RESTART2=  2. アイコンを右クリックして Quit を選びます（メニューは英語で表示されます）。"
set "M_RESTART3=  3. スタート メニューから Antigravity をもう一度起動します。"
set "M_REMOVED=完了しました。Antigravity から Gravitas をアンインストールし、ファイルを次の場所に移しました。"
set "M_DELETEOK=このフォルダーはいつ削除してもかまいません。"
set "M_NOTHING=このパソコンには Gravitas がインストールされていないため、アンインストールするものはありません。"
set "M_ERRBACKUP=バックアップ用フォルダーを作成できなかったため、何も変更していません。作成先は次の場所です。"
set "M_ERRCOPY=Gravitas のコピーに失敗したため、何も変更していません。ディスクの空き容量を確認してから、もう一度このインストーラーを実行してください。"
set "M_ERRCHECK=一部のファイルが正しくコピーされなかったため、何も変更していません。もう一度このインストーラーを実行してください。"
set "M_ERRMOVE=このパソコンにある Gravitas を移動できなかったため、何も変更していません。"
set "M_STILLRUNNING=Antigravity がまだ動いている可能性があります。時計の近くにある Antigravity のアイコンを右クリックして Quit を選び、終了させてから、もう一度このインストーラーを実行してください。"
set "M_ERRPLACE=Gravitas を次のフォルダーに置けなかったため、何も変更していません。"
set "M_AGAIN=もう一度このインストーラーを実行してください。"
set "M_ERRRESTORE=移動したものの一部を元に戻せませんでした。次の場所にあります。"
set "M_HOOK1=補足：Gravitas beta 1 が次のファイルに残したフック gravitas-always-on を、自動では削除できませんでした。"
set "M_HOOK2=このフックは依頼のたびに動きます。削除のしかたは GitHub の Gravitas のページで説明しています。"
set "M_KEY=何かキーを押すと、このウィンドウを閉じます。"
exit /b 0

:text_ko
set "M_HEAD=Gravitas 설치 프로그램"
set "M_INTRO=Antigravity에 Gravitas를 추가합니다. 이 컴퓨터의 다른 부분은 건드리지 않습니다."
set "M_ASK=원하는 작업을 선택하세요."
set "M_OPT5=Gravitas 제거"
set "M_LANGNOTE=가장 편하게 읽히는 언어를 고르세요. 어떤 언어를 고르든 Antigravity는 사용자가 쓴 언어로 답합니다."
set "M_PROMPT=번호를 입력하고 Enter 키를 누르세요. 잘 모르겠으면 그냥 Enter 키만 누르면 됩니다(%DEF%번이 선택됩니다)."
set "M_CANCEL=아무것도 바꾸지 않고 그만두려면 이 창을 닫으세요."
set "M_BAD=1부터 5까지의 번호 중 하나를 입력하세요."
set "M_ALONE1=이 설치 프로그램과 같은 폴더에 Gravitas의 나머지 파일이 없어서 아무것도 바꾸지 않았습니다."
set "M_ALONE2=ZIP 파일 안에서 바로 열었다면 이 창을 닫고, 폴더 창 위쪽의 [모두 압축 풀기]를 클릭한 다음 [압축 풀기]를 클릭하세요. 열린 폴더 안에 폴더가 하나만 있으면 먼저 그 폴더를 연 다음, Install Gravitas (Windows)를 더블클릭하세요."
set "M_ALONE3=이 파일 하나만 내려받았다면, 대신 아래 페이지에서 Gravitas 전체를 내려받으세요."
set "M_INCOMPLETE=내려받은 Gravitas에 빠진 파일이 있어서 아무것도 바꾸지 않았습니다. 아래 페이지에서 다시 내려받으세요."
set "M_COPYING=Gravitas를 복사하는 중..."
set "M_CHECKING=복사한 파일을 확인하는 중..."
set "M_MOVING=이전 Gravitas를 백업 폴더로 옮기는 중..."
set "M_INSTALLED=완료되었습니다. Gravitas가 다음 위치에 설치되었습니다."
set "M_KEPT=이전 Gravitas 파일은 다음 위치에 보관해 두었습니다."
set "M_HOOKDONE=beta 1의 이전 훅 gravitas-always-on도 지웠습니다. 이 훅이 들어 있던 hooks.json의 사본은 위 폴더에 보관해 두었습니다."
set "M_RESTART=이제 Antigravity를 다시 시작해야 변경 사항이 적용됩니다."
set "M_RESTART1=  1. Antigravity가 열려 있다면 화면 오른쪽 아래 시계 근처에서 Antigravity 아이콘을 찾으세요. 보이지 않으면 그곳의 작은 ^ 화살표를 클릭하세요."
set "M_RESTART2=  2. 아이콘을 마우스 오른쪽 버튼으로 클릭하고 Quit을 선택하세요(메뉴는 영어로만 나옵니다)."
set "M_RESTART3=  3. 시작 메뉴에서 Antigravity를 다시 실행하세요."
set "M_REMOVED=완료되었습니다. Antigravity에서 Gravitas를 제거하고, 파일은 다음 위치로 옮겼습니다."
set "M_DELETEOK=이 폴더는 언제 지워도 괜찮습니다."
set "M_NOTHING=이 컴퓨터에는 Gravitas가 설치되어 있지 않아 제거할 것이 없습니다."
set "M_ERRBACKUP=백업 폴더를 만들지 못해 아무것도 바꾸지 않았습니다. 백업 폴더는 다음 위치에 만들어집니다."
set "M_ERRCOPY=Gravitas를 복사하지 못해 아무것도 바꾸지 않았습니다. 디스크 공간이 남아 있는지 확인한 뒤 이 설치 프로그램을 다시 실행하세요."
set "M_ERRCHECK=일부 파일이 제대로 복사되지 않아 아무것도 바꾸지 않았습니다. 이 설치 프로그램을 다시 실행하세요."
set "M_ERRMOVE=이 컴퓨터에 있는 Gravitas를 옮기지 못해 아무것도 바꾸지 않았습니다."
set "M_STILLRUNNING=Antigravity가 아직 실행 중인 것 같습니다. 시계 근처의 Antigravity 아이콘을 마우스 오른쪽 버튼으로 클릭하고 Quit을 선택해 종료한 다음, 이 설치 프로그램을 다시 실행하세요."
set "M_ERRPLACE=Gravitas를 다음 폴더에 넣지 못해 아무것도 바꾸지 않았습니다."
set "M_AGAIN=이 설치 프로그램을 다시 실행하세요."
set "M_ERRRESTORE=옮겼던 파일 일부를 원래 자리로 되돌리지 못했습니다. 지금은 다음 위치에 있습니다."
set "M_HOOK1=참고: Gravitas beta 1이 다음 파일에 남긴 훅 gravitas-always-on을 자동으로 지우지 못했습니다."
set "M_HOOK2=이 훅은 요청할 때마다 실행됩니다. 지우는 방법은 GitHub의 Gravitas 페이지에 나와 있습니다."
set "M_KEY=아무 키나 누르면 이 창이 닫힙니다."
exit /b 0


rem ---- PowerShell ---------------------------------------------------------------------------------
rem :retire_hook runs everything below the marker line with PowerShell; cmd never reaches it.

#GRAVITAS-POWERSHELL
# Takes beta 1's gravitas-always-on entry out of hooks.json and writes the file back the way
# scripts\install.py writes it (Python's json.dump with indent=2, then a newline), after copying it
# into the backup folder. GV_HOOKS is the file and GV_BACKUP the folder. Exit 0 means it is done;
# anything else means hooks.json is unchanged.
$ErrorActionPreference = 'Stop'
$inv = [Globalization.CultureInfo]::InvariantCulture

function Format-PyString([string]$s) {
    # Python's ensure_ascii: anything outside printable ASCII becomes \uXXXX.
    $b = New-Object Text.StringBuilder
    [void]$b.Append([char]34)
    foreach ($c in $s.ToCharArray()) {
        $n = [int]$c
        if ($n -eq 34 -or $n -eq 92) { [void]$b.Append([char]92).Append($c) }
        elseif ($n -eq 10) { [void]$b.Append('\n') }
        elseif ($n -eq 13) { [void]$b.Append('\r') }
        elseif ($n -eq 9) { [void]$b.Append('\t') }
        elseif ($n -eq 8) { [void]$b.Append('\b') }
        elseif ($n -eq 12) { [void]$b.Append('\f') }
        elseif ($n -lt 32 -or $n -gt 126) { [void]$b.Append('\u').Append($n.ToString('x4', $inv)) }
        else { [void]$b.Append($c) }
    }
    [void]$b.Append([char]34)
    return $b.ToString()
}

function Format-PyFloat($v) {
    # Python's repr of a float: 1.0 rather than 1, and 1e-05 rather than 1E-05.
    $s = ([double]$v).ToString('R', $inv)
    if ($s -match '^(-?[0-9.]+)E([+-])0*([0-9]+)$') {
        return $Matches[1] + 'e' + $Matches[2] + $Matches[3].PadLeft(2, '0')
    }
    if ($s -notmatch '[.E]') { $s += '.0' }
    return $s
}

function Format-PyJson($v, [string]$indent) {
    if ($null -eq $v) { return 'null' }
    if ($v -is [bool]) { if ($v) { return 'true' } return 'false' }
    if ($v -is [string]) { return Format-PyString $v }
    if ($v -is [int] -or $v -is [long]) { return $v.ToString($inv) }
    if ($v -is [decimal]) {
        # ConvertFrom-Json reads 1.5 and very long whole numbers as decimals; only the first is a float.
        if ((([decimal]::GetBits($v)[3] -shr 16) -band 255) -eq 0) { return $v.ToString($inv) }
        return Format-PyFloat $v
    }
    if ($v -is [double] -or $v -is [single]) { return Format-PyFloat $v }
    $inner = $indent + '  '
    if ($v -is [Management.Automation.PSCustomObject]) {
        $parts = @(foreach ($p in $v.PSObject.Properties) {
            $inner + (Format-PyString $p.Name) + ': ' + (Format-PyJson $p.Value $inner)
        })
        if ($parts.Count -eq 0) { return '{}' }
        return "{`n" + ($parts -join ",`n") + "`n" + $indent + '}'
    }
    if ($v -is [array]) {
        $parts = @(foreach ($x in $v) { $inner + (Format-PyJson $x $inner) })
        if ($parts.Count -eq 0) { return '[]' }
        return "[`n" + ($parts -join ",`n") + "`n" + $indent + ']'
    }
    throw 'hooks.json holds a value this script does not write'
}

$path = $env:GV_HOOKS
$text = (New-Object Text.UTF8Encoding($false, $true)).GetString([IO.File]::ReadAllBytes($path))
if ($text.Length -gt 0 -and [int]$text[0] -eq 0xFEFF) { $text = $text.Substring(1) }
$data = ConvertFrom-Json -InputObject $text
if ($data -isnot [Management.Automation.PSCustomObject]) { exit 3 }
if (-not @($data.PSObject.Properties | Where-Object { $_.Name -ceq 'gravitas-always-on' })) { exit 4 }
$data.PSObject.Properties.Remove('gravitas-always-on')
$out = (Format-PyJson $data '') + "`n"
$null = ConvertFrom-Json -InputObject $out
Copy-Item -LiteralPath $path -Destination (Join-Path $env:GV_BACKUP 'hooks.json')
$tmp = $path + '.gravitas-new'
try {
    [IO.File]::WriteAllText($tmp, $out, (New-Object Text.UTF8Encoding($false)))
    [IO.File]::Replace($tmp, $path, [NullString]::Value)
} finally {
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force }
}
exit 0
