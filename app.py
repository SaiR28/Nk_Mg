from flask import Flask, request, jsonify, render_template,send_file
import csv

app = Flask(__name__)

# Create a CSV file for storing data
csv_file_path = 'received_data.csv'
csv_header = ['IST', 'espId', 'Temperature', 'Humidity', 'Luminosity', 'Seed_Studio_pH', 'DFRobot_pH', 'Light', 'Fan', 'Pump'] + [f'Heat_Matrix_{i+1}' for i in range(64)]

@app.route('/api/endpoint', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()

        # Process the received data as needed
        ist = data.get('IST', 'N/A')
        esp_id = data.get('espId', 'Unknown')
        temperature = data.get('bme', 'N/A')
        humidity = data.get('humidity', 'N/A')
        luminosity = data.get('luminosity', 'N/A')
        seed_ph = data.get('seedStudioPh', 'N/A')
        df_ph = data.get('dfrobotPh', 'N/A')
        light_status = data.get('light', 'Off')
        fan_status = data.get('fan', 'Off')
        pump_status = data.get('pump', 'Off')
        heat_matrix = data.get('heatMatrix', [])

        # Print or process the received data as needed
        print(f"Received data at {ist} from ESP ID {esp_id}")
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
        print(f"Luminosity: {luminosity}, Seed Studio pH: {seed_ph}, DFRobot pH: {df_ph}")
        print(f"Light: {light_status}, Fan: {fan_status}, Pump: {pump_status}")
        print(f"Heat Matrix: {heat_matrix}")

        # Save the received data to CSV file
        with open(csv_file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:  # Write header if the file is empty
                writer.writerow(csv_header)
            writer.writerow([ist, esp_id, temperature, humidity, luminosity, seed_ph, df_ph, light_status, fan_status, pump_status] + heat_matrix)

        return jsonify({"message": "Data received and saved successfully"}), 200
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"error": "Failed to process data"}), 500

@app.route('/view-data')
def view_data():
    # Pass the data to the HTML template
    # Update the heat_matrix variable with actual values
    return render_template('index.html', ist='IST Value', esp_id='ESP ID Value', temperature='Temperature Value', humidity='Humidity Value', luminosity='Luminosity Value', seed_ph='Seed Studio pH Value', df_ph='DFRobot pH Value', light_status='Light Status Value', fan_status='Fan Status Value', pump_status='Pump Status Value', heat_matrix=['Value 1', 'Value 2', ..., 'Value 64'])

@app.route('/download-csv')
def download_csv():
    return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
