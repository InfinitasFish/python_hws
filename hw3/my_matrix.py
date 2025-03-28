import numpy as np
from functools import reduce
import operator
from np_matrix import MatrixFileMixin


class MatrixHashMixin:
    def __hash__(self):
        """
        Возвращает хеш от кортежа (размерность, произведение сумм строк матрица)
        """
        mul_sum = reduce(operator.mul, (map(sum, self.matrix)))
        return hash((self.shape, mul_sum))


class MyMatrix(MatrixHashMixin, MatrixFileMixin):
    def __init__(self, list_2d):

        if not isinstance(list_2d, list) or not isinstance(list_2d[0], list):
            raise ValueError('not a matrix: __init__')
        h, w = len(list_2d), len(list_2d[0])
        if h == 0 or w == 0:
            raise ValueError('empty elements: __init__')
        for row in list_2d:
            if w != len(row):
                raise ValueError('inconsistent shape: __init__')

        self.matrix = list_2d
        self.shape = (h, w)

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    self.matrix[i][j] += other
            return self

        elif isinstance(other, MyMatrix):
            if self.shape == other.shape:
                for i in range(other.shape[0]):
                    for j in range(other.shape[1]):
                        self.matrix[i][j] += other.matrix[i][j]
                return self
            else:
                raise ValueError('incompatible shapes: __add__')
        else:
            raise ValueError('incompatible ltype: __add__')

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    self.matrix[i][j] *= other
            return self

        elif isinstance(other, MyMatrix):
            if self.shape == other.shape:
                for i in range(other.shape[0]):
                    for j in range(other.shape[1]):
                        self.matrix[i][j] *= other.matrix[i][j]
                return self
            else:
                raise ValueError('incompatible shapes: __mul__')
        else:
            raise ValueError('incompatible ltype: __mul__')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __matmul__(self, other):
        if isinstance(other, list):
            rmat = MyMatrix(other)
            return self.__matmul__(rmat)
        elif isinstance(other, MyMatrix):
            if not self.shape[1] == other.shape[0]:
                raise ValueError('incompatible shapes: __matmul__')
            h1, w1 = self.shape
            h2, w2 = other.shape
            new_matrix = MyMatrix([[0 for _ in range(w2)] for _ in range(h1)])
            for i in range(h1):
                for j in range(w2):
                    for k in range(h2):
                        new_matrix.matrix[i][j] += (self.matrix[i][k] * other.matrix[k][j])
            return new_matrix
        else:
            raise ValueError('incompatible rtype: __matmul__')

    def __rmatmul__(self, other):
        if isinstance(other, list):
            lmat = MyMatrix(other)
            return lmat @ self
        elif isinstance(other, MyMatrix):
            return other @ self
        else:
            raise ValueError('incompatible ltype: __rmatmul__')

    def __str__(self):
        rs = ''
        for row in self.matrix:
            rs += '[ ' + ' '.join(map(str, row)) + ' ]' + '\n'
        return rs


def test_op(op):
    np.random.seed(0)
    mat1 = MyMatrix(np.random.randint(0, 10, (10, 10)).tolist())
    np.random.seed(0)
    mat2 = MyMatrix(np.random.randint(0, 10, (10, 10)).tolist())

    # can't create file with '*' in its name
    with open(f'matrix{ord(op)}.txt', 'w') as f:
        if op == '+':
            mat3 = mat1 + mat2
        elif op == '*':
            mat3 = mat1 * mat2
        elif op == '@':
            mat3 = mat1 @ mat2
        f.write(str(mat3))


def hash_task_solve():
    A = MyMatrix([[1,2,3], [3,2,1]])
    C = MyMatrix([[3,2,1], [1,2,3]])
    B = MyMatrix([[2,1], [0,0], [0,0]])
    D = MyMatrix([[2,1], [0,0], [0,0]])

    A.save_matrix_to_file('A.txt')
    B.save_matrix_to_file('B.txt')
    C.save_matrix_to_file('C.txt')
    D.save_matrix_to_file('D.txt')

    AB = A @ B
    CD = C @ D

    AB.save_matrix_to_file('AB.txt')
    CD.save_matrix_to_file('CD.txt')

    with open('artefacts/3.3/hash.txt', 'w') as f:
        f.write(f'{hash(AB)}\n')
        f.write(f'{hash(CD)}\n')

    # all True
    #print(A.matrix != C.matrix, hash(A) == hash(C), B.matrix == D.matrix, AB.matrix != CD.matrix)


def main():
    # 3.1
    #test_op('+')
    #test_op('*')
    #test_op('@')

    # 3.3
    hash_task_solve()


if __name__ == '__main__':
    main()
