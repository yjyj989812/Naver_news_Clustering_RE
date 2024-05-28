@echo off
setlocal

rem 현재 폴더 아래의 results 폴더를 기준으로 경로 설정
set "result_path=%~dp0src\results"

rem Ctrl+C 핸들러 설정
set "trap_handler=handle_interrupt"


rem 폴더가 존재하는지 확인
if exist "%result_path%" (
    echo Directory already exists. Continuing on scripts...

    rem 추가 코드 실행
    kernprof -l -v src\main.py > "%result_path%\profiler_result.txt"
) else (
    rem 폴더가 존재하지 않으면 폴더를 생성
    mkdir "%result_path%"
    if errorlevel 1 (
        echo Error occurred while making directory
    ) else (
        echo Successfully made directory

        rem 추가 코드 실행
        kernprof -l -v src\main.py > "%result_path%\profiler_result.txt"
    )
)

rem 종료 시 메시지 출력
:end
echo Script completed.
endlocal
exit /b 0

rem Ctrl+C를 처리하는 함수 정의
:handle_interrupt
echo.
echo Caught SIGINT, exiting.
exit /b 1

rem EXIT 시 실행될 함수를 설정
call :set_trap

rem Ctrl+C 핸들러를 설정하는 함수
:set_trap
if "%trap_handler%"=="handle_interrupt" (
    rem 현재 콘솔 세션의 이벤트 트랩 설정
    for /f "delims=" %%I in ('copy /z "%~dpf0" nul') do (
        setlocal enabledelayedexpansion
        endlocal & set "trap_handler="
        call :handle_interrupt
    )
)
goto :eof