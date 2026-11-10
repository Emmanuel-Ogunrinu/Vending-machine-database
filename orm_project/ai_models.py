"""
AI-Generated Schema Models
Matches ai_schema_v1.sql (31 tables)
Works with your ORM framework
"""

from orm import Base, Column, Integer, String, Text, Boolean, Decimal, Date, Timestamp, Enum


# =============================================
# USER MANAGEMENT MODELS
# =============================================

class Users(Base):
    _table_name = 'Users'
    
    user_id = Column(Integer(), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    date_of_birth = Column(Date())
    created_at = Column(Timestamp())
    updated_at = Column(Timestamp())
    is_active = Column(Boolean(), default=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def orders(self):
        return Orders.filter_by(user_id=self.user_id)
    
    @property
    def reservations(self):
        return Reservations.filter_by(user_id=self.user_id)


class Roles(Base):
    _table_name = 'Roles'
    
    role_id = Column(Integer(), primary_key=True)
    role_name = Column(String(50), nullable=False, unique=True)
    description = Column(Text())


class UserRoles(Base):
    _table_name = 'UserRoles'
    
    user_id = Column(Integer(), primary_key=True)
    role_id = Column(Integer(), primary_key=True)
    assigned_at = Column(Timestamp())


class LoyaltyAccounts(Base):
    _table_name = 'LoyaltyAccounts'
    
    loyalty_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False, unique=True)
    loyalty_tier = Column(Enum('BRONZE', 'SILVER', 'GOLD', 'PLATINUM'), default='BRONZE')
    points_balance = Column(Integer(), default=0)
    lifetime_points = Column(Integer(), default=0)
    tier_expiry_date = Column(Date())


class Addresses(Base):
    _table_name = 'Addresses'
    
    address_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False)
    address_type = Column(Enum('HOME', 'WORK', 'OTHER'), default='HOME')
    street_address = Column(String(255), nullable=False)
    apartment_unit = Column(String(50))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default='USA')
    is_default = Column(Boolean(), default=False)


# =============================================
# PRODUCT MODELS
# =============================================

class Categories(Base):
    _table_name = 'Categories'
    
    category_id = Column(Integer(), primary_key=True)
    category_name = Column(String(100), nullable=False)
    parent_category_id = Column(Integer())
    description = Column(Text())
    image_url = Column(String(500))
    is_active = Column(Boolean(), default=True)
    
    @property
    def products(self):
        pcs = ProductCategories.filter_by(category_id=self.category_id)
        return [Products.get(product_id=pc.product_id) for pc in pcs]


class Suppliers(Base):
    _table_name = 'Suppliers'
    
    supplier_id = Column(Integer(), primary_key=True)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(100))
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    address = Column(String(500))
    payment_terms = Column(String(100))
    is_active = Column(Boolean(), default=True)
    
    @property
    def products(self):
        return Products.filter_by(supplier_id=self.supplier_id)


class Products(Base):
    _table_name = 'Products'
    
    product_id = Column(Integer(), primary_key=True)
    sku = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text())
    base_price = Column(Decimal(10, 2), nullable=False)
    cost_price = Column(Decimal(10, 2))
    weight = Column(Decimal(8, 2))
    dimensions = Column(String(50))
    barcode = Column(String(100))
    image_url = Column(String(500))
    is_perishable = Column(Boolean(), default=False)
    shelf_life_days = Column(Integer())
    minimum_stock_level = Column(Integer(), default=10)
    supplier_id = Column(Integer())
    is_active = Column(Boolean(), default=True)
    created_at = Column(Timestamp())
    
    @property
    def categories(self):
        pcs = ProductCategories.filter_by(product_id=self.product_id)
        return [Categories.get(category_id=pc.category_id) for pc in pcs]
    
    @property
    def reviews(self):
        return ProductReviews.filter_by(product_id=self.product_id)


class ProductCategories(Base):
    _table_name = 'ProductCategories'
    
    product_id = Column(Integer(), primary_key=True)
    category_id = Column(Integer(), primary_key=True)


class ProductReviews(Base):
    _table_name = 'ProductReviews'
    
    review_id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    user_id = Column(Integer(), nullable=False)
    rating = Column(Integer(), nullable=False)
    review_text = Column(Text())
    created_at = Column(Timestamp())
    is_verified_purchase = Column(Boolean(), default=False)


# =============================================
# LOCATION AND VENDING MACHINE MODELS
# =============================================

