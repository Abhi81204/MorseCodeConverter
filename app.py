from flask import Flask, render_template, request, jsonify
import pygame
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/translate', methods=['POST'])
def translate():
    user_input = request.json.get('input', '')

    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..'
    }
    morse_code_translation = []

    pygame.mixer.init()

    dot_sound = pygame.mixer.Sound('audio files/dot.wav')
    dash_sound = pygame.mixer.Sound('audio files/dash.wav')

    def play_morse_code(morse_code):
        for symbol in morse_code:
            if symbol == '.':
                dot_sound.play()
                time.sleep(0.4)
            elif symbol == '-':
                dash_sound.play()
                time.sleep(0.4)
            else:
                pass

    for char in user_input:
        if char == ' ':
            morse_code_translation.append('/')
        else:
            char = char.upper()
            code = morse_code_dict.get(char, ' ')
            if code:
                morse_code_translation.append(code)

    morse_output = '  '.join(morse_code_translation)


    for letter_code in morse_code_translation:
        if letter_code == '/':
            time.sleep(0.8)
        else:
            play_morse_code(letter_code)
            time.sleep(0.4)

    dot_sound.stop()
    dash_sound.stop()

    return jsonify({'output': morse_output})

if __name__ == '__main__':
    app.run(debug=True)
