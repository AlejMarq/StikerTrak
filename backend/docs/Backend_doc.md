# StikerTrak Backend Documentation

## Overview

This document describes the backend functions available for the StikerTrak project. These functions are located in:

backend/db_helpers.py

The frontend should call these functions instead of writing SQL queries directly.

---

# Database Tables

## users

Stores user account information.

Fields:
- id
- username
- email
- password_hash
- first_name
- last_name

---

## stickers

Stores every sticker in the album.

Fields:
- id
- sticker_number
- category
- section
- name
- country

Example:

MEX-04
Player
Mexico
JORGE SANCHEZ
Mexico

---

## user_collection

Stores which stickers each user owns.

Fields:
- id
- user_id
- sticker_id
- quantity

Example:

User 1
Sticker 54
Quantity 3

This means the user owns 3 copies of that sticker.

---

# Backend Functions

## get_all_stickers()

Purpose:
Returns every sticker in the database.

Example:

```python
stickers = get_all_stickers()
```

---

## get_stickers_by_country(country)

Purpose:
Returns all stickers for a specific country.

Example:

```python
stickers = get_stickers_by_country("Mexico")
```

---

## get_sticker_by_number(sticker_number)

Purpose:
Returns one sticker based on its sticker number.

Example:

```python
sticker = get_sticker_by_number("MEX-04")
```

---

## add_or_update_sticker(user_id, sticker_number)

Purpose:
Adds a sticker to a user's collection.

If the user already owns the sticker, the quantity increases by one.

Example:

```python
add_or_update_sticker(1, "MEX-04")
```

---

## get_user_collection(user_id)

Purpose:
Returns every sticker owned by the user.

Example:

```python
collection = get_user_collection(1)
```

---

## get_duplicate_stickers(user_id)

Purpose:
Returns stickers where quantity is greater than 1.

Example:

```python
duplicates = get_duplicate_stickers(1)
```

---

## get_missing_stickers(user_id)

Purpose:
Returns every sticker the user does not own.

Example:

```python
missing = get_missing_stickers(1)
```

---

## get_collection_progress(user_id)

Purpose:
Returns:

- Total stickers
- Collected stickers
- Missing stickers
- Completion percentage

Example:

```python
progress = get_collection_progress(1)
```

---

# Notes for Developers

- Do not have to write SQL queries in the frontend - can use the backend functions whenever possible.
- All database operations should go through `db_helpers.py`.
- If a new database feature is needed, can add a new backend function instead of duplicating code.