class Locations(Base):
    _table_name = 'Locations'
    
    location_id = Column(Integer(), primary_key=True)
    location_name = Column(String(255), nullable=False)
    location_type = Column(Enum('MALL', 'OFFICE', 'UNIVERSITY', 'AIRPORT', 'HOSPITAL', 'OTHER'), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default='USA')
    latitude = Column(Decimal(10, 8))
    longitude = Column(Decimal(11, 8))
    foot_traffic_score = Column(Integer())
    
    @property
    def machines(self):
        return VendingMachines.filter_by(location_id=self.location_id)


class VendingMachines(Base):
    _table_name = 'VendingMachines'
    
    machine_id = Column(Integer(), primary_key=True)
    machine_serial = Column(String(100), nullable=False, unique=True)
    location_id = Column(Integer(), nullable=False)
    machine_type = Column(Enum('STANDARD', 'REFRIGERATED', 'FROZEN', 'MIXED'), default='STANDARD')
    total_slots = Column(Integer(), nullable=False)
    installation_date = Column(Date())
    last_maintenance_date = Column(Date())
    firmware_version = Column(String(50))
    status = Column(Enum('ONLINE', 'OFFLINE', 'MAINTENANCE', 'OUT_OF_SERVICE'), default='ONLINE')
    temperature_setting = Column(Decimal(5, 2))
    
    @property
    def slots(self):
        return VendingSlots.filter_by(machine_id=self.machine_id)
    
    @property
    def location(self):
        return Locations.get(location_id=self.location_id)


class VendingSlots(Base):
    _table_name = 'VendingSlots'
    
    slot_id = Column(Integer(), primary_key=True)
    machine_id = Column(Integer(), nullable=False)
    slot_number = Column(String(10), nullable=False)
    product_id = Column(Integer())
    current_quantity = Column(Integer(), default=0)
    max_capacity = Column(Integer(), nullable=False)
    slot_price = Column(Decimal(10, 2))
    is_operational = Column(Boolean(), default=True)
    
    @property
    def product(self):
        if self.product_id:
            return Products.get(product_id=self.product_id)
        return None


# =============================================
# INVENTORY MODELS
# =============================================

class WarehouseInventory(Base):
    _table_name = 'WarehouseInventory'
    
    inventory_id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    quantity_on_hand = Column(Integer(), nullable=False, default=0)
    quantity_reserved = Column(Integer(), default=0)
    reorder_point = Column(Integer())
    last_restock_date = Column(Timestamp())


class InventoryTransactions(Base):
    _table_name = 'InventoryTransactions'
    
    transaction_id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    machine_id = Column(Integer())
    transaction_type = Column(Enum('RESTOCK', 'SALE', 'ADJUSTMENT', 'TRANSFER', 'EXPIRED', 'DAMAGED'), nullable=False)
    quantity_change = Column(Integer(), nullable=False)
    previous_quantity = Column(Integer())
    new_quantity = Column(Integer())
    notes = Column(Text())
    created_at = Column(Timestamp())
    created_by = Column(Integer())


# =============================================
# ORDER MODELS
# =============================================

class Orders(Base):
    _table_name = 'Orders'
    
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    order_number = Column(String(50), nullable=False, unique=True)
    order_type = Column(Enum('ONLINE', 'VENDING', 'RESERVATION'), nullable=False)
    order_status = Column(Enum('PENDING', 'CONFIRMED', 'PROCESSING', 'READY', 'COMPLETED', 'CANCELLED', 'REFUNDED'), default='PENDING')
    subtotal = Column(Decimal(10, 2), nullable=False)
    tax_amount = Column(Decimal(10, 2), default=0)
    discount_amount = Column(Decimal(10, 2), default=0)
    total_amount = Column(Decimal(10, 2), nullable=False)
    pickup_machine_id = Column(Integer())
    pickup_code = Column(String(20))
    pickup_expiry = Column(Timestamp())
    created_at = Column(Timestamp())
    completed_at = Column(Timestamp())
    
    @property
    def items(self):
        return OrderItems.filter_by(order_id=self.order_id)
    
    @property
    def payments(self):
        return Payments.filter_by(order_id=self.order_id)
    
    @property
    def user(self):
        if self.user_id:
            return Users.get(user_id=self.user_id)
        return None


