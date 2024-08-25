from backend.common.schema import SchemaBase


class PersonRelationSchema(SchemaBase):
    person_id: int
    other_id: int
    detail: str | None = None