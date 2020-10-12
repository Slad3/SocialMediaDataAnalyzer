from math import e
import matplotlib.pyplot as plt

maxHeight = 1.0
hShift = 2
stretch = 1

def sigmoid(x):
    return maxHeight/(1+e**(-stretch*x + hShift))


if __name__ == '__main__':
    print(sigmoid(0))
    print(sigmoid(1))


    print('=========')
    interval = 100
    for i in range(-interval, interval):
        x = i/20
        y = sigmoid(x)

        plt.scatter(x, 1-y)
    plt.xlim(-5, 5)
    plt.ylim(0, 2)

    plt.show()