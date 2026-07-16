# StikerTrak
FIFA 2026 World Cup Sticker Collection Tracker
A web application that allows users to digitally track their FIFA World Cup 2026 Panini sticker collection.

## Application Description

StikerTrak helps FIFA World Cup sticker collectors organize and manage their collection in one place. Users can create an account, browse the complete sticker catalog, track owned and missing stickers, manage duplicates, and monitor overall collection progress.

## Features

* User Authentication
  - Create a new account
  - Secure login and logout
  - Password validation
  - Session management

* Sticker Collection
  - Browse all FIFA World Cup 2026 stickers
  - Search stickers by number or name
  - Filter stickers by:
    - All
    - Owned
    - Missing
    - Duplicates
  - Sort stickers by:
    - Sticker Number
    - Sticker Name
    - Quantity Owned
  -  Add and remove stickers from a collection
  - Track collection progress

## Prerequisites

- Python 3.13 or newer
- Visual Studio Code or another code editor
- Git

## Installation & Setup

  1. Clone the repository

```bash
git clone https://github.com/AlejMarq/StikerTrak.git
```

  2. Navigate to the project directory

```bash
cd StikerTrak
```

  3. Install the required packages

```bash
pip install -r requirements.txt
```

  4. Initialize the database

```bash
py init_db.py
```

  5. Start the application

```bash
py backend/app.py
```

  6. Open your browser

Go to:

```
http://127.0.0.1:5000
```
