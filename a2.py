class Heap:
    # constructor
    def __init__(self,array):
        # assign heap to the array
        self.heap = array
        # if length of array is greater than 1, execute bottom up heap costruction
        if len(self.heap)>1:
            self.build_fast()
    
    # bottom up heap constructor        
    def build_fast(self):
        # parent of the last element of the initial heap
        parent = self.parent(len(self.heap)-1)
        i = parent
        while(i>=0):
            # downheap at every node
            self.down_heap(i)
            i-=1
     
    # the length of the heap       
    def __len__(self):
        return len(self.heap)
    
    # check if the heap is empty or not
    def is_empty(self):
        return len(self.heap) == 0
    
    # the parent index of element at index x
    def parent(self,x):
        return (x-1)//2
    
    # the index of left child of element at index x
    def left_child(self,x):
        return 2*x+1
    
    # the index of right child of element at index x
    def right_child(self,x):
        return 2*x+2
    
    # check if the element at index x has a left child or not
    def has_left(self,x):
        return 2*x+1<len(self.heap)
    
    # check if the element at index x has a right child or not
    def has_right(self,x):
        return 2*x+2<len(self.heap)
     
    # perform up-heap operation on element at index x   
    def up_heap(self,x):
        # the parent index of element at index x
        parent = self.parent(x)
        if x>0 and self.heap[x][0]<self.heap[parent][0]:
            self.heap[x],self.heap[parent] = self.heap[parent],self.heap[x]
            self.up_heap(parent)
            
    def down_heap(self,x):
        # if the element at index x has a left child
        if self.has_left(x):
            left = self.left_child(x)
            small_child = left
            # let the left child be the smaller one
            if self.has_right(x):
                # if the element at index x has a right child
                right = self.right_child(x)
                # compare the children to get the smaller child
                if (self.heap[right]<self.heap[left]):
                    small_child = right
        
            if self.heap[small_child][0]<self.heap[x][0]:
                # if the key of the smaller child is smaller, swap the elements
                self.heap[x],self.heap[small_child] = self.heap[small_child],self.heap[x]
                # down heap again on the small child
                self.down_heap(small_child)
                
    def add(self,key,value):
        # add new element at the end of the heap and keep on up-heaping until it is at the correct position
        self.heap.append((key,value))
        self.up_heap(len(self.heap)-1)
        
        
    def min(self):
        # if heap is empty, there is no minimum element
        if(self.is_empty()):
            print("Heap is empty")
        else:
            # the top of the heap is the minimum element
            return self.heap[0]
    
    def remove_min(self):
        if (self.is_empty()):
            print("Heap is empty")
        else:
            # swap the 1st and last elements
            self.heap[0],self.heap[len(self.heap)-1] = self.heap[len(self.heap)-1],self.heap[0]
            # pop off the last element
            item = self.heap.pop()
            # keep on downheaping until the root is at the correct position
            self.down_heap(0)
            return (item[0],item[1])
        
def listCollisions(M,x,v,m,T):
    collisions = 0                              # the total number of collisions till now
    time = 0                                    # the amount of time elapsed till now
    l = []                                      # the output list to be returned
    heap_builder = []                           # array to store elements of the heap
    i = 0
    particle_collisions=[0]*len(x)              # number of collisions of each particle till now
    times_of_collisions = [0]*len(x)            # the time of the most recent collision for each particle
    
    while(i<len(x)-1):
        # traverse through the whole list
        if v[i]>v[i+1]:
            # if collison b/w i'th and (i+1)'th particle is possible
            t = (x[i+1]-x[i])/(v[i]-v[i+1])
            # add it to the array which stores the elements of the heap
            heap_builder.append(((t,i),(x[i]+v[i]*t,[particle_collisions[i],particle_collisions[i+1]])))
        i+=1
     
    # create a heap from the array   
    data = Heap(heap_builder)  
     
    # till the number of collisions is less than m and time is less than T 
    while(collisions<=m and time<=T):
        # if there is no data in the heap, return
        if data.is_empty():
            return l
        else: 
            # the top element in the list, i.e the collision with minimum time
            ((t,b),(c,d)) = data.remove_min()

            # if the removed collision b/w particles b and b+1 is to be valid, they should not have collided with any other particles in that time interval
            if d==[particle_collisions[b],particle_collisions[b+1]]:
                collisions+=1                                                   # update the total number of collisions
                particle_collisions[b]+=1                                       # update the number of collisions of b'th particle
                particle_collisions[b+1]+=1                                     # update the number of collisions of (b+1)'th particle
                time = t                                                        # update the current time
                times_of_collisions[b] = times_of_collisions[b+1] = time        # update the time of most recent collision of b'th and (b+1)'th particle
                if collisions<=m and time<=T:
                    l.append((round(t,4),b,round(c,4)))                         # add the collision to the output list
                
                # update the positions and velocities of the particles which just collided    
                x[b]=x[b+1]=c   
                u1 = v[b]
                u2 = v[b+1]
                v[b] = ((M[b]-M[b+1])*u1 + 2*M[b+1]*u2)/(M[b]+M[b+1])
                v[b+1] = (2*M[b]*u1 + (M[b+1]-M[b])*u2)/(M[b]+M[b+1])
                
                # if a collision is possible between (b-1)'th and b'th particle
                if (b>0 and v[b-1]>v[b]):
                    interval1 = times_of_collisions[b]-times_of_collisions[b-1]                                 # to calculate how much the (b-1)'th particle has moved extra
                    t1 = (x[b]-(x[b-1]+v[b-1]*interval1))/(v[b-1]-v[b])                                         # the amount of time from the current instant in which the collision is expected to happen
                    data.add((time+t1,b-1),(x[b]+v[b]*t1,[particle_collisions[b-1],particle_collisions[b]]))    # add the collision to the heap
                   
                if (b<len(x)-2 and v[b+1]>v[b+2]):
                    interval2 = times_of_collisions[b+1]-times_of_collisions[b+2]                                   # to calculate how much the (b-1)'th particle has moved extra
                    t2 = ((x[b+2]+v[b+2]*interval2)-x[b+1])/(v[b+1]-v[b+2])                                         # the amount of time from the current instant in which the collision is expected to happen
                    data.add((time+t2,b+1),(x[b+1]+v[b+1]*t2,[particle_collisions[b+1],particle_collisions[b+2]]))  # add the collision to the heap
                    
            else:
                # the collision was not valid, go back to the loop
                continue
            
    return l
