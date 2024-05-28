import os, subprocess, pathlib
from time import localtime, strftime

BASEDIR = pathlib.Path(__file__).parent.resolve()


def log(msg, flag=None):    
    if flag == None:
        flag = 0

    head = ["debug", "error", "status"]
    now = strftime("%H:%M:%S", localtime())
    logpath = os.path.join(BASEDIR, "./debug.log")

    try:
        with open(logpath, "a") as logfile:
            logfile.write(f"[{now}][{head[flag]}] > {msg}\n")
    except Exception as e:
        print(f"exception on log function: {e}")




def step_log(flag, e):
    if flag==0: log(f"exception occurred during dataframe retrieval: {e}", 1)
    elif flag==1: log(f"exception occurred during data preprocess: {e}", 1)
    elif flag==2: log(f"exception occurred during tfidf calculation: {e}", 1)
    elif flag==3: log(f"exception occurred during cosine similarity calculation: {e}", 1)
    elif flag==4: log(f"exception occurred during clustering: {e}", 1)
    elif flag==5: log(f"exception occurred during dendrogram plotting: {e}", 1)
    elif flag==6: log(f"exception occurred during cluster result analysis: {e}", 1)
    else:
        log(f"exception on unexpected flag: {e}", 1)