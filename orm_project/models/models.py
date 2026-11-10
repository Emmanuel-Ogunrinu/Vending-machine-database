# models.py
#
# This file is where you define your ORM models. Models represent tables in the database,
# and each instance of a model corresponds to a row in that table.
#
# Models should inherit from the `Base` class, which provides methods for interacting with the database,
# such as saving records, querying, and deleting.
#
# In this file, you will:
#   - Define your own models, from your database schema in this project, by subclassing the `Base` class.
#   - Use `Column` objects to define columns and their types (e.g., `Integer`, `String`).
#   - Add attributes to each model class to represent columns in the corresponding database table.
#   - Define additional methods in the models as necessary for specific functionality (e.g., custom queries,
#     business logic, etc.).
#
#
# Students should implement their own models, specifying the columns using `Column` and selecting the appropriate
# `types` for each column, such as `Integer`, `String`, `Boolean`, etc.
#
# Below you can find two models examples that demonstrate the usage of the base class

from orm.base import Base
from orm.columns import Column
from orm.datatypes import Integer, String, Boolean, Decimal, Date, Timestamp, Text, Enum

class Customer(Base):
    """Customer model - base customer entity"""

    customer_id = Column(Integer, primary_key=True)
    tracking_code = Column(String(50), nullable=False)
    created_at = Column(Timestamp)
    last_activity = Column(Timestamp)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customer_id = kwargs.get('customer_id')
        self.tracking_code = kwargs.get('tracking_code')
        self.created_at = kwargs.get('created_at')
        self.last_activity = kwargs.get('last_activity')
        self.foreign_keys = []

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class RegisteredCustomer(Base):
    """Registered customer with account"""

    customer_id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    registration_date = Column(Timestamp)
    loyalty_points = Column(Integer, default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customer_id = kwargs.get('customer_id')
        self.email = kwargs.get('email')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.date_of_birth = kwargs.get('date_of_birth')
        self.registration_date = kwargs.get('registration_date')
        self.loyalty_points = kwargs.get('loyalty_points', 0)
        self.foreign_keys = []

    def full_name(self):
        """Get customer's full name"""
        return f"{self.first_name} {self.last_name}"

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class Product(Base):
    """Product model - items available for purchase"""

    product_id = Column(Integer, primary_key=True)
    sku = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    base_price = Column(Decimal(10, 2), nullable=False)
    weight = Column(Decimal(8, 2))
    width = Column(Decimal(8, 2))
    height = Column(Decimal(8, 2))
    depth = Column(Decimal(8, 2))
    expiration_date = Column(Date)
    created_at = Column(Timestamp)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_id = kwargs.get('product_id')
        self.sku = kwargs.get('sku')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.base_price = kwargs.get('base_price')
        self.weight = kwargs.get('weight')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.depth = kwargs.get('depth')
        self.expiration_date = kwargs.get('expiration_date')
        self.created_at = kwargs.get('created_at')
        self.foreign_keys = []

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class Category(Base):
    """Product category with hierarchical structure"""

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)
    parent_category_id = Column(Integer)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_id = kwargs.get('category_id')
        self.category_name = kwargs.get('category_name')
        self.parent_category_id = kwargs.get('parent_category_id')
        self.description = kwargs.get('description')
        self.is_active = kwargs.get('is_active', True)
        self.foreign_keys = []

    def deactivate(self):
        """Deactivate the category"""
        self.is_active = False
        self.save()

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class Order(Base):
    """Customer order for products"""
    _table_name = '`Order`'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    order_date = Column(Timestamp)
    pickup_machine_id = Column(String(20))
    order_status = Column(String(50), default='pending')
    total_amount = Column(Decimal(10, 2), nullable=False)
    pickup_code = Column(String(10))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_id = kwargs.get('order_id')
        self.customer_id = kwargs.get('customer_id')
        self.order_date = kwargs.get('order_date')
        self.pickup_machine_id = kwargs.get('pickup_machine_id')
        self.order_status = kwargs.get('order_status', 'pending')
        self.total_amount = kwargs.get('total_amount')
        self.pickup_code = kwargs.get('pickup_code')
        self.foreign_keys = []

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class OrderItem(Base):
    """Individual items within an order"""

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Decimal(10, 2), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_item_id = kwargs.get('order_item_id')
        self.order_id = kwargs.get('order_id')
        self.product_id = kwargs.get('product_id')
        self.quantity = kwargs.get('quantity')
        self.unit_price = kwargs.get('unit_price')
        self.foreign_keys = []

    def subtotal(self):
        """Calculate line item subtotal"""
        return float(self.unit_price) * self.quantity

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class VendingMachine(Base):
    """Smart vending machine"""

    machine_id = Column(String(20), primary_key=True)
    location_id = Column(Integer, nullable=False)
    model_number = Column(String(50), nullable=False)
    installation_date = Column(Date, nullable=False)
    last_maintenance = Column(Timestamp)
    operational_status = Column(String(50), default='online')
    total_slots = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.machine_id = kwargs.get('machine_id')
        self.location_id = kwargs.get('location_id')
        self.model_number = kwargs.get('model_number')
        self.installation_date = kwargs.get('installation_date')
        self.last_maintenance = kwargs.get('last_maintenance')
        self.operational_status = kwargs.get('operational_status', 'online')
        self.total_slots = kwargs.get('total_slots')
        self.foreign_keys = []

    def is_operational(self):
        """Check if machine is operational"""
        return self.operational_status == 'online'

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class VendingSlot(Base):
    """Individual slot within a vending machine"""

    slot_id = Column(Integer, primary_key=True)
    machine_id = Column(String(20), nullable=False)
    slot_number = Column(Integer, nullable=False)
    product_id = Column(Integer)
    current_quantity = Column(Integer, default=0)
    max_capacity = Column(Integer, nullable=False)
    temperature_zone = Column(String(50), default='ambient')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.slot_id = kwargs.get('slot_id')
        self.machine_id = kwargs.get('machine_id')
        self.slot_number = kwargs.get('slot_number')
        self.product_id = kwargs.get('product_id')
        self.current_quantity = kwargs.get('current_quantity', 0)
        self.max_capacity = kwargs.get('max_capacity')
        self.temperature_zone = kwargs.get('temperature_zone', 'ambient')
        self.foreign_keys = []

    def is_empty(self):
        """Check if slot is empty"""
        return self.current_quantity == 0

    def needs_restocking(self):
        """Check if slot needs restocking"""
        return self.current_quantity < (self.max_capacity * 0.25)

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class Location(Base):
    """Physical location where vending machines are placed"""

    location_id = Column(Integer, primary_key=True)
    address_id = Column(Integer, nullable=False)
    location_name = Column(String(255), nullable=False)
    operating_hours = Column(String(100))
    accessibility_features = Column(Text)
    foot_traffic_rating = Column(Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_id = kwargs.get('location_id')
        self.address_id = kwargs.get('address_id')
        self.location_name = kwargs.get('location_name')
        self.operating_hours = kwargs.get('operating_hours')
        self.accessibility_features = kwargs.get('accessibility_features')
        self.foot_traffic_rating = kwargs.get('foot_traffic_rating')
        self.foreign_keys = []

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class Inventory(Base):
    """Product inventory at each location"""

    inventory_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    location_id = Column(Integer, nullable=False)
    current_stock = Column(Integer, default=0)
    minimum_threshold = Column(Integer, nullable=False)
    last_updated = Column(Timestamp)
    reserved_quantity = Column(Integer, default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory_id = kwargs.get('inventory_id')
        self.product_id = kwargs.get('product_id')
        self.location_id = kwargs.get('location_id')
        self.current_stock = kwargs.get('current_stock', 0)
        self.minimum_threshold = kwargs.get('minimum_threshold')
        self.last_updated = kwargs.get('last_updated')
        self.reserved_quantity = kwargs.get('reserved_quantity', 0)
        self.foreign_keys = []

    def available_quantity(self):
        """Calculate available quantity"""
        return self.current_stock - self.reserved_quantity

    def needs_restock(self):
        """Check if inventory is below minimum threshold"""
        return self.current_stock < self.minimum_threshold

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()


class ProductReview(Base):
    """Customer product reviews"""

    review_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text)
    review_date = Column(Timestamp)
    helpful_votes = Column(Integer, default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.review_id = kwargs.get('review_id')
        self.customer_id = kwargs.get('customer_id')
        self.product_id = kwargs.get('product_id')
        self.rating = kwargs.get('rating')
        self.review_text = kwargs.get('review_text')
        self.review_date = kwargs.get('review_date')
        self.helpful_votes = kwargs.get('helpful_votes', 0)
        self.foreign_keys = []

    def is_positive(self):
        """Check if review is positive (4-5 stars)"""
        return self.rating >= 4

    def foreign_key(self, key, on_delete, on_update):
        self.foreign_keys.append(Column(Integer, foreign_key=key, on_delete=on_delete, on_update=on_update))

    @classmethod
    def descriptor(cls):
        return cls.__name__.lower()




