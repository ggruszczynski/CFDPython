### Exercice:

def add(x,y):
    return x+y

def multiply(x,y):
    return x*y

my_fun = add
my_fun(3,4)

my_fun = multiply
my_fun(3,4)


# For i from 1 to 100:

# * if i is divisible by `3` and `5` print `35`
# * if i is divisible by `3` print `3`
# * if i is divisible by `5` print `5`
# * for the rest, print i.

slownik = {
    (True, False): lambda i: print("%d is divisible by 3 \n" % i),
    (False, True): lambda i: print("%d is divisible by 5 \n" % i),
    (True, True): lambda i: print("%d jis divisible by 3 and 5 \n" % i),
    (False, False): lambda i: print("%d is not divisible by neither 3 nor 5\n" % i)
}


def fun():
    for i in range(100):
        stan = (i % 3 == 0, i % 5 == 0)
        ktora_funkcja = slownik[stan]
        ktora_funkcja(i)


fun()