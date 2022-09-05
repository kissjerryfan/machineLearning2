import os
from src.train import training
from src.test import test

if __name__ == "__main__":
    test.run_msdp_test(moea=13, target=[0, 2, 4], method=1)
    # test.run_ssdpM_test(method=1, soea=1)
    # test.run_ssdp_test(soea=1, method=1)
    # training.run_msdp_train(moea=13, targets=[0, 2, 4], predict_model=1)
    # test.run_msdp_test(method=1, moea=13, target=[0, 2, 4])
    # training.run_ssdp_train(soea=1, predict_model=1)  # 运行linear/CoDE算法
    # single_time = True
    # training.run_linearRegresion_model()
    # training.run_RRgcv_model(single_time)
    # training.run_lassoLarsCV(single_time)
    # training.run_Lars(single_time)
    # training.run_LassoLars(single_time)
    # training.run_MLPRegressor(single_time)
    # training.run_randomForestRegressor(single_time)

    # test.run_ssdp_test(soea = 1, method = 1) # 根据linear/CoDE算法训练结果进行测试
    # test.run_msdp_test(method=1, moea=13, target=[0, 2, 4])  # 根据linear/nsga2_random20p_toZero/FPA_NNZ_MSE训练结果进行测试
