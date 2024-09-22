from flask import Flask, jsonify, render_template
import adafruit_dht
import board
import time
import drivers
from time import sleep


sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)
display = drivers.Lcd()

app = Flask(__name__)

def read_dht():
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        print("Temperature in *C: {:.1f}C, Humidity: {:.1f}%".format(temperature, humidity))
        if humidity is not None and temperature is not None:
            return temperature, humidity
        else:
            return None, None
    except RuntimeError as error:
        print(error)
        time.sleep(2)
        return None, None
def diplay_data_lcd(temp, humd):
        display.lcd_clear()
        display.lcd_display_string("Temperature : {:.1f}%".format(temp), 1)  # Write line of text to first line of display
        display.lcd_display_string("Humidity : {:.1f}%".format(humd), 2)  # Write line of text to second line of display
        
@app.route('/')
def index():
    temperature, humidity = read_dht()                                  
    return render_template('index.html', temperature=temperature, humidity=humidity)

@app.route('/data')
def data():
    temperature, humidity = read_dht()
    diplay_data_lcd(temperature, humidity)
    print("Temperature in *C: {:.1f}*C, Humidity: {:.1f}%".format(temperature, humidity))
    return jsonify(temperature=temperature, humidity=humidity)

if __name__ == "__main__":
    try:
        display.lcd_clear()
        # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        app.run(host='0.0.0.0', port=8080)
    finally:
        sensor.exit()
