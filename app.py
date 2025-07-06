from flask import *
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import zipfile
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

# Folder setup
GENERATED_FOLDER = 'static/generated'
FONTS_FOLDER = 'static/fonts'
os.makedirs(GENERATED_FOLDER, exist_ok=True)

VALID_PASSWORD = "kuce&t"

def get_font_path(font_name):
    """Get the full path to a font file"""
    return os.path.join(FONTS_FOLDER, font_name)

def add_text_to_image(image, text, position, font_size=36, font_name="DancingScript-Regular.ttf", color=(0, 0, 0)):
    """Add text to an image at specified position with center alignment"""
    try:
        # Create a drawing object
        draw = ImageDraw.Draw(image)
        
        # Try to load the specified font, fallback to default if not found
        font = None
        font_path = get_font_path(font_name)
        
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
            except Exception as e:
                print(f"Error loading font {font_name}: {e}")
                font = ImageFont.load_default()
        else:
            print(f"Font file not found: {font_path}")
            font = ImageFont.load_default()
        
        # Get text bounding box to center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text at the given position
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        
        # Add text to image
        draw.text((x, y), text, font=font, fill=color)
        return image
    except Exception as e:
        print(f"Error adding text: {e}")
        return image

def calculate_text_position(template_width, template_height, field_type, field_index=0, layout_config=None):
    """Calculate optimal text position based on field type and template dimensions"""
    
    # Define relative positions (as percentages of template dimensions)
    positions = {
        'name': {
            'x': 0.5,  # 50% of width (center)
            'y': 0.45  # 45% of height (slightly above center)
        },
        'event': {
            'x': 0.5,
            'y': 0.55  # 55% of height (slightly below center)
        },
        'course': {
            'x': 0.5,
            'y': 0.65  # 65% of height
        },
        'date': {
            'x': 0.5,
            'y': 0.75  # 75% of height
        },
        'instructor': {
            'x': 0.5,
            'y': 0.85  # 85% of height
        },
        'organization': {
            'x': 0.5,
            'y': 0.92  # 92% of height
        },
        'duration': {
            'x': 0.5,
            'y': 0.95  # 95% of height
        },
        'top': {
            'x': 0.5,
            'y': 0.2  # 20% of height (top area)
        },
        'center': {
            'x': 0.5,
            'y': 0.5  # 50% of height (exact center)
        },
        'bottom': {
            'x': 0.5,
            'y': 0.8  # 80% of height (bottom area)
        },
        'default': {
            'x': 0.5,
            'y': 0.5 + (field_index * 0.08)  # Stack vertically with spacing
        }
    }
    
    # Check if custom layout is specified
    if layout_config and field_type in layout_config:
        custom_position = layout_config[field_type]
        if custom_position in positions:
            pos = positions[custom_position]
        else:
            pos = positions.get(field_type, positions['default'])
    else:
        pos = positions.get(field_type, positions['default'])
    
    # Convert percentages to actual pixel coordinates
    x = int(template_width * pos['x'])
    y = int(template_height * pos['y'])
    
    return (x, y)

def get_field_type(column_name):
    """Determine field type based on column name"""
    column_lower = column_name.lower()
    
    if any(word in column_lower for word in ['name', 'full_name', 'participant', 'student', 'attendee']):
        return 'name'
    elif any(word in column_lower for word in ['event', 'program', 'workshop', 'seminar', 'conference']):
        return 'event'
    elif any(word in column_lower for word in ['course', 'training', 'certification', 'module', 'class']):
        return 'course'
    elif any(word in column_lower for word in ['date', 'completion_date', 'issued_date', 'graduation_date']):
        return 'date'
    elif any(word in column_lower for word in ['instructor', 'trainer', 'teacher', 'facilitator', 'presenter']):
        return 'instructor'
    elif any(word in column_lower for word in ['organization', 'company', 'institution', 'school', 'university']):
        return 'organization'
    elif any(word in column_lower for word in ['duration', 'hours', 'credits', 'length']):
        return 'duration'
    else:
        return 'default'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/verify_password', methods=['POST'])
