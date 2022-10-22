import arcade

# Constants
SCREEN_WIDTH = 1777
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Chronobio"


class Window(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.DARK_OLIVE_GREEN)
        self.background_list: arcade.SpriteList = None

    def setup(self):
        self.background_list = arcade.SpriteList()
        grass = arcade.Sprite("chronobio/viewer/images/grass.jpeg")
        grass_width = grass.width
        grass_height = grass.height
        for x in range(0, SCREEN_WIDTH, grass_width):
            for y in range(0, SCREEN_HEIGHT, grass_height):
                grass = arcade.Sprite("chronobio/viewer/images/grass.jpeg")
                grass.position = x + grass_width // 2, y + grass_height // 2
                self.background_list.append(grass)

    def on_draw(self):
        self.clear()
        self.background_list.draw()


def gui_thread(window):
    window.setup()
    arcade.run()
