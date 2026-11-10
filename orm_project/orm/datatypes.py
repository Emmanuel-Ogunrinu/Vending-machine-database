"""
datatypes.py

SQL data type definitions and validation utilities for the ORM framework.

This module defines the data type abstractions used to represent database
column types within the ORM. Each type encapsulates the metadata and
behavior required to map Python values to their SQL equivalents.

These abstractions integrate with the Column class to support consistent
schema generation, value validation, and model-to-database mapping.

Supported Data Types
--------------------
Integer
    Represents an INTEGER column for storing whole numbers.

String
    Represents a text-based column with optional length constraints.

Boolean
    Represents a BOOLEAN column for storing logical values.

Date
    Represents a DATE column for storing calendar dates.

Core Functionality
------------------
SQL Type Mapping:
    get_sql()       Return the SQL representation of the data type.

Value Validation:
    validate()      Determine whether a value satisfies the data type's
                    requirements and applicable constraints.

ORM Integration
---------------
Data type instances provide column definitions with the information
required to generate SQL schemas and validate model values.

The Column class references these types to determine the appropriate
SQL representation and ensure that values conform to the expected
data types before database operations.

Example
-------
class User:
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date)

These definitions describe a User model with an integer primary key,
a required string field, a Boolean field with a default value, and
a date field.

The ORM uses the associated type metadata to construct SQL column
definitions and support validation during database interactions.

Design Considerations
---------------------
Centralizing SQL data type definitions provides a consistent interface
for column configuration and validation.

This design promotes:

    - Reusable data type definitions across ORM models.
    - Consistent mapping between Python values and SQL column types.
    - Separation of type validation from database persistence logic.
    - Easier extension to additional SQL data types.
    - Improved maintainability and schema consistency.

The module establishes a foundation for extensible type handling
without requiring model classes to manage SQL-specific details.
"""

class Integer:
    def __init__(self, type="INTEGER", length=None):
        self.type = type
        self.length = length

    def validate(self, value):
        """Validate if the value is a valid integer."""
        if value is None:
            return True

        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    def sql_type(self):
        """Get the SQL representation of the integer type."""
        if self.length:
            return f"{self.type}({self.length})"
        return self.type

    def to_sql(self):
        """Get the SQL representation of the integer type."""
        return self.sql_type()


class String:
    def __init__(self, length=255, type='VARCHAR'):
        self.type = type
        self.length = length

    def validate_length(self):
        """Validate if the length is valid."""
        if self.length is None:
            return True

        if not isinstance(self.length, int):
            return False

        if self.length <= 0:
            return False

        # Check maximum length constraints
        if self.type == 'VARCHAR' and self.length > 65535:
            return False

        if self.type == 'CHAR' and self.length > 255:
            return False

        return True

    def validate(self, value):
        """Validate if the value is a valid string."""
        if value is None:
            return True

        if not isinstance(value, str):
            return False

        if self.length and len(value) > self.length:
            return False

        return True

    def sql_type(self):
        """Get the SQL representation of the string type."""
        if self.length:
            return f"{self.type}({self.length})"
        return self.type

    def to_sql(self):
        """Get the SQL representation of the string type."""
        return self.sql_type()


class Text:
    def __init__(self, type='TEXT'):
        self.type = type

    def validate(self, value):
        """Validate if the value is a valid text."""
        if value is None:
            return True
        return isinstance(value, str)

    def sql_type(self):
        """Get the SQL representation of the text type."""
        return self.type

    def to_sql(self):
        """Get the SQL representation of the text type."""
        return self.sql_type()


class Float:
    def __init__(self, type='FLOAT'):
        self.type = type

    def validate(self, value):
        """Validate if the value is a valid float."""
        if value is None:
            return True

        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def sql_type(self):
        """Get the SQL representation of the float type."""
        return self.type

    def to_sql(self):
        """Get the SQL representation of the float type."""
        return self.sql_type()


class Decimal:
    def __init__(self, precision=10, scale=2):
        self.type = "DECIMAL"
        self.precision = precision
        self.scale = scale

    def validate(self, value):
        """Validate if the value is a valid decimal."""
        if value is None:
            return True

        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def sql_type(self):
        """Get the SQL representation of the decimal type."""
        return f"{self.type}({self.precision}, {self.scale})"

    def to_sql(self):
        """Get the SQL representation of the decimal type."""
        return self.sql_type()


class Boolean:
    def __init__(self):
        self.type = "BOOLEAN"

    def validate(self, value):
        """Validate if the value is a valid boolean."""
        if value is None:
            return True
        return isinstance(value, bool)

    def sql_type(self):
        """Get the SQL representation of the boolean type."""
        return self.type

    def to_sql(self):
        """Get the SQL representation of the boolean type."""
        return self.sql_type()


class Date:
    def __init__(self, type='DATE'):
        self.type = type

    def validate(self, value):
        """Validate if the value is a valid date."""
        if value is None:
            return True

        # Check if it's a date object
        if hasattr(value, 'year') and hasattr(value, 'month') and hasattr(value, 'day'):
            return True

        # Check if it's a string in date format
        if isinstance(value, str):
            try:
                from datetime import datetime
                datetime.strptime(value, '%Y-%m-%d')
                return True
            except ValueError:
                return False

        return False

    def sql_type(self):
        """Get the SQL representation of the date type."""
        return self.type

    def to_sql(self):
        """Get the SQL representation of the date type."""
        return self.sql_type()


class Timestamp:
    def __init__(self):
        self.type = "TIMESTAMP"

    def validate(self, value):
        """Validate if the value is a valid timestamp."""
        if value is None:
            return True

        # Check if it's a datetime object
        if hasattr(value, 'year') and hasattr(value, 'hour'):
            return True

        # Check if it's a string
        if isinstance(value, str):
            return True

        return False

    def sql_type(self):
        """Get the SQL representation of the timestamp type."""
        return self.type

    def to_sql(self):
        """Get the SQL representation of the timestamp type."""
        return self.sql_type()


class Blob:
    def __init__(self):
        self.type = "BLOB"

    def validate(self, value):
        """Validate if the value is valid for BLOB storage."""
        if value is None:
            return True

        # BLOB can store bytes or binary data
        return isinstance(value, (bytes, bytearray))

    def sql_type(self):
        """Get the SQL representation of the BLOB type."""
        return self.type

    def to_sql(self):
        """Get the SQL representation of the BLOB type."""
        return self.sql_type()


class Enum:
    def __init__(self, *values):
        self.type = "ENUM"
        self.values = values

    def validate(self, value):
        """Validate if the value is one of the allowed enum values."""
        if value is None:
            return True
        return value in self.values

    def sql_type(self):
        """Get the SQL representation of the enum type."""
        enum_values = "', '".join(str(v) for v in self.values)
        return f"ENUM('{enum_values}')"

    def to_sql(self):
        """Get the SQL representation of the enum type."""
        return self.sql_type()
