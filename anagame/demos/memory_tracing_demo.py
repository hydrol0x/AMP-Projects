import tracemalloc

# code or function for which memory
# has to be monitored
def app():
    lt = {}
    lt2={}
    for i in range(0, 100000):
        lt[i]=str(i)
    for i in range(0, 100000):
        lt2[i]=i

if __name__ == "__main__":
    # starting the monitoring
    tracemalloc.start()

    # function call
    app()

    # displaying the memory
    print(tracemalloc.get_traced_memory(), "bytes")

    # stopping the library
    tracemalloc.stop()
