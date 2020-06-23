def function1(a):
    print(3)

def function2(a):
    if a>3:
        print(1)
    elif a==5:
        print(2)
    else:
        print(3)

def function3(a):
    while(a>5):
        a+=1
        print(3)


def test_me(x, y, z):
    if y > 13:
        print("1")
        if x < 2:
            print("2")
            z = 3
            if x < -1:
                print("3")
                z = 1
    else:
        print("4")
        x = 2
    y = 50
    if z == 4:
        print("5")
        z = 1
    else:
        print("6")
        while x < 5:
            print("7")
            if y==30:
                break
            x += 1
            z = z + 1
    y = 0
    