        
class Node:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.ytree = None

def mergeX(l,r):
    if len(l)==0:
        return r
    if len(r)==0:
        return l
    
    a = []
    x = y = 0
    
    while x<len(l) and y<len(r):
        if l[x][0]<=r[y][0]:
            a.append(l[x])
            x+=1
        else:
            a.append(r[y])
            y+=1
            
        if x==len(l):
            a+=r[y:]
            break
        if y==len(r):
            a+=l[x:]
            break
    return a

def mergesortX(l):
    if len(l)<2:
        return l
    else:
        mid = len(l)//2
        return mergeX(mergesortX(l[0:mid]),mergesortX(l[mid:]))

def mergeY(l,r):
    if len(l)==0:
        return r
    if len(r)==0:
        return l
    
    a = []
    x = y = 0
    
    while x<len(l) and y<len(r):
        if l[x][1]<=r[y][1]:
            a.append(l[x])
            x+=1
        else:
            a.append(r[y])
            y+=1
            
        if x==len(l):
            a+=r[y:]
            break
        if y==len(r):
            a+=l[x:]
            break
    return a

def mergesortY(l):
    if len(l)<2:
        return l
    else:
        mid = len(l)//2
        return mergeY(mergesortY(l[0:mid]),mergesortY(l[mid:]))

class PointDatabase:
      
    def __init__(self,pointlist):
        X = mergesortX(pointlist)       # pointlist sorted in x
        Y = mergesortY(pointlist)       # pointlist sorted in y
                    
        def buildTree(X,Y):
            if len(X)==0:
                return None             # nothing in the tree
            if len(X)==1:
                root = Node(X[0])       # tree consists of only one element
                root.ytree = [Y[0]]
                return root
            
                
            else:
                mid = len(X)//2         # the median 
                X_L = X[0:mid]          # the left half of X list
                X_R = X[mid+1:]         # the right half of X list
                Y_L = []                
                Y_R = []                
            
                for i in range(len(Y)):
                    if Y[i][0]<X[mid][0]:
                        Y_L.append(Y[i])        # list containing same elements as X_L but sorted in y
                    elif(Y[i][0]>X[mid][0]):
                        Y_R.append(Y[i])        # list containing same elements as X_R but sorted in y
             
                root = Node(X[mid])                     # the median is the root
                root.left = buildTree(X_L,Y_L)          # the left child
                root.right = buildTree(X_R,Y_R)         # the right child
                
                if root.left!=None:
                    root.left.parent = root
                if root.right!=None:
                    root.right.parent = root
                    
                root.ytree = Y              # the y list if each node
                 
            return root
        
        self.data = buildTree(X,Y)          # reference to the root
    
    
        
    def searchNearby(self,q,d):
        # the ranges of x,y
        x_min = q[0]-d          
        x_max = q[0]+d          
        y_min = q[1]-d          
        y_max = q[1]+d          
        l = []
          
        def next(l,val):
            '''
            Retruns the index of the element just greater than val, if it doesn't exist, it returns -1
            '''
            left = 0
            right = len(l) - 1
        
            ans = -1
            if(len(l)==0):
                return -1
            
            while (left <= right):
                mid = (left + right) // 2
    
                if (l[mid][1] < val):
                    left = mid + 1

                else:
                    ans = mid
                    right = mid - 1
        
            return ans
        
        def minX(root,val):
            '''
            Returns the node whose value is just greater than or equal to val
            '''
            if root == None:
                return None
            if root.value[0] < val:
                return minX(root.right, val)
            if root.value[0] == val:
                return root
            if root.value[0] > val:
                left = minX(root.left,val)
                if left==None:
                    return root
                else:
                    return left
            
        def maxX(root,val):
            '''
            Returns the node whose value is just smaller than or equal to val
            '''
            if root==None:
                return None
            if root.value[0]==val:
                return root
            elif root.value[0]<val:
                right = maxX(root.right,val)
                if right == None:
                    return root
                else:
                    return right
            else:
                return maxX(root.left,val)
              
        def inorder(root):
            '''
            Returns the inorder traversal of the tree
            '''
            if root==None:
                return []
            else:
                left = inorder(root.left)
                right = inorder(root.right)
                return left + [root.value] + right
            
        
        def lcaX(root,x,y):
            '''
            Returns the least common ancestor of the nodes x,y
            If there is no least common ancestor, it returns None
            '''
            if root == None:
                return None
            if x==None or y==None:
                return None
            elif root.value[0]>x.value[0] and root.value[0]>y.value[0]:
                return lcaX(root.left,x,y)
            elif root.value[0]<x.value[0] and root.value[0]<y.value[0]:
                return lcaX(root.right,x,y)
            else:
                return root
            
        
        
        a = minX(self.data,x_min)       # the node whose x value is just >= x_min      
        b = maxX(self.data,x_max)       # the node whose x value is just <= x_max
        c = lcaX(self.data,a,b)         # the least common ancestor of a,b
        

        if a!=None and b!=None and a.value[0]>b.value[0]:
            return []

        while a!=c:
            if a.value[0]>=x_min and a.value[0]<=x_max:            
                if a.value[1]<=y_max and a.value[1]>=y_min:         
                    l.append(a.value)                           # a is in the range        
                    
                if a.right!=None:                               # the right subtree of a also is in the x range
                    idx = next(a.right.ytree,y_min)
                    if idx == -1:   
                        a = a.parent                # no element in y range in right subtree of a
                        continue
                    else:
                        while idx<len(a.right.ytree) and a.right.ytree[idx][1]<=y_max:
                            l.append(a.right.ytree[idx])                # add all elements in y range in the right subtree of a
                            idx += 1
        
            a = a.parent
            
        if c!=None and c.value[1]<=y_max and c.value[1]>=y_min:
            l.append(c.value)                           # least common ancestor of a,b is in the range

        while b!=c:
            if b.value[0]<=x_max and b.value[0]>=x_min:
                if b.value[1]>=y_min and b.value[1]<=y_max:
                    l.append(b.value)                   # b is in the range
            
                if b.left!=None:                        # th eleft subtree of b is also in x range
                    idx = next(b.left.ytree,y_min)
                    if idx == -1:
                        b = b.parent                    # no element of left subtree of b is in y range
                        continue
                    else:
                        while idx < len(b.left.ytree) and b.left.ytree[idx][1] <= y_max:
                            l.append(b.left.ytree[idx])         # add all elements in y range in the left subtree of b
                            idx += 1
            
            b = b.parent
                    
        return l
    
    
