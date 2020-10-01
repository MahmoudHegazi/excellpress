#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Sheet(Base):
    __tablename__ = 'sheet'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    pr = Column(String(255))
    date = Column(String(255))
    supplier = Column(String(255))
    quait = Column(String(255))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {            
            'id': self.id,
            'name': self.name,            
            'pr': self.pr,
            'date': self.date,
            'supplier': self.supplier,
            'quait': self.quait
        }

        
        

        
        
       
class History(Base):
    __tablename__ = 'history'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    pr = Column(String(20))
    order = Column(String(500))
    suplier = Column(String(500))
    date = Column(String(100))
    #menu_id = Column(Integer, ForeignKey('menu.id'))
    #menu = relationship(Menu)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'pr': self.pr,
            'order': self.order,
            'suplier': self.suplier,
            'date': self.date,
        }   




engine = create_engine('sqlite:///x.db')
Base.metadata.create_all(engine)
