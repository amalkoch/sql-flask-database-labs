# integer input 
num = input(" Please enter an integer number:")
num = int(num)
#find divisors on the number
for i in range(1, num+1):
    if num % i == 0:
        print(i)
print("code finished running")
