"""
base.py

Core ORM base model providing a standardized interface for database
persistence, schema management, and query construction.

The Base class serves as the foundation for all ORM models, encapsulating
common database operations and promoting consistent data access patterns.

Key Features
------------
Persistence Operations:
    save()          Insert a new record or update an existing instance.
    _insert()       Execute an INSERT operation for the current instance.
    _update()       Execute an UPDATE operation for the current instance.
    get()           Retrieve a record by its primary key.
    delete()        Delete a record by its primary key.
    all()           Retrieve all records associated with the model.
    query()         Retrieve records matching specified filter criteria.

Schema Management:
    create_schema() Generate SQL schema definitions from model metadata.
    create()        Create database tables using generated schema definitions.

Query Construction:
    join()          Construct queries involving multiple related models.
    where()         Apply conditional filters to query results.
    having()        Apply conditions to aggregated query results.
    group_by()      Group records based on specified fields.

Connection and Transaction Management
-------------------------------------
Database operations follow consistent resource management and transaction
handling practices to maintain reliability and data integrity.

    - Establish database connections and cursors for each operation.
    - Release database resources regardless of operation outcome.
    - Commit transactions following successful write operations.
    - Roll back transactions when errors occur.
    - Handle database exceptions without leaving open connections.
    - Use structured exception handling to ensure reliable cleanup.

Architecture
------------
Base is designed for inheritance. Model classes extending Base gain access
to shared persistence, query, and schema-management functionality, reducing
code duplication and supporting consistent database interaction patterns.

This design separates common database operations from model-specific
business logic, improving maintainability, extensibility, and testability.
"""


from .dbconnectors import MySQL
from .columns import Column


