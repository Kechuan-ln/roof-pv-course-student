@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "COURSE_CONDA=%CONDA_EXE%"
if exist "%COURSE_CONDA%" goto found
set "COURSE_CONDA="
for /f "delims=" %%I in ('where conda.exe 2^>nul') do if not defined COURSE_CONDA set "COURSE_CONDA=%%I"
if exist "%COURSE_CONDA%" goto found
set "COURSE_CONDA="
for %%I in ("%USERPROFILE%\miniconda3\Scripts\conda.exe" "%USERPROFILE%\anaconda3\Scripts\conda.exe" "%USERPROFILE%\miniforge3\Scripts\conda.exe" "%LOCALAPPDATA%\miniconda3\Scripts\conda.exe" "%LOCALAPPDATA%\anaconda3\Scripts\conda.exe" "%ProgramData%\miniconda3\Scripts\conda.exe" "%ProgramData%\anaconda3\Scripts\conda.exe") do if exist "%%~I" set "COURSE_CONDA=%%~I"
if exist "%COURSE_CONDA%" goto found
echo Install Anaconda or Miniconda first, then double-click this file. Python is included.
pause
exit /b 1
:found
call "%COURSE_CONDA%" run --no-capture-output --name base python "%~dp0scripts\launch_course.py" --conda "%COURSE_CONDA%"
set "COURSE_RESULT=%ERRORLEVEL%"
if not "%COURSE_RESULT%"=="0" pause
exit /b %COURSE_RESULT%
