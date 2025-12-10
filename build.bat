@echo off
chcp 65001 >nul
echo.
echo
echo       CYN 的铺面数据Getter - 打包脚本
echo
echo.

:: 1. 清理旧文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
del /f /q "*.spec" 2>nul

echo [1/4] PyInstaller 打包
call ".venv\Scripts\activate"
pyinstaller --onefile ^
            --windowed ^
            --icon=R.ico ^
            --add-data="R.ico;." ^
            --name="CYN 的铺面数据Getter" ^
            --noconfirm ^
            main.py
if not exist "dist\CYN 的铺面数据Getter.exe" (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo [成功] 单文件 exe 生成完成！

:: 2. UPX
echo.
echo [2/4] 正在使用 UPX
if exist "C:\upx-5.0.2-win64\upx-5.0.2-win64\upx.exe" (
    upx --best --compress-icons=0 "CYN 的铺面数据Getter.exe"
    echo [成功] UPX 压缩完成！
) else (
    echo [警告] 未找到 upx.exe
)

:: 3.Inno Setup
::echo.
::echo [3/4] 正在生成 Inno Setup 安装包...
::if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
::    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer.iss"
::    echo [成功] 安装包生成完成 → Output 文件夹
::) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
::    "C:\Program Files\Inno Setup 6\ISCC.exe" "installer.iss"
::    echo [成功] 安装包生成完成 → Output 文件夹
::) else (
::    echo [提示] 未安装 Inno Setup，已跳过安装包生成
::)

echo.
echo [4/4] 打包完成：
pause