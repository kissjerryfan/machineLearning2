import os

import src.test.test as test

if __name__ == "__main__":
    # 1. 测试单目标优化模型-仅记录一个结果----------
    # (1) 调用函数见“行25-30”
    # (2) 参数“soea”表示运行所使用的优化算法，参数“method”表示运行所使用的模型（如linear）
    # (3) 结果保存在“\results\single-objective\运行所使用的模型(如linear)\”中；
    # (4) 运行前需先创建好对应的文件夹——如：“\results\single-objective\linear\CoDE\test”

    # soea ：{1: 'CoDE', 2: 'DE_rand_1_bin', 3:'CoDE_toZero', 4: 'CoDE_10p_toZero', 5:'CoDE_20p_toZero',
    # 6:'CoDE_10p_lr_toZero', 7:'CoDE_20p_lr_toZero', 8:'CoDE_random10p_toZero', 9:'CoDE_random20p_toZero',
    # 10:'CoDE_random30p_toZero'} method ：{1: 'linear', 2: 'BPNN', 3:'NN', 4:'MLP', 5:'mlp3', 6: 'mlp5'}
    # test.run_ssdp_test(soea, method)
    test.run_ssdp_test(soea=1, method=1)  # 根据linear/CoDE算法训练结果进行测试
