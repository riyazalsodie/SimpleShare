// SimpleShare - Futuristic File Transfer JavaScript

class SimpleShare {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.setupSocketIO();
        this.checkSession();
        this.loadFiles();
        this.setupAutoRefresh();
        this.setupSystemInfo();
        this.requestDevices();
    }

    initializeElements() {
        // File inputs
        this.fileInput = document.getElementById('fileInput');
        this.pcFileInput = document.getElementById('pcFileInput');
        
        // Upload areas
        this.uploadArea = document.getElementById('uploadArea');
        this.pcUploadArea = document.getElementById('pcUploadArea');
        
        // Progress elements
        this.uploadProgress = document.getElementById('uploadProgress');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        
        // Results containers
        this.uploadResults = document.getElementById('uploadResults');
        this.fileList = document.getElementById('fileList');
        
        // Theme toggle
        this.themeToggle = document.getElementById('themeToggle');
        this.toggleIcon = this.themeToggle.querySelector('.toggle-icon');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        // Toast
        this.toast = document.getElementById('toast');
        
        // Session Management
        this.sessionModal = document.getElementById('sessionModal');
        this.sessionStatus = document.getElementById('sessionStatus');
        this.tokenDisplay = document.getElementById('tokenDisplay');
        this.sessionToken = document.getElementById('sessionToken');
        this.sessionError = document.getElementById('sessionError');
        this.createSessionBtn = document.getElementById('createSessionBtn');
        this.validateSessionBtn = document.getElementById('validateSessionBtn');
        
        // System info
        this.systemIP = document.getElementById('systemIP');
        this.maxFileSize = document.getElementById('maxFileSize');
        this.activeSessions = document.getElementById('activeSessions');
        this.connectedDevices = document.getElementById('connectedDevices');
        this.serverUptime = document.getElementById('serverUptime');
        
        // Devices tracking
        this.devicesGrid = document.getElementById('devicesGrid');
        this.devicesMap = new Map();
        
        // Real-time indicator
        this.realtimeIndicator = null;
        
        // Notification center
        this.notificationCenter = null;
    }

    setupEventListeners() {
        // File input change events
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e, 'phone'));
        this.pcFileInput.addEventListener('change', (e) => this.handleFileSelect(e, 'pc'));
        
        // Drag and drop events
        this.setupDragAndDrop(this.uploadArea, 'phone');
        this.setupDragAndDrop(this.pcUploadArea, 'pc');
        
        // Mobile touch events
        this.setupMobileTouchEvents();
        
        // Theme toggle
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Session management events
        this.setupSessionEvents();
        
        // Enhanced file controls
        this.setupFileControls();
        
        // Initialize theme from localStorage
        this.loadTheme();
    }

    setupDragAndDrop(area, type) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, () => {
                area.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, () => {
                area.classList.remove('dragover');
            });
        });

        area.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFiles(files, type);
            }
        });
    }

    handleFileSelect(event, type) {
        const files = event.target.files;
        if (files.length > 0) {
            this.handleFiles(files, type);
        }
    }

    async handleFiles(files, type) {
        this.showLoading();
        
        try {
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                await this.uploadFile(file, type);
            }
        } catch (error) {
            this.showToast('Error uploading files', 'error');
        } finally {
            this.hideLoading();
        }
    }

    // This method is now replaced by the enhanced version above

    addUploadResult(filename, size, timestamp) {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'upload-result';
        resultDiv.innerHTML = `
            <div>
                <div class="file-name">${filename}</div>
                <div class="file-details">
                    <span>Size: ${size}</span>
                    <span>Uploaded: ${timestamp}</span>
                </div>
            </div>
            <div class="file-icon">✅</div>
        `;
        
        this.uploadResults.appendChild(resultDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            resultDiv.remove();
        }, 5000);
    }

    async loadFiles() {
        try {
            const response = await fetch('/api/files');
            const files = await response.json();
            this.displayFiles(files);
        } catch (error) {
            this.showToast('Error loading files', 'error');
            this.displayFiles([]);
        }
    }

    displayFiles(files) {
        if (files.length === 0) {
            this.fileList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📁</div>
                    <div>No files available for download</div>
                    <div style="font-size: 0.9rem; margin-top: 10px; opacity: 0.7;">
                        Upload files from PC or phone to make them available
                    </div>
                </div>
            `;
            return;
        }

        this.fileList.innerHTML = files.map(file => {
            const source = file.source || 'unknown';
            const sourceIcon = source === 'phone' ? '📱' : '💻';
            const sourceText = source === 'phone' ? 'Phone' : 'PC';
            
            return `
                <div class="file-item" data-filename="${file.name}">
                    <div class="file-select">
                        <input type="checkbox" class="file-checkbox" value="${file.name}" id="file-${file.name.replace(/[^a-zA-Z0-9]/g, '')}">
                        <label for="file-${file.name.replace(/[^a-zA-Z0-9]/g, '')}"></label>
                    </div>
                    <div class="file-icon">${file.icon}</div>
                    <div class="file-info">
                        <div class="file-name" title="${file.name}">${file.name}</div>
                        <div class="file-details">
                            <span class="file-size">📏 ${file.size}</span>
                            <span class="file-date">📅 ${file.modified}</span>
                            <span class="file-type">📄 ${file.extension}</span>
                            <span class="file-source">${sourceIcon} ${sourceText}</span>
                        </div>
                    </div>
                    <div class="file-actions">
                        <button class="action-btn download-btn" onclick="simpleShare.downloadFile('${file.name}')" title="Download ${file.name}">
                            📥
                        </button>
                        <button class="action-btn delete-btn" onclick="simpleShare.deleteFile('${file.name}')" title="Delete ${file.name}">
                            🗑️
                        </button>
                    </div>
                </div>
            `;
        }).join('');

        // Add mobile-specific event listeners for better touch interaction
        this.setupMobileFileInteractions();
    }

    setupMobileFileInteractions() {
        const fileItems = document.querySelectorAll('.file-item');
        
        fileItems.forEach(item => {
            const filename = item.dataset.filename;
            const downloadBtn = item.querySelector('.download-btn');
            const deleteBtn = item.querySelector('.delete-btn');
            
            // Add long press for context menu (mobile)
            let pressTimer;
            
            item.addEventListener('touchstart', (e) => {
                pressTimer = setTimeout(() => {
                    this.showMobileContextMenu(e, filename, item);
                }, 500);
            });
            
            item.addEventListener('touchend', () => {
                clearTimeout(pressTimer);
            });
            
            item.addEventListener('touchmove', () => {
                clearTimeout(pressTimer);
            });
            
            // Prevent default context menu on mobile
            item.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                this.showMobileContextMenu(e, filename, item);
            });
        });
    }

    showMobileContextMenu(event, filename, item) {
        event.preventDefault();
        
        // Create mobile-friendly context menu
        const menu = document.createElement('div');
        menu.className = 'mobile-context-menu';
        menu.innerHTML = `
            <div class="menu-item" onclick="simpleShare.downloadFile('${filename}')">
                📥 Download
            </div>
            <div class="menu-item delete" onclick="simpleShare.deleteFile('${filename}')">
                🗑️ Delete
            </div>
            <div class="menu-item" onclick="this.parentElement.remove()">
                ❌ Cancel
            </div>
        `;
        
        // Position menu
        const rect = item.getBoundingClientRect();
        menu.style.position = 'fixed';
        menu.style.top = `${rect.top + rect.height / 2}px`;
        menu.style.left = `${rect.left + rect.width / 2}px`;
        menu.style.transform = 'translate(-50%, -50%)';
        menu.style.zIndex = '1000';
        
        document.body.appendChild(menu);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (menu.parentElement) {
                menu.remove();
            }
        }, 3000);
        
        // Remove on outside click
        document.addEventListener('click', function removeMenu(e) {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', removeMenu);
            }
        });
    }

    async downloadFile(filename) {
        try {
            this.showLoading();
            const response = await fetch(`/api/download/${filename}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                this.showToast(`${filename} downloaded successfully!`, 'success');
            } else {
                this.showToast(`Error downloading ${filename}`, 'error');
            }
        } catch (error) {
            this.showToast(`Error downloading ${filename}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async deleteFile(filename) {
        if (!confirm(`Are you sure you want to delete ${filename}?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/delete/${filename}`);
            const result = await response.json();

            if (result.success) {
                this.showToast(`${filename} deleted successfully!`, 'success');
                this.loadFiles(); // Refresh the list
            } else {
                this.showToast(`Error deleting ${filename}`, 'error');
            }
        } catch (error) {
            this.showToast(`Error deleting ${filename}`, 'error');
        }
    }

    setupAutoRefresh() {
        // Auto-refresh file list every 30 seconds
        setInterval(() => {
            this.loadFiles();
        }, 30000);
    }

    showLoading() {
        this.loadingOverlay.classList.add('show');
    }

    hideLoading() {
        this.loadingOverlay.classList.remove('show');
    }

    showToast(message, type = 'success') {
        // Use the new notification system instead
        this.showNotification(message, type);
    }

    toggleTheme() {
        const currentTheme = document.body.className;
        const themes = ['sci-fi-theme', 'day-theme', 'night-theme'];
        const themeIcons = ['🌙', '☀️', '⚡'];
        
        let currentIndex = themes.indexOf(currentTheme);
        currentIndex = (currentIndex + 1) % themes.length;
        
        const newTheme = themes[currentIndex];
        const newIcon = themeIcons[currentIndex];
        
        document.body.className = newTheme;
        this.toggleIcon.textContent = newIcon;
        
        localStorage.setItem('simpleShareTheme', newTheme);
        localStorage.setItem('simpleShareThemeIcon', newIcon);
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('simpleShareTheme') || 'sci-fi-theme';
        const savedIcon = localStorage.getItem('simpleShareThemeIcon') || '🌙';
        
        document.body.className = savedTheme;
        this.toggleIcon.textContent = savedIcon;
    }

    // Session Management Methods
    setupSessionEvents() {
        if (this.createSessionBtn) {
            this.createSessionBtn.addEventListener('click', () => {
                this.createSession();
            });
        }

        if (this.validateSessionBtn) {
            this.validateSessionBtn.addEventListener('click', () => {
                this.validateSession();
            });
        }
    }

    async checkSession() {
        try {
            const response = await fetch('/api/config');
            const config = await response.json();
            
            if (config.session_enabled) {
                // Check if we already have a valid token
                const existingToken = localStorage.getItem('simpleShareToken');
                if (existingToken) {
                    // Try to validate existing session first
                    const isValid = await this.validateExistingSession(existingToken);
                    if (isValid) {
                        return; // Session is valid, no need to create new one
                    }
                }
                
                // Create new session only if needed
                this.showSessionModal();
                this.createSession();
            }
        } catch (error) {
            console.error('Error checking session:', error);
        }
    }

    async validateExistingSession(token) {
        try {
            const response = await fetch('/api/session/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });

            const result = await response.json();
            return result.success && result.valid;
        } catch (error) {
            console.error('Error validating existing session:', error);
            return false;
        }
    }

    showSessionModal() {
        this.sessionModal.style.display = 'flex';
        this.sessionError.style.display = 'none';
    }

    hideSessionModal() {
        this.sessionModal.style.display = 'none';
    }

    async createSession() {
        try {
            this.sessionStatus.textContent = '⏳ Creating session...';
            this.tokenDisplay.style.display = 'none';
            
            const response = await fetch('/api/session/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (result.success) {
                this.sessionToken.textContent = result.token;
                this.tokenDisplay.style.display = 'block';
                
                // Store token in localStorage
                localStorage.setItem('simpleShareToken', result.token);
                
                if (result.is_new) {
                    this.sessionStatus.textContent = '✅ New session created successfully';
                    setTimeout(() => {
                        this.hideSessionModal();
                        this.showNotification('New session created successfully!', 'success');
                    }, 2000);
                } else {
                    this.sessionStatus.textContent = '✅ Connected to existing session';
                    setTimeout(() => {
                        this.hideSessionModal();
                        this.showNotification('Connected to existing session!', 'info');
                    }, 2000);
                }
            } else {
                this.showSessionError(result.error || 'Failed to create session');
            }
        } catch (error) {
            this.showSessionError('Session creation failed');
        }
    }

    async validateSession() {
        const token = localStorage.getItem('simpleShareToken');
        
        if (!token) {
            this.showSessionError('No session token found');
            return;
        }

        try {
            this.sessionStatus.textContent = '⏳ Validating session...';
            
            const response = await fetch('/api/session/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });

            const result = await response.json();

            if (result.success && result.valid) {
                this.sessionStatus.textContent = '✅ Session is valid';
                this.sessionToken.textContent = token;
                this.tokenDisplay.style.display = 'block';
                
                setTimeout(() => {
                    this.hideSessionModal();
                    this.showNotification('Session validated successfully!', 'success');
                }, 2000);
            } else {
                this.showSessionError('Session is invalid or expired');
                localStorage.removeItem('simpleShareToken');
            }
        } catch (error) {
            this.showSessionError('Session validation failed');
        }
    }

    showSessionError(message) {
        this.sessionError.textContent = message;
        this.sessionError.style.display = 'block';
    }

    // Real-time Updates
    setupSocketIO() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.createRealtimeIndicator(true);
            this.socket.emit('request_system_info');
            this.startHeartbeat();
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.createRealtimeIndicator(false);
            this.stopHeartbeat();
        });

        this.socket.on('file_event', (event) => {
            this.handleFileEvent(event);
        });

        this.socket.on('system_info', (info) => {
            this.updateSystemInfo(info);
        });

        this.socket.on('devices_update', (devices) => {
            this.updateDevicesList(devices);
        });

        this.socket.on('devices_list', (devices) => {
            this.updateDevicesList(devices);
        });

        this.socket.on('device_event', (event) => {
            this.handleDeviceEvent(event);
        });
    }
    
    startHeartbeat() {
        // Send heartbeat every 5 seconds to keep connection alive (more frequent)
        this.heartbeatInterval = setInterval(() => {
            if (this.socket && this.socket.connected) {
                this.socket.emit('heartbeat');
            }
        }, 5000); // Every 5 seconds instead of 10
    }
    
    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }

    setupFileControls() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const typeFilter = document.getElementById('typeFilter');
        const dateFilter = document.getElementById('dateFilter');
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchFiles(e.target.value, typeFilter?.value || '', dateFilter?.value || '');
            });
        }
        
        if (typeFilter) {
            typeFilter.addEventListener('change', () => {
                this.searchFiles(searchInput?.value || '', typeFilter.value, dateFilter?.value || '');
            });
        }
        
        if (dateFilter) {
            dateFilter.addEventListener('change', () => {
                this.searchFiles(searchInput?.value || '', typeFilter?.value || '', dateFilter.value);
            });
        }
        
        // Action buttons
        const selectAllBtn = document.getElementById('selectAllBtn');
        const downloadZipBtn = document.getElementById('downloadZipBtn');
        const cleanupBtn = document.getElementById('cleanupBtn');
        
        if (selectAllBtn) {
            selectAllBtn.addEventListener('click', () => {
                this.selectAllFiles();
            });
        }
        
        if (downloadZipBtn) {
            downloadZipBtn.addEventListener('click', () => {
                this.downloadSelectedFiles(this.getSelectedFiles());
            });
        }
        
        if (cleanupBtn) {
            cleanupBtn.addEventListener('click', () => {
                if (confirm('Are you sure you want to clean up files older than 24 hours?')) {
                    this.cleanupOldFiles(24);
                }
            });
        }
    }

    selectAllFiles() {
        const checkboxes = document.querySelectorAll('.file-checkbox');
        const allChecked = Array.from(checkboxes).every(cb => cb.checked);
        
        checkboxes.forEach(cb => {
            cb.checked = !allChecked;
        });
        
        const selectAllBtn = document.getElementById('selectAllBtn');
        if (selectAllBtn) {
            selectAllBtn.textContent = allChecked ? 'Select All' : 'Deselect All';
        }
    }

    getSelectedFiles() {
        const checkboxes = document.querySelectorAll('.file-checkbox:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    }

    requestDevices() {
        if (this.socket) {
            this.socket.emit('request_devices');
        }
    }

    createRealtimeIndicator(online) {
        if (!this.realtimeIndicator) {
            this.realtimeIndicator = document.createElement('div');
            this.realtimeIndicator.className = 'realtime-indicator';
            this.realtimeIndicator.innerHTML = `
                <div class="realtime-dot"></div>
                <span>Real-time</span>
            `;
            document.body.appendChild(this.realtimeIndicator);
        }

        if (online) {
            this.realtimeIndicator.classList.remove('offline');
        } else {
            this.realtimeIndicator.classList.add('offline');
        }
    }

    handleFileEvent(event) {
        const { type, data, timestamp } = event;
        
        switch (type) {
            case 'upload':
                this.showNotification(
                    `File uploaded: ${data.filename} (${data.size})`,
                    'success'
                );
                this.loadFiles(); // Refresh file list
                break;
            case 'delete':
                this.showNotification(
                    `File deleted: ${data.filename}`,
                    'warning'
                );
                this.loadFiles(); // Refresh file list
                break;
        }
    }

    // System Information
    setupSystemInfo() {
        this.updateSystemInfoPeriodically();
    }

    async updateSystemInfoPeriodically() {
        try {
            const response = await fetch('/api/system-info');
            const info = await response.json();
            this.updateSystemInfo(info);
            
            // Also request devices list
            this.requestDevices();
        } catch (error) {
            console.error('Error updating system info:', error);
        }

        // Update every 30 seconds
        setTimeout(() => this.updateSystemInfoPeriodically(), 30000);
    }

    updateSystemInfo(info) {
        if (this.systemIP) this.systemIP.textContent = info.local_ip || '--';
        if (this.maxFileSize) {
            const maxSize = info.max_file_size || '--';
            this.maxFileSize.textContent = maxSize === 'Unlimited' ? 'Unlimited' : maxSize;
        }
        if (this.activeSessions) this.activeSessions.textContent = info.active_sessions || '--';
        if (this.connectedDevices) this.connectedDevices.textContent = info.connected_devices || '--';
        
        // Start uptime timer only once, not on every update
        if (this.serverUptime && !this._uptimeStarted) {
            this.startGuaranteedUptimeTimer(info.server_start_time);
        }
        
        // Update devices list if available
        if (info.devices_list) {
            this.updateDevicesList(info.devices_list);
        }
    }

    startGuaranteedUptimeTimer(serverStartTime) {
        // Clear any existing timer
        if (this._uptimeInterval) {
            clearInterval(this._uptimeInterval);
        }
        
        // Calculate uptime based on server start time
        const startTime = serverStartTime || Date.now() / 1000;
        this._uptimeStarted = true;
        
        const update = () => {
            const currentTime = Date.now() / 1000;
            const uptimeSeconds = Math.floor(currentTime - startTime);
            const formatted = this.formatUptime(uptimeSeconds);
            this.serverUptime.textContent = formatted;
        };
        
        update(); // Update immediately
        this._uptimeInterval = setInterval(update, 1000);
    }

    formatUptime(seconds) {
        if (seconds < 60) return `${seconds}s`;
        if (seconds < 3600) {
            const m = Math.floor(seconds / 60);
            const s = seconds % 60;
            return `${m}m ${s}s`;
        }
        if (seconds < 86400) {
            const h = Math.floor(seconds / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            return `${h}h ${m}m`;
        }
        const d = Math.floor(seconds / 86400);
        const h = Math.floor((seconds % 86400) / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        return `${d}d ${h}h ${m}m`;
    }

    // Enhanced Notifications
    createNotificationCenter() {
        if (!this.notificationCenter) {
            this.notificationCenter = document.createElement('div');
            this.notificationCenter.className = 'notification-center';
            document.body.appendChild(this.notificationCenter);
        }
    }

    showNotification(message, type = 'success', title = null) {
        this.createNotificationCenter();
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        const notificationTitle = title || this.getNotificationTitle(type);
        
        notification.innerHTML = `
            <div class="notification-header">
                <div class="notification-title">${notificationTitle}</div>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="notification-message">${message}</div>
        `;
        
        this.notificationCenter.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 5000);
    }

    getNotificationTitle(type) {
        switch (type) {
            case 'success': return '✅ Success';
            case 'error': return '❌ Error';
            case 'warning': return '⚠️ Warning';
            default: return 'ℹ️ Info';
        }
    }

    // Enhanced file upload with progress
    async uploadFile(file, type) {
        const formData = new FormData();
        formData.append('file', file);

        const endpoint = type === 'phone' ? '/api/upload' : '/api/upload-pc';
        
        try {
            // Show progress
            this.showUploadProgress(file.name);
            
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.hideUploadProgress();
                this.showNotification(`${file.name} uploaded successfully!`, 'success');
                if (type === 'pc') {
                    this.loadFiles(); // Refresh file list for PC uploads
                } else {
                    this.addUploadResult(file.name, result.size, result.timestamp);
                }
            } else {
                this.hideUploadProgress();
                this.showNotification(`Error uploading ${file.name}: ${result.error}`, 'error');
            }
        } catch (error) {
            this.hideUploadProgress();
            this.showNotification(`Error uploading ${file.name}`, 'error');
        }
    }

    showUploadProgress(filename) {
        this.uploadProgress.style.display = 'block';
        this.progressText.textContent = `Uploading ${filename}...`;
        this.progressFill.style.width = '0%';
        
        // Simulate progress (since we can't get real progress from fetch)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            this.progressFill.style.width = `${progress}%`;
        }, 200);
        
        this.currentProgressInterval = progressInterval;
    }

    hideUploadProgress() {
        this.uploadProgress.style.display = 'none';
        if (this.currentProgressInterval) {
            clearInterval(this.currentProgressInterval);
        }
        this.progressFill.style.width = '100%';
        setTimeout(() => {
            this.progressFill.style.width = '0%';
        }, 500);
    }

    // Device Tracking Methods
    updateDevicesList(devices) {
        if (!this.devicesGrid) return;

        if (devices.length === 0) {
            this.devicesGrid.innerHTML = `
                <div class="no-devices">
                    <div class="no-devices-icon">📱</div>
                    <div>No devices connected</div>
                    <div style="font-size: 0.9rem; margin-top: 10px; opacity: 0.7;">
                        Connect your phone to see it here
                    </div>
                </div>
            `;
            return;
        }

        this.devicesGrid.innerHTML = devices.map(device => {
            // All devices in the list are now online (offline devices are removed)
            const statusClass = 'online';
            const statusText = '🟢 Online';
            const lastSeen = device.last_seen ? this.formatTime(device.last_seen) : 'Just now';
            
            // Use enhanced device display name
            const deviceDisplayName = device.display_name || device.device_name || device.type;
            const osInfo = device.os_name ? ` (${device.os_name})` : '';
            
            // Show PC username for desktop devices
            const pcUsername = device.pc_username || '';
            const usernameInfo = device.type === 'Desktop' && pcUsername ? ` - ${pcUsername}` : '';
            
            return `
                <div class="device-item ${statusClass}">
                    <div class="device-status-indicator ${statusClass}">
                        <div class="status-dot"></div>
                        <span class="status-text">${statusText}</span>
                    </div>
                    <div class="device-header">
                        <div class="device-icon">${this.getDeviceIcon(device.type)}</div>
                        <div class="device-type">${deviceDisplayName}${osInfo}${usernameInfo}</div>
                    </div>
                    <div class="device-details">
                        <div class="device-detail">
                            <span class="device-label">Device:</span>
                            <span class="device-value">${device.device_name}</span>
                        </div>
                        <div class="device-detail">
                            <span class="device-label">Browser:</span>
                            <span class="device-value">${device.browser}${device.browser_version ? ' ' + device.browser_version : ''}</span>
                        </div>
                        <div class="device-detail">
                            <span class="device-label">IP:</span>
                            <span class="device-value">${device.ip}</span>
                        </div>
                        <div class="device-detail">
                            <span class="device-label">Connected:</span>
                            <span class="device-value">${this.formatTime(device.connected_at)}</span>
                        </div>
                        <div class="device-detail">
                            <span class="device-label">Last Active:</span>
                            <span class="device-value">${lastSeen}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    getDeviceIcon(deviceType) {
        const icons = {
            'Mobile': '📱',
            'Tablet': '📱',
            'Desktop': '💻',
            'Unknown': '❓'
        };
        return icons[deviceType] || icons['Unknown'];
    }

    handleDeviceEvent(event) {
        const { type, data, timestamp } = event;
        
        switch (type) {
            case 'connect':
                this.showNotification(
                    `Device connected: ${data.type} (${data.browser})`,
                    'success'
                );
                break;
            case 'disconnect':
                this.showNotification(
                    `Device disconnected: ${data.type} (${data.browser})`,
                    'warning'
                );
                break;
        }
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `${diffHours}h ago`;
        
        return date.toLocaleTimeString();
    }

    // Enhanced File Management
    async searchFiles(query, type = '', date = '') {
        try {
            const params = new URLSearchParams();
            if (query) params.append('q', query);
            if (type) params.append('type', type);
            if (date) params.append('date', date);
            
            const response = await fetch(`/api/search-files?${params}`);
            const files = await response.json();
            this.displayFiles(files);
        } catch (error) {
            this.showNotification('Error searching files', 'error');
        }
    }

    async downloadSelectedFiles(selectedFiles) {
        if (selectedFiles.length === 0) {
            this.showNotification('Please select files to download', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/download-zip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ files: selectedFiles })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `simpleshare_files_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.zip`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                this.showNotification('Files downloaded successfully!', 'success');
            } else {
                this.showNotification('Error downloading files', 'error');
            }
        } catch (error) {
            this.showNotification('Error downloading files', 'error');
        }
    }

    async cleanupOldFiles(hours = 24) {
        try {
            const response = await fetch('/api/cleanup-files', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ hours })
            });

            const result = await response.json();

            if (result.success) {
                this.showNotification(result.message, 'success');
                this.loadFiles(); // Refresh file list
            } else {
                this.showNotification('Error cleaning up files', 'error');
            }
        } catch (error) {
            this.showNotification('Error cleaning up files', 'error');
        }
    }

    setupMobileTouchEvents() {
        // Prevent zoom on double tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (event) => {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);

        // Add touch feedback for buttons
        const buttons = document.querySelectorAll('.neon-button, .action-btn');
        buttons.forEach(button => {
            button.addEventListener('touchstart', () => {
                button.style.transform = 'scale(0.95)';
                button.style.opacity = '0.8';
            });
            
            button.addEventListener('touchend', () => {
                button.style.transform = '';
                button.style.opacity = '';
            });
        });

        // Improve file item touch interaction
        document.addEventListener('click', (e) => {
            if (e.target.closest('.file-item')) {
                const fileItem = e.target.closest('.file-item');
                const checkbox = fileItem.querySelector('.file-checkbox');
                if (checkbox && !e.target.closest('.file-actions')) {
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            }
        });

        // Add swipe gestures for file actions (optional)
        this.setupSwipeGestures();
    }

    setupSwipeGestures() {
        let startX = 0;
        let startY = 0;
        let isSwiping = false;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isSwiping = false;
        });

        document.addEventListener('touchmove', (e) => {
            if (!startX || !startY) return;

            const deltaX = e.touches[0].clientX - startX;
            const deltaY = e.touches[0].clientY - startY;

            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
                isSwiping = true;
                e.preventDefault();
            }
        });

        document.addEventListener('touchend', (e) => {
            if (!isSwiping) return;

            const deltaX = e.changedTouches[0].clientX - startX;
            const fileItem = e.target.closest('.file-item');

            if (fileItem && Math.abs(deltaX) > 50) {
                // Swipe right to select, left to deselect
                const checkbox = fileItem.querySelector('.file-checkbox');
                if (checkbox) {
                    checkbox.checked = deltaX > 0;
                    checkbox.dispatchEvent(new Event('change'));
                }
            }

            startX = 0;
            startY = 0;
            isSwiping = false;
        });
    }
}

// Initialize the application
let simpleShare;

document.addEventListener('DOMContentLoaded', () => {
    simpleShare = new SimpleShare();
    // Add owner credit to main UI sections
    const credit = document.createElement('div');
    credit.className = 'owner-credit';
    credit.innerHTML = 'Credits: <b>R ! Y 4 Z</b> &copy;';
    // Add to header
    const header = document.querySelector('.header');
    if (header) header.appendChild(credit.cloneNode(true));
    // Add to system info
    const sysPanel = document.querySelector('.system-panel');
    if (sysPanel) sysPanel.appendChild(credit.cloneNode(true));
    // Add to devices panel
    const devPanel = document.querySelector('.devices-panel');
    if (devPanel) devPanel.appendChild(credit.cloneNode(true));
    // Add to transfer container
    const transfer = document.querySelector('.transfer-container');
    if (transfer) transfer.appendChild(credit.cloneNode(true));
    // Add to connection section
    const qr = document.querySelector('.qr-container');
    if (qr) qr.appendChild(credit.cloneNode(true));
});

// Global function for onclick handlers
window.simpleShare = null;

// Make loadFiles globally accessible
window.loadFiles = function() {
    if (simpleShare) {
        simpleShare.loadFiles();
    }
};