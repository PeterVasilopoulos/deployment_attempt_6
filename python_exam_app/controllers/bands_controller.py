from flask import render_template, request, redirect, session

from python_exam_app.models import users_model, bands_model

from python_exam_app import app

# All bands page
@app.route('/bands')
def bands():
    if not 'uid' in session:
        return redirect('/')
    
    user = users_model.User.get_user_by_id(session['uid'])

    bands = bands_model.Band.get_all_bands_bb()

    return render_template('bands.html', user = user, bands = bands)

# New band page
@app.route('/bands/new')
def new_band():
    if not 'uid' in session:
        return redirect('/')

    user = users_model.User.get_user_by_id(session['uid'])
    
    return render_template('new_band.html', user = user)

# Store new band
@app.route('/bands/store', methods = ['POST'])
def store_band():
    validate = bands_model.Band.validate_band(request.form)

    if validate:
        bands_model.Band.create(request.form)
        return redirect('/bands')
    else:
        return redirect('/bands/new')

# Edit band page
@app.route('/bands/edit/<int:id>')
def edit_band(id):
    if not 'uid' in session:
        return redirect('/')

    user = users_model.User.get_user_by_id(session['uid'])
    
    band = bands_model.Band.get_one_band(id)

    return render_template('edit_band.html', user = user, band = band)

# Store updated band
@app.route('/bands/update', methods = ['POST'])
def update_band():
    validate = bands_model.Band.validate_band(request.form)

    if validate:
        bands_model.Band.update(request.form)
        return redirect('/bands')
    else:
        return redirect(f'/bands/edit/{request.form["band_id"]}')

# My bands page
@app.route('/bands/my_bands')
def my_bands():
    if not 'uid' in session:
        return redirect('/')

    user = users_model.User.get_user_by_id(session['uid'])

    bands_from_user = bands_model.Band.get_bands_from_user(session['uid'])

    joined_bands = users_model.User.get_joined_bands(session['uid'])

    return render_template('my_bands.html', user = user, my_bands = bands_from_user, joined_bands = joined_bands)

# Delete band
@app.route('/bands/delete/<int:id>')
def delete_band(id):
    bands_model.Band.delete(id)

    return redirect('/bands')

# Join band
@app.route('/bands/join/<int:band_id>')
def join_band(band_id):
    bands_model.Band.join_band(band_id, session['uid'])

    return redirect('/bands')

# Quit band
@app.route('/bands/quit/<int:band_id>')
def quit_band(band_id):
    bands_model.Band.quit_band(band_id, session['uid'])

    return redirect('/bands')