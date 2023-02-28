import typing 
import uuid 
import strawberry
from strawberry.types import Info
import datetime
from GraphQLAPI.utils.directives import Keys

DATA_LOOKUP = {
  "actors":[
      dict(
         id = 1
        ,first_name= 'Jeff'
        ,last_name = 'Bridges'
        ,age= 73
        ,admin= 'True'
        ,height= 185
        ,data_created_on= datetime.datetime.now()
        ,uniqueId = uuid.uuid4()
   ), 
   dict(
         id = 3
        ,first_name= 'John'
        ,last_name = 'Goodman'
        ,age= 70
        ,admin= 'True'
        ,height= 188
        ,data_created_on= datetime.datetime.now()
        ,uniqueId = uuid.uuid4()
   ),
   dict(
         id = 4
        ,first_name= 'Julianne'
        ,last_name = 'Moore'
        ,age= 62
        ,admin= 'True'
        ,height= 160
        ,data_created_on= datetime.datetime.now()
        ,uniqueId = uuid.uuid4()
   ),
    dict(
         id = 2
        ,first_name= 'Jeff'
        ,last_name = 'Goldblum'
        ,age= 71
        ,admin= 'True'
        ,height= 180
        ,data_created_on= datetime.datetime.now()
        ,uniqueId = uuid.uuid4()
   )
  ],
    "films":[
      dict(
         id = 1
        ,title= 'The Big Lebowski'
        ,actorId= 1
        ,date= datetime.date(1998,5,1)
   ),
    dict(
         id = 2
        ,title= 'The Fly'
        ,actorId= 2
        ,date= datetime.date(1986,3,23)
   ), dict(
         id = 3
        ,title= 'Hell or High Water'
        ,actorId= 1
        ,date= datetime.date(2016,1,12)
   ),
  ],
  "actorFilms":[
   dict(
    actorId=1,
    filmId= 1
   ),
   dict(
    actorId=3,
    filmId= 1
   ),
   dict(
    actorId=4,
    filmId= 1
   ),
   dict(
    actorId=1,
    filmId= 3
   ),
    dict(
    actorId=2,
    filmId= 2
   ),
  ]
}

#resolvers
async def get_actors(root:"Actor", info: Info, name:typing.Optional[str]=None)-> typing.List["Actor"]:
  if name:
     return [Actor(**actor) for actor in DATA_LOOKUP['actors'] if actor['first_name'].lower() == name.lower() ]  
  return [Actor(**actor) for actor in DATA_LOOKUP['actors']]   

async def get_actor(root:"Actor", info: Info, id:int) -> "Actor":
    _actor=[Actor(**actor) for actor in DATA_LOOKUP['actors'] if actor['id'] == id ]
    return _actor[0]

async def get_actors_for_film(root:"Film", info: Info) -> typing.List["Actor"]:
    actor_ids = [mapping['actorId'] for mapping in DATA_LOOKUP['actorFilms'] if mapping["filmId"] == root.id] 
    _actors=[Actor(**actor) for actor in DATA_LOOKUP['actors'] if actor['id'] in actor_ids]
    return _actors

async def full_name(root: "Actor", info: Info) -> str: 
    return f"{root.first_name} {root.last_name}"#{info.field_name}"

async def get_film(root: "Film", info: Info, id:int) -> typing.List["Film"]:
  film=[Film(**film) for film in DATA_LOOKUP['films'] if film['id'] == id]
  return film[0]

async def get_films(root: "Film", info: Info) -> typing.List["Film"]:
  films=[Film(**film) for film in DATA_LOOKUP['films']]
  return films

async def get_films_for_actor(root: "Actor", info: Info ) -> "Film":
  film_ids = [mapping['filmId'] for mapping in DATA_LOOKUP['actorFilms'] if mapping["actorId"] == root.id] 
  films = [Film(**film) for film in DATA_LOOKUP['films'] if film['id'] in film_ids]   
  return films

@strawberry.type
class Film:
  actorId: strawberry.Private[str]
  id: strawberry.Private[str]
  title: str
  actors: typing.List["Actor"] = strawberry.field(resolver=get_actors_for_film)
  date: datetime.date

##schema 
#@strawberry.type(directives=[Keys(fields="id")])
@strawberry.type
class Actor:
  id: strawberry.Private[str]
  first_name: strawberry.Private[str]
  last_name: strawberry.Private[str]
  full_name: str = strawberry.field(resolver=full_name)
  age: int
  admin: str
  films: typing.List["Film"] = strawberry.field(resolver=get_films_for_actor)
  height: int
  data_created_on: datetime.datetime
  uniqueId: uuid.UUID


@strawberry.type
class FilmQuery:
    getActors: typing.List[Actor] = strawberry.field(resolver=get_actors) 
    getActor: Actor = strawberry.field(resolver=get_actor)
    getAllFilms: typing.List[Film] = strawberry.field(resolver=get_films)


