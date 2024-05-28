import os, subprocess, pathlib



BASEDIR = pathlib.Path(__file__).parent.resolve()


def log(msg, flag=None):    
    if flag==None:
        flag = 0
    head = ["debug", "error", "status"]
    from time import localtime, strftime
    now = strftime("%H:%M:%S", localtime())
    logpath = os.path.join(BASEDIR, "./debug.log")
    if not os.path.isfile(logpath):
        assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" > {logpath}", shell=True)==0, f"[error] > shell command failed to execute"
    else: assert subprocess.call(f"echo \"[{now}][{head[flag]}] > {msg}\" >> {logpath}", shell=True)==0, f"[error] > shell command failed to execute"