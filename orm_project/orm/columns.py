# columns.py
#
# This file defines the `Column` class used in the ORM framework. Each instance of
# the `Column` class represents a single column in a database table. The `Column` class
# allows us to define the column's data type, constraints (e.g., primary key, nullable, etc.),
# and foreign key relationships.
#
# The `Column` class is used by the ORM framework to map the attributes of Python classes
# (like `User`, `Post`, etc.) to actual database tables. The ORM will automatically generate
# the necessary SQL queries based on these column definitions.
#
# The `Column` class handles attributes such as:
#   - `column_type`: The type of the column (e.g., INTEGER, TEXT).
#   - `primary_key`: Whether the column is part of the primary key.
#   - `nullable`: Whether the column can be null.
#   - `unique`: Whether the column values must be unique.
#   - `foreign_key`: The foreign key constraint that relates to another table.
#
# Students need to implement the following methods to complete the functionality of this class:
#   - `get_sql()`: Generates the SQL representation of the column.
#   - `validate_type()`: Validates that the column's type is supported.
#   - `is_primary_key()`: Checks if the column is part of the primary key.
#   - `to_dict()`: Returns the column's configuration as a dictionary.
#   - `get_constraints()`: Generates a string of the column's constraints (e.g., "NOT NULL").
#   - `is_foreign_key()`: Checks if the column is a foreign key.
#
# Example usage in the ORM base class:
#
#   class User:
#       id = Column(Integer, primary_key=True)  # Primary key column of type Integer
#       name = Column(String(255), nullable=False)  # String column, not nullable
#       email = Column(String(100), unique=True)  # String column, with a unique constraint
#       created_at = Column(Date)  # Date column
#       profile_id = Column(Integer, foreign_key='Profile(id)')  # Foreign key referencing 'Profile' table
#
#   The ORM will use these `Column` instances to define the table schema and generate the
#   corresponding SQL for table creation, validation, and foreign key enforcement.


class Column:
    def __init__(self, column_type, primary_key=False, nullable=True, unique=False,
                foreign_key=None, default=None, on_delete=None, on_update=None,
                 auto_increment=False):
        self.type = column_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique
        self.foreign_key = foreign_key
        self.on_update = on_update
        self.on_delete = on_delete
        self.default = default
        self.auto_increment = auto_increment

    def sql_type(self):
        """Get the SQL type string from the column type."""
        if hasattr(self.type, 'sql_type'):
            return self.type.sql_type()
        return str(self.type)

    def to_sql(self):
        """Return the SQL representation of the column."""
        sql_parts = [self.sql_type()]

        # Add constraints
        constraints = self.get_constraints()
        if constraints:
            sql_parts.append(constraints)

        return " ".join(sql_parts)

    def validate_type(self):
        """Validate if the column's type is valid."""
        # List of valid SQL types
        valid_types = [
            'INT', 'INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT',
            'VARCHAR', 'CHAR', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT',
            'DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE',
            'DATE', 'DATETIME', 'TIMESTAMP', 'TIME',
            'BOOLEAN', 'BOOL',
            'BLOB', 'MEDIUMBLOB', 'LONGBLOB',
            'ENUM', 'SET'
        ]

        # Get the SQL type string
        sql_type_str = self.sql_type().upper()

        # Check if the base type is valid (handles VARCHAR(255) -> VARCHAR)
        base_type = sql_type_str.split('(')[0].strip()

        if base_type in valid_types:
            return True

        # If type has a sql_type method, assume it's valid (custom type)
        if hasattr(self.type, 'sql_type'):
            return True

        return False

    def is_primary_key(self):
        """Check if the column is part of a primary key."""
        return self.primary_key

    def to_dict(self):
        """Return a dictionary representation of the column."""
        return {
            'type': self.sql_type(),
            'primary_key': self.primary_key,
            'nullable': self.nullable,
            'unique': self.unique,
            'foreign_key': self.foreign_key,
            'default': self.default,
            'on_delete': self.on_delete,
            'on_update': self.on_update,
            'auto_increment': self.auto_increment
        }

    def get_constraints(self):
        """Generate the column's constraints as a string."""
        constraints = []

        # Primary key constraint
        if self.primary_key:
            constraints.append("PRIMARY KEY")

        # Auto increment
        if self.auto_increment:
            constraints.append("AUTO_INCREMENT")

        # Not null constraint
        if not self.nullable and not self.primary_key:
            constraints.append("NOT NULL")

        # Unique constraint
        if self.unique and not self.primary_key:
            constraints.append("UNIQUE")

        # Default value
        if self.default is not None and self.default is not True:
            if isinstance(self.default, str):
                constraints.append(f"DEFAULT '{self.default}'")
            elif isinstance(self.default, bool):
                constraints.append(f"DEFAULT {1 if self.default else 0}")
            else:
                constraints.append(f"DEFAULT {self.default}")

        # Foreign key constraint
        if self.foreign_key:
            fk_constraint = f"REFERENCES {self.foreign_key}"

            if self.on_delete:
                fk_constraint += f" ON DELETE {self.on_delete}"

            if self.on_update:
                fk_constraint += f" ON UPDATE {self.on_update}"

            constraints.append(fk_constraint)

        return " ".join(constraints)

    def is_foreign_key(self):
        """Check if the column has a foreign key constraint."""
        return self.foreign_key is not None