class OrderItems(Base):
    _table_name = 'OrderItems'
    
    order_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), nullable=False)
    product_id = Column(Integer(), nullable=False)
    slot_id = Column(Integer())
    quantity = Column(Integer(), nullable=False)
    unit_price = Column(Decimal(10, 2), nullable=False)
    discount_amount = Column(Decimal(10, 2), default=0)
    total_price = Column(Decimal(10, 2), nullable=False)
    
    @property
    def product(self):
        return Products.get(product_id=self.product_id)


class PaymentMethods(Base):
    _table_name = 'PaymentMethods'
    
    payment_method_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False)
    method_type = Column(Enum('CREDIT_CARD', 'DEBIT_CARD', 'DIGITAL_WALLET', 'LOYALTY_POINTS'), nullable=False)
    provider = Column(String(50))
    card_last_four = Column(String(4))
    expiry_date = Column(String(7))
    is_default = Column(Boolean(), default=False)
    created_at = Column(Timestamp())


class Payments(Base):
    _table_name = 'Payments'
    
    payment_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), nullable=False)
    payment_method_id = Column(Integer())
    payment_type = Column(Enum('CREDIT_CARD', 'DEBIT_CARD', 'DIGITAL_WALLET', 'LOYALTY_POINTS', 'CASH'), nullable=False)
    amount = Column(Decimal(10, 2), nullable=False)
    points_used = Column(Integer(), default=0)
    payment_status = Column(Enum('PENDING', 'AUTHORIZED', 'CAPTURED', 'FAILED', 'REFUNDED'), default='PENDING')
    transaction_reference = Column(String(100))
    processed_at = Column(Timestamp())


# =============================================
# PRICING MODEL
# =============================================

class PricingRules(Base):
    _table_name = 'PricingRules'
    
    rule_id = Column(Integer(), primary_key=True)
    rule_name = Column(String(100), nullable=False)
    rule_type = Column(Enum('TIME_BASED', 'DEMAND_BASED', 'LOCATION_BASED', 'PROMOTIONAL'), nullable=False)
    product_id = Column(Integer())
    category_id = Column(Integer())
    location_id = Column(Integer())
    machine_id = Column(Integer())
    price_modifier = Column(Decimal(5, 2))
    modifier_type = Column(Enum('PERCENTAGE', 'FIXED_AMOUNT'), default='PERCENTAGE')
    start_date = Column(Date())
    end_date = Column(Date())
    days_of_week = Column(String(20))
    min_demand_threshold = Column(Integer())
    is_active = Column(Boolean(), default=True)
    priority = Column(Integer(), default=0)


# =============================================
# EMPLOYEE MODELS
# =============================================

class Employees(Base):
    _table_name = 'Employees'
    
    employee_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False, unique=True)
    employee_number = Column(String(50), nullable=False, unique=True)
    department = Column(Enum('OPERATIONS', 'MAINTENANCE', 'LOGISTICS', 'MANAGEMENT', 'CUSTOMER_SERVICE'), nullable=False)
    job_title = Column(String(100))
    hire_date = Column(Date(), nullable=False)
    salary = Column(Decimal(10, 2))
    manager_id = Column(Integer())
    
    @property
    def user(self):
        return Users.get(user_id=self.user_id)


class Technicians(Base):
    _table_name = 'Technicians'
    
    technician_id = Column(Integer(), primary_key=True)
    employee_id = Column(Integer(), nullable=False, unique=True)
    certification_level = Column(Enum('JUNIOR', 'SENIOR', 'EXPERT'), default='JUNIOR')
    specialization = Column(String(100))
    
    @property
    def employee(self):
        return Employees.get(employee_id=self.employee_id)


class MaintenanceRecords(Base):
    _table_name = 'MaintenanceRecords'
    
    maintenance_id = Column(Integer(), primary_key=True)
    machine_id = Column(Integer(), nullable=False)
    technician_id = Column(Integer())
    maintenance_type = Column(Enum('SCHEDULED', 'EMERGENCY', 'PREVENTIVE', 'REPAIR'), nullable=False)
    description = Column(Text())
    cost = Column(Decimal(10, 2))
    scheduled_date = Column(Timestamp())
    started_at = Column(Timestamp())
    completed_at = Column(Timestamp())
    status = Column(Enum('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'), default='SCHEDULED')


class RestockSchedules(Base):
    _table_name = 'RestockSchedules'
    
    schedule_id = Column(Integer(), primary_key=True)
    machine_id = Column(Integer(), nullable=False)
    assigned_employee_id = Column(Integer())
    scheduled_date = Column(Timestamp(), nullable=False)
    status = Column(Enum('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'), default='SCHEDULED')
    notes = Column(Text())
    completed_at = Column(Timestamp())
    
    @property
    def items(self):
        return RestockItems.filter_by(schedule_id=self.schedule_id)


