'' 這個 VBS 腳本會「靜默」執行 BAT，不會跳出黑色終端機視窗
' 雙擊這個檔案即可在背景啟動 AI 課堂小助手伺服器

Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

' 靜默執行 bat 檔 (第二個參數 0 = 隱藏視窗，第三個 False = 不等待)
WshShell.Run _
    "cmd /c ""C:\Users\yangh\OneDrive\Desktop\ai-study-assistant\啟動伺服器.bat""", _
    0, False

' 等 3 秒讓伺服器啟動
WScript.Sleep 3000

' 自動開啟本機瀏覽器（方便電腦本人使用）
WshShell.Run "http://localhost:8501"

Set WshShell = Nothing
