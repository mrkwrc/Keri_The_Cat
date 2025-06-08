class Settings:
    """A class to hold the settings for the application."""
    def __init__(self):
        """Initialize the application's settings."""
        # Screen settings
        self.screen_width = 1920 # designed
        self.screen_height = 1080 # designed
        # self.screen_height = 500 # for testing
        self.bg_color = (180, 180, 180)
        self.fullscreen = False # for testing; comment for prod
        # self.fullscreen = input(
        #     "Do you want to run the game in full screen mode? (y/n): "
        # ).strip().lower() == 'y' # uncomment for prod

        # Cat settings
        self.cats_limit = 3

        # Heart settings
        self.heart_width = 15
        self.heart_height = 3
        self.heart_color = (30, 30, 30)
        # Pigeon settings
        self.pigeon_hits = 0
        self.pigeon_hits_limit = 10

        # Speed scalings
        self.speedup_scale = 1.05

        # Score scalings
        self.score_scale = 1.5 # to consider to use   

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # cat dynamic settings
        self.cat_speed = 1.8

        # heart dynamic settings
        self.hearts_allowed = 5
        self.heart_speed = 2.0
        
        # pigeon dynamic settings
        self.pigeon_speed = 0.8
        self.pigeon_frequency = 0.008
        self.pigeon_hits = 0

        # Scoring
        self.pigeon_points = 10
 
    def increase_speed(self):
        """Increase speed settings."""
        self.cat_speed *= self.speedup_scale
        self.heart_speed *= self.speedup_scale
        self.pigeon_speed *= self.speedup_scale
        self.pigeon_frequency *= self.speedup_scale
        # to consider to use:
        # self.pigeon_points = int(self.pigeon_points * self.score_scale)

