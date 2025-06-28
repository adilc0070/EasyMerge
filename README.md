# File Merger Studio

A modern, professional desktop application for merging PDF and Excel files with an intuitive dark-themed interface.

## ✨ Features

### 📄 PDF Merger
- Merge multiple PDF files into a single document
- Maintain original formatting and quality
- Preserve file order and structure
- Support for all standard PDF formats

### 📊 Excel Merger
- Combine multiple Excel files (.xlsx, .xls) into one workbook
- Automatically add source file tracking
- Preserve data integrity and formatting
- Handle multiple sheets and complex data

### 🎨 Modern Interface
- **Dark Theme**: Professional appearance with reduced eye strain
- **Intuitive Design**: Clean, modern UI inspired by contemporary applications
- **Tab-Based Navigation**: Easy switching between PDF and Excel modes
- **Real-time Progress**: Visual feedback during file processing
- **Drag & Drop Ready**: Interface designed for future drag-and-drop functionality

### 🔧 Advanced Features
- **Session Persistence**: Remembers your file selections between sessions
- **File Management**: Easy add/remove files with visual feedback
- **Size Information**: Displays individual file sizes and total size
- **Error Handling**: Comprehensive error messages and recovery
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 7+, macOS 10.12+, or Linux
- **Python**: 3.7 or higher
- **Memory**: 2GB RAM minimum
- **Storage**: 50MB free space

### Python Dependencies
```
tkinter (included with Python)
PyPDF2>=3.0.0
pandas>=1.3.0
openpyxl>=3.0.0
```

## 🚀 Installation

### Method 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/adilc0070/EasyMerge.git
cd EasyMerge

# Install dependencies
pip install -r requirements.txt

# Run the application
python EasyMerge.py
```

### Method 2: Direct Download
1. Download the latest release from [Releases](https://github.com/adilc0070/EasyMerge/releases)
2. Extract the ZIP file
3. Install dependencies: `pip install PyPDF2 pandas openpyxl`
4. Run: `python EasyMerge.py`

### Method 3: Create Executable (Optional)
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed EasyMerge.py

# Find executable in dist/ folder
```

## 📖 Usage Guide

### Getting Started
1. **Launch the Application**
   ```bash
   python EasyMerge.py
   ```

2. **Select File Type**
   - Click "📄 PDF Merger" for PDF files
   - Click "📊 Excel Merger" for Excel files

3. **Add Files**
   - Click "Select Files" button
   - Choose multiple files from your computer
   - Files will appear in the list below

4. **Manage Files**
   - Remove individual files using the ✕ button
   - Clear all files with "Clear All" button
   - View file details (name, path, size)

5. **Merge Files**
   - Click "🔗 Merge Files" button
   - Choose output location and filename
   - Watch the progress bar for completion

### PDF Merger Usage
```python
# Example: Merging presentation slides
Files: slide1.pdf, slide2.pdf, slide3.pdf
Output: complete_presentation.pdf
```

### Excel Merger Usage
```python
# Example: Combining monthly reports
Files: january.xlsx, february.xlsx, march.xlsx
Output: quarterly_report.xlsx
# Note: Source file names are automatically added as a column
```

## 🎨 Interface Overview

### Main Components
- **Header**: Application title and description
- **Tab Navigation**: Switch between PDF and Excel modes
- **Upload Section**: File selection area with clear instructions
- **File List**: Scrollable list of selected files with details
- **Progress Bar**: Shows processing status during operations
- **Action Buttons**: Merge files and clear selection options

### Color Scheme
- **Background**: `#1a1a1a` (Dark)
- **Surface**: `#2d2d2d` (Medium Dark)
- **Primary**: `#3b82f6` (Blue)
- **Success**: `#10b981` (Green)
- **Danger**: `#ef4444` (Red)
- **Text**: `#ffffff` (White)

## ⚙️ Configuration

### Session Files
The application creates a `session.json` file to remember your selections:
```json
{
  "pdf_files": ["path/to/file1.pdf", "path/to/file2.pdf"],
  "excel_files": ["path/to/file1.xlsx", "path/to/file2.xlsx"],
  "current_tab": "pdf"
}
```

### Customization
You can modify the application by editing these sections:
- **Colors**: Update the `colors` dictionary in `setup_styles()`
- **Fonts**: Modify font specifications in style configurations
- **Window Size**: Change `geometry()` parameters

## 🛠️ Development

### Project Structure
```
EasyMerge/
├── EasyMerge.py          # Main application file
├── requirements.txt        # Python dependencies
├── session.json           # Session data (auto-generated)
├── README.md              # Documentation
└── assets/                # Screenshots and resources
```

### Code Architecture
- **ModernFileManager**: Main application class
- **UI Components**: Modular interface sections
- **File Operations**: PDF and Excel processing logic
- **Session Management**: Save/load functionality

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**"Module not found" Error**
```bash
# Install missing dependencies
pip install PyPDF2 pandas openpyxl
```

**"Permission denied" Error**
- Make sure you have write permissions to the output directory
- Try running as administrator (Windows) or with sudo (macOS/Linux)

**Files not merging properly**
- Ensure all files are valid and not corrupted
- Check that PDF files are not password-protected
- Verify Excel files are in supported formats (.xlsx, .xls)

**Application won't start**
- Check Python version: `python --version` (requires 3.7+)
- Verify tkinter installation: `python -c "import tkinter"`
- Update pip: `pip install --upgrade pip`

### Performance Tips
- **Large Files**: For files over 100MB, allow extra processing time
- **Memory**: Close other applications when merging many large files
- **Storage**: Ensure sufficient disk space (at least 2x total file size)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🤝 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/adilc0070/EasyMerge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/adilc0070/EasyMerge/discussions)
- **Email**: [Contact adilc0070](mailto:adilc0070@gmail.com)

### Funding
If you find this project useful, consider supporting development:
- ⭐ Star the repository
- 🐛 Report bugs and suggest features
- 💝 [Sponsor on GitHub](https://github.com/sponsors/adilc0070)

## 🎉 Acknowledgments

- **PyPDF2**: For excellent PDF manipulation capabilities
- **Pandas**: For powerful Excel data processing
- **Tkinter**: For the GUI framework
- **Community**: For feedback and contributions

---

**Made with ❤️ by [adilc0070](https://github.com/adilc0070)**

*Transform your file management workflow with File Merger Studio*