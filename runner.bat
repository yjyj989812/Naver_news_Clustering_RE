@echo off
setlocal

rem 현재 폴더 아래의 results 폴더를 기준으로 경로 설정
set "result_path=%~dp0src\results"

rem Ctrl+C 핸들러 설정
set "trap_handler="
set trap_handler

rem Ctrl+C를 처리하는 함수 정의
:handle_interrupt
echo.
echo Caught SIGINT, terminating...
exit /b 1

rem trap 명령을 사용하여 Ctrl+C 입력을 처리
rem trap_handler를 실행하도록 설정
trap_handler=handle_interrupt

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
echo Script terminated with exit code 0.
endlocal
exit /b 0