import decimal
import uuid

from sqlalchemy import DECIMAL, ForeignKey, MetaData, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

meta_obj = MetaData()


class Base(DeclarativeBase):
    metadata = meta_obj


class BaseMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=True)


class Menu(Base, BaseMixin):
    __tablename__ = 'menu'

    # submenu_counter: Mapped[int] = mapped_column(SmallInteger, nullable=False, insert_default=0)
    # dish_counter: Mapped[int] = mapped_column(SmallInteger, nullable=False, insert_default=0)
    submenus: Mapped[list['SubMenu']] = relationship(
        back_populates='menu',
        cascade='all, delete',
        passive_deletes=True,
    )


class SubMenu(Base, BaseMixin):
    __tablename__ = 'submenu'

    # dish_counter: Mapped[int] = mapped_column(SmallInteger, nullable=False, insert_default=0)
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)
    menu: Mapped['Menu'] = relationship(back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu',
        cascade='all, delete',
        passive_deletes=True,
    )


class Dish(Base, BaseMixin):
    __tablename__ = 'dish'

    price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(precision=6, scale=2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
    submenu: Mapped['SubMenu'] = relationship(back_populates='dishes')
