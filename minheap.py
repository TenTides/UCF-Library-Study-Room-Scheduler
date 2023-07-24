class GenPurposeMinHeap:
     
    def __init__(self):
        self.heap = []
        self.size = 0

    def parent (self,index):
        return self.heap[(index-1)//2]	
    
    def insert(self, element):
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
            if(self.heap[index*2+1] < self.heap[index]):
                self.swap(index*2+1,index)
            
    def minimum(self,a, indexa, b, indexb):
        if (a < b):
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