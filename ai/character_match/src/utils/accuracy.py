def accuracy(labels, predicts) -> float:
    """计算预测准确度

    Args:
        labels (_type_): 标签
        predicts (_type_): 预测值

    Returns:
        float: 准确率
    """
    prop = 0.5
    lens = len(labels)
    right = 0
    for i in range(lens):
        if labels[i][0] > prop and predicts[i][0] > prop:
            right += 1
        elif labels[i][0] < prop and predicts[i][0] <= prop:
            right += 1
    return right / lens