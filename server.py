from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.templating import Jinja2Templates
from redis_interface import Redis
from pydantic import BaseModel
import datetime
import uvicorn
import base64
import uuid
import time


class Entity(BaseModel):
    name: str
    current_date: str

html_encoded = "PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8dGl0bGU+V2ViR29hdCBTVFVCPC90aXRsZT4KPC9oZWFkPgo8Ym9keSBzdHlsZT0iYmFja2dyb3VuZDogbGF2ZW5kZXIiPgoKICAgIDxjZW50ZXIgY2xhc3M9ImNlbnRlci1jb250IG1pZGRsZSIgc3R5bGU9Im1hcmdpbi10b3A6IDUlIj4KICAgICAgICA8aHI+PGRpdiBpZD0iZGl2LWNvbnQiIHN0eWxlPSJiYWNrZ3JvdW5kOiB3aGl0ZXNtb2tlIj4KICAgICAgICAgICAgPGJyPgogICAgICAgICAgICA8cHJlPiA8aT48Yj5UaGUgU2lnbmF0dXJlIENoYW5nZXMgRXZlcnkgMyBTZWNvbmRzPC9iPjwvaT4gPC9wcmU+CiAgICAgICAgICAgIDxici8+CiAgICAgICAgICAgIDxwcmU+PGI+Q2xvY2s6IDwvYj48L3ByZT48cHJlIGlkPSJ0aW1lciI+PC9wcmU+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9InRleHQtY29udCIgc3R5bGU9InBhZGRpbmc6IDVweDsiPgogICAgICAgICAgICAgICAgPHByZT48Yj5TaWduYXR1cmU6IDwvYj48L3ByZT48cHJlIGlkPSJyYW5kb20tdGV4dCI+PC9wcmU+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICA8YnIvPgogICAgICAgIDwvZGl2Pjxocj4KICAgIDwvY2VudGVyPgo8L2JvZHk+CjxzY3JpcHQ+CiAgICAoCiAgICAgICAgZnVuY3Rpb24oKSB7CiAgICAgICAgICAgIGxldCBkID0gbmV3IERhdGUoKTsKICAgICAgICAgICAgbGV0IHRpbWVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInRpbWVyIik7CiAgICAgICAgICAgIHRpbWVyLmlubmVySFRNTCA9IGAke2QuZ2V0RGF0ZSgpfS0ke2QuZ2V0TW9udGgoKX0tJHtkLmdldEZ1bGxZZWFyKCl9ICR7ZC5nZXRIb3VycygpfToke2QuZ2V0TWludXRlcygpfToke2QuZ2V0U2Vjb25kcygpfToke2QuZ2V0TWlsbGlzZWNvbmRzKCl9YDsKICAgICAgICAgICAgbGV0IHNpZyA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJyYW5kb20tdGV4dCIpOwogICAgICAgICAgICBzaWcuaW5uZXJIVE1MID0gYnRvYSgiVGhpcyBpcyBhIGNvb2wgdGVzdCBmb3IgQXV0b21hdGlvbiEhISEiKTsKICAgICAgICAgICAgY29uc3QgdXBkYXRlX3RpbWUgPSBzZXRJbnRlcnZhbChmdW5jdGlvbiAoKSB7CiAgICAgICAgICAgICAgICBkID0gbmV3IERhdGUoKTsKICAgICAgICAgICAgICAgIHRpbWVyLmlubmVySFRNTCA9IGAke2QuZ2V0RGF0ZSgpfS0ke2QuZ2V0TW9udGgoKX0tJHtkLmdldEZ1bGxZZWFyKCl9ICR7ZC5nZXRIb3VycygpfToke2QuZ2V0TWludXRlcygpfToke2QuZ2V0U2Vjb25kcygpfToke2QuZ2V0TWlsbGlzZWNvbmRzKCl9YDsKICAgICAgICAgICAgfSwgMTAwMCk7CiAgICAgICAgICAgIGNvbnN0IGNoYW5nZV90ZXh0ID0gc2V0SW50ZXJ2YWwoZnVuY3Rpb24oKXsKICAgICAgICAgICAgICAgIHNpZy5pbm5lckhUTUwgPSBudWxsOwogICAgICAgICAgICAgICAgc2lnLmlubmVySFRNTCA9IGJ0b2EoYCR7dGltZXIuaW5uZXJIVE1MfToke01hdGgucmFuZG9tKCl9YCk7CiAgICAgICAgICAgIH0sIDMwMDApOwogICAgICAgICAgICB1cGRhdGVfdGltZSgpOwogICAgICAgICAgICBjaGFuZ2VfdGV4dCgpOwogICAgICAgIH0KICAgICkoKTsKPC9zY3JpcHQ+CjwvaHRtbD4="
with open("./index.html", "w") as fin:
    content = base64.b64decode(html_encoded).decode()
    fin.write(content)
    fin.close()

