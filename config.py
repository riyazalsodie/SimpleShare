# Owner: R ! Y 4 Z
# SimpleShare Configuration
# Edit these settings to customize your SimpleShare experience

# Server Configuration
SERVER_HOST = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 5000        # Port number
DEBUG_MODE = True         # Enable debug mode

# File Upload Configuration
MAX_FILE_SIZE_MB = 0      # 0 = No file size limit (unlimited)
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 
    'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'avi', 'mov', 
    'wmv', 'flv', 'webm', 'mkv', 'wav', 'aac', 'ogg', 'ppt', 'pptx'
}

# Session Configuration
SESSION_ENABLED = True    # Enable/disable session management
SESSION_TIMEOUT = 86400   # Session timeout in seconds (24 hours)
MAX_SESSIONS = 100        # Maximum number of active sessions

# Real-time Updates Configuration
AUTO_REFRESH_INTERVAL = 10  # File list refresh interval in seconds
REALTIME_UPDATES = True   # Enable real-time file event updates
SYSTEM_INFO_UPDATE_INTERVAL = 30  # System info update interval in seconds

# UI Configuration
DEFAULT_THEME = 'sci-fi-theme'  # Default theme: sci-fi-theme, day-theme, night-theme
ANIMATIONS_ENABLED = True  # Enable/disable UI animations
NOTIFICATION_DURATION = 5000  # Notification display duration in milliseconds

# Security Configuration
SECURE_FILENAMES = True   # Sanitize uploaded filenames
LOG_FILE_OPERATIONS = True  # Log file upload/download operations
RATE_LIMIT_ENABLED = False  # Enable rate limiting (requires additional setup)

# Advanced Configuration
ENABLE_COMPRESSION = True  # Enable response compression
ENABLE_CACHING = True     # Enable static file caching
MAX_CONNECTIONS = 100     # Maximum concurrent connections

# Customization
APP_NAME = 'SimpleShare'
APP_VERSION = '2.0.0'
APP_DESCRIPTION = 'Futuristic File Transfer Application'

# File Storage Configuration
UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'
TEMP_FOLDER = 'temp'  # Temporary files folder

# Logging Configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = 'simpleshare.log'  # Log file path
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Network Configuration
ALLOWED_HOSTS = ['*']  # Allowed host headers (use ['localhost', '127.0.0.1'] for local only)
CORS_ENABLED = True     # Enable CORS for cross-origin requests
CORS_ORIGINS = ['*']    # Allowed CORS origins

# Performance Configuration
WORKER_THREADS = 4      # Number of worker threads
CONNECTION_TIMEOUT = 30  # Connection timeout in seconds
UPLOAD_TIMEOUT = 300    # Upload timeout in seconds

# Feature Flags
ENABLE_QR_CODE = True    # Enable QR code generation
ENABLE_SYSTEM_INFO = True  # Enable system information display
ENABLE_FILE_PREVIEW = False  # Enable file preview (experimental)
ENABLE_BATCH_OPERATIONS = True  # Enable batch file operations
ENABLE_SEARCH = True     # Enable file search functionality

# Device Tracking Configuration
DEVICE_TRACKING_ENABLED = True  # Enable device tracking
MAX_DEVICE_HISTORY = 50  # Maximum number of device events to store
DEVICE_TIMEOUT_SECONDS = 30  # Timeout for device connection status
DEVICE_DETECTION_ENABLED = True  # Enable automatic device type detection

# File Management Configuration
AUTO_CLEANUP_ENABLED = True  # Enable automatic file cleanup
DEFAULT_CLEANUP_HOURS = 24  # Default hours for file cleanup
MAX_FILE_AGE_HOURS = 168  # Maximum file age (7 days)
ENABLE_ZIP_DOWNLOAD = True  # Enable ZIP download functionality
MAX_ZIP_SIZE_MB = 0  # 0 = No ZIP file size limit (unlimited)

# Search and Filter Configuration
SEARCH_ENABLED = True  # Enable file search functionality
MAX_SEARCH_RESULTS = 100  # Maximum search results to return
SEARCH_INDEX_ENABLED = True  # Enable search indexing

# Mobile Optimization
MOBILE_OPTIMIZED = True  # Enable mobile-specific optimizations
TOUCH_GESTURES = True    # Enable touch gesture support
RESPONSIVE_DESIGN = True  # Enable responsive design features

# Notification Configuration
BROWSER_NOTIFICATIONS = True  # Enable browser notifications
SOUND_NOTIFICATIONS = False   # Enable sound notifications
DESKTOP_NOTIFICATIONS = False  # Enable desktop notifications (requires setup)

# Backup Configuration
AUTO_BACKUP = False      # Enable automatic file backup
BACKUP_INTERVAL = 3600   # Backup interval in seconds
BACKUP_RETENTION = 7     # Number of days to keep backups

# Monitoring Configuration
ENABLE_MONITORING = True  # Enable system monitoring
MONITORING_INTERVAL = 60  # Monitoring update interval in seconds
ALERT_THRESHOLD_CPU = 80  # CPU usage alert threshold
ALERT_THRESHOLD_MEMORY = 80  # Memory usage alert threshold
ALERT_THRESHOLD_DISK = 90  # Disk usage alert threshold

# Owner: R ! Y 4 Z 