class RestockItems(Base):
    _table_name = 'RestockItems'
    
    restock_item_id = Column(Integer(), primary_key=True)
    schedule_id = Column(Integer(), nullable=False)
    slot_id = Column(Integer(), nullable=False)
    product_id = Column(Integer(), nullable=False)
    quantity_to_add = Column(Integer(), nullable=False)
    quantity_added = Column(Integer())


# =============================================
# RESERVATION MODEL
# =============================================

class Reservations(Base):
    _table_name = 'Reservations'
    
    reservation_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False)
    product_id = Column(Integer(), nullable=False)
    machine_id = Column(Integer(), nullable=False)
    slot_id = Column(Integer(), nullable=False)
    quantity = Column(Integer(), default=1)
    qr_code = Column(String(255), unique=True)
    reservation_status = Column(Enum('ACTIVE', 'CLAIMED', 'EXPIRED', 'CANCELLED'), default='ACTIVE')
    created_at = Column(Timestamp())
    expires_at = Column(Timestamp(), nullable=False)
    claimed_at = Column(Timestamp())
    
    @property
    def product(self):
        return Products.get(product_id=self.product_id)
    
    @property
    def machine(self):
        return VendingMachines.get(machine_id=self.machine_id)


# =============================================
# ANALYTICS MODELS
# =============================================

class SalesAnalytics(Base):
    _table_name = 'SalesAnalytics'
    
    analytics_id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    machine_id = Column(Integer())
    location_id = Column(Integer())
    date = Column(Date(), nullable=False)
    hour = Column(Integer())
    units_sold = Column(Integer(), default=0)
    revenue = Column(Decimal(10, 2), default=0)
    avg_price = Column(Decimal(10, 2))


class DemandPredictions(Base):
    _table_name = 'DemandPredictions'
    
    prediction_id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    machine_id = Column(Integer())
    location_id = Column(Integer())
    prediction_date = Column(Date(), nullable=False)
    predicted_demand = Column(Integer(), nullable=False)
    confidence_score = Column(Decimal(5, 2))
    created_at = Column(Timestamp())


# =============================================
# NOTIFICATION MODELS
# =============================================

class Notifications(Base):
    _table_name = 'Notifications'
    
    notification_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False)
    notification_type = Column(Enum('ORDER_UPDATE', 'RESERVATION_READY', 'PROMOTION', 'LOW_STOCK', 'SYSTEM'), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text())
    is_read = Column(Boolean(), default=False)
    created_at = Column(Timestamp())


class MachineAlerts(Base):
    _table_name = 'MachineAlerts'
    
    alert_id = Column(Integer(), primary_key=True)
    machine_id = Column(Integer(), nullable=False)
    alert_type = Column(Enum('LOW_STOCK', 'MALFUNCTION', 'TEMPERATURE', 'CONNECTIVITY', 'SECURITY'), nullable=False)
    severity = Column(Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'), default='MEDIUM')
    message = Column(Text())
    is_resolved = Column(Boolean(), default=False)
    created_at = Column(Timestamp())
    resolved_at = Column(Timestamp())
    resolved_by = Column(Integer())


# =============================================
# PROMOTION MODELS
# =============================================

class Promotions(Base):
    _table_name = 'Promotions'
    
    promotion_id = Column(Integer(), primary_key=True)
    promo_code = Column(String(50), unique=True)
    description = Column(Text())
    discount_type = Column(Enum('PERCENTAGE', 'FIXED_AMOUNT', 'BUY_ONE_GET_ONE', 'FREE_ITEM'), nullable=False)
    discount_value = Column(Decimal(10, 2), nullable=False)
    minimum_purchase = Column(Decimal(10, 2), default=0)
    usage_limit = Column(Integer())
    usage_count = Column(Integer(), default=0)
    start_date = Column(Timestamp(), nullable=False)
    end_date = Column(Timestamp(), nullable=False)
    is_active = Column(Boolean(), default=True)


class PromotionUsage(Base):
    _table_name = 'PromotionUsage'
    
    usage_id = Column(Integer(), primary_key=True)
    promotion_id = Column(Integer(), nullable=False)
    user_id = Column(Integer(), nullable=False)
    order_id = Column(Integer(), nullable=False)
    discount_applied = Column(Decimal(10, 2))
    used_at = Column(Timestamp())
