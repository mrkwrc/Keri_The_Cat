from pathlib import Path
class GameStats:
    """Track statistics for the game."""
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # best high score should never be reset.
        self.high_score = 0
        self.path = Path('highscore.txt')
        self._load_high_score_from_file()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.cats_left = self.settings.cats_limit
        self.score = 0
        self.level = 1

    def _load_high_score_from_file(self):
        try:
            score = int(self.path.read_text())
            if score > self.high_score:
                self.high_score = score
        except:
            pass
    
    def save_high_score_to_file(self):
        self.path.write_text(str(self.high_score))
