def accuracy(labels, predicts) -> float:
    lens = len(labels)
    right = 0
    for i in range(lens):
        if labels[i][0] - 1.0 > 0.5 and predicts[i][0] > 0.5:
            right += 1
        elif labels[i][0] <= 0.5 and predicts[i][0] <= 0.5:
            right += 1
    return right / lens