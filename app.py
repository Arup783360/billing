from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)
items = []  # List to hold invoice entries
next_id = 1  # Unique ID for each entry

@app.route('/', methods=['GET', 'POST'])
def index():
    global next_id
    if request.method == 'POST':
        # Get form data
        item_id = request.form.get('item_id')
        model = request.form['model']
        quantity = request.form['quantity']

        # Check if we are updating an existing item
        if item_id:
            for item in items:
                if item['ID'] == int(item_id):
                    item['Mobile Model'] = model
                    item['Quantity'] = quantity
                    break
        else:
            # Add new entry
            items.append({'ID': next_id, 'SL Number': len(items) + 1, 'Mobile Model': model, 'Quantity': quantity})
            next_id += 1

    return render_template('index.html', items=items)

@app.route('/edit/<int:item_id>', methods=['GET'])
def edit(item_id):
    # Find the item to edit
    item = next((item for item in items if item['ID'] == item_id), None)
    if item:
        return render_template('index.html', items=items, item_to_edit=item)
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    global items
    # Remove the item with the specified ID
    items = [item for item in items if item['ID'] != item_id]

    # Update SL Numbers
    for i, item in enumerate(items):
        item['SL Number'] = i + 1

    return redirect(url_for('index'))

@app.route('/export', methods=['GET'])
def export():
    # Convert list to DataFrame
    df = pd.DataFrame(items)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Invoice')

    # Prepare file download response
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='invoice.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
