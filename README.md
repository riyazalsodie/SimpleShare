# SimpleShare - Futuristic File Transfer Application

**Owner: R ! Y 4 Z**

A modern, sci-fi themed file transfer application that allows seamless file sharing between PC and mobile devices with a beautiful futuristic interface.

## ⚡ Quick Start (Windows)

1. **Download** the SimpleShare folder
2. **Double-click** `install.bat` to install dependencies
3. **Double-click** `start.bat` to start the server
4. **Open browser** to `http://localhost:5000`

That's it! 🚀

## 📱 Features

- **🎨 Futuristic UI** with sci-fi themes
- **📱 Mobile-optimized** interface
- **🔗 QR Code** connection for phones
- **📁 Drag & Drop** file upload
- **⚡ Real-time** progress updates
- **🌐 Live uptime** counter
- **📊 Device tracking**
- **🎯 Session management**
- **📱 Touch-friendly** mobile interface

## 🛠️ Installation

### Windows (Recommended)
```bash
# Just double-click these files:
install.bat    # Install dependencies
start.bat      # Start the server
```

### Manual Installation
```bash
# Install Python dependencies
pip install flask flask-cors flask-socketio qrcode pillow psutil

# Start the server
python app.py
```

## 📖 How to Use

### For PC Users:
1. Open `http://localhost:5000` in your browser
2. Drag files to the upload area
3. Files appear in the download list
4. Click download to get files

### For Phone Users:
1. Connect to same WiFi as PC
2. Scan the QR code on the webpage
3. Upload files from your phone
4. Download files to your phone

## 🎨 Themes

- **Sci-Fi Theme**: Neon cyan/pink with grid animations
- **Day Theme**: Clean blue/white interface
- **Night Theme**: Dark purple/blue interface

## 🔧 Configuration

- **File Size Limit**: Unlimited (no size restrictions)
- **Port**: 5000 (configurable)
- **Supported Formats**: Images, Videos, Documents, Archives

## 📁 File Structure

```
SimpleShare/
├── app.py              # Main server
├── install.bat         # Windows installer
├── start.bat          # Windows launcher
├── SETUP_GUIDE.md     # Complete setup guide
├── static/            # Web assets
└── templates/         # HTML templates
```

## 🛠️ Troubleshooting

- **Python not found**: Install from https://python.org
- **Port in use**: Close other apps or change port
- **QR not working**: Check WiFi connection
- **Files not uploading**: Check size and type limits

## 🎯 Credits

**Owner: R ! Y 4 Z**

SimpleShare - Making file transfer simple, secure, and stylish! 🚀

---

**Ready to share files like it's the future! 🚀**

**Owner: R ! Y 4 Z** 
