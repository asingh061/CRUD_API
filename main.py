from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/",summary="API information")
async def read_root():
        return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}  

@app.get("/health",summary="Health check")
async def health_check():
        return {"status": "ok"}

tasks = [
    {"id": 1, "title": "TopGun", "done": False},
    {"id": 2, "title": "TopGun2", "done": True},
    {"id": 3, "title": "TopGun3", "done": False}
]

@app.get("/tasks",summary="List all tasks")
async def get_tasks():
        return tasks

@app.get("/tasks/{id}",summary="Get a single task by id")
async def get_task(id:int):
        for task in tasks:
                if task["id"] == id:
                        return task
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

class TaskCreate(BaseModel):
        title: str

@app.post("/tasks", status_code=201,summary="Create a new task")
async def create_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Task title cannot be empty")
    if not tasks:
        next_id = 1
    else:
        next_id = max(t["id"] for t in tasks) + 1

    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.put("/tasks/{id}",summary="Update an existing task")
async def update_task(id: int, payload: TaskUpdate):
    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=400, detail="At least one field (title or done) must be provided for update")
    for task in tasks:
        if task["id"] == id:
            if payload.title is not None:
                task["title"] = payload.title

            if payload.done is not None:
                task["done"] = payload.done

            return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.delete("/tasks/{id}", status_code=204,summary="Delete a task by id")
async def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=404, detail=f"Task {id} not found")