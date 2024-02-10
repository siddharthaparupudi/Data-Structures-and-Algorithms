
#implement an ArrayStack
class ArrayStack: 
    #constructor
    def __init__(self):
        self.ArrayStack = [None]*50     #create an array of default capacity
        self._size = 0                  #maintain the size of the stack
        self._capacity = 50             #maintain the capacity of the array
        
    # the length of the stack
    def __len__(self):
        if(self.size==0):
            print("Stack is Empty")
        else:
            return (self._size)
     
    #check if the stack  is empty    
    def is_empty(self):
        return self._size == 0
    
    #removes and returns the top element of the stack
    def pop(self):
        if(self._size==0):
            print("Stack is empty")
        else:
            top = self.ArrayStack[self._size-1]
            self.ArrayStack[self._size-1] = None
            self._size-=1
            return top  
        
    #returns the top element of the stack  without removing it   
    def top(self):
        if(self._size==0):
            print("Stack is empty")
        else:
            return self.ArrayStack[self._size-1]  
        
    #adds an element x to the top of the stack 
    def push(self,x):
        if self._size==self._capacity:              #check if the array is full or not
            self._capacity = 2*self._capacity       #if it is, double the cqpacity of the array
            l=[None]*self._capacity                 #allocate a new memory location for the new array of double size
            for i in range(self._size):
                l[i]=self.ArrayStack[i]             #copy all the elements
            l[self._size]=x                         #add the element x to the top of the stack
            self.ArrayStack=l
            self._size+=1                           #increment the size of the stack
        else:
            self.ArrayStack[self._size]=x           #add the element x to the top of the stack
            self._size+=1                           #increment the size of the stack
         
 

def findPositionandDistance(P):
    x = 0           #x coordinate variable
    y = 0           #y coordinate variable
    z = 0           #z coordinate variable
    d = 0           #distance variable
    i = 0           #iterator
    char = "XYZ"    #characters we encounter in the input string
   
     
    s1 = ArrayStack()       #stack to maintain characters
    s2 = ArrayStack()       #stack to maintain operations
    s3 = ArrayStack()       #stack to maintain integers
    
    while(i<len(P)):
        if(P[i]=="X" or P[i]=="Y" or P[i]=="Z"):        #if we encounter a character
            s1.push(P[i])                               #push it onto stack s1
           
        elif(P[i]=="+" or P[i]=="-" or P[i]=="("):      #if we encounter an operation
            s2.push(P[i])                               #push it onto stack s2
           
        elif(P[i]!="X" and P[i]!="Y" and P[i]!="Z" and P[i]!="(" and P[i]!=")"):    #if we encounter a number
            
            j = i
            k = 0                       #variable to store the integer
            while(P[j]!="("):           #the number can be of multiple digits, so we evaluate till we reach "("
                k = 10*k + int(P[j])    #update the variab;e
                j+=1
           
            if (s3.is_empty()):         #if the stack of integers is empty, we have not encountered nesting
                s3.push(k)              #push the integer directly onto stack s3
               
            else:                       #if the stack of integers is not empty, we have encountered nesting
                top = s3.top()          
                s3.push(k*top)          #multiply the integer with the top element and then push it onto the stack s3
               
            i = j-1                     #update i
    
        elif(P[i]==")"):                #if we encounter closing bracket, we have to evaluate till we go back to the opening bracket
       
            while(s2.top()!="("):                       #we will be evaluating from the top till we encounter the opening bracket
                
                if(s2.top()=="+"):                      #we have to perform addition
                    
                    if (char.index(s1.top())==0):       #operand is X
                        x+=s3.top()                     #update x
                        d+=s3.top()                     #update d
                        s1.pop()                        #pop off X as we have performed the operation
                        s2.pop()                        #pop off + as we have performed the operation
                        
                    elif (char.index(s1.top())==1):     #operand is Y
                        y+=s3.top()                     #update y
                        d+=s3.top()                     #update d
                        s1.pop()                        #pop off Y as we have performed the operation
                        s2.pop()                        #pop off + as we have performed operation
                        
                    else:                               #operand is Z
                        z+=s3.top()                     #update z
                        d+=s3.top()                     #update d
                        s1.pop()                        #pop off Z as we have performed the operation
                        s2.pop()                        #pop off + as we have performed the operation
                        
                elif(s2.top()=="-"):                    #we have to perform subtraction
                    
                    if (char.index(s1.top())==0):       #operand is X
                        x-=s3.top()                     #update x
                        d+=s3.top()                     #update d
                        s1.pop()                        #pop off X as we have performed the operation
                        s2.pop()                        #pop off - as we have performed the operation
                        
                    elif (char.index(s1.top())==1):
                        y-=s3.top()                     #update y
                        d+=s3.top()                     #update d
                        s1.pop()                        #pop off Y as we have performed the operation
                        s2.pop()                        #pop off - as we have performed the operation
                        
                    else:
                        z-=s3.top()                     #update z
                        d+=s3.top()                     #update d
                        s1.pop()                        #pop off Z as we have performed the operation
                        s2.pop()                        #pop off - as we have performed the operation
                    
             
            s2.pop()    #we have encounterd the opening bracket, so pop it off
            s3.pop()    #we have used the integer corresponding to the bracket we just evaluated, so pop it off
        
        i+=1            #update i
        
    while((not s1.is_empty()) and (not s2.is_empty())):     #after the above operations, if elements are still left in stacks s1 and s2
                                                            #there are no parentheses, so update the coordinates by 1 each
                                                        
        if(s2.top()=="+"):                                  #we have to perform addition
            
            if (char.index(s1.top())==0):                   #operand is X
                x+=1                                        #update x
                d+=1                                        #update d
                s1.pop()                                    #pop off X as we have performed the operation
                s2.pop()                                    #pop off + as we have performed the operation
                
            elif (char.index(s1.top())==1):                 #operand is Y
                y+=1                                        #update y
                d+=1                                        #update d
                s1.pop()                                    #pop off Y as we have performed the operation
                s2.pop()                                    #pop off + as we have performed the operation 
                
            else:                                           #operand is Z
                z+=1                                        #update z
                d+=1                                        #update d
                s1.pop()                                    #pop off Z as we have performed the operation
                s2.pop()                                    #pop off + as we have performed the operation
                
        elif(s2.top()=="-"):                                #we have to perform subtraction
            
            if (char.index(s1.top())==0):                   #operand is X
                x-=1                                        #update x
                d+=1                                        #update d   
                s1.pop()                                    #pop off X as we have performed the operation
                s2.pop()                                    #pop off - as we have performed the operation 
                
            elif (char.index(s1.top())==1):                 #operand is Y
                y-=1                                        #update y
                d+=1                                        #update d
                s1.pop()                                    #pop off Y as we have performed the operation
                s2.pop()                                    #pop off - as we have performed the operation
                
            else:                                           #operand is Z
                z-=1                                        #update z
                d+=1                                        #update d
                s1.pop()                                    #pop off Z as we have performed the operation
                s2.pop()                                    #pop off - as we have performed the operation 

        
        else:                   #1st element of stack s3 is an integer
            #update all the coordinates by multiplying with the remaining element of the stack
            x = s3.top()*x      
            y = s3.top()*y
            z = s3.top()*z
            d = s3.top()*d
            
            #pop off the last element of the stack s3 after using the integer to update all the coordinates
            s3.pop()
            
    return [x,y,z,d]            #return the position and distance

