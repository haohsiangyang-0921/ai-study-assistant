'' 建立桌面捷徑：雙擊開啟小助手
' 執行這個 VBS 一次後，桌面就會出現捷徑圖示

Dim WshShell, oShortcut
Dim desktopPath, vbsPath

Set WshShell = CreateObject("WScript.Shell")

' 捷徑放到桌面
desktopPath = WshShell.SpecialFolders("Desktop")
vbsPath     = "C:\Users\yangh\OneDrive\Desktop\ai-study-assistant\雙擊開啟小助手.vbs"

Set oShortcut = WshShell.CreateShortcut(desktopPath & "\🎓 AI 課堂小助手.lnk")
oShortcut.TargetPath       = "wscript.exe"
oShortcut.Arguments        = """" & vbsPath & """"
oShortcut.WorkingDirectory = "C:\Users\yangh\OneDrive\Desktop\ai-study-assistant"
oShortcut.Description      = "啟動 AI 課堂摘要與互動測驗小助手"
oShortcut.Save

Set oShortcut = Nothing
Set WshShell  = Nothing

MsgBox "✅ 桌面捷徑建立完成！" & vbCrLf & _
       "往後直接雙擊桌面上的「🎓 AI 課堂小助手」即可啟動。" & vbCrLf & vbCrLf & _
       "其他裝置（手機/平板）連線網址：" & vbCrLf & _
       "  http://172.16.11.200:8501", _
       vbInformation, "AI 課堂小助手"
