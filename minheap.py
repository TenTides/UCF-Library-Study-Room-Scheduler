from datetime import datetime

class taskObj:
    def __init__(self,date, start_time, duration, reservationType, room_option, room_number, min_capacity):
        self._date = datetime.strptime(date, '%Y-%m-%d')
        self._start_time = start_time
        self._duration = duration
        self._reservationType = reservationType
        self._room_number = room_number
        self._room_option = room_option
        self._min_capacity = min_capacity

    def get_start_time(self):
        return self._start_time
    
    def get_date(self):
        return self._date
    
    def get_duration(self):
        return self._duration

    def get_reservation_type(self):
        return self._reservationType

    def get_room_number(self):
        return self._room_number

    def get_room_option(self):
        return self._room_option

    def get_min_capacity(self):
        return self._min_capacity
    
    def get_all_variables(self):
        return [
            self._date,
            self._start_time,
            self._duration,
            self._reservationType,
            self._room_option,
            self._room_number,
            self._min_capacity
        ]
class taskMinHeap:
     
    def __init__(self):
        self.heap = []
        self.size = 0

    def parent (self,index):
        return self.heap[(index-1)//2]	
    
    def insert(self, element):
        if not isinstance(element, taskObj):
            raise ValueError("Only taskObj instances can be inserted into the taskMinHeap.")
        self.heap.append(element)
        self.size += 1
        self.percolateUp(len(self.heap)-1)

    def percolateUp(self, elementIndex):
        if self.size > 1:
            parentIndex = (elementIndex - 1) // 2
            if parentIndex >= 0 and self.heap[parentIndex] > self.heap[elementIndex]:
                self.swap(parentIndex, elementIndex)
                self.percolateUp(parentIndex)

    def percolateDown(self,index):
        if self.size >= (index*2+2): #two children
            min = self.minimum(self.heap[index*2+1],index*2+1,self.heap[index*2+2],index*2+2)
            if(self.heap[min] < self.heap[index]):
                self.swap(min,index)
                self.percolateDown(min)
        if self.size == (index*2+1):
            if(self.heap[index*2+1].get_date() < self.heap[index].get_date()):
                self.swap(index*2+1,index)
            
    def minimum(self,a, indexa, b, indexb):
        if (a.get_date() < b.get_date()) :
            return indexa
        else:
            return indexb

    def swap(self,element1index, element2index):
        temp = self[element1index]
        self.heap[element1index] = self.heap[element2index]
        self.heap[element2index] = temp

    def getMin(self):
        return self.heap[0]

    def extractMin(self):
        retval = self.getMin()
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.percolateDown(self.heap[0])
        return retval

    def isEmpty(self):
        return len(self.heap) == 0

    def getSize(self):
        return self.size