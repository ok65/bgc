
from database import get_db

class GameDatabase:


    @classmethod
    def search(cls, name: str):

        with get_db() as db:
            cur = db.cursor()
            cur.execute(query, (game.id, game.name, game.min_players, game.max_players, "Description goes here"))
            db.commit()
            cur.close()
            print(f"New game added, id: {game.id}")