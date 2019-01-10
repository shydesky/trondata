"""Database module, including the SQLAlchemy database object and DB-related
utilities."""

from sqlalchemy import desc, or_, asc
from sqlalchemy.orm import relationship
from sqlalchemy.sql import sqltypes
from backend.extensions import db
from backend.utils import missing_singleton

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship

class CRUDMixin(object):
    @classmethod
    def create(cls, need_to_commit=True, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(
            **{k: v for k, v in kwargs.items() if v is not missing_singleton}
        )
        return instance.save(need_to_commit=need_to_commit)

    @classmethod
    def create_from_dict(cls, d, need_to_commit=True):
        """Create a new record and save it the database."""
        assert isinstance(d, dict)
        instance = cls(
            **{k: v for k, v in d.items() if v is not missing_singleton}
        )
        return instance.save(need_to_commit=need_to_commit)

    def save(self, need_to_commit=True):
        """Save the record."""
        db.session.add(self)
        db.session.flush()
        if need_to_commit:
            db.session.commit()
        return self

class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    @classmethod
    def column_names(cls):
        from sqlalchemy import inspect
        inst = inspect(cls)
        column_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        return column_names


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id``
    to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (isinstance(record_id, basestring) and record_id.isdigit(),
             isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None