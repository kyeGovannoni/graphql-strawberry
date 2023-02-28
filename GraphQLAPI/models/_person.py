import typing 
import uuid 
import strawberry
from strawberry.types import Info
import datetime
from GraphQLAPI.utils.directives import Keys

DATA_LOOKUP = {
  "persons":[
      dict(
         id = 1
        ,first_name= 'Jeff'
        ,last_name = 'Bridges'
        ,age= 63
        ,admin= 'True'
        ,email= 'jeffB@hotmail.com'
        ,created_on= datetime.datetime.now()
        ,tag = uuid.uuid4()
   ),
    dict(
         id = 2
        ,first_name= 'Jeff'
        ,last_name = 'Goldblum'
        ,age= 71
        ,admin= 'True'
        ,email= 'jeffGB@hotmail.com'
        ,created_on= datetime.datetime.now()
        ,tag = uuid.uuid4()
   )
  ],
    "posts":[
      dict(
         id = 1
        ,title= 'what is GraphQL? '
        ,authorId= 1
        ,created_on= datetime.datetime.now()
   ),
    dict(
         id = 2
        ,title= '1+1=3?'
        ,authorId= 1
        ,created_on= datetime.datetime.now()
   )
  ]
}

#resolvers
async def get_persons(root:"Person", info: Info, name:typing.Optional[str]=None)-> typing.List["Person"]:
  if name:
     return [Person(**person) for person in DATA_LOOKUP['persons'] if person['first_name'].lower() == name.lower() ]  
  return [Person(**person) for person in DATA_LOOKUP['persons']]   

async def get_person(root:"Person", info: Info, id:int) -> "Person":
    _person=[Person(**person) for person in DATA_LOOKUP['persons'] if DATA_LOOKUP['id'] == id ]
    return _person[0]

async def get_person_for_post(root:"Post", info: Info) -> "Person":
    _person=[Person(**person) for person in DATA_LOOKUP['persons'] if person['id'] == root.authorId ]
    return _person[0]

async def full_name(root: "Person", info: Info) -> str: 
    return f"{root.first_name} {root.last_name}"#{info.field_name}"

async def get_post(root: "Post", info: Info, id:int) -> typing.List["Post"]:
  post=[Post(**post) for post in DATA_LOOKUP['posts'] if post['id'] == id]
  return post[0]

async def get_posts(root: "Post", info: Info) -> typing.List["Post"]:
  posts=[Post(**post) for post in DATA_LOOKUP['posts']]
  return posts

async def get_posts_for_author(root: "Person", info: Info ) -> "Post":
  posts = [Post(**post) for post in DATA_LOOKUP['posts'] if post['authorId'] == root.id ]   
  return posts

@strawberry.type
class Post:
  authorId: strawberry.Private[str]
  id: strawberry.Private[str]
  title: str
  author: "Person" = strawberry.field(resolver=get_person_for_post)
  created_on: datetime.datetime

##schema 
#@strawberry.type(directives=[Keys(fields="id")])
@strawberry.type
class Person:
  id: strawberry.Private[str]
  first_name: strawberry.Private[str]
  last_name: strawberry.Private[str]
  full_name: str = strawberry.field(resolver=full_name)
  age: int
  admin: str
  posts: typing.List["Post"] = strawberry.field(resolver=get_posts_for_author)
  email: str
  created_on: datetime.datetime
  tag: uuid.UUID

@strawberry.type
class PersonsQuery:
    getPersons: typing.List[Person] = strawberry.field(resolver=get_persons) 
    getPerson: Person = strawberry.field(resolver=get_person)
    getAllPosts: typing.List[Post] = strawberry.field(resolver=get_posts)


