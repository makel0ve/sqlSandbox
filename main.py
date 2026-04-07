import os
import urllib.parse
from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

import db
from config import UPLOAD_FILENAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db.dispose_engine()

    if os.path.exists(UPLOAD_FILENAME):
        os.remove(UPLOAD_FILENAME)


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "wrap.html")


@app.get("/db/{filename:path}/", response_class=HTMLResponse)
async def show_db(request: Request):
    tables = await db.get_tables_name()

    if not tables:
        return templates.TemplateResponse(request, "wrap.html")

    records, column_names, table = await db.get_table_data(
        f"SELECT * FROM {tables[-1]}"
    )

    return templates.TemplateResponse(request, "main.html", {
        "table": table, 
        "tables": tables, 
        "records": records, 
        "column_names": column_names
    })


@app.post("/uploadDB", response_class=RedirectResponse)
async def upload_db(request: Request, file: UploadFile = File()):
    with open(UPLOAD_FILENAME, "wb") as f:
        f.write(await file.read())

    filename = Path(file.filename).stem
    safe_filename = urllib.parse.quote(filename)

    return RedirectResponse(f"/db/{safe_filename}", status_code=303)


@app.post("/choice_table", response_class=HTMLResponse)
async def choice_table(request: Request, data=Body()):
    table_name = data["name"]

    if not await db.validate_table_name(table_name):
        return templates.TemplateResponse(request, "table.html", {
            "records": [],
            "column_names": [],
            "error": f"Таблица '{table_name}' не найдена",
        })

    records, column_names, _ = await db.get_table_data(
        f"SELECT * FROM {table_name}"
    )

    return templates.TemplateResponse(request, "table.html", {
        "records": records,
        "column_names": column_names,
    })


@app.post("/sqlquery", response_class=HTMLResponse)
async def sqlquery(request: Request, data=Body()):
    query = data["name"]

    try:
        records, column_names, table = await db.get_table_data(query)

    except ValueError as e:
        return templates.TemplateResponse(request, "table.html", {
            "records": [],
            "column_names": [],
            "error": str(e),
        })
    
    except Exception as e:
        return templates.TemplateResponse(request, "table.html", {
            "records": [],
            "column_names": [],
            "error": f"Ошибка SQL: {e}",
        })

    return templates.TemplateResponse(request, "table.html", {
        "records": records,
        "column_names": column_names,
        "table": table,
    })


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)