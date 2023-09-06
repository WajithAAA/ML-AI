import os
from app import create_app

app = create_app('development')
current_dir = os.getcwd()


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), debug=True)

#