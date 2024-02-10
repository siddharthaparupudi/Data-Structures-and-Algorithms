class Heap:
    # constructor
    def __init__(self):
        self.heap = []
     
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
        if x>0 and self.heap[x][0]>self.heap[parent][0]:
            self.heap[x],self.heap[parent] = self.heap[parent],self.heap[x]
            self.up_heap(parent)
            
    def down_heap(self,x):
        # if the element at index x has a left child
        if self.has_left(x):
            left = self.left_child(x)
            big_child = left
            # let the left child be the smaller one
            if self.has_right(x):
                # if the element at index x has a right child
                right = self.right_child(x)
                # compare the children to get the smaller child
                if (self.heap[right]>self.heap[left]):
                    big_child = right
        
            if self.heap[big_child][0]>self.heap[x][0]:
                # if the key of the smaller child is smaller, swap the elements
                self.heap[x],self.heap[big_child] = self.heap[big_child],self.heap[x]
                # down heap again on the small child
                self.down_heap(big_child)
                
    def add(self,key,value):
        # add new element at the end of the heap and keep on up-heaping until it is at the correct position
        self.heap.append((key,value))
        self.up_heap(len(self.heap)-1)
    
    def remove_max(self):
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

def findMaxCapacity(n,links,s,t):
    m = len(links)
    capacities = [-1]*n
    capacities[s] = float('inf')
    path = [-1]*n
    path[s] = s
    
    graph = []
    for i in range(n):
        graph.append([])
        
    for i in range(m):
        u,v,c = links[i]
        graph[u].append((c,v))
        graph[v].append((c,u))
        
    
    heap = Heap()
    
    curr = s
    while curr!=t:
        neighbours = graph[curr]
        for i in range(len(neighbours)):
            cap,node = neighbours[i]
            new_cap = min(capacities[curr],cap)
            if new_cap > capacities[node]:
                capacities[node] = new_cap
                heap.add(new_cap,node)
                path[node]= curr
                
        next_cap,next_node = heap.remove_max()
        curr = next_node
   
    ptr = t    
    route_rev = [ptr]
    while path[ptr]!=s:
        route_rev.append(path[ptr])
        ptr = path[ptr]
    route_rev.append(s) 
    
    route = []
    for i in range(len(route_rev)):  
        route.append(route_rev[len(route_rev)-i-1]) 
        
    return(capacities[t],route)

