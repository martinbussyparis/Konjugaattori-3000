mode con:cols=150 lines=400
@echo off

IF EXIST ".\dist" (
    rmdir ".\dist" /s /q
)

IF EXIST ".\build" (
    rmdir ".\build" /s /q
)

echo building Menu.py...
pyinstaller --noconfirm --log-level=ERROR ^
	--hidden-import=queue ^
	--nowindow ^
    --add-data="Website.url;." ^
	--add-data="ReadMe.txt;." ^
	--add-data="data;data" ^
	--add-data="Konjugaattori 3000.lnk;." ^
    Menu.py
	
echo Renaming files...
rename "dist\Menu" "bin"
rename "dist\bin\Menu.exe" "Konjugaattori.exe"
echo Moving files...
move "dist\bin\data" "dist"
move "dist\bin\Konjugaattori 3000.lnk" "dist"
move "dist\bin\Website.url" "dist"
move "dist\bin\ReadMe.txt" "dist"

echo building done.

REM echo compiling inno setup script...
REM iscc "setup\setup.iss"
REM echo inno setup script compiled. Setup generated.

echo zipping files...
del Konjugaattori_3000.zip
7z a Konjugaattori_3000.zip .\dist\* -mx9
echo zip file created.

pause