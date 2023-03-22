import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
# from .models import Books
from .models import Quizzes, Category, Question, Answer

# class BooksType(DjangoObjectType):
#     class Meta:
#         model = Books
#         fields = ('id', 'title', 'excerpt')


# class Query(graphene.ObjectType):
#     all_books = graphene.List(BooksType)
#
#     def resolve_all_books(root, info):
#         return Books.objects.all()
#
#
# schema = graphene.Schema(query=Query)

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ('id', 'title', 'category', 'quiz')


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('title', 'quiz')


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ('question', 'answer_text')


class Query(graphene.ObjectType):

    # all_quizzes = DjangoListField(QuizzesType) --- another way of receiving similar result
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    # all_questions = graphene.List(QuestionType)

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

    # def resolve_all_questions(root, info):
    #     return Question.objects.all()


# class CategoryMutation(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#
#     category = graphene.Field(CategoryType)
#
#     @classmethod
#     def mutate(cls, root, info, name):
#         category = Category(name=name)
#         category.save()
#         return CategoryMutation(category=category)
#
class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryMutation(category=category)


class QuizzesMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)

    quiz = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, id, title):
        quiz = Quizzes.objects.get(id=id)
        quiz.title = title
        quiz.save()
        return QuizzesMutation(quiz=quiz)


class Mutation(graphene.ObjectType):
    update_category = CategoryMutation.Field()
    update_quizzes = QuizzesMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
