from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)

# In-memory storage for multiple warehouses
varastot = {}
next_id = 1


@app.route('/')
def index():
    """List all storages."""
    return render_template('index.html', varastot=varastot)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new storage."""
    global next_id
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            alku_saldo = float(request.form.get('alku_saldo', 0))
        except ValueError:
            return render_template('create.html', error='Invalid numeric values')

        if not name:
            return render_template('create.html', error='Name is required')

        if tilavuus <= 0:
            return render_template('create.html', error='Capacity must be positive')

        varasto = Varasto(tilavuus, alku_saldo)
        varastot[next_id] = {'name': name, 'varasto': varasto}
        next_id += 1
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/view/<int:varasto_id>')
def view(varasto_id):
    """View a specific storage."""
    if varasto_id not in varastot:
        return redirect(url_for('index'))
    data = varastot[varasto_id]
    return render_template('view.html', varasto_id=varasto_id, name=data['name'],
                           varasto=data['varasto'])


@app.route('/add/<int:varasto_id>', methods=['POST'])
def add(varasto_id):
    """Add contents to a storage."""
    if varasto_id not in varastot:
        return redirect(url_for('index'))
    try:
        maara = float(request.form.get('maara', 0))
    except ValueError:
        return redirect(url_for('view', varasto_id=varasto_id))

    # Validate that amount is positive
    if maara <= 0:
        return redirect(url_for('view', varasto_id=varasto_id))

    varastot[varasto_id]['varasto'].lisaa_varastoon(maara)
    return redirect(url_for('view', varasto_id=varasto_id))


@app.route('/remove/<int:varasto_id>', methods=['POST'])
def remove(varasto_id):
    """Remove contents from a storage."""
    if varasto_id not in varastot:
        return redirect(url_for('index'))
    try:
        maara = float(request.form.get('maara', 0))
    except ValueError:
        return redirect(url_for('view', varasto_id=varasto_id))

    # Validate that amount is positive
    if maara <= 0:
        return redirect(url_for('view', varasto_id=varasto_id))

    varastot[varasto_id]['varasto'].ota_varastosta(maara)
    return redirect(url_for('view', varasto_id=varasto_id))


@app.route('/delete/<int:varasto_id>', methods=['POST'])
def delete(varasto_id):
    """Delete a storage."""
    if varasto_id in varastot:
        del varastot[varasto_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
