from fastapi import FastAPI

app = FastAPI()

numbers = [10, 20, 30]

@app.get("/")
def hello_world():
    return {"message": "Welcome to FastAPI"}

# GET - Display all numbers
@app.get("/numbers")
def get_numbers():
    return {"numbers": numbers}

# GET - Add two numbers
@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

# POST - Insert a number
@app.post("/numbers")
def post_number(num: int):
    numbers.append(num)
    return {"message": "Number added", "numbers": numbers}

# PUT - Update a number
@app.put("/numbers")
def put_number(old: int, new: int):
    if old in numbers:
        index = numbers.index(old)
        numbers[index] = new
        return {"message": "Number updated", "numbers": numbers}
    return {"message": "Number not found"}

# DELETE - Delete a number
@app.delete("/numbers")
def delete_number(num: int):
    if num in numbers:
        numbers.remove(num)
        return {"message": "Number deleted", "numbers": numbers}
    return {"message": "Number not found"}