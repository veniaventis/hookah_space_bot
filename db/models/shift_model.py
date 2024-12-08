from sqlalchemy import BigInteger, Integer, Text, ForeignKey, Stirng, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.database import Base
from .order_model import Order


class Shift(Base):
    __tablename__ = 'shifts'

    # Поля начала смены

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    open_datetime: Mapped[str] = mapped_column(DateTime, nullable=False)
    point: Mapped[str] = mapped_column(Text, nullable=False)
    start_shift_cash: Mapped[int] = mapped_column(Integer, nullable=False)
    start_shift_tobacco_photo: Mapped[str] = mapped_column(Text, nullable=False)

    # Связь заказов со сменами

    orders: Mapped[Order] = relationship('Order', back_populates='shift', uselist=True)

    # Поля конца смены

    end_shift_cash: Mapped[int] = mapped_column(Integer, nullable=False)
    end_shift_terminal_report: Mapped[str] = mapped_column(Integer, nullable=False)
    end_shift_tobacco_photo: Mapped[str] = mapped_column(Text, nullable=False)
    end_shift_coals_count: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_information: Mapped[str] = mapped_column(Text, nullable=True)
    close_datetime: Mapped[str] = mapped_column(DateTime, nullable=False)
