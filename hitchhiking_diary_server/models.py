import enum
import hashlib
import uuid
from functools import cached_property

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from hitchhiking_diary_server.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")


class TripStatus(enum.Enum):
    draft = "draft"
    in_progress = "in-progress"
    archived = "archived"


class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    status = Column(Enum(TripStatus), default=TripStatus.draft, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="trips")
    # TODO: reimplement as lazy='dynamic'
    records = relationship(
        "TripRecord",
        back_populates="trip",
        cascade="all, delete-orphan",
        primaryjoin="and_(TripRecord.trip_id==Trip.id, TripRecord.deleted_at==None)",
        order_by="desc(TripRecord.happened_at)",
    )


class TripRecordType(enum.Enum):
    interesting = "interesting"
    workout = "workout"
    camping = "camping"
    pickup = "pickup"
    dropoff = "dropoff"
    story = "story"

    def title(self):
        match self:
            case self.interesting:
                return "Interesting"
            case self.workout:
                return "Workout"
            case self.camping:
                return "Camping"
            case self.pickup:
                return "Pickup"
            case self.dropoff:
                return "Drop-off"
            case self.story:
                return "Story"

    def icon(self):
        match self:
            case self.interesting:
                return "bi-star-fill"
            case self.workout:
                return "bi-person-walking"
            case self.camping:
                return "bi-house-fill"
            case self.pickup:
                return "bi-person-raised-hand"
            case self.dropoff:
                return "bi-sign-stop"
            case self.story:
                return "bi-pencil"


class TripRecord(Base):
    __tablename__ = "trip_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(TripRecordType), nullable=False)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False)
    content = Column(Text, nullable=True)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    happened_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    trip = relationship("Trip", back_populates="records")
    photos = relationship("Photo", back_populates="record", cascade="all, delete-orphan")

    @property
    def latitude(self):
        return to_shape(self.location).x

    @property
    def longitude(self):
        return to_shape(self.location).y

    @cached_property
    def hash(self):
        return hashlib.md5(str(self.id).encode()).hexdigest()


class Photo(Base):
    __tablename__ = "photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id = Column(UUID(as_uuid=True), ForeignKey("trip_records.id"), nullable=False)
    mime = Column(String, nullable=True)
    path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    record = relationship(
        "TripRecord",
        back_populates="photos",
        primaryjoin="and_(Photo.record_id==TripRecord.id, Photo.deleted_at==None)",
    )
