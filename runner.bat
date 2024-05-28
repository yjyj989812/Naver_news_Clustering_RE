@echo off

rem 현재 폴더 아래의 results 폴더를 기준으로 경로 설정
set "result_path=%~dp0src\results"

rem 폴더가 존재하는지 확인
if exist "%result_path%" (
    echo directory already exists. continuing on scripts...

    rem 추가 코드 실행
    kernprof -l -v src\main.py > "%result_path%\profiler_result.txt"
) else (
    rem 폴더가 존재하지 않으면 폴더를 생성
    mkdir "%result_path%"
    if errorlevel 1 (
        echo error occured while making directory
    ) else (
        echo successfully made directory

        rem 추가 코드 실행
        kernprof -l -v src\main.py > "%result_path%\profiler_result.txt"
    )
)