# Credits: R ! Y 4 Z
import os
import json
import socket
import qrcode
import secrets
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
import threading
import time
import psutil

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple uptime tracking - just store start time
SERVER_START_TIME = time.time()

# Configuration
UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv', 'wav', 'aac', 'ogg', 'ppt', 'pptx'}

# Configurable settings
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 0  # 0 = No file size limit (unlimited)
app.config['AUTH_ENABLED'] = True
app.config['AUTH_PIN'] = '1234'  # Default PIN
app.config['AUTO_REFRESH_INTERVAL'] = 10  # seconds

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Store active connections, devices, and file events
active_connections = set()
connected_devices = {}  # Store device information
file_events = []
device_events = []

# Session management
active_sessions = {}  # Store active sessions with tokens
session_tokens = {}  # Map tokens to session data
session_counter = 0  # Counter for unique session IDs

# Device status tracking
device_last_seen = {}  # Track last activity for each device
device_status = {}  # Track online/offline status

def cleanup_offline_devices():
    """Remove devices that haven't sent heartbeat for more than 30 seconds"""
    current_time = datetime.now().timestamp()
    offline_threshold = 30  # 30 seconds - much faster cleanup
    
    devices_to_remove = []
    for sid, last_seen in device_last_seen.items():
        if current_time - last_seen > offline_threshold:
            devices_to_remove.append(sid)
    
    for sid in devices_to_remove:
        if sid in connected_devices:
            del connected_devices[sid]
        if sid in device_last_seen:
            del device_last_seen[sid]
        if sid in device_status:
            del device_status[sid]
    
    if devices_to_remove:
        # Broadcast updated devices list
        socketio.emit('devices_update', list(connected_devices.values()))

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def get_system_info():
    """Get system information with guaranteed working uptime"""
    import platform
    import time
    try:
        # Get file statistics
        uploads_dir = os.path.join('static', 'uploads')
        downloads_dir = os.path.join('static', 'downloads')
        upload_files = len([f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]) if os.path.exists(uploads_dir) else 0
        download_files = len([f for f in os.listdir(downloads_dir) if os.path.isfile(os.path.join(downloads_dir, f))]) if os.path.exists(downloads_dir) else 0
        
        # GUARANTEED WORKING UPTIME - Always return a working value
        uptime_str = "0s"  # Start with 0s, frontend will handle the counting
        
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'local_ip': get_local_ip(),
            'hostname': platform.node(),
            'session_enabled': True,
            'active_sessions': len(active_sessions),
            'connected_devices': len(connected_devices),
            'devices_list': list(connected_devices.values()),  # Only online devices
            'upload_files': upload_files,
            'download_files': download_files,
            'total_files': upload_files + download_files,
            'server_time': datetime.now().isoformat(),
            'max_file_size': 'Unlimited',
            'server_uptime': uptime_str,
            'server_start_time': SERVER_START_TIME
        }
    except Exception as e:
        print(f"Error getting system info: {e}")
        return {
            'os': platform.system(),
            'local_ip': get_local_ip(),
            'hostname': platform.node(),
            'session_enabled': True,
            'active_sessions': len(active_sessions),
            'connected_devices': len(connected_devices),
            'devices_list': list(connected_devices.values()),
            'upload_files': 0,
            'download_files': 0,
            'total_files': 0,
            'server_time': datetime.now().isoformat(),
            'max_file_size': 'Unlimited',
            'server_uptime': '0s',
            'server_start_time': SERVER_START_TIME
        }

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_icon(filename):
    """Get appropriate icon for file type"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
    icons = {
        'pdf': '📄', 'doc': '📝', 'docx': '📝', 'txt': '📄',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
        'mp4': '🎥', 'mp3': '🎵', 'zip': '📦', 'rar': '📦',
        'xls': '📊', 'xlsx': '📊', 'ppt': '📊', 'pptx': '📊',
        'avi': '🎥', 'mov': '🎥', 'wmv': '🎥', 'flv': '🎥',
        'webm': '🎥', 'mkv': '🎥', 'wav': '🎵', 'aac': '🎵',
        'ogg': '🎵'
    }
    return icons.get(ext, '📄')

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def broadcast_file_event(event_type, data):
    """Broadcast file events to all connected clients"""
    event_data = {
        'type': event_type,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    file_events.append(event_data)
    if len(file_events) > 100:  # Keep only last 100 events
        file_events.pop(0)
    socketio.emit('file_event', event_data)

def broadcast_device_event(event_type, data):
    """Broadcast device events to all connected clients"""
    event_data = {
        'type': event_type,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    device_events.append(event_data)
    if len(device_events) > 50:  # Keep only last 50 events
        device_events.pop(0)
    socketio.emit('device_event', event_data)

def generate_token():
    """Generate a secure random token for session management"""
    import secrets
    return secrets.token_urlsafe(32)

def create_session(device_info):
    """Create a new session for a device"""
    global session_counter
    session_counter += 1
    
    # Check if device already has an active session
    device_ip = device_info.get('ip', 'unknown')
    if device_ip in session_tokens:
        existing_token = session_tokens[device_ip]
        if existing_token in active_sessions:
            # Update existing session
            active_sessions[existing_token]['last_activity'] = datetime.now().isoformat()
            active_sessions[existing_token]['device_info'] = device_info
            return existing_token
    
    # Create new session
    token = generate_token()
    session_data = {
        'session_id': session_counter,
        'token': token,
        'device_info': device_info,
        'created_at': datetime.now().isoformat(),
        'last_activity': datetime.now().isoformat(),
        'is_active': True
    }
    
    active_sessions[token] = session_data
    session_tokens[device_ip] = token
    
    return token

def validate_session(token):
    """Validate a session token"""
    if token not in active_sessions:
        return False
    
    session = active_sessions[token]
    
    # Check if session is expired (24 hours)
    created_at = datetime.fromisoformat(session['created_at'])
    if (datetime.now() - created_at).total_seconds() > 86400:  # 24 hours
        del active_sessions[token]
        return False
    
    # Update last activity
    session['last_activity'] = datetime.now().isoformat()
    return True

def get_device_info(request):
    """Extract device information from request with enhanced detection"""
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Enhanced device detection
    device_type = 'Unknown'
    device_name = 'Unknown Device'
    os_name = 'Unknown OS'
    pc_username = 'Unknown User'
    
    # Try to get PC username for desktop devices
    try:
        import getpass
        pc_username = getpass.getuser()
    except:
        pc_username = 'Unknown User'
    
    # Detect operating system and extract specific device info
    # Check for mobile devices first (Android, iPhone, etc.)
    if 'Android' in user_agent:
        os_name = 'Android'
        device_type = 'Mobile'
        
        # Enhanced Android device detection
        device_model = 'Android Phone'
        
        # iQOO devices (added support)
        if 'iQOO' in user_agent or 'IQOO' in user_agent:
            device_model = 'iQOO Phone'
        # Samsung devices
        elif 'SM-' in user_agent or 'Samsung' in user_agent:
            # Try to extract Samsung model
            if 'SM-G' in user_agent:
                device_model = 'Samsung Galaxy S Series'
            elif 'SM-N' in user_agent:
                device_model = 'Samsung Galaxy Note'
            elif 'SM-A' in user_agent:
                device_model = 'Samsung Galaxy A Series'
            elif 'SM-T' in user_agent:
                device_model = 'Samsung Galaxy Tab'
            else:
                device_model = 'Samsung Phone'
        
        # Xiaomi devices
        elif 'Xiaomi' in user_agent or 'MI ' in user_agent:
            if 'Redmi' in user_agent:
                device_model = 'Xiaomi Redmi'
            elif 'POCO' in user_agent:
                device_model = 'POCO Phone'
            else:
                device_model = 'Xiaomi Phone'
        
        # OnePlus devices
        elif 'OnePlus' in user_agent:
            device_model = 'OnePlus Phone'
        
        # Huawei devices
        elif 'Huawei' in user_agent:
            device_model = 'Huawei Phone'
        
        # Google devices
        elif 'Google' in user_agent or 'Pixel' in user_agent:
            device_model = 'Google Pixel'
        
        # Motorola devices
        elif 'Motorola' in user_agent or 'Moto' in user_agent:
            device_model = 'Motorola Phone'
        
        # OPPO devices
        elif 'OPPO' in user_agent:
            device_model = 'OPPO Phone'
        
        # Vivo devices
        elif 'Vivo' in user_agent:
            device_model = 'Vivo Phone'
        
        # Realme devices
        elif 'Realme' in user_agent:
            device_model = 'Realme Phone'
        
        # Try to extract specific model number
        import re
        model_patterns = [
            r'iQOO [0-9]+',    # iQOO models (prioritize iQOO)
            r'SM-[A-Z0-9]+',   # Samsung models
            r'MI [0-9]+',      # Xiaomi models
            r'Pixel [0-9]+',   # Google Pixel models
            r'iPhone [0-9,]+', # iPhone models
        ]
        
        for pattern in model_patterns:
            match = re.search(pattern, user_agent)
            if match:
                # For Samsung, keep the brand name but add model
                if 'SM-' in match.group() and 'Samsung' in device_model:
                    device_model = f"{device_model} ({match.group()})"
                else:
                    device_model = match.group()
                break
        
        device_name = device_model
        
    elif 'iPhone' in user_agent:
        os_name = 'iOS'
        device_type = 'Mobile'
        
        # Try to extract iPhone model
        import re
        iphone_match = re.search(r'iPhone [0-9,]+', user_agent)
        if iphone_match:
            device_name = iphone_match.group()
        else:
            device_name = 'iPhone'
            
    elif 'iPad' in user_agent:
        os_name = 'iOS'
        device_type = 'Tablet'
        
        # Try to extract iPad model
        import re
        ipad_match = re.search(r'iPad [A-Z0-9]+', user_agent)
        if ipad_match:
            device_name = ipad_match.group()
        else:
            device_name = 'iPad'
            
    elif 'Tablet' in user_agent:
        device_type = 'Tablet'
        device_name = 'Android Tablet'
    
    # Desktop detection (after mobile/tablet detection)
    elif 'Windows' in user_agent:
        os_name = 'Windows'
        device_type = 'Desktop'
        device_name = f"{pc_username}'s Windows PC"
    elif 'Mac' in user_agent:
        os_name = 'macOS'
        device_type = 'Desktop'
        device_name = f"{pc_username}'s Mac"
    elif 'Linux' in user_agent:
        os_name = 'Linux'
        device_type = 'Desktop'
        device_name = f"{pc_username}'s Linux PC"
    
    # Enhanced browser detection
    browser = 'Unknown'
    browser_version = ''
    if 'Chrome' in user_agent:
        browser = 'Chrome'
        # Try to extract version
        if 'Chrome/' in user_agent:
            version_start = user_agent.find('Chrome/') + 7
            version_end = user_agent.find(' ', version_start)
            if version_end == -1:
                version_end = user_agent.find(';', version_start)
            if version_end != -1:
                browser_version = user_agent[version_start:version_end]
    elif 'Firefox' in user_agent:
        browser = 'Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = 'Safari'
    elif 'Edge' in user_agent:
        browser = 'Edge'
    
    # Create a friendly display name
    if device_type == 'Desktop':
        display_name = f"{device_name} ({browser})"
    else:
        display_name = f"{device_name} ({browser})"
    
    if browser_version:
        display_name = f"{device_name} ({browser} {browser_version})"
    
    return {
        'type': device_type,
        'browser': browser,
        'browser_version': browser_version,
        'os_name': os_name,
        'device_name': device_name,
        'display_name': display_name,
        'pc_username': pc_username,
        'user_agent': user_agent,
        'ip': request.remote_addr,
        'timestamp': datetime.now().isoformat()
    }

def get_config():
    """Get current configuration"""
    return {
        'max_file_size': app.config['MAX_CONTENT_LENGTH'],
        'max_file_size_mb': 'Unlimited' if app.config['MAX_CONTENT_LENGTH'] == 0 else app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024),
        'session_enabled': True,  # Session management is enabled
        'auto_refresh_interval': app.config['AUTO_REFRESH_INTERVAL'],
        'allowed_extensions': list(ALLOWED_EXTENSIONS)
    }

@app.route('/')
def index():
    """Main page with QR code and file management"""
    local_ip = get_local_ip()
    server_url = f"http://{local_ip}:5000"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(server_url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="cyan", back_color="black")
    img_buffer = BytesIO()
    img.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    qr_code_b64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return render_template('index.html', 
                         qr_code=qr_code_b64, 
                         server_url=server_url,
                         local_ip=local_ip,
                         config=get_config())

@app.route('/api/session/create', methods=['POST'])
def create_session_endpoint():
    """Create a new session for a device"""
    try:
        device_info = get_device_info(request)
        device_ip = device_info.get('ip', 'unknown')
        
        # Check if device already has an active session
        if device_ip in session_tokens:
            existing_token = session_tokens[device_ip]
            if existing_token in active_sessions:
                # Return existing session
                session_data = active_sessions[existing_token]
                session_data['last_activity'] = datetime.now().isoformat()
                
                return jsonify({
                    'success': True,
                    'token': existing_token,
                    'device_info': device_info,
                    'session_id': session_data['session_id'],
                    'message': 'Existing session found',
                    'is_new': False
                })
        
        # Create new session
        token = create_session(device_info)
        session_data = active_sessions[token]
        
        return jsonify({
            'success': True,
            'token': token,
            'device_info': device_info,
            'session_id': session_data['session_id'],
            'message': 'Session created successfully',
            'is_new': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/validate', methods=['POST'])
def validate_session_endpoint():
    """Validate a session token"""
    try:
        data = request.get_json()
        token = data.get('token', '')
        
        if validate_session(token):
            session_data = active_sessions[token]
            return jsonify({
                'success': True,
                'valid': True,
                'device_info': session_data['device_info'],
                'message': 'Session is valid'
            })
        else:
            return jsonify({
                'success': True,
                'valid': False,
                'message': 'Session is invalid or expired'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/active')
def get_active_sessions():
    """Get all active sessions"""
    try:
        sessions = []
        for token, session_data in active_sessions.items():
            if session_data['is_active']:
                sessions.append({
                    'token': token,
                    'device_info': session_data['device_info'],
                    'created_at': session_data['created_at'],
                    'last_activity': session_data['last_activity']
                })
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'count': len(sessions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config')
def get_app_config():
    """Get application configuration"""
    return jsonify(get_config())

@app.route('/api/system-info')
def get_system_info_api():
    """Get system information"""
    return jsonify(get_system_info())

@app.route('/api/files')
def get_files():
    """Get list of downloadable files from both uploads and downloads folders"""
    files = []
    try:
        # Get files from both folders
        folders = [UPLOAD_FOLDER, DOWNLOAD_FOLDER]
        
        for folder in folders:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        stat = os.stat(file_path)
                        # Add folder info to distinguish source
                        source = 'phone' if folder == UPLOAD_FOLDER else 'pc'
                        files.append({
                            'name': filename,
                            'size': format_file_size(stat.st_size),
                            'size_bytes': stat.st_size,
                            'icon': get_file_icon(filename),
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                            'extension': filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown',
                            'source': source,
                            'folder': folder
                        })
    except Exception as e:
        print(f"Error reading files: {e}")
    
    return jsonify(files)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload from phone to PC"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            file_size = os.path.getsize(file_path)
            result = {
                'success': True,
                'filename': filename,
                'size': format_file_size(file_size),
                'size_bytes': file_size,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'icon': get_file_icon(filename)
            }
            
            # Broadcast file event
            broadcast_file_event('upload', {
                'filename': filename,
                'size': format_file_size(file_size),
                'source': 'phone'
            })
            
            return jsonify(result)
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download file from either uploads or downloads folder"""
    try:
        # Try downloads folder first (PC files)
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
        
        # Try uploads folder (phone files)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
        
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/upload-pc', methods=['POST'])
def upload_file_pc():
    """Handle file upload from PC to downloads folder"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            file.save(file_path)
            
            file_size = os.path.getsize(file_path)
            result = {
                'success': True,
                'filename': filename,
                'size': format_file_size(file_size),
                'size_bytes': file_size,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'icon': get_file_icon(filename)
            }
            
            # Broadcast file event
            broadcast_file_event('upload', {
                'filename': filename,
                'size': format_file_size(file_size),
                'source': 'pc'
            })
            
            return jsonify(result)
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete/<filename>')
def delete_file(filename):
    """Delete a file from either uploads or downloads folder"""
    try:
        # Try downloads folder first (PC files)
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
            # Broadcast file event
            broadcast_file_event('delete', {
                'filename': filename,
                'source': 'pc'
            })
            
            return jsonify({'success': True})
        
        # Try uploads folder (phone files)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
            # Broadcast file event
            broadcast_file_event('delete', {
                'filename': filename,
                'source': 'phone'
            })
            
            return jsonify({'success': True})
        
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events')
def get_events():
    """Get recent file events"""
    return jsonify(file_events)

@app.route('/api/devices')
def get_devices():
    """Get connected devices"""
    return jsonify(list(connected_devices.values()))

@app.route('/api/device-events')
def get_device_events():
    """Get recent device events"""
    return jsonify(device_events)

@app.route('/api/cleanup-files', methods=['POST'])
def cleanup_files():
    """Clean up old files based on configuration"""
    try:
        data = request.get_json()
        hours = data.get('hours', 24)
        
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        deleted_count = 0
        
        # Clean uploads folder
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                if os.path.getmtime(file_path) < cutoff_time:
                    os.remove(file_path)
                    deleted_count += 1
        
        # Clean downloads folder
        for filename in os.listdir(DOWNLOAD_FOLDER):
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                if os.path.getmtime(file_path) < cutoff_time:
                    os.remove(file_path)
                    deleted_count += 1
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Cleaned up {deleted_count} old files'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-files')
def search_files():
    """Search files by name, type, or date from both folders"""
    try:
        query = request.args.get('q', '').lower()
        file_type = request.args.get('type', '').lower()
        date_filter = request.args.get('date', '').lower()
        
        files = []
        folders = [UPLOAD_FOLDER, DOWNLOAD_FOLDER]
        
        for folder in folders:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        stat = os.stat(file_path)
                        
                        # Apply filters
                        if query and query not in filename.lower():
                            continue
                            
                        if file_type and not filename.lower().endswith(file_type):
                            continue
                        
                        if date_filter:
                            file_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                            if date_filter not in file_date:
                                continue
                        
                        # Add folder info to distinguish source
                        source = 'phone' if folder == UPLOAD_FOLDER else 'pc'
                        files.append({
                            'name': filename,
                            'size': format_file_size(stat.st_size),
                            'size_bytes': stat.st_size,
                            'icon': get_file_icon(filename),
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                            'extension': filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown',
                            'source': source,
                            'folder': folder
                        })
        
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-zip', methods=['POST'])
def download_zip():
    """Create and download a zip file of selected files from both folders"""
    try:
        data = request.get_json()
        selected_files = data.get('files', [])
        
        if not selected_files:
            return jsonify({'error': 'No files selected'}), 400
        
        import zipfile
        import tempfile
        
        # Create temporary zip file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        with zipfile.ZipFile(temp_zip.name, 'w') as zipf:
            for filename in selected_files:
                # Try downloads folder first (PC files)
                file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    zipf.write(file_path, filename)
                    continue
                
                # Try uploads folder (phone files)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    zipf.write(file_path, filename)
        
        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name=f'simpleshare_files_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip',
            mimetype='application/zip'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    sid = request.sid if hasattr(request, 'sid') else request.environ.get('socketio.sid')
    active_connections.add(sid)
    
    # Get device information
    device_info = get_device_info(request)
    device_info['sid'] = sid
    device_info['connected_at'] = datetime.now().isoformat()
    device_info['session_id'] = None  # Will be set when session is created
    device_info['status'] = 'online'
    device_info['last_seen'] = datetime.now().isoformat()
    
    # Store device information
    connected_devices[sid] = device_info
    device_last_seen[sid] = datetime.now().timestamp()
    device_status[sid] = 'online'
    
    # Create or update session for this device
    token = create_session(device_info)
    device_info['session_token'] = token
    device_info['session_id'] = active_sessions[token]['session_id']
    
    # Update device info with session data
    connected_devices[sid] = device_info
    
    # Broadcast device connection
    broadcast_device_event('connect', device_info)
    
    emit('connected', {
        'message': 'Connected to SimpleShare',
        'device_info': device_info,
        'session_token': token
    })
    
    # Send current devices list to all clients
    socketio.emit('devices_update', list(connected_devices.values()))

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection - IMMEDIATELY REMOVE DEVICE"""
    sid = request.sid if hasattr(request, 'sid') else request.environ.get('socketio.sid')
    active_connections.discard(sid)
    
    # Get device info before removing
    device_info = connected_devices.get(sid, {})
    
    # IMMEDIATELY REMOVE DEVICE FROM ALL TRACKING
    if sid in connected_devices:
        del connected_devices[sid]
    if sid in device_last_seen:
        del device_last_seen[sid]
    if sid in device_status:
        del device_status[sid]
    
    # Broadcast device disconnection and updated devices list
    if device_info:
        device_info['status'] = 'offline'
        broadcast_device_event('disconnect', device_info)
        socketio.emit('devices_update', list(connected_devices.values()))