app = FastAPI()
templates = Jinja2Templates(directory='.')
redis = Redis(db=1, data={
    0: {uuid.uuid1().hex: {"name": None, "currentDate": None}},
    -1: {uuid.uuid3(uuid.NAMESPACE_URL, 'test1').hex: {"name": "bar", "currentDate": "1970-01-01T00:00:00.000000"}},
    -2: {uuid.uuid4().hex: {"name": "foo", "currentDate": datetime.datetime.today()}},
    -3: {uuid.uuid5(uuid.NAMESPACE_X500, 'test2').hex: {"name": "spam", "currentDate": "2002-20-02T00:00:00.000000"}}
})

app.add_middleware(
    GZipMiddleware, minimum_size=512
)
app.add_middleware(
    CORSMiddleware, allow_methods=["*"], allow_origins=["*"], allow_headers=["*"], allow_credentials=True
)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"], www_redirect=True
)


@app.on_event('startup')
async def prepare_rds():
    redis.dump_to_storage()

@app.middleware('http')
async def add_process_time_header(req: Request, call_next):
    start_time = time.time()
    res: Response = await call_next(req)
    res.headers.setdefault('x-process-time', str(time.time() - start_time))
    return res

@app.middleware('http')
async def add_response_id(req: Request, call_next):
    res: Response = await call_next(req)
    res.headers.setdefault('x-response-id', uuid.uuid5(uuid.NAMESPACE_DNS, f'{req.client.host}:{time.time()}').hex)
    return res

@app.get('/')
async def index(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})

@app.get('/api/entities')
async def get_entities():
    return JSONResponse(
        jsonable_encoder({
            'status': 'success',
            'timestamp': datetime.datetime.now().isoformat(),
            'entities': redis.data[redis.db]
        }),
        status_code=200,
        media_type='application/json',
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
    )

@app.get('/api/entities/{entity_id}')
async def get_entity_by_id(entity_id):
    try:
        if not redis.get(int(entity_id)):
            raise
        entity = redis.get(int(entity_id))
        return JSONResponse(
            jsonable_encoder({
                'status': 'success',
                'timestamp': datetime.datetime.now().isoformat(),
                'entity': entity
            }),
            status_code=200,
            media_type='application/json',
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
        )
    except:
        return JSONResponse(
            jsonable_encoder({
                'status': 'fail',
                'timestamp': datetime.datetime.now().isoformat(),
                'reason': 'not found'
            }),
            status_code=404,
            media_type='application/json',
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
        )

@app.post('/api/entities')
async def create_new_entity(entity: Entity):
    try:
        if not entity.name or not entity.current_date:
            raise
        data = {
            uuid.uuid5(uuid.NAMESPACE_X500, time.time().hex()).hex: {
                "name": entity.name,
                "currentDate": entity.current_date
            }
        }
        entry = -(len(redis.data[redis.db])+1)
        redis.set(entry, data)
        redis.dump_to_storage()
        return JSONResponse(
            jsonable_encoder({
                'status': 'success',
                'timestamp': datetime.datetime.now().isoformat()
            }),
            status_code=201,
            media_type='application/json',
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
        )
    except:
        return JSONResponse(
            jsonable_encoder({
                'status': 'fail',
                'timestamp': datetime.datetime.now().isoformat(),
                'reason': 'missing body / params'
            }),
            status_code=400,
            media_type='application/json',
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
        )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8443)
