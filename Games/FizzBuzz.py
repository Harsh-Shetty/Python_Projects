number = int(input("Enter a Number between 1 & 101: "))

while number > 100 or number < 1:
    number = int(input("Give valid number between 1 & 101: "))

for number in range(1, number):
    if number % 3 == 0 and number % 5 == 0:
        print("Fizzbuzz")
    elif number % 5 == 0:
        print("Buzz")
    elif number % 3 == 0:
        print("Fizz")
    else:
        print(number, "is not divisible by 3 or 5")
