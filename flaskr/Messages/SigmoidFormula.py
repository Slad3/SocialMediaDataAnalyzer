from math import e
import matplotlib.pyplot as plt

maxHeight = 1.0
hShift = 1

def sigmoid(x):
    return maxHeight/(1+e**(-x + hShift))

def form(x):
    return 13**x -1


if __name__ == '__main__':
    print(sigmoid(0))
    print(sigmoid(1))


    print('=========')
    interval = 20
    for i in range(-interval, interval):
        x = i/interval
        y = sigmoid(x)

        plt.scatter(x, y)
    plt.show()