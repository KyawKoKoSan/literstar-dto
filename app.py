from __future__ import annotations

from dataclasses import dataclass

from litestar import Litestar,Controller, get,post, put, patch
from litestar.dto import DataclassDTO, DTOConfig, DTOData


# get process


# @dataclass
# class Address:
#     street: str
#     city: str
#     country: str


# @dataclass
# class Person:
#     name: str
#     age: int
#     email: str
#     address: Address
#     children: list[Person]


# class ReadDTO(DataclassDTO[Person]):
#     config = DTOConfig(
#         exclude={"email", "address.street", "children.0.email", "children.0.address"},
#         rename_fields={"address": "location"},
#         rename_strategy="upper",
#         max_nested_depth =2,
#     )


# @get("/person/{name:str}", return_dto=ReadDTO, sync_to_thread=False)
# def get_person(name: str) -> Person:
#     # Your logic to retrieve the person goes here
#     # For demonstration purposes, a placeholder Person instance is returned
#     address = Address(street="123 Main St", city="Cityville", country="Countryland")
#     child1 = Person(name="Child1", age=10, email="child1@example.com", address=address, children=[])
#     child2 = Person(name="Child2", age=8, email="child2@example.com", address=address, children=[])
#     return Person(
#         name=name,
#         age=30,
#         email=f"email_of_{name}@example.com",
#         address=address,
#         children=[child1, child2],
#     )

@dataclass
class Person:
    name: str
    age: int
    email: str
    id: int


class ReadDTO(DataclassDTO[Person]):
    config = DTOConfig(exclude={"email"})


class WriteDTO(DataclassDTO[Person]):
    config = DTOConfig(exclude={"id"})


class PatchDTO(DataclassDTO[Person]):
    config = DTOConfig(exclude={"id"}, partial=True)


class PersonController(Controller):
    dto = WriteDTO
    return_dto = ReadDTO

    @post("/person", sync_to_thread=False)
    def create_person(self, data: DTOData[Person]) -> Person:
        # Logic for persisting the person goes here
        return data.create_instance(id=1)

    @put("/person/{person_id:int}", sync_to_thread=False)
    def update_person(self, person_id: int, data: DTOData[Person]) -> Person:
        # Usually the Person would be retrieved from a database
        person = Person(id=person_id, name="John", age=50, email="email_of_john@example.com")
        return data.update_instance(person)

    @patch("/person/{person_id:int}", dto=PatchDTO, sync_to_thread=False)
    def patch_person(self, person_id: int, data: DTOData[Person]) -> Person:
        # Usually the Person would be retrieved from a database
        person = Person(id=person_id, name="John", age=50, email="email_of_john@example.com")
        return data.update_instance(person)


app = Litestar(route_handlers=[PersonController])