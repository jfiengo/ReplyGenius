# models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
import numpy as np
from sqlalchemy import TypeDecorator

Base = declarative_base()

# Custom type for vector storage
class Vector(TypeDecorator):
    impl = ARRAY(FLOAT)
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, np.ndarray):
            return value.tolist()
        return value
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return np.array(value)


class Business(Base):
    __tablename__ = 'businesses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    business_type = Column(String(100), nullable=False)
    services = Column(Text)
    hours = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    phone_numbers = relationship("PhoneNumber", back_populates="business", cascade="all, delete-orphan")
    context_items = relationship("ContextItem", back_populates="business", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="business")


class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'
    
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    provider = Column(String(50), nullable=False, default='twilio')
    provider_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="phone_numbers")


class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), nullable=False, unique=True)
    first_interaction_at = Column(DateTime(timezone=True), server_default=func.now())
    last_interaction_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    messages = relationship("Message", back_populates="customer", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    direction = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    message_sid = Column(String(100))
    status = Column(String(20), nullable=False, default='received')
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="messages")
    business = relationship("Business", back_populates="messages")


class ContextItem(Base):
    __tablename__ = 'context_items'
    
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    context_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    embedding = Column(Vector(1536))  # For OpenAI embeddings (adjust dimension as needed)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="context_items")