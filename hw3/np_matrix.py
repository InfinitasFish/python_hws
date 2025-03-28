import numpy as np


class MatrixFileMixin:
    def save_matrix_to_file(self, fname):
        with open(fname, 'w') as f:
            f.write(str(self))


class MatrixReprMixin:
    def __str__(self):
        rs = ''
        for row in self.matrix:
            rs += '[ ' + ' '.join(map(str, row)) + ' ]' + '\n'
        return rs


class MatrixPropertyMixin:
    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix_2d):
        if not (isinstance(matrix_2d, list) or isinstance(matrix_2d[0], list) or isinstance(matrix_2d, np.ndarray)):
            raise ValueError('not a matrix: matrix.setter')
        self._matrix = np.array(matrix_2d, dtype=np.float32)
        if self.matrix.ndim != 2:
            raise ValueError('not a matrix: matrix.setter')
        self.shape = self._matrix.shape


class MatrixOperationsMixin:
    def __add__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(self.matrix + np.array(other))
        elif isinstance(other, BorrowMatrix):
            return self.__class__(self.matrix + other.matrix)
        raise NotImplemented('not implemented mixin: __add__')

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(self.matrix * np.array(other))
        elif isinstance(other, BorrowMatrix):
            return self.__class__(self.matrix * other.matrix)
        raise NotImplemented('not implemented mixin: __mul__')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __matmul__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(self.matrix @ np.array(other))
        elif isinstance(other, BorrowMatrix):
            return self.__class__(self.matrix @ other.matrix)
        raise NotImplemented('not implemented mixin: __matmul__')

    def __rmatmul__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(np.array(other) @ self.matrix)
        elif isinstance(other, BorrowMatrix):
            return self.__class__(other.matrix @ self.matrix)
        raise NotImplemented('not implemented mixin: __rmatmul__')

    def __sub__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(self.matrix - np.array(other))
        elif isinstance(other, BorrowMatrix):
            return self.__class__(self.matrix - other.matrix)
        raise NotImplemented('not implemented mixin: __sub__')

    def __rsub__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(np.array(other) - self.matrix)
        elif isinstance(other, BorrowMatrix):
            return self.__class__(other.matrix - self.matrix)
        raise NotImplemented('not implemented mixin: __rsub__')

    def __truediv__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(self.matrix / np.array(other))
        elif isinstance(other, BorrowMatrix):
            return self.__class__(self.matrix / other.matrix)
        raise NotImplemented('not implemented mixin: __truediv__')

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, np.ndarray)):
            return self.__class__(np.array(other) / self.matrix)
        elif isinstance(other, BorrowMatrix):
            return self.__class__(other.matrix / self.matrix)
        raise NotImplemented('not implemented mixin: __rtruediv__')

    def __pow__(self, power):
        if isinstance(power, (int, float, np.ndarray)):
            return self.__class__(self.matrix ** np.array(power))
        elif isinstance(power, BorrowMatrix):
            return self.__class__(self.matrix ** power.matrix)
        raise NotImplemented('not implemented mixin: __pow__')

    def __rpow__(self, base):
        if isinstance(base, (int, float, np.ndarray)):
            return self.__class__(np.array(base) ** self.matrix)
        elif isinstance(base, BorrowMatrix):
            return self.__class__(base.matrix ** self.matrix)
        raise NotImplemented('not implemented mixin: __rpow__')


class BorrowMatrix(MatrixPropertyMixin, MatrixReprMixin,
                   MatrixOperationsMixin, MatrixFileMixin):
    def __init__(self, matrix_2d):
        self.matrix = matrix_2d


def test_op(op):
    np.random.seed(0)
    mat1 = BorrowMatrix(np.random.randint(0, 10, (10, 10)).tolist())
    np.random.seed(0)
    mat2 = BorrowMatrix(np.random.randint(0, 10, (10, 10)).tolist())

    if op == '+':
        mat3 = mat1 + mat2
    elif op == '*':
        mat3 = mat1 * mat2
    elif op == '@':
        mat3 = mat1 @ mat2
    elif op == '/':
        mat3 = mat1 / mat2
    elif op == '**':
        op = 'p'
        mat3 = mat1 ** mat2
    else:
        raise ValueError('invalid operation: test_op()')

    mat3.save_matrix_to_file(f'matrix{ord(op)}.txt')


def main():
    test_op('+')
    test_op('*')
    test_op('@')
    test_op('/')
    test_op('**')


if __name__ == '__main__':
    main()
