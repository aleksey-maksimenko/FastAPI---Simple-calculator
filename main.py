from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from сalculator import Calculator

app = FastAPI()
calc = Calculator()

# модель с двумя операндами - для эндпоинтов с вызовом одной операции
class Operands(BaseModel):
    a: float
    b: float

# модель для простого выражения с двумя операндами
class SimpleExpression(BaseModel):
    a: float
    op: str
    b: float
# модель для сложного выражения в виде строки
class ComplexExpression(BaseModel):
    expression: str

# эндпоинты для одиночных операций
@app.post("/sum/")
async def sum(op: Operands):
    result = calc.sum(op.a, op.b) # вызов соотетствующего метода для двух операндов
    return {"expression": f'{op.a}+{op.b}',
            "result": result}

@app.post("/subtract/")
async def subtract(op: Operands):
    result = calc.subtract(op.a, op.b)
    return {"expression": f'{op.a}-{op.b}',
            "result": result}

@app.post("/multiply/")
async def multiply(op: Operands):
    result = calc.multiply(op.a, op.b)
    return {"expression": f'{op.a}*{op.b}',
            "result": result}

@app.post("/divide/")
async def divide(op: Operands):
    try:
        result = calc.divide(op.a, op.b)
        return {"expression": f'{op.a}/{op.b}',
                "result": result}
    except ValueError as e: # предусматриваем возможность нулевого делителя
        raise HTTPException(status_code=400, detail=str(e))

# эндпоинт для создания простого выражения
@app.post("/create_expression/")
async def create_expression(expr: SimpleExpression):
    try:
        calc.set_expression(expr.a, expr.op, expr.b)
        return {"message": "Expression created",
                "expression": calc.get_expression()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# получить текущее выражение
@app.get("/current_expression/")
async def current_expression():
    return {"current_expression": calc.get_expression()}

# получить результат текущего выражения
@app.get("/get_result/")
async def evaluate():
    try:
        result = calc.get_result()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# вычислить составное выражение в виде строки
@app.post("/eval_complex/")
async def get_result(expr: ComplexExpression):
    try:
        result = calc.evaluate(expr.expression)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
