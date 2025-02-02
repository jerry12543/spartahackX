from loanminnow.api.model import db, Venture, User
from flask import Flask
from datetime import datetime, timedelta
import pathlib
import os
import loanminnow

app = loanminnow.app

LOANMINNOWROOT = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = os.path.join(LOANMINNOWROOT, "var", "loanminnow.db")
app.config['SQLALCHEMY_DATABASE_URI']  = f'sqlite:///{DB_PATH}'


# Create a new venture inside the application context
with app.app_context():
    owner = User.query.get(1)  # Fetch user with ID 1
    if owner:
        new_venture = Venture(
            name="Solar Energy Project",
            description="A venture to install solar panels in rural areas.",
            goal=50000.00,
            interest_rate=5.0,
            due_date=datetime.utcnow() + timedelta(days=90),
            owner=owner
        )

        db.session.add(new_venture)
        db.session.commit()
        print(f"Venture '{new_venture.name}' created successfully with ID {new_venture.id}")
    else:
        print("Error: Owner not found!")