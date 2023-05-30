def accuracy(labels, predicts) -> float:
    prop = 0.5
    lens = len(labels)
    right = 0
    for i in range(lens):
        if labels[i][0] > prop and predicts[i][0] > prop:
            right += 1
        elif labels[i][0] < prop and predicts[i][0] <= prop:
            right += 1
    return right / lens