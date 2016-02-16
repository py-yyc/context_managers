from threading import Lock

mutex = Lock()

mutex.acquire()
print "is locked: ", mutex.locked()
mutex.release()
print "is locked: ", mutex.locked()

mutex = Lock()
with mutex:
    print "is locked: ", mutex.locked()
print "is locked: ", mutex.locked()
