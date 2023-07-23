<br />

<div align="center">
    <h1>Kascade ORM</h1>
    <p><h3 align="center">Python ORM for SQL Databases based on Pydantic</h3></p>
    <div align="center">
    </div>
</div>

<hr>

## What is Kascade ORM?

Kascade ORM is the next-geneneration ORM built on top of Pydantic in order to have the best integration with frameworks like FastAPI.

---

## Roadmap

Our plan is to give the users maximum access to SQL Databases inside Python code without making them hard to understand.
To do so, we plan to structure everything in `Objects`.

### Notes about Callable:

This util callables could be created directly in SQL or via Python.
If is it possible it is always created on SQL.

- cuid: Depends
- uuid: Depends
- random: Depends
- autoincrement: SQL Always
- utcnow: SQL Always
- now: SQL Always
- custom: Python Always

### Things to store per column:

- Type: `Type Hint`
- Name: `str`
- Unique: `bool`
- Optional: `bool`
- IsId: `bool`
- Default: `Any` or `Callable`
- OnUpdate: `None` or `Callable`

### Things to store per Relation:
- Table1: `Table`
- Table2: `Table`
- Table1Columns: `List[Column]`
- Table2Columns: `List[Column]`

### Things to store per Table:

- Columns: `List[Column]`
- CompoundUniques: `List[List[Column]]`
- Indexes: `List[Column]`
- Relations: `List[Relation]`

---

## Extra features planned to be added

1. If we have two tables we plan to substract them in order to detect differences between them. This whay we can easily manage `apply`s to update the tables.
2. Users should be capable to create fast Type Hints from their tables in order to allow returning for example an `User` without the `password` in FastAPI without needing to create a custom Schema that is just a duplication of the `User` schema without this field.
3. Important: Allow to generate the Python file with the current Database schema.

## This is an example of how we plan to create tables

```python
from pydantic import EmailStr
from kascade import ForeignKey, Table, Column, column_defaults

class Item(Table):
    # Note that if it is called ID and is an int,
    # this configuration is equivalente to the
    # `User` table configuration
    id: int
    name: str
    user_id: int

class User(Table):
    name: str
    email: EmailStr
    password: str
    id: Column = Column(
        type=int,
        unique=True,
        default=column_defaults.autoincrement,
    )
    avatar: Optional[bytes] = None
    items: ForeignKey = ForeignKey(
        table=Item,
        column='user_id',
    )
```

This is just an idea, we could change it. Also, we are still thinking on the best way to manage relationships.

On this example the generated Python code (internally) will look similar to:

```python

from pydantic import EmailStr
from kascade import ForeignKey, Table, Column, column_defaults

class Item(Table):
    id: int
    name: str
    user_id: int    

    @property
    def user(self):
        # Code to get user dynamically (or explicitly)
        pass

class User(Table):
    name: str
    email: EmailStr
    password: str
    id: int
    avatar: Optional[bytes] = None
    
    @property
    def items(self):
        # Code to get items dynamically (or explicitly)
        pass

```

This class will have also other methods based on Table ones.

---

Also, this is an example on how an end user will use this tables:

```python
import asyncio

from kascade import Kascade


async def main():
    async with Kascade() as db:
        user = await db.User.create({
            name='Fernando Pérez',
            email='fernaperg@gmail.com',
            password='super-secure-kascade-password',
        })

        item = await db.Item.create({
            name='Laptop',
            # Only one of the following is needed
            user_id=user.id,
            user=user,
        })

        all_users_with_avatar = await db.User.find_many({
            'where': {
                'avatar': {
                    'not': None,
                }
            }
        })

        # In this case we know that for some reasson we need
        # to query all items for each user,
        # Therefore, in order to improve performance and
        # avoid unexpected loads when querying items from
        # each user with the code: all_kascade_emails[0].items
        all_kascade_emails = await db.User.find_many({
            'where': {
                'email': {
                    'ends_with': '@kascade.com',
                }
            }
            'include': {
                'items': True,
            }
        })


if __name__ == '__main__':
    asyncio.run(main())

```