import matplotlib.pyplot as plt
from scipy.stats import uniform, norm
import numpy as np

def draw_uniform():
    a = 2
    b = 10
    x = np.linspace(a, b, 100)
    dist = uniform(loc=3, scale=4)
    figure, ax = plt.subplots(figsize=(9, 9))
    plt.subplot(221)
    plt.title('Функция распределения')
    plt.plot(x, dist.cdf(x), color='r', label=r'F({0}, {1})'.format(a, b))
    plt.legend()

    plt.subplot(222)
    plt.title('Функция плотности распределения')
    plt.plot(x, dist.pdf(x), color='b', label=r'f({0}, {1})'.format(a, b))
    plt.legend()

    dist = norm(loc=7, scale = 1.1)
    plt.subplot(223)
    plt.title('Функция распределения')
    plt.plot(x, dist.cdf(x), color='r', label=r'F({0}, {1})'.format(a, b))
    plt.legend()

    plt.subplot(224)
    plt.title('Функция плотности распределения')
    plt.plot(x, dist.pdf(x), color='b', label=r'f({0}, {1})'.format(a, b))
    plt.legend()
    
    plt.show()

def main():
    draw_uniform()

if __name__ == '__main__':
    main()
