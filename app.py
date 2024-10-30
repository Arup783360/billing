from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

# Global list to store billing items
billing_items = []

@app.route('/')
def index():
    return render_template('index.html', billing_items=billing_items)

@app.route('/add_item', methods=['POST'])
def add_item():
    model = request.form.get('model')
    quantity = request.form.get('quantity')
    # Append item to the global list with serial number
    serial_number = len(billing_items) + 1  # Calculate the serial number
    billing_items.append({'serial_number': serial_number, 'model': model, 'quantity': quantity})
    return '', 204  # No content response

@app.route('/edit_item', methods=['POST'])
def edit_item():
    serial_number = int(request.form.get('serial_number')) - 1  # Convert to index
    model = request.form.get('model')
    quantity = request.form.get('quantity')
    
    if 0 <= serial_number < len(billing_items):
        billing_items[serial_number] = {'serial_number': serial_number + 1, 'model': model, 'quantity': quantity}
    return '', 204  # No content response

@app.route('/delete_item', methods=['POST'])
def delete_item():
    serial_number = int(request.form.get('serial_number')) - 1  # Convert to index
    
    if 0 <= serial_number < len(billing_items):
        billing_items.pop(serial_number)
        # Update serial numbers
        for i, item in enumerate(billing_items):
            item['serial_number'] = i + 1
    return '', 204  # No content response

@app.route('/clear_items', methods=['POST'])
def clear_items():
    global billing_items
    billing_items = []  # Clear all items
    return '', 204  # No content response

@app.route('/export', methods=['GET'])
def export_to_excel():
    # Create a DataFrame from the billing items
    df = pd.DataFrame(billing_items)
    # Create a BytesIO buffer to save the Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Billing Items')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='billing_items.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
