# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea  # 导入geatpy库

class moea_NSGA2_DE_toZero(ea.MoeaAlgorithm):
    """
moea_NSGA2_DE_templet : class - 基于NSGA-II-DE算法的多目标进化算法模板

算法描述:
    采用NSGA-II-DE进行多目标优化，算法详见参考文献[1]。
模板使用注意:
    与模板相比，进行的修改，对参数小于1的，直接设置为0.

参考文献:
    [1] Deb K , Pratap A , Agarwal S , et al. A fast and elitist multiobjective
    genetic algorithm: NSGA-II[J]. IEEE Transactions on Evolutionary
    Computation, 2002, 6(2):0-197.

    [2] Tanabe R., Fukunaga A. (2014) Reevaluating Exponential Crossover in
    Differential Evolution. In: Bartz-Beielstein T., Branke J., Filipič B.,
    Smith J. (eds) Parallel Problem Solving from Nature – PPSN XIII. PPSN 2014.
    Lecture Notes in Computer Science, vol 8672. Springer, Cham

    """

    def __init__(self, problem, population):
        ea.MoeaAlgorithm.__init__(self, problem, population)  # 先调用父类构造方法
        self.name = 'NSGA2-DE-toZero'
        if self.problem.M < 10:
            self.ndSort = ea.ndsortESS  # 采用ENS_SS进行非支配排序
        else:
            self.ndSort = ea.ndsortTNS  # 高维目标采用T_ENS进行非支配排序，速度一般会比ENS_SS要快
        self.selFunc = 'tour'  # 选择方式，采用锦标赛选择
        if population.Encoding == 'RI':
            self.mutOper = ea.Mutde(F=0.5)  # 生成差分变异算子对象
            self.recOper = ea.Xovbd(XOVR=0.5, Half=True)  # 生成二项式分布交叉算子对象，这里的XOVR即为DE中的Cr
        else:
            raise RuntimeError('编码方式必须为''RI''.')

    def reinsertion(self, population, offspring, NUM):

        """
        描述:
            重插入个体产生新一代种群（采用父子合并选择的策略）。
            NUM为所需要保留到下一代的个体数目。
            注：这里对原版NSGA-II进行等价的修改：先按帕累托分级和拥挤距离来计算出种群个体的适应度，
            然后调用dup选择算子(详见help(ea.dup))来根据适应度从大到小的顺序选择出个体保留到下一代。
            这跟原版NSGA-II的选择方法所得的结果是完全一样的。
        """

        # 父子两代合并
        population = population + offspring
        # 选择个体保留到下一代
        [levels, criLevel] = self.ndSort(self.problem.maxormins * population.ObjV, NUM, None,
                                         population.CV)  # 对NUM个个体进行非支配分层
        dis = ea.crowdis(population.ObjV, levels)  # 计算拥挤距离
        population.FitnV[:, 0] = np.argsort(np.lexsort(np.array([dis, -levels])), kind='mergesort')  # 计算适应度
        chooseFlag = ea.selecting('dup', population.FitnV, NUM)  # 调用低级选择算子dup进行基于适应度排序的选择，保留NUM个个体
        return population[chooseFlag]

    def run(self):
        # ==========================初始化配置===========================
        population = self.population
        NIND = population.sizes
        self.initialization()  # 初始化算法模板的一些动态参数
        # ===========================准备进化============================
        if population.Chrom is None:
            population.initChrom()  # 初始化种群染色体矩阵（内含解码，详见Population类的源码）
        else:
            population.Phen = population.decoding()  # 染色体解码
        self.problem.aimFunc(population)  # 计算种群的目标函数值
        self.evalsNum = population.sizes  # 记录评价次数
        [levels, criLevel] = self.ndSort(self.problem.maxormins * population.ObjV, NIND, None,
                                         population.CV)  # 对NIND个个体进行非支配分层
        population.FitnV[:, 0] = 1 / levels  # 直接根据levels来计算初代个体的适应度
        # ===========================开始进化============================
        while self.terminated(population) == False:
            # 进行差分进化操作
            r0 = ea.selecting(self.selFunc, population.FitnV, NIND)  # 得到基向量索引
            offspring = population.copy()  # 存储子代种群
            offspring.Chrom = self.mutOper.do(offspring.Encoding, offspring.Chrom, offspring.Field, r0)  # 变异
            tempPop = population + offspring  # 当代种群个体与变异个体进行合并（为的是后面用于重组）
            offspring.Chrom = self.recOper.do(tempPop.Chrom)  # 重组

            # ====================================设置小于1的参数设置为0======================================
            offspring.Chrom[offspring.Chrom < 1] = 0

            # 求进化后个体的目标函数值
            offspring.Phen = offspring.decoding()  # 染色体解码
            self.problem.aimFunc(offspring)
            self.evalsNum += offspring.sizes  # 更新评价次数
            # 重插入生成新一代种群
            population = self.reinsertion(population, offspring, NIND)

        return self.finishing(population)  # 调用finishing完成后续工作并返回结果