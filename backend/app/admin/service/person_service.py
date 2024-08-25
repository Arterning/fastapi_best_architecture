#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from typing import Sequence

from backend.app.admin.crud.crud_person import person_dao
from backend.app.admin.crud.crud_person_relation import person_relation_dao
from backend.app.admin.crud.crud_attachment import attachment_dao
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session

from backend.app.admin.model import Person
from backend.app.admin.schema.person import CreatePersonParam, UpdatePersonParam
from backend.app.admin.schema.attachment import UpdateAttachmentParam
from backend.app.admin.schema.person_relation import PersonRelationSchema
from backend.app.admin.model.sys_org_person import sys_org_person

class PersonService:
    
    @staticmethod
    async def get(*, pk: int) -> Person:
        async with async_db_session() as db:
            person = await person_dao.get(db, pk)
            if not person:
                raise errors.NotFoundError(msg='人物不存在')
            return person
        
    @staticmethod
    async def get_docs(pk: int):
        async with async_db_session() as db:
            person = await person_dao.get(db, pk)
            name = person.name
            docs = person.docs
            ocr_res = []
            for doc in docs:
                ocr_res.append(doc.ocr_res)
            return ocr_res, name


    @staticmethod
    async def get_all(name: str = None) -> Sequence[Person]:
        async with async_db_session() as db:
            all = await person_dao.get_all(db, name=name)
            return all
    
    @staticmethod
    async def get_hot_persons() -> Sequence[Person]:
        async with async_db_session() as db:
            persons = await person_dao.get_hot_persons(db)
            # for person in persons:
            #     icon = person_service.get_person_icon(person)
            #     setattr(person, 'icon', icon)
            return persons
        
    @staticmethod
    async def get_hot_words() -> Sequence[Person]:
        async with async_db_session() as db:
            words = await person_dao.get_hot_words(db)
            return words

    @staticmethod
    async def get_count() -> int:
        async with async_db_session() as db:
            count = await person_dao.get_count(db)
            return count

    @staticmethod
    async def get_select(*, name: str = None, job: str = None, docs: list[int] = None) -> Select:
        return await person_dao.get_list(name=name, job=job, docs=docs)

   
    @staticmethod
    async def create(*, obj: CreatePersonParam) -> None:
        async with async_db_session.begin() as db:
            person = await person_dao.create(db, obj)
            if obj.attachments is not None:
                ids = [attachment['id'] for attachment in obj.attachments]
                await attachment_dao.update_by_ids(db, ids=ids, person_id=person.id)
            if obj.relations is not None:
                for r in obj.relations:
                    other_id = r["other_id"]
                    detail = r["detail"]
                    if other_id and detail:
                        exist = await person_relation_dao.select_model_by_columns(db, person_id=person.id, other_id=other_id)
                        if exist is None:
                            relation = PersonRelationSchema(person_id=person.id, other_id=other_id, detail=detail)
                            await person_relation_dao.create_model(db, relation)
                        else:
                            await person_relation_dao.update_model(db, pk=exist.id, obj={
                                "person_id": person.id,
                                "other_id": other_id,
                                "detail": detail,
                            })
                        
                        reverse = await person_relation_dao.select_model_by_columns(db, person_id=other_id, other_id=person.id)
                        if reverse is None:
                            reverse = PersonRelationSchema(person_id=other_id, other_id=person.id, detail=detail)
                            await person_relation_dao.create_model(db, reverse)
                        else:
                            await person_relation_dao.update_model(db, pk=reverse.id, obj={
                                "person_id": other_id,
                                "other_id": person.id,
                                "detail": detail,
                            })
                
        

    @staticmethod
    async def batch_create(*, objs: list[CreatePersonParam]) -> None:
        async with async_db_session.begin() as db:
            await person_dao.batch_create(db, objs)

    @staticmethod
    async def update(*, pk: int, obj: UpdatePersonParam) -> int:
        async with async_db_session.begin() as db:
            if obj.attachments:
                ids = [attachment['id'] for attachment in obj.attachments]
                await attachment_dao.update_by_ids(db, ids=ids, person_id=pk)
                first = obj.attachments[0]
                obj.icon = first['obj_name']
            count = await person_dao.update(db, pk, obj)
            if obj.relations is not None:
                for r in obj.relations:
                    other_id = r["other_id"]
                    detail = r["detail"]
                    if other_id and detail:
                        exist = await person_relation_dao.select_model_by_columns(db, person_id=pk, other_id=other_id)
                        if exist is None:
                            relation = PersonRelationSchema(person_id=pk, other_id=other_id, detail=detail)
                            await person_relation_dao.create_model(db, relation)
                        else:
                            await person_relation_dao.update_model(db, pk=exist.id, obj={
                                "person_id": pk,
                                "other_id": other_id,
                                "detail": detail,
                            })
                        
                        reverse = await person_relation_dao.select_model_by_columns(db, person_id=other_id, other_id=pk)
                        if reverse is None:
                            reverse = PersonRelationSchema(person_id=other_id, other_id=pk, detail=detail)
                            await person_relation_dao.create_model(db, reverse)
                        else:
                            await person_relation_dao.update_model(db, pk=reverse.id, obj={
                                "person_id": other_id,
                                "other_id": pk,
                                "detail": detail,
                            })
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await person_dao.delete(db, pk)
            return count

    @staticmethod
    async def get_by_names(names: list[str]) -> Sequence[Person]:
        async with async_db_session.begin() as db:
           persons = await person_dao.get_by_names(db, names)
           return persons


    @staticmethod
    async def relate_org(person_id: int, org_id: int) -> None:
         async with async_db_session() as db:
            insert_stmt = sys_org_person.insert().values(person_id=person_id, org_id=org_id)
            await db.execute(insert_stmt)
            await db.commit()

    @staticmethod
    def get_person_icon(person: Person) -> str:
        attachments = person.attachments
        icon = ''
        if attachments:
            icon = attachments[0].obj_name
        return icon


    @staticmethod
    async def get_relations(person_id: int, person_name: str) -> dict:
        async with async_db_session() as db:
            relations = await person_relation_dao.get_relations(db, pk=person_id)
            nodes = []
            lines = []
            persons = []
            person = await person_dao.get(db, pk=person_id)
            icon = person.icon
            nodes.append({
                "id": str(person_id),
                "text": person_name,
                "color": "#ec6941",
                "borderColor": "#ff875e",
                "data": {
                    "icon": icon,
                }
            })
            relation_list = []
            for relation in relations:
                other_id = relation.other_id
                detail = relation.detail

                relation_list.append({
                    "person_id": person_id,
                    "other_id": other_id, 
                    "detail": detail,
                })

                person = await person_dao.get(db, pk=other_id)
                icon = person.icon

                # 添加节点
                nodes.append({
                    "id": str(other_id),
                    "text": person.name,
                    "data": {
                        "icon": icon,
                    }
                })

                persons.append({
                    "id": other_id,
                    "name": person.name
                })

                # 添加线条
                lines.append({
                    "from": str(person_id),
                    "to": str(other_id),
                    "text": detail
                })

            relation_json = {
                "nodes": nodes,
                "lines": lines
            }

            return relation_json, relation_list, persons

person_service = PersonService()