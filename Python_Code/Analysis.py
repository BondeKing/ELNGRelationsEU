import math


def Exp(list):
    
    sum = 0
    
    for item in list:
        sum += item

    return sum/len(list)



def Var(list):
    
    E = Exp(list)
    sum_v = 0
    
    for item in list:
        sum_v += (item-E)**2
    
    return sum_v/len(list)


def Std(list):
    
    return math.sqrt(Var(list))


def Cov(list1, list2):
    
    if len(list1) != len(list2):
        return None
    
    E1 = Exp(list1)
    E2 = Exp(list2)
    sum_cov = 0
    
    for i in range(len(list1)):
        sum_cov += (list1[i]-E1)*(list2[i]-E2)
    
    return sum_cov/(len(list1)-1)



def Corr(list1, list2):
    
    if len(list1) != len(list2):
        return None
    
    return Cov(list1, list2)/math.sqrt(Var(list1)*Var(list2))


