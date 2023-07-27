from flask import Flask, render_template, request

app = Flask(__name__)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None

def encrypt(message, e, n):
    return [pow(ord(char), e, n) for char in message]

def decrypt(ciphertext, d, n):
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        p = int(request.form['p'])
        q = int(request.form['q'])
        e = int(request.form['e'])
        message = request.form['message']

        n = p * q
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) == 1:
            d = mod_inverse(e, phi)
            if d:
                encrypted_message = encrypt(message, e, n)
                decrypted_message = decrypt(encrypted_message, d, n)
                return render_template('index.html', encrypted_message=encrypted_message, decrypted_message=decrypted_message)
        
        return "Invalid input. Make sure 'p' and 'q' are prime numbers, and 'e' is coprime with (p-1)*(q-1)."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
