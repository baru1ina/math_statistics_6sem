import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import math

from scipy.stats import norm, t, uniform
size = [20, 100]
quantiles = [30.14, 124.34]


def hyp_testing(distName, param=0):
    results = []
    for i in range(len(size)):
        if distName == t:
            x = (distName.rvs(df=param, size=size[i]))
            name = "Student's distribution"
        elif distName == uniform:
            x = (distName.rvs(loc=-np.sqrt(3), scale=2 * np.sqrt(3), size=size[i]))
            name = "Uniform distribution"
        else:
            x = (distName.rvs(size=size[i]))
            name = "Normal distribution"

        print(f"РАСПРЕДЕЛЕНИЕ {name}; РАЗМЕР ВЫБОРКИ n = {size[i]}\n")

        alpha = 0.05
        k = round(1 + (3.3 * math.log10(size[i])))
        print("k = ", k)

        chi_q = quantiles[i]
        a = min(x)
        b = max(x)

        deltas = np.linspace(a, b, k+1)

        deltas[-1] = float('inf')
        deltas[0] = float('-inf')

        print("------------------------deltas: ")
        print(deltas)
        print("-------------------------------\n")
        m = 0
        while m != len(deltas) - 1:
            if distName == t:
                p_i = distName.cdf(deltas[m + 1], df=param) - distName.cdf(deltas[m], df=param)
            elif distName == uniform:
                p_i = (distName.cdf(deltas[m + 1], loc=-np.sqrt(3), scale=2 * np.sqrt(3))
                       - distName.cdf(deltas[m], loc=-np.sqrt(3), scale=2 * np.sqrt(3)))
            else:
                p_i = distName.cdf(deltas[m + 1]) - distName.cdf(deltas[m])
            if size[i] * p_i >= 5:
                m += 1
                continue
            if m + 1 == len(deltas) - 1:
                deltas = np.delete(deltas, m)
                k -= 1
                continue
            deltas = np.delete(deltas, (m+1))
            k -= 1

        print("new k = ", k)
        print("------------------------new deltas: ")
        print(deltas)
        print("-------------------------------")


        P = []
        for j in range(len(deltas)-1):
            if distName == t:
                p_i = distName.cdf(deltas[j + 1], df=param) - distName.cdf(deltas[j], df=param)
            elif distName == uniform:
                p_i = (distName.cdf(deltas[j + 1], loc=-np.sqrt(3), scale=2 * np.sqrt(3))
                       - distName.cdf(deltas[j], loc=-np.sqrt(3), scale=2 * np.sqrt(3)))
            else:
                p_i = distName.cdf(deltas[j + 1]) - distName.cdf(deltas[j])
            P.append(p_i)

        sumP = sum(P)
        if sumP == 1.0:
            print("SUM { p_i } = ", sumP, " - ВЕРНО\n")
        else:
            print("SUM { p_i } != 1.0 - woopsie! sth went wrong...\n")

        n_k = [0 for _ in range(k)]
        for value in x:
            for j in range(k):
                if deltas[j] < value <= deltas[j + 1]:
                    n_k[j] += 1

        print("------------------------------n_k: ")
        print(n_k)
        print("-------------------------------")

        sumN_K = sum(n_k)
        if sumN_K == size[i]:
            print("sum n_k = ", sumN_K, " - ВЕРНО\n")
        else:
            print("sum n_k != ", size[i], " - woopsie! sth went wrong...\n")

        print("-------------------------------P: ")
        print(P)
        print("-------------------------------\n")

        chi_Bs = [((n_k[m] - size[i] * P[m]) ** 2) / (size[i] * P[m]) for m in range(k)]

        print("-------------------------------chi_Bs: ")
        print(chi_Bs)
        print("-------------------------------\n")

        chi_B = sum(chi_Bs)

        print("chi_B = ", chi_B)

        print("chi_q = ", chi_q)

        if chi_B < chi_q:
            results.append(True)
            print("\nchi_B < chi_q => гипотеза 𝐻_0 на данном этапе проверки принимается\n\n")
        else:
            results.append(False)
            print("\nchi_B >= chi_q => гипотеза 𝐻_0 на данном этапе проверки отвергается: выберем одно из альтернативных распределений"
                  " и повторим процедуру проверки\n\n")

    return results


print("\n----------> testing NORMAL DISTRIBUTION\n")
print("РЕЗУЛЬТАТ: ", hyp_testing(norm))
print("<--------------------------------------------------------------\n")

print("\n----------> testing STUDENT'S DISTRIBUTION\n")
print("РЕЗУЛЬТАТ: ", hyp_testing(t, 3))
print("<--------------------------------------------------------------\n")

print("\n----------> testing UNIFORM DISTRIBUTION\n")
print("РЕЗУЛЬТАТ: ", hyp_testing(uniform))
print("<--------------------------------------------------------------\n")
