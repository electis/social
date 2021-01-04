# import declaration
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
import random
import uvicorn

# initialization
app = FastAPI()

# mount static folder to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template instance for returning webpage via template engine
templates = Jinja2Templates(directory="templates")


# Pydantic data model class
class Item(BaseModel):
    # language: str
    language = 'english'


# hello world, GET method, return string
@app.get("/", response_class=PlainTextResponse)
async def hello():
    return "Hello World!"


# random number, GET method, return string
@app.get('/random-number', response_class=PlainTextResponse)
async def random_number():
    return str(random.randrange(100))


# check isAlpha, GET method, query parameter, return JSON
@app.get('/alpha')
async def alpha(text: str):
    result = {'text': text, 'is_alpha': text.isalpha()}

    return result


# create new user, POST method, form fields, return JSON
@app.post('/create-user')
async def create_user(id: str = Form(...), name: str = Form(...)):
    # code for authentication, validation, update database

    data = {'id': id, 'name': name}
    result = {'status_code': '0', 'status_message': 'Success', 'data': data}

    return result


# update language, PUT method, JSON input, return string
@app.put('/update-language', response_class=PlainTextResponse)
async def update_language(item: Item):
    language = item.language

    return "Successfully updated language to %s" % (language)


# serve webpage, GET method, return HTML
@app.get('/get-webpage', response_class=HTMLResponse)
async def get_webpage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Contact Us"})


# file response, GET method, return file as attachment
@app.get('/get-language-file/{language}')
async def get_language_file(language: str):
    file_name = "%s.json" % (language)
    file_path = "./static/language/" + file_name

    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


# main
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