def verify_password():
    password = request.form.get('password')
    if password == VALID_PASSWORD:
        return redirect(url_for('index'))
    else:
        flash('Invalid password! Try again.', 'error')
        return redirect(url_for('home'))

@app.route('/index')
def index():
    # Check if there's existing certificate session to restore form data
    form_data = None
    if 'certificate_session' in session:
        form_data = session['certificate_session'].get('form_data')
        print(f"DEBUG: Form data found in index: {form_data}")
    
    return render_template('index.html', form_data=form_data)

@app.route('/back_to_generate')
def back_to_generate():
    """Go back to generate page with preserved form data"""
    if 'certificate_session' not in session:
        return redirect(url_for('index'))
    
    # Keep the session data for form restoration but don't clean up files yet
    form_data = session['certificate_session'].get('form_data')
    print(f"DEBUG: Form data being restored: {form_data}")
    
    return render_template('index.html', form_data=form_data)

@app.route('/clear_session')
def clear_session():
    """Clear session data and start fresh"""
    if 'certificate_session' in session:
        session_id = session['certificate_session']['session_id']
        session_folder = os.path.join(GENERATED_FOLDER, session_id)
        if os.path.exists(session_folder):
            import shutil
            try:
                shutil.rmtree(session_folder)
            except Exception as e:
                print(f"Error cleaning up session folder: {e}")
        session.pop('certificate_session', None)
    
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate_certificates():
    # Check if we have existing form data and no new files uploaded
    existing_form_data = None
    if 'certificate_session' in session:
        existing_form_data = session['certificate_session'].get('form_data')
    
    # Check if new files are uploaded
    new_template = 'template' in request.files and request.files['template'].filename
    new_data_file = 'data_file' in request.files and request.files['data_file'].filename
    
    if not new_template and not new_data_file and existing_form_data:
        # Use existing files from previous session
        session_id = session['certificate_session']['session_id']
        session_folder = os.path.join(GENERATED_FOLDER, session_id)
        
        template_path = os.path.join(session_folder, existing_form_data['template_filename'])
        data_path = os.path.join(session_folder, existing_form_data['data_filename'])
        
        if not os.path.exists(template_path) or not os.path.exists(data_path):
            flash('Previous files not found. Please upload files again.', 'error')
            return redirect(url_for('index'))
        
        # Create file objects from existing files
        from werkzeug.datastructures import FileStorage
        template_file = FileStorage(open(template_path, 'rb'), filename=existing_form_data['template_filename'])
        data_file = FileStorage(open(data_path, 'rb'), filename=existing_form_data['data_filename'])
    else:
        # Use new uploaded files
        if 'data_file' not in request.files or 'template' not in request.files:
            return "Missing data file or template", 400
        data_file = request.files['data_file']
        template_file = request.files['template']

    font_name = request.form.get('font', 'DancingScript-Regular.ttf')
    font_size = int(request.form.get('fontsize', 36))
    
    # Get layout configuration
    layout_config = {}
    if request.form.get('name_position'):
        layout_config['name'] = request.form.get('name_position')
    if request.form.get('event_position'):
        layout_config['event'] = request.form.get('event_position')
    if request.form.get('date_position'):
        layout_config['date'] = request.form.get('date_position')
    if request.form.get('course_position'):
        layout_config['course'] = request.form.get('course_position')
    
    try:
        # Read the data file
        file_extension = os.path.splitext(data_file.filename)[1].lower()
        if file_extension == '.csv':
            df = pd.read_csv(data_file)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(data_file)
        else:
            return "Unsupported file format. Please upload a CSV or Excel file.", 400

        # Load the template image
        template = Image.open(template_file)
        template_width, template_height = template.size

        # Load saved layout configuration
        saved_layout = {}
        layout_file_path = 'static/uploads/layout.json'
        if os.path.exists(layout_file_path):
            try:
                with open(layout_file_path, 'r') as f:
                    saved_layout = json.load(f)
            except Exception as e:
                print(f"Error loading layout file: {e}")
                saved_layout = {}

        # Generate unique session ID for this batch
        session_id = str(uuid.uuid4())
        session_folder = os.path.join(GENERATED_FOLDER, session_id)
        os.makedirs(session_folder, exist_ok=True)

        # Save template and data files for reuse
        template_filename = f"template_{session_id}.jpg"
        data_filename = f"data_{session_id}{file_extension}"
        
        template_path = os.path.join(session_folder, template_filename)
        data_path = os.path.join(session_folder, data_filename)
        
        template_file.save(template_path)
        data_file.save(data_path)

        # Create certificates
        certificate_files = []
        for idx, row in df.iterrows():
            cert_name = f"certificate_{idx + 1}.jpg"
            cert_path = os.path.join(session_folder, cert_name)
            cert_image = template.copy()
            
            # Only add text for fields that are in the saved layout
            for field_name, position in saved_layout.items():
                if field_name in row:
                    text_value = str(row[field_name])
                    # Convert canvas coordinates to image coordinates
                    x = int(position[0] * template_width / 1000)  # canvas width is 1000
                    y = int(position[1] * template_height / 700)  # canvas height is 700
                    
                    cert_image = add_text_to_image(
                        cert_image, 
                        text_value, 
                        (x, y), 
                        font_size, 
                        font_name
                    )
            
            cert_image.save(cert_path, quality=95)
            certificate_files.append(cert_name)

        # Store session info for preview and download
        session['certificate_session'] = {
            'session_id': session_id,
            'total_certificates': len(df),
            'certificate_files': certificate_files,
            'form_data': {
                'font_name': font_name,
                'font_size': font_size,
                'layout_config': layout_config,
                'template_filename': template_filename,
                'data_filename': data_filename,
                'file_extension': file_extension
            }
        }
        
        print(f"DEBUG: Form data being saved: {session['certificate_session']['form_data']}")

        return redirect(url_for('preview_certificates'))

    except Exception as e:
        return f"Error generating certificates: {str(e)}", 500

