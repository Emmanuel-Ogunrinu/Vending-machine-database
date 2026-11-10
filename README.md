# Retail Commerce & Vending Machine ORM

**A Python/MySQL project exploring a custom object-relational mapper and a data model for commerce across online retail and vending machines.**

## Overview

This repository combines two related areas of development:

1. **A lightweight ORM framework** that maps Python model classes to MySQL tables and provides methods for common database operations.
2. **Retail commerce data models** representing customers, products, orders, inventory, vending machines, and other business operations.

The goal is to explore how software can organize the data behind a business that sells through more than one channel. The project focuses on database design and backend abstractions; it is **not a deployed storefront, vending-machine integration, or production-ready ORM**.

## Features and architecture

### Custom ORM (`orm/`)

- **Model persistence:** `save()`, `_insert()`, `_update()`, `get()`, `get_all()`, `filter_by()`, and `delete()` in `Base`.
- **Table definitions:** `Column` metadata for SQL types, defaults, primary keys, nullability, uniqueness, and foreign-key configuration.
- **Data types:** `Integer`, `String`, `Text`, `Float`, `Decimal`, `Boolean`, `Date`, `Timestamp`, `Blob`, and `Enum` implementations.
- **SQL generation:** `create_schema()` creates a basic MySQL `CREATE TABLE` statement; `create_table()` executes it.
- **Query utilities:** `where()`, `having()`, and `group_by()` produce SQL clause strings; `join()` provides a limited convention-based join operation.
- **Database access:** MySQL connector configuration loaded from environment variables.

**Implementation note:** Defining a constraint in `Column` does not mean all constraints are included in `Base.create_schema()`. In particular, the current schema generator does not apply every uniqueness or foreign-key setting. Query helpers are also not a complete composable query builder.

### Commerce models

`models/models.py` defines an initial retail domain with entities such as:

- Customers and registered customers
- Products and categories
- Orders and order items
- Vending machines, slots, and locations
- Inventory and product reviews

`ai_models.py` contains an expanded **32-model schema definition** covering additional scenarios, including:

- User roles, accounts, addresses, and loyalty programs
- Suppliers and product-category relationships
- Orders, order items, payments, and payment methods
- Vending machine inventory, maintenance, and restocking
- Reservations, promotions, notifications, and alerts
- Sales analytics and demand prediction records

These models represent *database structures* and supporting convenience properties; they do not by themselves establish that payment processing, automated predictions, live inventory synchronization, or other full application workflows are implemented.

## Repository structure

```text
orm_project/
├── orm/
│   ├── __init__.py        # Package exports
│   ├── base.py            # Persistence and query methods
│   ├── columns.py         # Column metadata and constraints
│   ├── datatypes.py       # SQL type definitions and validation
│   ├── dbconnectors.py    # MySQL connection helper
│   ├── migrations.py      # Migration API placeholders
│   └── relations.py       # Relationship feature placeholder
├── models/
│   └── models.py          # Initial retail/vending models
├── ai_models.py           # Expanded commerce schema models
├── tests.py               # Manual database exercise script
├── requirements.txt
├── .env.example           # Sample local configuration
└── README.md
```

## Getting started

### Prerequisites

- Python and `pip`
- A locally accessible MySQL server
- Permission to create and modify a **separate development database**

### Installation

```bash
# Clone your repository, then enter its root directory
cd orm_project

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

The original project uses `mysql-connector-python` and `pytest`. It also imports `python-dotenv` in `orm/dbconnectors.py`; this GitHub-ready package adds that missing dependency to `requirements.txt`.

### Configure MySQL

Create a test database using a MySQL account with suitable local permissions:

```sql
CREATE DATABASE orm_retail_demo;
```

Copy the sample configuration file and provide **your own** local credentials:

```bash
cp .env.example .env
```

```dotenv
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_local_password
MYSQL_DATABASE=orm_retail_demo
```

Never commit `.env` or share database passwords. The project's `.gitignore` excludes `.env`.

> **Important:** The repository does not include the external database schema or seed data referenced by parts of `tests.py`. Defining Python models does not automatically populate a complete working database. You must create and validate the necessary MySQL tables before running data-access examples.

## Usage examples

These examples illustrate methods present in the repository. Database reads require matching tables and data in your configured MySQL database.

### Generate SQL from a model

```python
from ai_models import Products

schema = Products.create_schema()
print(schema)
```

`create_schema()` returns a SQL statement. Review its output before executing it, as the current implementation does not include all model-level constraints.

### Retrieve and filter records

```python
from ai_models import Products, VendingMachines

# Fetch an existing product by its ID
product = Products.get(product_id=1)
if product is not None:
    print(product.name, product.base_price)

# Read products that are marked active
active_products = Products.filter_by(is_active=True)

# Read machines and inspect their status
machines = VendingMachines.get_all()
for machine in machines:
    print(machine.machine_id, machine.operational_status)
```

### Generate a SQL clause

```python
from ai_models import Products

print(Products.where(is_active=1))
print(Products.group_by("supplier_id"))
```

The clause helpers currently generate SQL **strings** rather than safely parameterized query objects. Do not use them with untrusted inputs.

## Testing

`tests.py` is a **manual integration script**, not an automated test suite with assertions. It exercises CRUD operations, queries, model helpers, and relationships against databases whose tables and records already exist.

**Caution:** It creates records, changes product data, and attempts deletions. It also switches the configured database to `ai_retail_vending_db` during execution. **Do not run this script against a production database or one containing data you need to preserve.**

After preparing a disposable database and reviewing the script, run:

```bash
python tests.py
```

A successful Python syntax check alone is not evidence that all database operations have passed integration testing.

## Current status and limitations

This is an **in-development portfolio project** with implemented ORM methods and model definitions, alongside incomplete or experimental functionality:

- `orm/migrations.py` declares migration operations but currently contains `pass` placeholders.
- `orm/relations.py` does not yet implement a general relationship layer.
- `Base.create_schema()` supports basic table generation but omits some metadata represented by `Column`.
- `join()` assumes a naming convention; it does not discover arbitrary relationships.
- Some initial models pass data type *classes*, while the expanded models use type *instances*. This difference should be reconciled before treating both model sets as interchangeable.
- Query construction and identifier handling need additional validation and security hardening.
- The project has no verified production deployment, live vending integration, automated forecasting pipeline, or complete automated test suite.

## Next steps

- Standardize model declarations and validate them against MySQL.
- Add schema-level support for unique constraints, foreign keys, and nonnumeric primary keys.
- Replace string-interpolated query helpers with parameterized, validated SQL construction.
- Implement and test a migration system.
- Add automated tests with disposable database fixtures.
- Provide repeatable database schema/seed scripts and an end-to-end demo.
- Prototype a merchant-facing dashboard for inventory, sales, and vending-machine health.

## Project focus

This project demonstrates hands-on exploration of **Python, SQL, object-oriented design, schema modeling, database operations, and commerce workflows**. It also illustrates a product-oriented question: how can a business see and manage inventory, purchases, and operations across online and physical channels using a consistent data model?
