import network
import machine
import time
import dht
import ujson
import urequests as requests

# Konfigurasi WiFi
SSID = "azza"
PASSWORD = "malang123"

# Inisialisasi WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

if not wifi.isconnected():
    print(f"Menghubungkan ke WiFi {SSID}...")
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(1)

print("Terhubung ke WiFi!", wifi.ifconfig())

# URL tujuan untuk mengirim data
API_URL = "https://czv5tl6x-3000.asse.devtunnels.ms/sensor"

# Inisialisasi Sensor
sensor_pin = machine.Pin(23, machine.Pin.IN)  # Sensor Ultrasonik pada D23
pir_sensor = machine.Pin(2, machine.Pin.IN)   # Sensor PIR pada D2
dht_sensor = dht.DHT11(machine.Pin(22))       # Sensor DHT11 pada D22

time.sleep(2)  # Beri waktu sensor DHT untuk inisialisasi

while True:
    try:
        # Membaca status sensor ultrasonik (D23)
        ultrasonic_status = sensor_pin.value()
        print(f"Sensor D23 (Ultrasonic): {'0' if ultrasonic_status else '1'}")

        # Membaca status PIR (D2)
        pir_status = pir_sensor.value()
        print(f"PIR Sensor: {'Gerakan Terdeteksi!' if pir_status else 'Tidak Ada Gerakan'}")

        # Membaca suhu dan kelembaban dari DHT11
        dht_sensor.measure()
        suhu = dht_sensor.temperature()
        kelembaban = dht_sensor.humidity()
        print(f"Suhu: {suhu}°C, Kelembaban: {kelembaban}%")

        # Menyiapkan data dalam format JSON
        data = {
            "ultrasonic": 1 if not ultrasonic_status else 0,
            "pir": 1 if pir_status else 0,
            "temperature": suhu,
            "humidity": kelembaban
        }

        # Mengirim data ke server
        response = requests.post(API_URL, json=data)
        print("Response:", response.text)

    except Exception as e:
        print("Error:", e)

    time.sleep(10)  # Tunggu sebelum pengukuran berikutnya
