import time


@profile
def exe(a):
    for i in a:
        return i
    
@profile
def main():
    a = [x for x in range(1_000_000)]
    x = exe(a)
    x = x+1
    
if __name__ == "__main__":
    main()