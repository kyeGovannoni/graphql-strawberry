import typing 
import uuid 
import strawberry
from strawberry.types import Info
import datetime
from GraphQLAPI.scalars.custom import Base64
from GraphQLAPI.schemas.directives import Keys



#from .directives import Keys

data = {
  "persons":[
      dict(
         id = 1
        ,first_name= 'Jeff'
        ,last_name = 'Bridges'
        #,is_employee = True
        ,age= 23
        ,admin= 'True'
        #,post= ''
        ,email= 'jeff@hotmail.com'
        ,created_on= datetime.datetime.now()
        ,tag = uuid.uuid4()
   )
  ],
    "posts":[
      dict(
         id = 1
        ,title= 'ripe bananas, carsonagenic? '
        #,is_employee = True
        ,authorId= 1
        ,created_on= datetime.datetime.now()
   ),
    dict(
         id = 2
        ,title= 'ripe bananas, the secret to life? '
        #,is_employee = True
        ,authorId= 1
        ,created_on= datetime.datetime.now()
   )
  ]
}

#resolvers
async def get_persons(root:"Person", info: Info)-> typing.List["Person"]:
  return [Person(**person) for person in data['persons']]   

async def get_person(root:"Person", info: Info, id:int) -> "Person":
    _person=[Person(**person) for person in data['persons'] if person['id'] == id ]
    return _person[0]

async def get_person_for_post(root:"Post", info: Info) -> "Person":
    _person=[Person(**person) for person in data['persons'] if person['id'] == root.authorId ]
    return _person[0]

async def full_name(root: "Person", info: Info) -> str: 
    return f"{root.first_name} {root.last_name} {info.field_name}"

async def get_post(root: "Post", info: Info, id:int) -> typing.List["Post"]:
  post=[Post(**post) for post in data['posts'] if post['id'] == id]
  return post[0]

async def get_posts(root: "Post", info: Info) -> typing.List["Post"]:
  posts=[Post(**post) for post in data['posts']]
  return posts

async def get_posts_for_author(root: "Person", info: Info ) -> "Post":
  posts = [Post(**post) for post in data['posts'] if post['authorId'] == root.id ]   
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
    allPersons: typing.List[Person] = strawberry.field(resolver=get_persons) 
    person: Person = strawberry.field(resolver=get_person)
    allPosts: typing.List[Post] = strawberry.field(resolver=get_posts)

    @strawberry.field
    def base64(self, nput:str)-> Base64:
      return Base64(str.encode(nput))



