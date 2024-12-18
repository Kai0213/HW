import pyotp
from flask import Flask, render_template

app = Flask(__name__)

def get_google_code(secret_key):
    """生成當前的 Google Authenticator 驗證碼"""
    totp = pyotp.TOTP(secret_key)
    return totp.now()

@app.route('/')
def show_codes():
    codes = {
        "pre_shawn": get_google_code("TLTSS7DBWEEFN356"), #替換自己的 secret
        "pre_admin": get_google_code("G3CCTF47G2EBSUHR"),
        "Beta_shawn": get_google_code("MCQMLQFGG2OHABY6"),
        "Beta_admin": get_google_code("JCNP7EHYEVUC7GWX"),
        "OL_shawn": get_google_code("FZKWB37Z7PIQMKWC"),
        "OL_admin": get_google_code("UNN4NIBRCXRBFMI4"),
        "Payment_Pre": get_google_code("EXC6QCULV5MWJV4R"),
        "Payment_OL": get_google_code("PLCXB4HOQEFFCTER"),
        "越南_Pool": get_google_code("MFWQGJAPPN5BRJ4F"),
        "泰国_Pool": get_google_code("XSR5N6RCA57FSQFE"),
        "RDP": get_google_code("Z6U57VOOEAEPN23TBKTCPQ3XKE")
    }
    remaining_seconds = 30
    return render_template('codes.html', codes=codes, remaining_seconds=remaining_seconds)

if __name__ == '__main__':
    app.run(debug=True)