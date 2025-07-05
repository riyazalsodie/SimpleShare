# 🚀 SimpleShare - Futuristic File Transfer Application

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, sci-fi themed file transfer application that enables seamless file sharing between PC and mobile devices with a beautiful futuristic interface. **No file size limits, real-time updates, and cross-platform compatibility.**

## ✨ Features

- 🎨 **Futuristic UI** with sci-fi themes (Sci-fi, Day, Night)
- 📱 **Mobile-optimized** interface with touch gestures
- 🔗 **QR Code** connection for instant phone pairing
- 📁 **Drag & Drop** file upload with progress tracking
- ⚡ **Real-time** updates and live file synchronization
- 🌐 **Live uptime** counter and system monitoring
- 📊 **Device tracking** and connection status
- 🎯 **Session management** with secure authentication
- 📏 **Unlimited file sizes** - no restrictions
- 🔍 **File search** and filtering capabilities
- 📦 **ZIP downloads** for multiple files
- 🌍 **Cross-platform** - Windows, macOS, Linux

## 🚀 Quick Start

### Windows (Recommended)
```bash
# 1. Download and extract SimpleShare
# 2. Double-click start.bat
# 3. Open http://localhost:5000 in your browser
# 4. Scan QR code with your phone
```

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/riyazalsodie/SimpleShare.git
cd SimpleShare

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

## 📱 How to Use

### From PC to Phone
1. **Start the server** by running `start.bat` or `python app.py`
2. **Open browser** to `http://localhost:5000`
3. **Drag files** to the PC upload area
4. **Scan QR code** with your phone
5. **Download files** on your phone

### From Phone to PC
1. **Connect to same WiFi** as your PC
2. **Scan QR code** or enter server URL on phone
3. **Upload files** from your phone
4. **Download files** on your PC

## 🎨 Themes

- **🔮 Sci-Fi Theme**: Neon cyan/pink with grid animations and futuristic effects
- **☀️ Day Theme**: Clean blue/white interface for professional use
- **🌙 Night Theme**: Dark purple/blue interface for low-light environments

## ⚙️ Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| **Port** | 5000 | Server port (configurable) |
| **File Size** | Unlimited | No file size restrictions |
| **Authentication** | Enabled | Token System |
| **Real-time Updates** | Enabled | Live file synchronization |
| **Auto-refresh** | 10s | File list refresh interval |

## 📁 Project Structure

```
SimpleShare/
├── app.py                 # Main Flask server
├── config.py              # Configuration settings
├── start.bat             # Windows launcher (auto-installer)
├── requirements.txt       # Python dependencies
├── static/               # Web assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   ├── uploads/         # Phone uploads
│   └── downloads/       # PC uploads
├── templates/            # HTML templates
│   └── index.html       # Main interface
└── README.md            # This file
```

## 🛠️ System Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, Linux
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space
- **Network**: WiFi connection for phone access

## 🔧 Advanced Setup

### Custom Port
Edit `config.py`:
```python
SERVER_PORT = 8080  # Change to your preferred port
```

### Custom Authentication
Edit `app.py`:
```python
app.config['AUTH_PIN'] = 'your-pin-here'
```

### File Type Restrictions
Edit `config.py`:
```python
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'mp4', 'zip'}
```

## 🛠️ Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **Python not found** | Install from [python.org](https://python.org) |
| **Port already in use** | Change port in `config.py` or close other apps |
| **QR code not working** | Check WiFi connection and firewall settings |
| **Files not uploading** | Verify file type is supported |
| **Phone can't connect** | Ensure both devices are on same network |

### Debug Mode
```bash
# Enable debug mode for detailed logs
python app.py --debug
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Clone repository
git clone https://github.com/riyazalsodie/SimpleShare.git
cd SimpleShare

# Install development dependencies
pip install -r requirements.txt

# Run in development mode
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Web framework
- **SocketIO** - Real-time communication
- **QR Code** - Mobile connection
- **Pillow** - Image processing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/riyazalsodie/SimpleShare/issues)
- **Documentation**: [Wiki](https://github.com/riyazalsodie/SimpleShare/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/riyazalsodie/SimpleShare/discussions)

---

<div align="center">

**Made with ❤️ by R ! Y 4 Z**

*SimpleShare - Making file transfer simple, secure, and stylish! 🚀*

[![GitHub stars](https://img.shields.io/github/stars/riyazalsodie/SimpleShare.svg?style=social&label=Star)](https://github.com/riyazalsodie/SimpleShare)
[![GitHub forks](https://img.shields.io/github/forks/riyazalsodie/SimpleShare.svg?style=social&label=Fork)](https://github.com/riyazalsodie/SimpleShare)

</div> 
