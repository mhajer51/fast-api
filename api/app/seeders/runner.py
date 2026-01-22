from app.seeders.user_seeder import UserSeeder


def seed_all() -> None:
    seeders = [UserSeeder()]
    for seeder in seeders:
        seeder.run()
