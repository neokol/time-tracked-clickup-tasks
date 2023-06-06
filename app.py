from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
from flask import session
import csv
import io
import task_service

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Save data from POST request
        list_id = request.form.get('list_id')
        year = int(request.form.get('year'))
        month = int(request.form.get('month'))
        day = int(request.form.get('day'))
        #Check if user have import a list
        if not list_id:
            render_template(
                'form.html', error_message="List ID cannot be empty")

        data_rows, header, error_message = task_service.process_task_data(
            year, month, day, list_id)

        if error_message:
            return render_template('form.html', error_message=error_message)

        # Save all data to session so they can be printed in the frontend and use them to create csv file
        session['data'] = data_rows

        return render_template('index.html', header=header, data_rows=data_rows)
    return render_template('form.html')


@app.route('/download', methods=['POST'])
def download():
    # get data from session
    data = session.get('data', None)
    if data is None:
        # redirect to home page if no data given
        return redirect(url_for('home'))

    header = ['ID', 'Name', 'Invoice Description', 'Status',
              'Date Created', 'Date Closed', 'Time Logged', 'Time in hours']

    # Create the csv file
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(header)
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == '__main__':
    app.run(debug=True)
