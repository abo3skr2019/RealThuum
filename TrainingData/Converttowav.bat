@echo off
setlocal enabledelayedexpansion

REM Loop through all files in the current directory
for %%A in (*) do (
    REM Check if the file is not already a WAV file
    if not "%%~xA"==".wav" (
        REM Generate the output file name by replacing the extension with .wav
        set "output=%%~nA.wav"
        
        REM Convert the file to WAV using FFmpeg
        ffmpeg -i "%%A" -acodec pcm_s16le -ar 44100 -ac 2 "!output!"
        
        REM Check if the conversion was successful
        if exist "!output!" (
            echo Converted "%%A" to "!output!"
            REM Delete the original file
            del "%%A"
        ) else (
            echo Failed to convert "%%A" to "!output!"
        )
    )
)

endlocal