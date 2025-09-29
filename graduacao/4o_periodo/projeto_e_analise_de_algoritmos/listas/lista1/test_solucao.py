from solucao import *


def test_6():
    raiz = TreeNode(val=100)

    r = TreeNode(val=13)
    l = TreeNode(val=900)
    raiz.left = l
    raiz.right = r

    l.left = TreeNode(val = 9)
    l.right = TreeNode(val = 10)

    min = problema_6(raiz)

    print(min)


def test_7():
    A = [7, 17, 74, 21, 7, 9, 26, 10]
    print(problema_7(A))


def test_8():
    A = [3, 2, 6]
    A = [1, 4, 5, 1, 3, 2, 6, 6]
    k=2
    r = problema_8_b(A, k)
    
    print(r)
#test_6()


#test_7()

test_8()
