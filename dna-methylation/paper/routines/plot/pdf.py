import numpy as np

def get_pdf_x_and_y(data, num_bins=1000, x_left=None, x_right=None):
    data = np.asarray(data)
    data = data[~np.isnan(data)]

    if x_left is not None:
        min_x = x_left
    else:
        min_x = min(data)
        min_x -= 1e-12

    if x_right is not None:
        max_x = x_left
    else:
        max_x = max(data)
        max_x += 1e-12

    shift = (max_x - min_x) / num_bins

    xs = [min_x + (shift / 2) + i * shift for i in range(0, num_bins)]

    ys = [0] * num_bins
    num_outliers = 0
    for d in data:
        if d > max_x or d < min_x:
            num_outliers += 1
        else:
            index = int(np.floor((d - min_x) / (max_x - min_x) * num_bins))
            if index < 0 or index >= num_bins:
                num_outliers += 1
            else:
                ys[index] += 1

    #print(f'num_outliers: {num_outliers}')

    sum_y = sum(ys)
    ys = [curr_y / (sum_y * shift) for curr_y in ys]

    return xs, ys