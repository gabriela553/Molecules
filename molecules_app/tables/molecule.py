from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MoleculeInDB(Base):
    __tablename__ = "molecules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    formula: Mapped[str]
    weight_in_units: Mapped[float]

    def __repr__(self) -> str:

        return f"Molecule(name={self.name!r}, formula={self.formula!r}, weight={self.weight_in_units!r})"