@app.route('/preview')
def preview_certificates():
    if 'certificate_session' not in session:
        flash('No certificates to preview. Please generate certificates first.', 'error')
        return redirect(url_for('index'))
    
    session_data = session['certificate_session']
    session_id = session_data['session_id']
    certificate_files = session_data['certificate_files']
    
    return render_template('preview.html', 
                         session_id=session_id, 
                         certificate_files=certificate_files,
                         total_certificates=session_data['total_certificates'])

@app.route('/download')
def download_certificates():
    if 'certificate_session' not in session:
        flash('No certificates to download. Please generate certificates first.', 'error')
        return redirect(url_for('index'))
    
    session_id = session['certificate_session']['session_id']
    session_folder = os.path.join(GENERATED_FOLDER, session_id)
    
    if not os.path.exists(session_folder):
        flash('Certificate files not found. Please generate certificates again.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Create zip file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(session_folder):
                file_path = os.path.join(session_folder, filename)
                # Only include generated certificate images (e.g., certificate_1.jpg)
                if os.path.isfile(file_path) and filename.startswith('certificate_') and filename.lower().endswith('.jpg'):
                    zipf.write(file_path, arcname=filename)
        
        zip_buffer.seek(0)
        
        # Clean up session folder after download
        import shutil
        shutil.rmtree(session_folder)
        
        # Clear session data
        session.pop('certificate_session', None)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='certificates.zip'
        )
        
    except Exception as e:
        return f"Error downloading certificates: {str(e)}", 500

@app.route('/static/generated/<session_id>/<filename>')
def serve_certificate(session_id, filename):
    """Serve individual certificate images for preview"""
    file_path = os.path.join(GENERATED_FOLDER, session_id, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Certificate not found", 404

@app.route('/save_layout', methods=['POST'])
def save_layout():
    """Save layout configuration from the position editor"""
    try:
        layout_data = request.get_json()
        # Save layout to a JSON file
        with open('static/uploads/layout.json', 'w') as f:
            json.dump(layout_data, f, indent=2)
        return jsonify({"status": "success", "message": "Layout saved successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask app running at: http://127.0.0.1:5000/")
    print("📎 Try these URLs in your browser:")
    print("  • Home page:            http://127.0.0.1:5000/")
    app.run(debug=True)