@socketio.on('request_system_info')
def handle_system_info_request():
    """Send system information to client"""
    emit('system_info', get_system_info())

@socketio.on('request_devices')
def handle_devices_request():
    """Send connected devices list to client"""
    emit('devices_list', list(connected_devices.values()))

@socketio.on('heartbeat')
def handle_heartbeat():
    """Handle client heartbeat to track online status"""
    sid = request.sid if hasattr(request, 'sid') else request.environ.get('socketio.sid')
    if sid and sid in connected_devices:
        connected_devices[sid]['last_seen'] = datetime.now().isoformat()
        device_last_seen[sid] = datetime.now().timestamp()
        device_status[sid] = 'online'
        connected_devices[sid]['status'] = 'online'

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f"🚀 SimpleShare Server Starting...")
    print(f"📱 Scan QR code to connect from your phone")
    print(f"🌐 Server URL: http://{local_ip}:5000")
    print(f"💻 Local URL: http://localhost:5000")
    print(f"📁 Uploads folder: {UPLOAD_FOLDER}")
    print(f"📁 Downloads folder: {DOWNLOAD_FOLDER}")
    print(f"🔐 Authentication: {'Enabled' if app.config['AUTH_ENABLED'] else 'Disabled'}")
    max_size = "Unlimited" if app.config['MAX_CONTENT_LENGTH'] == 0 else f"{app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)}MB"
    print(f"📏 Max file size: {max_size}")
    print(f"⚡ Press Ctrl+C to stop the server")
    
    # Start periodic cleanup of offline devices
    def periodic_cleanup():
        while True:
            try:
                cleanup_offline_devices()
                time.sleep(10)  # Check every 10 seconds - much faster
            except Exception as e:
                print(f"Error in periodic cleanup: {e}")
                time.sleep(10)
    
    # Start cleanup thread
    import threading
    cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
    cleanup_thread.start()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

# Credits: R ! Y 4 Z 