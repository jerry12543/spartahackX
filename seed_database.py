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
    user_0 = User(
        name="Bob Dylan",
        email="bobdylan@gmail.com",
        password="penicillin",
        available_credits=1000
    )
    user_1 = User(
        name="Jerry Zhu",
        email="jerruzhu@umich.edu",
        password="password",
        available_credits=5000
    )

    # add users to the database
    db.session.add(user_0)
    db.session.add(user_1)
    db.session.commit()

    owner0 = User.query.get(1)
    owner1 = User.query.get(2)
    if owner0 and owner1:
        project_1 = Venture(
            name="Amina's Artisan Bakery",
            description="Amina, a single mother of three in rural Kenya, dreams of opening a small bakery to sell fresh bread and pastries to her community. With access to an oven and essential baking tools, she can provide for her family while offering affordable baked goods to her neighbors.",
            goal=500,
            interest_rate=0.1,
            due_date=datetime(2023, 11, 30),
            owner=owner0,
            image_url="aminas-bakery.jpg"
        )

        project_2 = Venture(
            name="Maria’s Sewing Studio",
            description="Maria, a skilled seamstress in Guatemala, wants to expand her home-based sewing business by purchasing an industrial sewing machine. This will allow her to take on larger orders and create school uniforms for local children, helping her community while growing her income.",
            goal=750,
            interest_rate=0.1,
            due_date=datetime(2023, 12, 15),
            owner=owner0,
            image_url="sewing-studio.png"
        )

        project_3 = Venture(
            name="Green Sprouts Family Farm",
            description="The Kumar family in India is starting a small organic vegetable farm to supply fresh produce to their village. They need funds for seeds, tools, and irrigation equipment to begin their first planting season. Their goal is to promote sustainable farming practices and improve local food security.",
            goal=1000,
            interest_rate=0.4,
            due_date=datetime(2023, 12, 20),
            owner=owner0,
            image_url="small-farm-green-sprouts.jpg"
        )

        project_4 = Venture(
            name="Fatima’s Handcrafted Jewelry",
            description="Fatima in Morocco creates beautiful handcrafted jewelry using traditional Berber techniques. She needs funding to purchase raw materials like silver and gemstones to fulfill growing demand from tourists and online buyers. Her goal is to preserve her cultural heritage while supporting her family.",
            goal=400,
            interest_rate=0.3,
            due_date=datetime(2023, 11, 25),
            owner=owner1,
            image_url="handcrafted-jewerly.jpg"
        )

        project_5 = Venture(
            name="Bright Minds Tutoring Center",
            description="Esther, a retired teacher in Nigeria, wants to open a tutoring center for children in her neighborhood who lack access to quality education. She plans to buy desks, chairs, and books to create a welcoming learning space where she can teach math and reading skills.",
            goal=600,
            interest_rate=0.2,
            due_date=datetime(2023, 12, 10),
            owner=owner1,
            image_url="tutoring-center.jpg"
        )

        for project in [project_1, project_2, project_3, project_4, project_5]:
            db.session.add(project)
            db.session.commit()
            print(f"Added project: {project.name}")

    else:
        print("Error: Owner not found!")