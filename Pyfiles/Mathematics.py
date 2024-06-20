def find_maximum_maxima(input_list):
    maxima = []
    for i in range(1, len(input_list) - 1):
        if input_list[i] > input_list[i - 1] and input_list[i] > input_list[i + 1]:
            maxima.append(input_list[i])
    return max(maxima)

