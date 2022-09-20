import os
from api import app



if __name__ == '__main__':
    bank_id = os.environ.get("BANK_ID")

    if bank_id == "BANK1":
        app.run(host='0.0.0.0', port=5001)
    elif bank_id == "BANK2":
        app.run(host='0.0.0.0', port=5002)
