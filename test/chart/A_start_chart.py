import matplotlib.pyplot as plt
def test_show(points):
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    plt.plot(y_values,marker='o')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Line Chart of Given Data')

    plt.show()
    print('test_show')