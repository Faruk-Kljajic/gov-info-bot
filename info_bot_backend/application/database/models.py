# models.py
from sqlalchemy import Column, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chat'

    chat_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    content_id = Column(UUID(as_uuid=True), ForeignKey('content.content_id'))
    created = Column(TIMESTAMP, server_default=func.now())
    last_modified = Column(TIMESTAMP, onupdate=func.now())

    # Relationship to content
    content = relationship("Content", back_populates="chats")


class Content(Base):
    __tablename__ = 'content'

    content_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    prompt = Column(Text)
    answer = Column(Text)
    created = Column(TIMESTAMP, server_default=func.now())

    # Relationship to chat
    chats = relationship("Chat", back_populates="content")
