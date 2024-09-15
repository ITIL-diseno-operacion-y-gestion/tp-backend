from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "GESTIÓN DE PROBLEMAS"