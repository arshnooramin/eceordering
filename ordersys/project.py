from flask import *
from ordersys.db import get_db
from flask_login import login_required, current_user
from ordersys.enums import *
from ordersys.auth import admin_required

bp = Blueprint('project', __name__, url_prefix='/project')

def update_cost(project_id, inc_cost):
    db = get_db()

    project = db.execute(
        "SELECT * FROM project WHERE id = ?", (project_id,)
    ).fetchone()
    
    project_total = project['total'] + float(inc_cost)
    db.execute('UPDATE project SET total = ? WHERE id = ?', (project_total, project['id'],))
    db.commit()

@bp.route('/')
@login_required
def index():        
    project_id = current_user.project_id
    db = get_db()
    project = db.execute(
        'SELECT * FROM project WHERE id = ?', (project_id,)
    ).fetchone()
    orders = db.execute(
        'SELECT * FROM eorder o JOIN project p ON p.id = o.project_id WHERE p.id = ? ORDER BY created DESC', (project_id,)
    ).fetchall()

    return render_template('project/index.html', project=project, orders=orders, status_enum=status_enum)

@bp.route('/<int:project_id>')
@login_required
@admin_required
def index_admin(project_id):
    session['prev_project'] = url_for('project.index_admin', project_id = project_id)

    db = get_db()
    project = db.execute(
        'SELECT * FROM project WHERE id = ?', (project_id,)
    ).fetchone()
    orders = db.execute(
        'SELECT * FROM eorder o JOIN project p ON p.id = o.project_id WHERE p.id = ? ORDER BY created DESC', (project_id,)
    ).fetchall()

    return render_template('project/index.html', project=project, orders=orders, status_enum=status_enum)

@bp.route('/delete/<int:project_id>/')
@login_required
@admin_required
def delete_project(project_id):
    db = get_db()
    
    db.execute('DELETE FROM project WHERE id = ?', (project_id,))
    db.commit()
    
    return redirect(url_for('admin.index'))