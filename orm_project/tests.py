# test.py
#
# This file is meant for testing the functionality of the models you define in models.py.
# Use it as a sandbox to manually verify that your model classes and their methods work correctly.
#
# Suggested tests include:
#   - Creating, updating, and deleting records
#   - Querying and retrieving data
#   - Retrieving data using filters such as having and where
#   - Applying group_by and order_by for data retrieved
#   - Testing relationships between models (e.g., foreign keys, joins)
#   - OPTIONAL AND EXTRA CREDIT ONLY: test your migrations properly
#
# Guidelines:
#   - Import your model classes from models.py
#   - Use the database connector provided (e.g., from db.py) to connect to your test database
#   - Clean up test data between runs if needed
#
# NOTE: This is not a formal unit test file. You are encouraged to add and run meaningful tests
# here as you build your ORM functionality.

from models.models import *

"""
Example usage with sample models.
You should **delete** this sample code and write your own tests using the models you create.
Make sure to test all major models and relationships defined in your project’s database schema.
"""
"""
# Create a new company with title AI Labs
ai_labs = Company()
ai_labs.title = "AI Labs"
ai_labs.num_employees = 3
ai_labs.field = "Engineering"
ai_labs.save()

# Create a new user
john = User(name="John Doe", email="john@example.com", age=30)

# Update user fields
john.email = "johndoe@example.com"
john.age = 32
john.save()

# Query all users in the database
# Equivalent to: SELECT * FROM User;
users = User.get_all()
for user in users:
    print(user.name, user.email)

# Retrieve a user by ID
# Equivalent to: SELECT * FROM User WHERE User.id = 1;
user = User.get(id=1)
print(f"User active status: {user.is_active}")

# Assign this user to the company
# Equivalent to: ALTER TABLE User ADD COLUMN company_id INT FOREIGN KEY REFERENCES User(id) ON DELETE CASCADE ON UPDATE CASCADE;
john.foreign_key(key=ai_labs.id, on_delete='CASCADE', on_update='CASCADE')

# Delete a user by ID
# Equivalent to: DELETE FROM USER WHERE User.id = 2;
User.delete(id=2)

# Join: Get all employees working for AI Labs company
# This is similar to: SELECT * FROM User JOIN Company ON Company.id = User.company_id WHERE Company.title = "AI Labs";
# Note that it would also be a good approach to create an employee model to handle specific employee logic
employees = ai_labs.join(User.descriptor())
for employee in employees:
    print(f"{employee.john.name} works for {employee.ai_labs.title}")

# Deactivate the company (without deleting it)
# This prevents it from being used by new records until reactivated
# Equivalent to: UPDATE Company SET is_active = FALSE WHERE Company.id = [the id of ai_labs entity (dynamically assigned by the ORM)];
ai_labs.deactivate()

"""
"""
Now remove the example code above and begin testing your own models below.
Make sure your tests reflect the structure of your actual database schema.
"""

from models.models import *
import time


print("Starting ORM Tests...\n")

# ============================================================================
# CREATE OPERATIONS
# ============================================================================

# Create a new customer
print("Creating new customer...")
new_customer = Customer()
new_customer.tracking_code = f"TRACK_TEST_{int(time.time())}"
new_customer.save()

print(f"Created customer with tracking code: {new_customer.tracking_code}\n")

# Create a new product
print("Creating new product...")
test_product = Product()
test_product.sku = f"TEST_ENERGY_{int(time.time())}"
test_product.name = "Test Energy Drink"
test_product.description = "High caffeine drink for testing"
test_product.base_price = 4.99
test_product.save()
print(f"Created product: {test_product.name} at ${test_product.base_price}\n")

# Create a new category
print("Creating new category...")
test_category = Category()
test_category.category_name = f"Test Beverages {int(time.time())}"
test_category.is_active = True
test_category.save()
print(f"Created category: {test_category.category_name}\n")


# ============================================================================
# READ OPERATIONS
# ============================================================================

# Get a single customer by ID
# Equivalent to: SELECT * FROM Customer WHERE customer_id = 1;
print("Retrieving customer by ID...")
customer = Customer.get(customer_id=1)
if customer:
    print(f"Found customer: {customer.tracking_code}\n")

