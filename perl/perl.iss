#define APPVER "5.18.2"
#define APPARCH "x86"
#if APPARCH == "x64"
#define PERLLOC "..\..\..\..\perl-5.18\x64"
#else
#define PERLLOC "..\..\..\..\perl-5.18\Win32"
#endif

[Setup]
AppName=Perl
AppVerName=Perl {#APPVER}
AppVersion={#APPVER}
OutputBaseFilename=Perl {#APPVER} {#APPARCH}
AppPublisher=HexChat
AppPublisherURL=http://hexchat.github.io/
AppSupportURL=https://github.com/hexchat/hexchat/issues
AppUpdatesURL=http://hexchat.github.io/downloads.html
DefaultDirName=C:\Perl
DisableProgramGroupPage=yes
DisableDirPage=no
SolidCompression=yes
Compression=lzma2/ultra64
OutputDir={#SourcePath}
SourceDir={#PERLLOC}
FlatComponentsList=no
PrivilegesRequired=lowest
ShowComponentSizes=no
CreateUninstallRegKey=yes
ChangesEnvironment=yes
Uninstallable=yes
DirExistsWarning=no
#if APPARCH == "x64"
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
#else
ArchitecturesAllowed=x86 x64
#endif

[Files]
Source: ".\*"; DestDir: "{app}"; Flags: createallsubdirs recursesubdirs

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: string; ValueName:"PATH"; ValueData:"{olddata};{app}\bin"; Flags: preservestringtype
