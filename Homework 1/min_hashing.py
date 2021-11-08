import random
import sympy

class MinHashing:

    def __init__(self, n: int = 100):
        self.n = n
        
        # Record the maximum shingle ID that we assigned (we used 32 bits).
        self.maxShingleID = 2**32-1
        self.c = sympy.nextprime(self.maxShingleID)

        self.a = self.get_coefficients(n)
        self.b = self.get_coefficients(n)

    def get_coefficients(self, k):
        randList = []
      
        for i in range(k):
            # Get a random shingle ID.
            randIndex = random.randint(0, self.maxShingleID)
            # Ensure that each random number is unique.
            while randIndex in randList:
                randIndex = random.randint(0, self.maxShingleID)
            # Add the random number to the list.
            randList.append(randIndex)

        return randList

    def get_signature(self, shingles):
        signature = []
        
        #function will be: h(x) = (a*x + b) % c
        for i in range(self.n):
            minHashCode = self.c + 1
            
            for x in shingles:
                hashCode = (self.a[i] * x + self.b[i]) % self.c
                if hashCode < minHashCode:
                    minHashCode = hashCode
            
            signature.append(minHashCode)

        return signature

# example usage
#m = MinHashing(2)
#result = m.get_signature([901544789, 2659403885, 3265866552])
#print(result)