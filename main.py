from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
        return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}  

@app.get("/health")
async def health_check():
        return {"status": "ok"}

tasks = [
    {"id": 1, "title": "TopGun", "done": False},
    {"id": 2, "title": "TopGun2", "done": True},
    {"id": 3, "title": "TopGun3", "done": False}
]

@app.get("/tasks")
async def get_tasks():
        return tasks

@app.get("/tasks/{id}")
async def get_task(id:int):
        for task in tasks:
                if task["id"] == id:
                        return task
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

class TaskCreate(BaseModel):
        title: str

@app.post("/tasks", status_code=201)
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