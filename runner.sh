#!/bin/bash

# SIGINT 시그널을 처리하는 핸들러 함수
handle_interrupt() {
    echo "Caught SIGINT, terminating..."
    exit 1
}

# SIGINT(2) 시그널을 handle_interrupt 함수로 트랩
trap 'handle_interrupt' INT

# 현재 폴더 아래의 results 폴더를 기준으로 경로 설정
result_path="$(dirname "$0")/src/results"

# 폴더가 존재하는지 확인
if [ -d "$result_path" ]; then
    echo "Directory already exists. Continuing on scripts..."

    # 추가 코드 실행
    kernprof -l -v src/main.py > $result_path/profiler_result.txt
else
    # 폴더가 존재하지 않으면 폴더를 생성
    mkdir -p $result_path
    if [ $? -ne 0 ]; then
        echo "Error occurred while making directory"
    else
        echo "Successfully made directory"

        # 추가 코드 실행
        kernprof -l -v src/main.py > $result_path/profiler_result.txt
    fi
fi