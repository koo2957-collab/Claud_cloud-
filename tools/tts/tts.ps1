param([string]$dir)
Add-Type -AssemblyName System.Speech
$lines = Get-Content -Raw -Encoding UTF8 (Join-Path $dir 'lines.json') | ConvertFrom-Json
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice('Microsoft Heami Desktop')
$s.Rate = 0
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(44100, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
for ($i = 0; $i -lt $lines.Count; $i++) {
  $f = Join-Path $dir ('{0:D2}.wav' -f $i)
  $s.SetOutputToWaveFile($f, $fmt)
  $s.Speak($lines[$i])
}
$s.SetOutputToNull()
"done $($lines.Count)"
