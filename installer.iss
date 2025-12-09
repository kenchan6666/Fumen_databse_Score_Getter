; CYN 的铺面数据Getter - 安装包
#define MyAppName "CYN 的铺面数据Getter"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "CYN"
#define MyAppURL "https://github.com/kenchan6666/Fumen_databse_Score_Getter.git"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=Output
OutputBaseFilename={#MyAppName} v{#MyAppVersion} Setup
Compression=lzma/max
SolidCompression=yes
WizardStyle=modern
SetupIconFile=R.ico
UninstallDisplayIcon={app}\CYN 的铺面数据Getter.exe

[Files]
Source: "dist\CYN 的铺面数据Getter.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\CYN 的铺面数据Getter.exe"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\CYN 的铺面数据Getter.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "创建桌面快捷方式"

[Run]
Filename: "{app}\CYN 的铺面数据Getter.exe"; Description: "立即运行"; Flags: nowait postinstall skipifsilent