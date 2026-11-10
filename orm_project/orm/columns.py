"""
columns.py

Column metadata and schema definition utilities for the ORM framework.

The Column class defines the structure and constraints of individual
database fields, providing the metadata required to map Python model
attributes to relational database columns.

Each Column instance describes a field's data type, validation rules,
and relational constraints. This metadata supports SQL schema generation,
data validation, and consistent model-to-database mapping.

Key Features
------------
Column Configuration:
    column_type     Defines the SQL data type associated with the field.
    primary_key     Indicates whether the column is part of a primary key.
    nullable        Specifies whether the column accepts NULL values.
    unique          Enforces uniqueness constraints on column values.
    foreign_key     Defines a relationship to a referenced table or column.

Schema Generation and Validation:
    get_sql()           Generate the SQL definition for the column.
    validate_type()     Validate the column's supported data type.
    is_primary_key()    Determine whether the column is a primary key.
    to_dict()           Return column metadata as a dictionary.
    get_constraints()   Generate SQL constraint definitions.
    is_foreign_key()    Determine whether a foreign key relationship exists.

ORM Integration
---------------
Column definitions serve as the mapping layer between Python model
attributes and relational database fields.

The ORM uses this metadata to construct table schemas, generate SQL
statements, and apply database constraints consistently across models.

Example
-------
class User:
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    created_at = Column(Date)
    profile_id = Column(Integer, foreign_key="Profile(id)")

The ORM can interpret these definitions to construct the corresponding
SQL table schema, including data types, primary keys, uniqueness
constraints, nullability rules, and foreign key relationships.

Design Considerations
---------------------
The Column abstraction centralizes database field configuration,
reducing repetitive SQL definitions and improving consistency across
the ORM framework.

Separating column metadata from model persistence logic also supports
maintainability, extensibility, and future enhancements to schema
validation and query generation.
"""


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
