class Calculator:
    def __init__(self):
        self.expression = "" # изначально пустое выражение

    def sum(self, a: float, b: float):
        return a + b

    def subtract(self, a: float, b: float):
        return a - b

    def multiply(self, a: float, b: float):
        return a * b

    def divide(self, a: float, b: float):
        if b == 0:
            raise ValueError("Деление на ноль недопустимо!")
        return a / b
    # задать простое выражение a op b
    def set_expression(self, a: float, op: str, b: float):
        if op not in ['+', '-', '*', '/']:
            raise ValueError("Недопустимая операция!")
        self.expression = f"({a} {op} {b}) "
    # получить выражение
    def get_expression(self):
        return self.expression.strip()
    # получить результат
    def get_result(self):
        try:
            result = eval(self.expression) # метод вычисления
            return result
        except Exception as e:
            raise ValueError(f"Ошибка при вычислении выражения: {str(e)}")

    # вычислить выражение, переданное в виде строки (по алгоритму Дейкстры)
    def evaluate(self, expression: str):

        # cписки для хранения чисел и операторов
        values = []
        operators = []
        # вспомогательная функция для применения оператора к двум значениям
        def apply_operator(op: str):
            right = values.pop()
            left = values.pop()
            if op == '+':
                values.append(self.sum(left, right))
            elif op == '-':
                values.append(self.subtract(left, right))
            elif op == '*':
                values.append(self.multiply(left, right))
            elif op == '/':
                values.append(self.divide(left, right))

        # приоритет операторов
        priors = {'+': 1, '-': 1, '*': 2, '/': 2}
        expression = expression.replace(" ", "") # выражение без пробелов
        # парсинг выражение и вычисление по алгоритму Дейкстры
        i = 0
        while i < len(expression):
            # если встретили число или минус перед скобкой
            if expression[i].isdigit() or (expression[i] == '-' and (i == 0 or expression[i - 1] == '(')):
                # считываем всё число
                num_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                values.append(float(num_str)) # в список значений
                continue
            elif expression[i] in priors: # если знак операции
                # применяем операции по приоритету для имеющихся значений
                while (operators and operators[-1] in priors and priors[operators[-1]] >= priors[expression[i]]):
                    apply_operator(operators.pop())
                operators.append(expression[i]) # новый оператор в список
            elif expression[i] == '(': # открывающую скобку просто в список операторов
                operators.append(expression[i])
            elif expression[i] == ')': # при закрывающий нужно вычислить часть выражения
                while operators and operators[-1] != '(': # пока не дойдем до открывающей
                    apply_operator(operators.pop())
                operators.pop()  # удаляем (
            i += 1
        # применение оставшихся операторов
        while operators:
            apply_operator(operators.pop())
        # итоговый результат получается в начале списка
        return values[0]