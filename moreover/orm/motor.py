#! /usr/bin/env python
#
#
# @file: meta
# @time: 2022/01/29
# @author: Mori
#

import bson
from schema import Schema
from moreover.base.logger import gen_logger
from typing import Dict, List, Tuple, Union
from motor import MotorClient, MotorDatabase, MotorCollection
from motor.core import (
    AgnosticClient,
    AgnosticDatabase,
    AgnosticCollection,
    AgnosticCursor,
)
from moreover.base.config import global_config, define

logger = gen_logger("orm")
CursorOrList = Union[List, AgnosticCursor]

define("MONGO_URI", default_value="MONGO_URI")
define("MONGO_DB", default_value="MONGO_DB")


class MotorMeta(type):
    __db = None
    __client = None
    __cached_collection = {}

    @classmethod
    def get_client(cls) -> Union[MotorClient, AgnosticClient]:
        if not cls.__client:
            cls.__client = MotorClient(global_config.MONGO_URI)
        return cls.__client

    @classmethod
    def get_db(cls) -> Union[MotorDatabase, AgnosticDatabase]:
        if not cls.__db:
            cls.__db = cls.get_client().get_database(global_config.MONGO_DB)
        return cls.__db


    @classmethod
    def read_collection(
        cls, collection_name: str
    ) -> Union[MotorCollection, AgnosticCollection]:
        # print(collection_name)
        if collection_name not in cls.__cached_collection:
            cls.__cached_collection[collection_name] = cls.get_db().get_collection(
                collection_name
            )
        return cls.__cached_collection[collection_name]


    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        setattr(new_cls, "client", cls.get_client())
        setattr(new_cls, "db", cls.get_db())

        target_collection = cls.read_collection(name)
        setattr(new_cls, "collection", target_collection)

        for method_or_attr in filter(
            lambda x: not x.startswith("__") and not hasattr(cls, x),
            dir(target_collection),
        ):
            setattr(new_cls, method_or_attr, getattr(target_collection, method_or_attr))

        schema = getattr(new_cls, "schema")
        indexs = getattr(new_cls, "indexs")

        if schema is not None and not isinstance(schema, Schema):
            raise ValueError(f"{name} orm class: schema is not schema.Schema")
        if schema is None:
            logger.warning(f"{name} orm class schema is empty")

        if not isinstance(indexs, list):
            raise ValueError(f"{name} orm class: indexs is not list")
        if len(indexs) == 0:
            logger.warning(f"{name} orm class indexs is empty")

        logger.info(f"{name} orm class inited")
        return new_cls


class Collection(object, metaclass=MotorMeta):
    db: MotorDatabase
    client: MotorClient
    collection: MotorCollection

    schema: Schema = None
    indexs = []

    def __init__(self, document: Dict) -> None:
        super(Collection, self).__init__()
        self.__document = document
        if self.schema:
            self.__document = self.schema.validate(document)

    @property
    def document(self):
        return self.__document

    def update_document(self, **kwargs):
        if self.schema:
            self.__document = self.schema.validate({**self.__document, **kwargs})
        else:
            self.__document.update(kwargs)

    async def save(self):
        if "_id" in self.__document and self.__document["_id"] is not None:
            await self.collection.replace_one(
                {"_id": self.__document["_id"]}, self.__document
            )
        else:
            insert_result = await self.collection.insert_one(self.__document)
            self.__document.update({"_id": insert_result.inserted_id})
        return self.document

    @classmethod
    async def get(
        cls,
        filter: Dict = None,
        projection: Dict = None,
        sort: List[Tuple[str, int]] = None,
        limit: int = None,
        offset: int = None,
        with_count: bool = False,
        return_cursor: bool = False,
    ) -> Union[Tuple[CursorOrList, int], Tuple[object, int]]:
        cursor = cls.query(
            filter=filter, projection=projection, sort=sort, limit=limit, offset=offset
        )
        count = None
        if with_count:
            count = await cls.count_documents(filter)
        if limit == 1:
            [cls(item) async for item in cursor][0], count
        if return_cursor:
            return cursor, count
        else:
            data = [cls(item) async for item in cursor]
            return data, count

    @classmethod
    async def get_one(cls, id_or_filter: Union[bson.ObjectId, Dict]):
        if isinstance(id_or_filter, bson.ObjectId):
            document = await cls.find_one({"_id": id_or_filter})
        else:
            document = await cls.find_one(id_or_filter)
        return cls(document)
