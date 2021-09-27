from gino import Gino
from aiohttp import web
import datetime
import pydantic
import asyncpg
from pydantic import Field

app = web.Application()
PG_DSN = f'postgres://aiohttp:1234@172.31.61.174:5432/aiohttp'
db = Gino()


class PostModel(db.Model):
    __tablename__ = 'posts'

    title = db.Column(db.String(64))
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.String(64))
    author = db.Column(db.String(64))


class PostSerializer(pydantic.BaseModel):
    title: str
    id: int
    author: str
    created_at: str = Field(default_factory=datetime.datetime.now)



class Post(web.View):

    async def post(self):
        post_data = await self.request.json()
        post_serialized = PostSerializer(**post_data)
        post_data = post_serialized.dict()
        new_post = await PostModel.create(**post_data)
        new_post = new_post.to_dict()
        new_post['created_at'] = str(new_post['created_at'])
        return web.json_response(new_post)

    async def get(self):
        post_id = self.request.match_info['post_id']
        post = await PostModel.get(int(post_id))
        post_data = post.to_dict()
        post_data['created_at'] = str(post_data['created_at'])
        return web.json_response(post_data)

    async def delete(self):
        post_id = self.request.match_info['post_id']
        post = await PostModel.delete.where(PostModel.id == int(post_id)).gino.status()
        return web.json_response(post)


async def init_orm(app):
    print('приложение стартовало')

    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


app.add_routes([web.post('/post', Post)])
app.add_routes([web.get('/post/{post_id:\d+}', Post)])
app.add_routes([web.delete('/post/{post_id:\d+}', Post)])
app.cleanup_ctx.append(init_orm)

web.run_app(app, port=8080)
