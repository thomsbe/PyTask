import graphene
from graphene_django import DjangoObjectType

from pytask.models import ToDoModel


class ToDoType(DjangoObjectType):
    class Meta:
        model = ToDoModel


class CreateToDo(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    duedate = graphene.DateTime()

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        duedate = graphene.DateTime()

    def mutate(self, info, name, description, duedate):
        todo = ToDoModel(name=name, description=description, duedate=duedate)
        todo.save()

        return CreateToDo(
            id = todo.id,
            name = todo.name,
            description = todo.description,
            duedate = todo.duedate
        )

class Query(graphene.ObjectType):
    todos = graphene.List(ToDoType)

    def resolve_todos(self, info):
        return ToDoModel.objects.all()

class Muation(graphene.ObjectType):
    create_todo = CreateToDo.Field()


schema = graphene.Schema(query=Query, mutation=Muation)
