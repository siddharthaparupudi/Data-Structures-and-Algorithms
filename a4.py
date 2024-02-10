
import random
import math

# convert character to corresponding hashcode value
def code(s):
    if s != "?":
        return ord(s)-65
    else:
        return 0

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)
    # q is O(m/eps * log(m/eps))
    # therefore, log(q) is O(log(m/eps))
    # therefore randPatternMatch runs in O((m+n)*log(q)) time which is O((m+n)*log(m/eps))
    # and it has space complexity O(log(n)+log(q)) which is O(log(n)+log(m/eps))

#pattern matching with wildcard
# def randPatternMatchWildcard(eps,p,x):
# 	N = findN(eps,len(p))
# 	q = randPrime(N)
# 	return modPatternMatchWildcard(q,p,x)

def randPatternMatchWildCard(eps,p,x):
    N = findN(eps,len(p))
    q = randPrime(N)
    return modPatternMatchWildcard(q,p,x)
    # q is O(m/eps * log(m/eps))
    # therefore, log(q) is O(log(m/eps))
    # therefore randPatternMatchWildCard runs in O((m+n)*log(q)) time which is O((m+n)*log(m/eps))
    # and it has space complexity O(log(n)+log(q)) which is O(log(n)+log(m/eps))

# return appropriate N that satisfies the error bounds
def findN(eps,m):
    # find upper bound on prime N such that probability of false +ve is less than eps
    # if the hash value is same and the pattern is not same
    # it must mean that the prime must divide the difference of the hash values
    # probability that the hash values are same is (no. of primes that divide |hash1-hash2|)/(no. of primes less than or equal to N)
    # the no. of primes less than or equal to N is atleast N/log(N,2)
    # |hash1-hash2| has order 26^m
    # the no. of prime divisors of a +ve no. d is atmost log(d,2)
    # thereofore, the no. of prime divisors of 26^m is atleast log(26^m,2) = mlog(26,2)
    # thus, the probability of false positive is atleast mlog(26,2)/(N/log(N,2))
    # we need this to be less than eps
    # therefore N/log(N,2) >= 2mlog(26,2)/eps
    # taking log both sides, log(N,2) - log((log(N,2),2)) >= log(2mlog(26,2)/eps),2)
    # multiplying the above eqns, N(1 - log((log(N,2),2)) >= 2mlog(26,2)/eps * log(2mlog(26,2)/eps),2)
    # the maximum value of log((log(N,2),2) is 0.531
    # therefore 1 - log((log(N,2),2) >= 0.469
    # therefore N >= 2mlog(26,2)/eps * log(2mlog(26,2)/eps),2)/0.469 
    #  if we equate N to the ceiling of the RHS, the initial inequality will also be True
    x = math.log(26,2)
    y = 2*m*x/eps
    z = math.log(y,2)*y*2.17
    N = math.ceil(z)
    
    return N



def hash(q,p):
        i = 0
        x = 0
        while i<len(p):                                 # calculating the polynomial hash function in O(m*log(q)) time 
            x = (((26%q)*(x))%q + code(p[i])%q)%q       # at every step, we have taken remainder with q 
            i+=1                                        # so that the working memory never exceeds O(log(q))
            
        return x%q
    

def exp(q,a,b):
    if b==0:
        return 1                                                    # calculating the exponent a^b in O(log(b)*log(q)) time 
    temp = exp(q,a,int(b/2))                                        # at every step, we have taken remainder with q 
    if b%2==0:                                                      # so that the working memory never exceeds O(log(q))
        return ((exp(q,a,int(b/2))%q) * (exp(q,a,int(b/2))%q))%q
    else:
        return ((a%q)*(exp(q,a,int(b/2))%q)*(exp(q,a,int(b/2))%q))%q
    
    
# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):

    l = []
    m = len(p)                  # the length of the pattern
    n = len(x)                  # the length of the text
    power = exp(q,26,m-1)       # precompute 26^(m-1) in O(log(m)*log(q)) time and O(log(q)) space
           
    pattern_hash = hash(q,p)            # the hash value of pattern is computed in O(m*log(q)) time as arithmetic operations involve q which is a log(q) bit number and O(log(q)) space
    substring_hash = hash(q,x[:m])      # the hash value of 1st substring is computed in O(m*log(q)) time and O(log(q)) space
    i = 0                               # index of position currently in text, this takes O(log(n)) memory
    
    # loop contains only O(1) operations, therefore total time is O(n*log(q)) as arithmetic operations involve q which is a log(q) bit number
    while i<n-m:
        if substring_hash == pattern_hash:                                                                  # the hash value matches
            l.append(i)                                                                                     # add the index to the list
            substring_hash = (26*(substring_hash - ((power)*(code(x[i])%q))%q) + code(x[i+m])%q)%q          # rehash the hash value of the substring in O(1) time without using any extra space
            i+=1
            continue                                                                                        # go back to start of while loop
        
        else:                                                                                               # the hash value does not match
            substring_hash = (26*(substring_hash - ((power)*(code(x[i])%q))%q) + code(x[i+m])%q)%q          # rehash the hash value of the substring in O(1) time without using any extra space
            i+=1
            continue                                                                                        # go back to start of while loop
    
  
    if substring_hash == pattern_hash:      # check hash value for last substring
        l.append(i)                         # if it matches, add it to the 
      
    # time complexity is O((m+n)*log(q))
    # we know that m<n, so the time complexity is O(n*log(q))
    # space complexity is O(log(q)+log(n)) 
    return l                                
	
     

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
    n = len(x)          # the length of the text
    m = len(p)          # the length of the pattern
    l = []
    
    # returns the index at which the wildcard is present, if not present, returns False
    def wildcard(p):
        for i in range(len(p)):
            if p[i]=="?":
                return i
        return False
    
    def hash_wildcard(q,p,idx):         # computes the hash value of a pattern with wildcard at index 'idx'
        x = hash(q,p)                   # the hash function if wildcard is present is that we just ignore the corresponding term in the normal hash function
        power = exp(q,26,m-idx-1)       # O(log(m)) time and O(log(q)) space
        x = x - power*code(p[idx])     # subtract the term at index 'idx'
    
        return x%q                      # take remainder with q to use only O(log(q)) space
            
    
    if wildcard(p)==False:              # no wildcard present in pattern
        return modPatternMatch(q,p,x)   # same as modPatternMatch
    else:
        idx = wildcard(p)                                   # the index at which wildcard is present found in
        hash_pattern = hash_wildcard(q,p,idx)               # compute the hash value of the pattern in O(m*log(q)) time and O(log(q)) space
        hash_substring = hash_wildcard(q,x[:m],idx)         # compute the hash value of the 1st substring in O(m*log(q)) time and O(log(q)) space
        i = 0                                               # store the index currently present in the text which take O(log(n)) space
        power1 = exp(q,26,m-1)                              
        power2 = exp(q,26,m-idx-1)                          # precompute powers which take O(log(m)*log(q)) time and O(log(q)) space
        power3 = exp(q,26,m-idx-2)
        
        while i<n-m:
            if hash_substring == hash_pattern:                                                                                                                                          # check if the hash value of substring matches with that of the pattern
                l.append(i)                                                                                                                                                             # add it to the list if it does
                hash_substring = (26*(hash_substring - ((power1)*(code(x[i])%q))%q + ((power2)*(code(x[i+idx])%q))%q - ((power3)*(code(x[i+idx+1])%q))%q) + code(x[i+m])%q)%q           # rehash the hash value of the substring in O(1) time
                i+=1
                continue                                                                                                                                                                # return to top of while loop
            
            else:                                                                                                                                                                       # the hash value does not match
                hash_substring = (26*(hash_substring - ((power1)*(code(x[i])%q))%q + ((power2)*(code(x[i+idx])%q))%q - ((power3)*(code(x[i+idx+1])%q))%q) + code(x[i+m])%q)%q           # rehash the hash value of the substring in O(1) time
                i+=1
                continue                                                                                                                                                                 # return to top of while loop
            
        if hash_substring == hash_pattern:      # check if hash value for last substring is match
            l.append(i)                         # add the index to the list if it is
         
        # the time complexity is O((m+n)*log(q))
        # the space complexity is O(log(n)+log(q))   
        return l



