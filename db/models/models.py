from sqlalchemy import Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.database import Base


class PointOfSale(Base):
    __tablename__ = 'points_of_sale'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Связь с таблицей смен, опционально
    shifts: Mapped[list["Shift"]] = relationship('Shift', back_populates='point_of_sale')


class Employee(Base):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    # Связь с таблицей смен, опционально
    shifts: Mapped[list["Shift"]] = relationship('Shift', back_populates='employee')


class Shift(Base):
    __tablename__ = 'shifts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey('employees.id'), nullable=False)
    point_id: Mapped[int] = mapped_column(Integer, ForeignKey('points_of_sale.id'), nullable=False)
    open_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    point: Mapped[str] = mapped_column(String(100), nullable=False)

    # Поля начала смены
    start_shift_cash: Mapped[int] = mapped_column(Integer, nullable=False)
    start_shift_tobacco_photo_id: Mapped[str] = mapped_column(Text, nullable=False)

    # Поля конца смены
    end_shift_cash: Mapped[int] = mapped_column(Integer, nullable=True)
    end_shift_terminal_report: Mapped[str] = mapped_column(Integer, nullable=True)
    end_shift_tobacco_photo_id: Mapped[str] = mapped_column(Text, nullable=True)
    extra_information: Mapped[str] = mapped_column(Text, nullable=True)
    close_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    # Связи
    employee: Mapped["Employee"] = relationship('Employee', back_populates='shifts')
    point_of_sale: Mapped["PointOfSale"] = relationship('PointOfSale', back_populates='shifts')

