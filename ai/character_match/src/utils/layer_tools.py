def calc_conv_layer(H: int, W: int, P: int, K: int, S: int) -> tuple[int]:
    """计算通过卷积层后的层大小

    Args:
        H (int): 高
        W (int): 宽
        P (int): Padding
        K (int): Kernel Size
        S (int): Strike

    Returns:
        tuple[int]: 层大小 
    """
    h = (H + 2 * P - K) / S + 1 # H_out = (H + 2P - K) / S + 1
    w = (W + 2 * P - K) / S + 1 # W_out = (W + 2P - K) / S + 1
    return (h, w)

def calc_pool_layer(H: int, W: int, K: int, S: int) -> tuple[int]:
    """计算通过池化层后的大小

    Args:
        H (int): 高
        W (int): 宽
        K (int): Kernel Size
        S (int): Strike

    Returns:
        tuple[int]: 层大小
    """
    h = (H - K) / S + 1 # H_out = (H - K) / S + 1
    w = (W - K) / S + 1 # W_out = (W - K) / S + 1
    return (h, w)