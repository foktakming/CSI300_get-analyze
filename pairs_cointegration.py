def pairs_cointegration(share_a, share_b):
    """
    share_a , share_b 要为DataFrame格式的数据
    数据格式为 yahoo来源
    """

    #     得出两个股票的数据量是否一致
    share_a_count = len(share_a)
    share_b_count = len(share_b)

    if share_a_count != share_b_count:
        return f'{share_a}:{share_a_count},{share_b}:{share_b_count}'

    import numpy as np
    point_list = []
    #     将股票A与股票B的收盘价记录为（x,y)的点
    for share_index in range(share_a_count):
        point_list.append([share_a.iloc[share_index, 5], share_b.iloc[share_index, 5]])
    #     将装有所有点的列表化为数组
    arr = np.array(point_list)

    #     准备进行线性回归的x，y数据
    #     注意：data需要转化成一维数组
    x_share = arr.T[0].reshape((share_a_count, 1))
    y_share = arr.T[1].reshape((share_a_count, 1))

    #     创建回归模型对象
    from sklearn.linear_model import LinearRegression
    line_model = LinearRegression()
    #     进行学习训练
    line_model.fit(x_share, y_share)
    #     获取回归方程K值
    k = line_model.coef_[0, 0]
    #     计算残差值
    residual_list = []
    for residual_index in range(len(arr)):
        x_value = arr[residual_index, 0]
        y_value = arr[residual_index, 1]
        residual_value = y_value - x_value * k
        residual_list.append(residual_value)
    #     进行ADF Test
    from statsmodels.tsa.stattools import adfuller

    result = adfuller(residual_list, 1)
    #     print(result)

    #     进行判断
    if result[0] < result[4]['1%']:
        return "stable"
    elif result[0] < result[4]['5%']:
        return "r-stable"
    else:
        return "unstable"
