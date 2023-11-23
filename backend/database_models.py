from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import datetime

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String)
    password_expire_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    group: Mapped[int] = mapped_column(Integer, sa.ForeignKey("group.id"))
    groups = relationship("Group", backref="users")


class PredictionModel(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    configuration: Mapped[str] = mapped_column(String, nullable=False)
    modify_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    user: Mapped[int] = mapped_column(Integer, sa.ForeignKey("user.id"))
    users = relationship("User", backref="prediction_models")


class File(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    modify_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    path: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[int] = mapped_column(Integer, sa.ForeignKey("user.id"))
    users = relationship("User", backref="files")


class Group(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    permissions = relationship(
        "Permission", secondary='group_permission', backref="groups"
    )


class Permission(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


group_permission_m2m = db.Table(
    "group_permission",
    sa.Column("group_id", sa.ForeignKey(Group.id), primary_key=True),
    sa.Column("permission_id", sa.ForeignKey(Permission.id), primary_key=True),
)
