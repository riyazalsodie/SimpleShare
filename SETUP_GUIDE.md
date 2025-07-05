# 🚀 SimpleShare - Complete Setup Guide

**Owner: R ! Y 4 Z**

## 📋 Prerequisites

- **Windows 10/11** (or any OS with Python support)
- **Python 3.7+** installed
- **Internet connection** (for first-time setup)

## ⚡ Quick Start (Windows)

### Step 1: Download & Extract
1. Download the SimpleShare folder
2. Extract to any location (e.g., `C:\SimpleShare`)

### Step 2: One-Click Installation
1. **Double-click** `install.bat`
2. Wait for installation to complete
3. You'll see "Installation Complete!" when done

### Step 3: Start the Server
1. **Double-click** `start.bat`
2. Server will start automatically
3. Open your browser to `http://localhost:5000`

## 🔧 Manual Setup (All Platforms)

### Step 1: Install Python
- Download from: https://python.org
- Make sure to check "Add Python to PATH"

### Step 2: Install Dependencies
```bash
pip install flask flask-cors flask-socketio qrcode pillow psutil
```

### Step 3: Run the Server
```bash
python app.py
```

## 📱 How to Use

### For PC Users:
1. Open browser to `http://localhost:5000`
2. Drag files to the upload area
3. Files appear in the download list
4. Click download to get files

### For Phone Users:
1. Connect to same WiFi as PC
2. Scan QR code on the webpage
3. Upload files from your phone
4. Download files to your phone

## 🌐 Network Access

### Local Network (Recommended):
- Works on same WiFi network
- Fast and secure
- No internet required

### Internet Access (Advanced):
- Configure port forwarding on router
- Use your public IP address
- Works from anywhere

## 🔧 Configuration

### File Size Limits:
- **Unlimited**: No file size restrictions
- **Large Files**: Supported for all file types

### Port Settings:
- Default: Port 5000
- Edit `app.py` line 728 to change

### Theme Settings:
- Click the theme toggle button
- Choose from Sci-Fi, Day, or Night themes

## 🛠️ Troubleshooting

### "Python not found":
- Install Python from https://python.org
- Make sure to check "Add to PATH"

### "Port already in use":
- Close other applications using port 5000
- Or change port in `app.py`

### "QR code not working":
- Make sure phone and PC are on same WiFi
- Check firewall settings

### "Files not uploading":
- Check file size (max 5GB)
- Check file type (see allowed extensions)
- Check available disk space

## 📁 File Structure

```
SimpleShare/
├── app.py              # Main server file
├── install.bat         # Windows installer
├── start.bat          # Windows launcher
├── requirements.txt    # Python dependencies
├── static/            # Web assets
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript
│   ├── uploads/      # Uploaded files
│   └── downloads/    # Available files
└── templates/         # HTML templates
```

## 🔒 Security Features

- **Session-based authentication**
- **File type validation**
- **Size limits protection**
- **Real-time connection monitoring**

## 🎨 Features

- **Drag & Drop** file upload
- **QR Code** mobile connection
- **Real-time** progress updates
- **Multiple themes** (Sci-Fi, Day, Night)
- **Mobile-optimized** interface
- **Live uptime** counter
- **Device tracking**

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Ensure Python 3.7+ is installed
3. Run `install.bat` again
4. Check firewall settings

## 🎯 Credits

**Owner: R ! Y 4 Z**

SimpleShare - Making file transfer simple, secure, and stylish! 🚀

---

**Ready to share files like it's the future! 🚀** 