# Get a registered customer
# Equivalent to: SELECT * FROM RegisteredCustomer WHERE customer_id = 1;
print("Retrieving registered customer...")
registered = RegisteredCustomer.get(customer_id=1)
if registered:
    print(f"Customer: {registered.full_name()}")
    print(f"Email: {registered.email}")
    print(f"Loyalty Points: {registered.loyalty_points}\n")

# Get a product
# Equivalent to: SELECT * FROM Product WHERE product_id = 1;
print("Retrieving product...")
product = Product.get(product_id=1)
if product:
    print(f"Product: {product.name}")
    print(f"Price: ${product.base_price}")
    print(f"SKU: {product.sku}\n")


# ============================================================================
# UPDATE OPERATIONS
# ============================================================================

# Update customer loyalty points
#print("Updating customer loyalty points...")
#customer_to_update = RegisteredCustomer.get(customer_id=2)
#if customer_to_update:
#   print(f"Before: {customer_to_update.loyalty_points} points")
#   customer_to_update.loyalty_points = customer_to_update.loyalty_points + 50
#   customer_to_update.save()
#   print(f"After: {customer_to_update.loyalty_points} points\n")

# Update product price
print("Updating product price...")
product_to_update = Product.get(product_id=3)
if product_to_update:
    print(f"Before: ${product_to_update.base_price}")
    product_to_update.base_price = 2.99
    product_to_update.save()
    print(f"After: ${product_to_update.base_price}\n")


# ============================================================================
# GET ALL RECORDS
# ============================================================================

# Query all products in the database
# Equivalent to: SELECT * FROM Product;
print("Retrieving all products...")
all_products = Product.get_all()
print(f"Total products: {len(all_products)}")
for product in all_products[:5]:
    print(f"  - {product.name}: ${product.base_price}")
print()

# Query all orders in the database
# Equivalent to: SELECT * FROM Order;
print("Retrieving all orders...")
all_orders = Order.get_all()
print(f"Total orders: {len(all_orders)}")
for order in all_orders[:5]:
    print(f"  - Order #{order.order_id}: ${order.total_amount} ({order.order_status})")
print()

# Query all vending machines
# Equivalent to: SELECT * FROM VendingMachine;
print("Retrieving all vending machines...")
all_machines = VendingMachine.get_all()
print(f"Total machines: {len(all_machines)}")
for machine in all_machines[:5]:
    print(f"  - {machine.machine_id}: {machine.operational_status}")
print()


# ============================================================================
# FILTERING DATA
# ============================================================================

# Filter orders by status
# Equivalent to: SELECT * FROM Order WHERE order_status = 'completed';
print("Finding completed orders...")
completed_orders = Order.filter_by(order_status='completed')
print(f"Found {len(completed_orders)} completed orders")
for order in completed_orders[:3]:
    print(f"  - Order #{order.order_id}: ${order.total_amount}")
print()

# Filter vending machines by status
# Equivalent to: SELECT * FROM VendingMachine WHERE operational_status = 'online';
print("Finding online vending machines...")
online_machines = VendingMachine.filter_by(operational_status='online')
print(f"Found {len(online_machines)} online machines")
for machine in online_machines[:3]:
    print(f"  - {machine.machine_id}: {machine.model_number}")
print()


# ============================================================================
# WHERE, HAVING, GROUP BY
# ============================================================================

# Using WHERE clause
print("Testing WHERE clause:")
where_clause = Product.where(base_price=2.50)
print(f"Generated: {where_clause}\n")

# Using HAVING clause
print("Testing HAVING clause:")
having_clause = Order.having(total_amount=10)
print(f"Generated: {having_clause}\n")

# Using GROUP BY clause
print("Testing GROUP BY clause:")
group_by_clause = Product.group_by('category_id', 'base_price')
print(f"Generated: {group_by_clause}\n")


# ============================================================================
# RELATIONSHIPS
# ============================================================================

