#!/bin/bash

# 현재 폴더 아래의 results 폴더를 기준으로 경로 설정
result_path="$(dirname "$0")/src/results"

# 폴더가 존재하는지 확인
if [ -d "$result_path" ]; then
    echo "directory already exists. continuing on scripts..."

    # 추가 코드 실행
    kernprof -l -v src/main.py > "$result_path/profiler_result.txt"
else
    # 폴더가 존재하지 않으면 폴더를 생성
    mkdir -p "$result_path"
    if [ $? -ne 0 ]; then
        echo "error occured while making directory"
    else
        echo "successfully made directory"

        # 추가 코드 실행
        kernprof -l -v src/main.py > "$result_path/profiler_result.txt"
    fi
fi