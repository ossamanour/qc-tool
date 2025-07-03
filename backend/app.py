from app import create_app

import sys
print(sys.executable)

app = create_app()
app.run(debug=True, port=app.config["PORT"])