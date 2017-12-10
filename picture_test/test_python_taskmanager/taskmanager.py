import singleton


@Singleton
class TaskManager:
    def __init__(self):
        print 'TaskManager created'


#f = TaskManager.Instance()  # Good. Being explicit is in line with the Python Zen
#g = TaskManager.Instance()  # Returns already created instance

#print f is g  # True
