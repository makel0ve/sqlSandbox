import urllib
import urllib.parse
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

import db


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("wrap.html", {"request": request})


@app.get('/{filename}', response_class=HTMLResponse)
async def show_db(request: Request):
    tables = await db.get_tables_name()
    records, column_names, table = await db.get_table_data(f"SELECT * FROM {tables[-1]}")
    
    return templates.TemplateResponse("main.html", {"request": request, "table": table, "tables": tables, "records": records, "column_names": column_names})    


@app.post("/uploadDB", response_class=RedirectResponse)
async def choice_db(request: Request, file: UploadFile = File()):
    with open(f"uploaded_{file.filename}", "wb") as f:
        f.write(await file.read())
    
    filename = Path(file.filename).stem
    safe_filename = urllib.parse.quote(filename)
    
    return RedirectResponse(f"/{safe_filename}", status_code=303) 


@app.post("/choice_table", response_class=HTMLResponse)
async def choice_table(request: Request, data = Body()):
    name = data["name"]

    records, column_names, _ = await db.get_table_data(f"SELECT * FROM {name}")

    return templates.TemplateResponse("table.html", {"request": request, "records": records, "column_names": column_names})


@app.post("/sqlquery", response_class=HTMLResponse)
async def sqlquery(request: Request, data = Body()):
    sqlquery = data["name"]
    try:
        records, column_names, table = await db.get_table_data(sqlquery)
    except:
        tables = await db.get_tables_name()
        records, column_names, table = await db.get_table_data(f"SELECT * FROM {tables[-1]}")
    
    return templates.TemplateResponse("table.html", {"request": request, "records": records, "column_names": column_names, "table": table})
    

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)