#! /usr/bin/env python
#
#
# @file: meta
# @time: 2022/01/29
# @author: Mori
#
import pymongo
import pymongo.results
from typing import Dict, List, Union
from tornado.options import options as project_options
from motor.motor_tornado import MotorClient, MotorDatabase, MotorCollection
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection

project_options.define("MONGO_URI", default="mongo_uri", help="mongo url")
project_options.define("MONGO_DB", default="mongo_db", help="mongo database name")


class MotorMeta(type):
    __db = None
    __client = None
    __cached_collection = {}

    @classmethod
    def get_client(cls) -> Union[MotorClient, AgnosticClient]:
        if not cls.__client:
            cls.__client = MotorClient(project_options.MONGO_URI)
        return cls.__client

    @classmethod
    def get_db(cls) -> Union[MotorDatabase, AgnosticDatabase]:
        if not cls.__db:
            cls.__db = cls.get_client().get_database(project_options.MONGO_DB)
        return cls.__db

    @classmethod
    def read_collection(
        cls, collection_name: str
    ) -> Union[MotorCollection, AgnosticCollection]:
        if collection_name in cls.__cached_collection:
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

        for method_or_attr in dir(target_collection):
            setattr(new_cls, method_or_attr, getattr(target_collection, method_or_attr))
        return new_cls


class Collection(object, metaclass=MotorMeta):
    db: MotorDatabase
    client: MotorClient
    collection: MotorCollection

    @classmethod
    async def bulk_write(
        cls, requests: List, ordered=True, bypass_document_validation=False, **kwargs
    ) -> pymongo.results.BulkWriteResult:
        ...

    @classmethod
    async def insert_one(
        cls, document: Dict, bypass_document_validation=False, **kwargs
    ):
        ...

    @classmethod
    async def insert_many(
        cls, documents, ordered=True, bypass_document_validation=False, **kwargs
    ):
        ...

    @classmethod
    async def replace_one(
        cls,
        filter,
        replacement,
        upsert=False,
        bypass_document_validation=False,
        collation=None,
        hint=None,
        **kwargs
    ):
        ...

    @classmethod
    async def update_one(
        cls,
        filter,
        update,
        upsert=False,
        bypass_document_validation=False,
        collation=None,
        array_filters=None,
        hint=None,
        **kwargs
    ):
        ...

    @classmethod
    async def update_many(
        cls,
        filter,
        update,
        upsert=False,
        array_filters=None,
        bypass_document_validation=False,
        collation=None,
        hint=None,
        **kwargs
    ):
        ...

    @classmethod
    async def delete_one(
        cls, filter, collation=None, hint=None, **kwargs
    ) -> pymongo.results.DeleteResult:
        ...

    @classmethod
    async def delete_many(cls, filter, collation=None, hint=None, **kwargs):
        ...

    @classmethod
    async def find_one(cls, filter=None, *args, **kwargs):
        ...

    @classmethod
    async def find(cls, *args, **kwargs):
        ...

    @classmethod
    def find_one_and_update(
        cls,
        filter,
        update,
        projection=None,
        sort=None,
        upsert=False,
        return_document=pymongo.ReturnDocument.AFTER,
        array_filters=None,
        hint=None,
        session=None,
        **kwargs
    ):
        ...
