
#!/usr/bin/env python3

#!/usr/bin/env python3
import rumps
import subprocess
import os

class DaliApp(rumps.App):
    def __init__(self):
        super(DaliApp, self).__init__("🤖", quit_button=None)
        self.menu = [
            rumps.MenuItem("Dali Status: Running", callback=None),
            None,
            rumps.MenuItem("Quit Dali", callback=self.quit_app)
        ]
    
    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    DaliApp().run()
