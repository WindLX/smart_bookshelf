(& "E:\anaconda\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
conda activate sd
tensorboard --logdir='./ai/character_match/logs'