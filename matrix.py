class Matrix:
    def __init__(self, rows: int, cols: int, data):
        self.rows = rows
        self.cols = cols

        data_creator = []
        for i in range(rows):
            data_creator.append([0]*cols)

        for i, v in enumerate(data):
            data_creator[i // cols][i % cols] = v

        self.data = data_creator

    # TODO: Add out of bounds checking
    def get_element(self, row_num, col_num):
        return self.data[row_num][col_num]

    # TODO: Add out of bounds checking
    def set_element(self, row_num, col_num, new_value):
        self.data[row_num][col_num] = new_value

    def __str__(self):
        out = ""
        for a in self.data:
            out += str(a) + "\n"
        return out

    def __add__(self, matrix2):
        if not (self.rows == matrix2.rows and self.cols == matrix2.cols):
            raise Exception("Adding matrices requires matrices of the same size")

        result = Matrix(self.rows, self.cols, [])
        for r in range(self.rows):
            for c in range(self.cols):
                result.set_element(r, c, self.get_element(r, c) + matrix2.get_element(r, c))

        return result

    def divide_by_scalar(self, divisor):
        output = Matrix(self.rows, self.cols, [])

        for r in range(self.rows):
            for c in range(self.cols):
                output.set_element(r, c, self.get_element(r, c) / divisor)

        return output

    def multiply_by_matrix(self, matrix2):
        if self.cols != matrix2.rows:
            # We cannot multiply these matrices
            raise Exception("Number of rows of matrix 1 must equal number of cols of matrix 2 to multiply")

        output = Matrix(self.rows, matrix2.cols, [])

        for r in range(self.rows):
            cur = 0
            for matrix2_row in range(matrix2.cols):
                cur = 0
                for matrix1_element in range(self.cols):
                    cur += self.get_element(r, matrix1_element) * matrix2.get_element(matrix1_element, matrix2_row)
                output.set_element(r, matrix2_row, cur)

        return output

    def multiply_by_scalar(self, multiplier):
        output = Matrix(self.rows, self.cols, [])

        for r in range(self.rows):
            for c in range(self.cols):
                output.set_element(r, c, self.get_element(r, c) * multiplier)

        return output

    def __mul__(self, multiplier):
        if isinstance(multiplier, Matrix):
            return self.multiply_by_matrix(multiplier)
        return self.multiply_by_scalar(multiplier)

    def __rmul__(self, multiplier):
        if isinstance(multiplier, Matrix):
            return multiplier.multiply_by_matrix(self)

        return self.multiply_by_scalar(multiplier)

    def get_minor(self, row, col):
        output = Matrix(self.rows - 1, self.cols - 1, [])

        current_row = 0
        current_col = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if r != row and c != col:
                    output.set_element(current_row, current_col, self.get_element(r, c))
                    current_col += 1
                    if current_col >= self.cols - 1:
                        current_row += 1
                        current_col = 0

        return output

    def determinant(self):
        if self.cols != self.rows:
            raise Exception("Only NxN (square) matrices have a determinant.")

        if self.cols == 1:
            return self.get_element(0, 0)

        out = 0
        for r in range(self.rows):
            mul = 1
            if r % 2 == 1:
                mul = -1
            out += mul * self.get_element(r, 0) * self.get_minor(r, 0).determinant()

        return out

    def transpose(self):
        output = Matrix(self.cols, self.rows, [])

        for r in range(self.rows):
            for c in range(self.cols):
                output.set_element(c, r, self.get_element(r, c))

        return output

    def cofactor_matrix(self):
        output = Matrix(self.rows, self.cols, [])

        for r in range(self.rows):
            for c in range(self.cols):
                mul = 1
                if (r + c) % 2 == 1:
                    mul = -1

                output.set_element(r, c, mul * self.get_minor(r, c).determinant())

        return output

    def inverse(self):
        if self.cols != self.rows:
            raise Exception("Only NxN (square) matrices have an inverse.")

        determinant = self.determinant()

        if determinant == 0:
            raise Exception("This matrix does not have an inverse as the determinant is 0")

        return self.cofactor_matrix().transpose().divide_by_scalar(determinant)
