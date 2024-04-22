
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/tainted7/<something>')
def test_sources_7(something):
    # Insecure use of os.system with potentially untrusted input addressed
    # Securely log or other actions can be taken here with the remote address
    remote_addr = request.remote_addr
    # Example: Log the remote address
    print(f"Remote address: {remote_addr}")
    
    return 'foo'

if __name__ == '__main__':
    app.run(debug=True)