class Base:
    def __init__(self, **kwargs):
        """Initialize model instance with attributes."""
        self._db = MySQL()  # instance of MySQL connector
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Insert or update the record in the database."""
        # Find the primary key column
        pk_column = None
        pk_value = None

        for attr_name in dir(self):
            attr = getattr(self.__class__, attr_name, None)
            if isinstance(attr, Column) and attr.primary_key:
                pk_column = attr_name
                pk_value = getattr(self, attr_name, None)
                break

        # If primary key exists and has a value, update; otherwise insert
        if pk_column and pk_value is not None:
            self._update()
        else:
            self._insert()

    def _insert(self):
        """Insert the current instance into the database."""
        connection = None
        cursor = None

        try:
            # Open connection and cursor using instance()
            connection, cursor = self._db.instance()

            # Get table name from class
            table_name = getattr(self.__class__, '_table_name', self.__class__.__name__)

            # Build column names and values
            columns = []
            values = []
            placeholders = []

            for attr_name in dir(self):
                attr = getattr(self.__class__, attr_name, None)
                if isinstance(attr, Column):
                    # Skip primary key if it's auto-increment
                    if attr.primary_key and hasattr(self, attr_name):
                        value = getattr(self, attr_name)
                        if value is None:
                            continue

                    if hasattr(self, attr_name):
                        columns.append(attr_name)
                        values.append(getattr(self, attr_name))
                        placeholders.append('%s')

            # Construct INSERT query
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

            # Execute query
            cursor.execute(query, values)
            connection.commit()

            # Get the last inserted id
            if hasattr(self, 'id') and self.id is None:
                cursor.execute("SELECT LAST_INSERT_ID() as id")
                result = cursor.fetchone()
                if result:
                    self.id = result['id']

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error inserting record: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def _update(self):
        """Update the current instance in the database."""
        connection = None
        cursor = None

        try:
            # Open connection and cursor using instance()
            connection, cursor = self._db.instance()

            # Get table name from class
            table_name = getattr(self.__class__, '_table_name', self.__class__.__name__)

            # Build SET clause
            set_parts = []
            values = []

            for attr_name in dir(self):
                attr = getattr(self.__class__, attr_name, None)
                if isinstance(attr, Column) and not attr.primary_key:
                    if hasattr(self, attr_name):
                        set_parts.append(f"{attr_name} = %s")
                        values.append(getattr(self, attr_name))

            # Find primary key
            pk_column = None
            for attr_name in dir(self):
                attr = getattr(self.__class__, attr_name, None)
                if isinstance(attr, Column) and attr.primary_key:
                    pk_column = attr_name
                    break

            # Add primary key value for WHERE clause
            values.append(getattr(self, pk_column))

            # Construct UPDATE query
            query = f"UPDATE {table_name} SET {', '.join(set_parts)} WHERE {pk_column} = %s"

            # Execute query
            cursor.execute(query, values)
            connection.commit()

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error updating record: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def get(cls, **kwargs):
        """Retrieve a record from the database by filters."""
        connection = None
        cursor = None
        db = MySQL()

        try:
            # Open connection and cursor using instance()
            connection, cursor = db.instance()

            # Get table name from class
            table_name = getattr(cls, '_table_name', cls.__name__)

            # Build WHERE clause
            if 'id' in kwargs:
                query = f"SELECT * FROM {table_name} WHERE id = %s"
                cursor.execute(query, (kwargs['id'],))
            else:
                # Build dynamic WHERE clause for multiple conditions
                conditions = []
                values = []
                for key, value in kwargs.items():
                    conditions.append(f"{key} = %s")
                    values.append(value)

                where_clause = " AND ".join(conditions)
                query = f"SELECT * FROM {table_name} WHERE {where_clause}"
                cursor.execute(query, values)

            # Fetch result
            result = cursor.fetchone()

            if result:
                return cls(**result)
            return None

        except Exception as e:
            print(f"Error retrieving record: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def delete(cls, **kwargs):
        """Delete a record from the database."""
        connection = None
        cursor = None
        db = MySQL()

        try:
            connection, cursor = db.instance()
            table_name = getattr(cls, '_table_name', cls.__name__)

            # Find primary key column
            pk_column = None
            for attr_name in dir(cls):
                attr = getattr(cls, attr_name, None)
                if isinstance(attr, Column) and attr.primary_key:
                    pk_column = attr_name
                    break

            # Get the value to delete
            pk_value = kwargs.get(pk_column) if pk_column else kwargs.get('id')

            query = f"DELETE FROM {table_name} WHERE {pk_column} = %s"
            cursor.execute(query, (pk_value,))
            connection.commit()

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error deleting record: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def get_all(cls):
        """Retrieve all records of this model from the database."""
        connection = None
        cursor = None
        db = MySQL()

        try:
            # Open connection and cursor using instance()
            connection, cursor = db.instance()

            # Get table name from class
            table_name = getattr(cls, '_table_name', cls.__name__)

            # Construct SELECT query
            query = f"SELECT * FROM {table_name}"

            # Execute query
            cursor.execute(query)
            results = cursor.fetchall()

            # Convert results to model instances
            instances = []
            for row in results:
                instances.append(cls(**row))

            return instances

        except Exception as e:
            print(f"Error retrieving all records: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def filter_by(cls, **filters):
        """Query records based on filters."""
        connection = None
        cursor = None
        db = MySQL()

        try:
            # Open connection and cursor using instance()
            connection, cursor = db.instance()

            # Get table name from class
            table_name = getattr(cls, '_table_name', cls.__name__)

            # Build WHERE clause
            conditions = []
            values = []

            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                values.append(value)

            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM {table_name} WHERE {where_clause}"

            # Execute query
            cursor.execute(query, values)
            results = cursor.fetchall()

            # Convert results to model instances
            instances = []
            for row in results:
                instances.append(cls(**row))

            return instances

        except Exception as e:
            print(f"Error querying records: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def create_table(cls):
        """Create a table for the model if it doesn't exist."""
        connection = None
        cursor = None
        db = MySQL()

        try:
            # Open connection and cursor using instance()
            connection, cursor = db.instance()

            # Generate schema
            schema = cls.create_schema()

            # Execute CREATE TABLE query
            cursor.execute(schema)
            connection.commit()

            print(f"Table {cls.__name__} created successfully")

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error creating table: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def create_schema(cls):
        """Generate the schema for the model."""
        table_name = getattr(cls, '_table_name', cls.__name__)
        columns_sql = []

        # Iterate through class attributes to find Column definitions
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name, None)
            if isinstance(attr, Column):
                column_def = f"{attr_name} {attr.sql_type()}"

                if attr.primary_key:
                    column_def += " PRIMARY KEY AUTO_INCREMENT"

                if not attr.nullable:
                    column_def += " NOT NULL"

                if attr.default is not None:
                    if isinstance(attr.default, str):
                        column_def += f" DEFAULT '{attr.default}'"
                    elif isinstance(attr.default, bool):
                        column_def += f" DEFAULT {1 if attr.default else 0}"
                    else:
                        column_def += f" DEFAULT {attr.default}"

                columns_sql.append(column_def)

        # Build CREATE TABLE statement
        schema = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_sql)})"

        return schema

    @classmethod
    def join(cls, other_model):
        """Join with another model."""
        connection = None
        cursor = None
        db = MySQL()

        try:
            # Open connection and cursor using instance()
            connection, cursor = db.instance()

            # Get table names
            table1 = cls.__name__
            table2 = other_model

            # Simple join assuming foreign key relationship
            query = f"""
                SELECT * FROM {table1}
                JOIN {table2} ON {table1}.id = {table2}.{table1.lower()}_id
            """

            cursor.execute(query)
            results = cursor.fetchall()

            return results

        except Exception as e:
            print(f"Error performing join: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def where(cls, **conditions):
        """Generate WHERE clause from conditions."""
        if not conditions:
            return ""

        where_parts = []
        for key, value in conditions.items():
            if isinstance(value, str):
                where_parts.append(f"{key} = '{value}'")
            else:
                where_parts.append(f"{key} = {value}")

        return "WHERE " + " AND ".join(where_parts)

    @classmethod
    def having(cls, **conditions):
        """Generate HAVING clause from conditions."""
        if not conditions:
            return ""

        having_parts = []
        for key, value in conditions.items():
            having_parts.append(f"{key} = {value}")

        return "HAVING " + " AND ".join(having_parts)

    @classmethod
    def group_by(cls, *columns):
        """Generate GROUP BY clause."""
        if not columns:
            return ""

        return "GROUP BY " + ", ".join(columns)
