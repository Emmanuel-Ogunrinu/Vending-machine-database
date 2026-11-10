# datatypes.py
#
# This file defines the data types used in the ORM framework. Each class represents
# a specific column type that can be used in the database schema. These types
# are then used by the ORM's base class to define columns in database tables.
#
# The `Column` class in the ORM will reference these data types to configure the
# column's behavior, such as validating values, determining the SQL representation,
# and enforcing constraints.
#
# For example,
#   - The `Integer` class represents an INTEGER column type in SQL.
#   - The `String` class represents a TEXT column type with an optional length constraint.
#   - The `Boolean` class represents a BOOLEAN column type.
#
# Students should implement the missing methods for each type (e.g., `get_sql`, `validate`)
# to ensure proper integration with the ORM and the generation of valid SQL queries.
#
# Example usage in the ORM base class:
#
#   class User:
#       id = Column(Integer, primary_key=True)   # An INTEGER primary key column
#       name = Column(String(255), nullable=False)  # A TEXT column with a length of 255, not nullable
#       is_active = Column(Boolean, default=True)  # A BOOLEAN column with a default value of True
#       created_at = Column(Date)  # A DATE column
#
#   This would represent a "User" table with columns: "id", "name", "is_active", and "created_at".
#   The ORM will use the data types (Integer, String, Boolean, Date) to validate values and generate
#   SQL queries when interacting with the database.

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