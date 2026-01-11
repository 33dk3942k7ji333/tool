import asyncio
import random

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()
semaphore = asyncio.Semaphore(5)


@app.post("/getDataFromDao")
async def api_get_data(id: int):
    async with semaphore:
        if random.random() < 0.5:
            raise HTTPException(status_code=500, detail="Internal Server Error")

        await asyncio.sleep(1)

        header = "id~|status~|value"
        row = f"{id}~|success~|{random.randint(1, 100)}"
        csv_content = f"{header}\n{row}\n{row}"

        return {"id": id, "status": "success", "data": csv_content}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
