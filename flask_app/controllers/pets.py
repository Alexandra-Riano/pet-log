from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.pet import Pet
from flask_app.models.user import User


@app.route('/dashboard')
def dashboard():
    # check if user is logged in
    if 'user_id' not in session:
        return redirect('/user/login')

    # get user object by id from the session
    user = User.get_by_id({"id": session['user_id']})

    # if user object is not found, log them out
    if not user:
        return redirect('/user/logout')
    return render_template('dashboard.html', user=user, pets=Pet.get_all())


@app.route('/pets/new')
def create_pet():
    # check if user is logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('pet_new.html')


@app.route('/pets/new/process', methods=['POST'])
def process_pet():
    # check if user is logged in
    if 'user_id' not in session:
        return redirect('/user/login')

    # validate the pet data, redirect to the form if it's not valid
    if not Pet.validate_pet(request.form):
        return redirect('/pets/new')

    # save the pet data to the database and redirect to the dashboard
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'food': request.form['food'],
        'notes': request.form['notes'],
        'date': request.form['date'],
        'potty': request.form['potty'],
    }
    Pet.save(data)
    return redirect('/dashboard')


@app.route('/pets/<int:id>')
def view_pet(id):
    # check if user is logged in
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('pet_view.html', pet=Pet.get_by_id({'id': id}))


@app.route('/pets/edit/<int:id>')
def edit_pet(id):
    # check if user is logged in
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('pet_edit.html', pet=Pet.get_by_id({'id': id}))


@app.route('/pets/edit/process/<int:id>', methods=['POST'])
def process_edit_pet(id):
    # check if user is logged in
    if 'user_id' not in session:
        return redirect('/user/login')

    # validate the edited pet data, redirect to the form if it's not valid
    if not Pet.validate_pet(request.form):
        return redirect(f'/pets/edit/{id}')

    # update the pet data in the database and redirect to the dashboard
    data = {
        'id': id,
        'name': request.form['name'],
        'food': request.form['food'],
        'notes': request.form['notes'],
        'date': request.form['date'],
        'potty': request.form['potty'],
    }
    Pet.update(data)
    return redirect('/dashboard')


@app.route('/pets/destroy/<int:id>')
def destroy_pet(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Pet.destroy({'id': id})
    return redirect('/dashboard')
