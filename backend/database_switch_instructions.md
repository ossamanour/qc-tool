# Instructions on Switch PostgreSQL Database

### Create PostgreSQL database

The following instructions are on how to create PostgreSQL database under Ubuntu OS system in WSL of Windows 11.

1. Install PostgreSQL, skip if you already have it installed.

```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

2. Start PostgreSQL service
   `sudo systemctl start postgresql.service`
3. Access the PostgreSQL prompt
   `sudo -i -u postgres`
   Launch the interactive terminal
   `psql`
4. Create new databse
   `CREATE DATABASE database_name;`
5. Create user with a password
   `CREATE USER testuser WITH PASSWORD 'password';`
6. Give user access to the database
   `GRANT ALL PRIVILEGES ON DATABASE database_name TO testuser;`

### Connect the database to the Flask app

1. Got to the script `/backend/app/__init__.py`, uncomment the lines (line 41-43) that help to create registrtion code.

```
    # create registration code if available code is less than 5
    # with app.app_context():
    #     create_registration_code()
```

- _This function is help to generate registration code to limit the test user to only people with permission. This will not needed for later use. But for current testing version, please remember to uncomment them after the database setups are done. The function will create random registration code._

2. Modify the config file for Flask app `/backend/config.py`. Change the `SQLALCHEMY_DATABASE_URI` to the one with the new database, user, hostip and other necessary information.
   `SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:password@host/database?application_name=dev"`

3. Navigate to the directory of `app.py`, in this project, it should be `/backend/app`. Delete the `migrations` folder which containing all migration information of the old database.
   `rm -r migrations`

4. Initialize the new migration
   `flask db init`
   A new migration folder will be created under the current directory.

5. Create initial migration
   `flask db migrate -m "Initial migration"`

- _If an error message of `psycopg2.errors.InsufficientPrivilege: permission denied for schema public` showed, go to the database and grant usage on schema public for the current user._

6. Apply the migration
   `flask db upgrade`

7. All defined tables (under `/backend/app/models) should be created in the new database.

### Extra process for registration code generation

Uncomment the code to generate registration code and re-run the backend, 50 new registration code will be generated. These code will be used for new user generation.
