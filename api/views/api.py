from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request, name: str = "mundo"):
    return {"message": f"Olá, {name}!"}
