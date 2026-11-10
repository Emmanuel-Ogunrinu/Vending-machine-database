# EXTRA CREDIT AND OPTIONAL (3 points)
# migrations.py
#
# This file is responsible for managing database migrations. Migrations allow you to manage changes
# to the database schema over time, including creating tables, adding columns, and modifying the schema.
#
# Students are required to implement the following methods to perform migration tasks on the database.
#
# Example migration tasks include:
#   - Creating a new table.
#   - Adding new columns to an existing table.
#   - Removing columns from an existing table.
#   - Renaming columns in a table.
#   - Altering column types or constraints.
#
# Each method should:
#   - Open a connection and cursor to the database.
#   - Ensure the connection and cursor are properly closed after the operation, even in case of errors.
#   - Handle exceptions with appropriate error messages.
#   - Commit the transaction if the operation is successful, and rollback if there is an error.

class Migrations:

    @classmethod
    def create_table(cls, table_name, schema):
        """Create a new table in the database.

        TODO:
            - Open a new connection and cursor.
            - Construct a `CREATE TABLE` SQL query using the provided table name and schema.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def add_column(cls, table_name, column_name, column_type):
        """Add a new column to an existing table.

        TODO:
            - Open a new connection and cursor.
            - Construct an `ALTER TABLE` SQL query to add the new column to the table.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def remove_column(cls, table_name, column_name):
        """Remove a column from an existing table.

        TODO:
            - Open a new connection and cursor.
            - Construct an `ALTER TABLE` SQL query to drop the column from the table.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def rename_column(cls, table_name, old_column_name, new_column_name):
        """Rename a column in an existing table.

        TODO:
            - Open a new connection and cursor.
            - Construct an `ALTER TABLE` SQL query to rename the column.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def change_column_type(cls, table_name, column_name, new_column_type):
        """Change the data type of an existing column.

        TODO:
            - Open a new connection and cursor.
            - Construct an `ALTER TABLE` SQL query to change the column type.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def add_constraint(cls, table_name, constraint_type, column_name, constraint_name):
        """Add a constraint to a column (e.g., UNIQUE, NOT NULL).

        TODO:
            - Open a new connection and cursor.
            - Construct an `ALTER TABLE` SQL query to add the constraint.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def remove_constraint(cls, table_name, constraint_name):
        """Remove a constraint from a column.

        TODO:
            - Open a new connection and cursor.
            - Construct an `ALTER TABLE` SQL query to drop the constraint.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def rename_table(cls, old_table_name, new_table_name):
        """Rename an existing table.

        TODO:
            - Open a new connection and cursor.
            - Construct a `RENAME TABLE` SQL query to rename the table.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def apply_migration(cls, migration_file):
        """Apply a migration from a given migration file.

        TODO:
            - Open a new connection and cursor.
            - Read the SQL commands from the migration file.
            - Execute the SQL commands to update the database schema.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass

    @classmethod
    def rollback_migration(cls, migration_file):
        """Rollback a previously applied migration.

        TODO:
            - Open a new connection and cursor.
            - Read the rollback SQL commands from the migration file.
            - Execute the SQL commands to revert the database schema.
            - Ensure the connection and cursor are properly closed after the operation.
            - Commit the transaction if successful, and rollback on failure.
        """
        pass