# Get order and its items
print("Testing order-to-items relationship...")
order = Order.get(order_id=1)
if order:
    items = OrderItem.filter_by(order_id=order.order_id)
    print(f"Order #{order.order_id} has {len(items)} items:")
    for item in items:
        prod = Product.get(product_id=item.product_id)
        if prod:
            print(f"  - {prod.name}: {item.quantity} x ${item.unit_price} = ${item.subtotal()}")
print()

# Get vending machine and its slots
print("Testing machine-to-slots relationship...")
machine = VendingMachine.get(machine_id='VM001')
if machine:
    slots = VendingSlot.filter_by(machine_id=machine.machine_id)
    print(f"Machine {machine.machine_id} has {len(slots)} slots:")
    for slot in slots[:5]:
        prod = Product.get(product_id=slot.product_id) if slot.product_id else None
        product_name = prod.name if prod else "Empty"
        print(f"  - Slot {slot.slot_number}: {product_name} ({slot.current_quantity}/{slot.max_capacity})")
print()

# Get customer and their orders
print("Testing customer-to-orders relationship...")
reg_customer = RegisteredCustomer.get(customer_id=1)
if reg_customer:
    customer_orders = Order.filter_by(customer_id=reg_customer.customer_id)
    print(f"{reg_customer.full_name()} has {len(customer_orders)} orders:")
    for order in customer_orders[:3]:
        print(f"  - Order #{order.order_id}: ${order.total_amount} ({order.order_status})")
print()


# ============================================================================
# CUSTOM METHODS
# ============================================================================

# Test inventory computed properties
print("Testing inventory properties...")
inventory = Inventory.get(inventory_id=1)
if inventory:
    print(f"Current Stock: {inventory.current_stock}")
    print(f"Available: {inventory.available_quantity()}")
    print(f"Needs Restock: {inventory.needs_restock()}\n")

# Test vending slot methods
print("Testing vending slot methods...")
slot = VendingSlot.get(slot_id=1)
if slot:
    print(f"Slot {slot.slot_number}: {slot.current_quantity}/{slot.max_capacity}")
    print(f"Is Empty: {slot.is_empty()}")
    print(f"Needs Restocking: {slot.needs_restocking()}\n")

# Test category deactivation
print("Testing category deactivation...")
category_deactivate = Category.get(category_name="Test Beverages")
if category_deactivate:
    category_deactivate.deactivate()
    print(f"Category '{category_deactivate.category_name}' is now inactive\n")


# ============================================================================
# DELETE OPERATIONS
# ============================================================================

# Delete a record by ID
# Equivalent to: DELETE FROM Product WHERE product_id = [id];
print("Deleting test product...")
product_to_delete = Product.get(sku="TEST_ENERGY_001")
if product_to_delete:
    Product.delete(product_id=product_to_delete.product_id)
    print(f"Deleted product: {product_to_delete.name}\n")


print("All tests completed successfully!")

"""
AI Database
"""
print("\n" + "="*50)
print("AI DATABASE TESTS")
print("="*50)

# Switch to AI database
import os
os.environ['MYSQL_DATABASE'] = 'ai_retail_vending_db'

# Import AI models
from ai_models import Users, Products, Categories, Orders, VendingMachines, VendingSlots

# Test get_all
print("\nProducts.get_all():")
products = Products.get_all()
print(f"  Found {len(products)} products")

# Test get
print("\nProducts.get(product_id=1):")
p = Products.get(product_id=1)
if p:
    print(f"  Found: {p.name}")
else:
    print("  Not found")

# Test filter_by
print("\nProducts.filter_by(is_active=1):")
active = Products.filter_by(is_active=1)
print(f"  Found {len(active)} active products")

# Test Users
print("\nUsers.get_all():")
users = Users.get_all()
print(f"  Found {len(users)} users")

# Test VendingMachines
print("\nVendingMachines.get_all():")
machines = VendingMachines.get_all()
print(f"  Found {len(machines)} machines")

# Test lazy relationship
if machines:
    print("\nMachine slots (lazy load):")
    m = machines[0]
    slots = m.slots
    print(f"  Machine has {len(slots)} slots")