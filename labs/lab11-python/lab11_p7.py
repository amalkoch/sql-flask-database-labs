score = float(input("Enter score (0.0 - 1.0): "))

if score > 1.0 or score < 0.0:
    print("Error")
elif score >= 0.9:
    print("A")
elif score >= 0.8:
    print("B")
elif score >= 0.7:
    print("C")
elif score >= 0.6:
    print("D")
else:
    print("F")
