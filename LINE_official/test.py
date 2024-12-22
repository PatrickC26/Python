import threading
import time
a = 9
def ini():
    print("asasd")

ini()
def worker(name, duration):
    global a
    print(f"Thread {name} starting", a)
    time.sleep(duration)  # Simulate some work
    a += 1
    print(f"Thread {name} finished", a)

# Creating threads
thread1 = threading.Thread(target=worker, args=("A", 2))
thread2 = threading.Thread(target=worker, args=("B", 4))

# Starting threads
thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()

print("All threads finished")
