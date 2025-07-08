# SyftBox File Editor

A beautiful, modern file system browser and code editor for the SyftBox ecosystem. This editor provides a clean, intuitive interface for browsing directories and editing text files directly from your web browser.

## Features

### 🎨 Syft-Themed Design
- **Pastel Rainbow Colors**: Beautiful color palette extracted from the SyftBox logo
- **Authentic Branding**: Uses the actual `box.svg` logo with signature gradients
- **Modern UI**: Clean, responsive interface with smooth animations
- **Consistent Styling**: Matches the Syft ecosystem's design language

### 📁 File Management
- **Directory Navigation**: Intuitive file explorer with breadcrumb navigation
- **Smart Breadcrumbs**: Handles long paths with responsive wrapping and hover expansion
- **File Type Support**: Recognizes and handles various text file formats
- **Create Operations**: Create new files and directories directly from the interface

### ✏️ Code Editor
- **Syntax Highlighting**: Powered by Prism.js for various programming languages
- **Real-time Editing**: Instant feedback with modified state indicators
- **Auto-save**: Ctrl+S keyboard shortcut for quick saving
- **Cursor Position**: Live line and column tracking
- **File Info**: Display file size, type, and modification details

### 🔐 Security Features
- **Path Validation**: Prevents directory traversal attacks
- **File Type Restrictions**: Only allows editing of safe text file types
- **Size Limits**: Prevents loading of excessively large files
- **Permission Checks**: Respects file system permissions

### 📱 Responsive Design
- **Mobile-Friendly**: Works seamlessly on all screen sizes
- **Touch Support**: Optimized for touch interactions
- **Adaptive Layout**: Adjusts to different viewport sizes
- **Accessible**: Keyboard navigation and screen reader support

## Supported File Types

The editor supports a comprehensive list of text file formats:

### Programming Languages
- **Python**: `.py`
- **JavaScript/TypeScript**: `.js`, `.ts`, `.jsx`, `.tsx`
- **Web**: `.html`, `.css`, `.scss`, `.sass`
- **Config**: `.json`, `.yaml`, `.yml`, `.xml`, `.toml`
- **Documentation**: `.md`, `.txt`, `.rst`, `.tex`
- **Scripts**: `.sh`, `.bash`, `.zsh`, `.fish`, `.ps1`
- **And many more...**

### File Operations
- **Read**: Load file contents with encoding detection
- **Write**: Save changes with atomic operations
- **Create**: New files and directories
- **Delete**: Remove files and directories (with confirmation)
- **Navigate**: Browse directory structure

## API Endpoints

The editor communicates with the backend through these endpoints:

### Directory Operations
- `GET /api/filesystem/list?path={path}` - List directory contents
- `POST /api/filesystem/create-directory` - Create new directory

### File Operations
- `GET /api/filesystem/read?path={path}` - Read file contents
- `POST /api/filesystem/write` - Write file contents
- `DELETE /api/filesystem/delete?path={path}` - Delete file/directory

## Usage

### Basic Navigation
1. **Browse Files**: Click on folders to navigate directories
2. **Edit Files**: Click on text files to open them in the editor
3. **Navigate Back**: Use breadcrumb navigation to go to parent directories
4. **Create Content**: Use the "New File" or "New Folder" buttons

### Keyboard Shortcuts
- **Ctrl+S**: Save current file
- **Escape**: Close modals/dialogs
- **Tab**: Indent in editor
- **Shift+Tab**: Outdent in editor

### File Management
- **Create File**: Click "📄 New File" button and enter filename
- **Create Folder**: Click "📁 New Folder" button and enter folder name
- **Save Changes**: Click "💾 Save" button or use Ctrl+S
- **Track Changes**: Modified files show a dot (•) in the title

## Design Elements

### Color Palette
The editor uses a carefully crafted pastel color scheme:
- **Coral**: `rgb(220, 122, 110)` - Warm accent
- **Peach**: `rgb(246, 164, 100)` - Friendly highlight
- **Yellow**: `rgb(253, 197, 119)` - Attention-grabbing
- **Lime**: `rgb(185, 213, 153)` - Fresh accent
- **Mint**: `rgb(141, 204, 166)` - Calm success
- **Teal**: `rgb(92, 184, 183)` - Primary brand
- **Blue**: `rgb(76, 165, 184)` - Secondary brand
- **Lavender**: `rgb(117, 138, 168)` - Subtle accent
- **Pink**: `rgb(215, 104, 109)` - Error/warning
- **Magenta**: `rgb(198, 75, 119)` - Strong accent
- **Purple**: `rgb(162, 99, 142)` - Deep accent

### Interactive Elements
- **Hover Effects**: Smooth transitions on interactive elements
- **Gradient Backgrounds**: Subtle gradients using brand colors
- **Rainbow Header**: Animated rainbow gradient top border
- **Drop Shadows**: Subtle shadows for depth and hierarchy
- **Rounded Corners**: Consistent border radius throughout

## Technical Implementation

### Architecture
- **Backend**: Python FastAPI with secure file operations
- **Frontend**: Vanilla JavaScript with modern ES6+ features
- **Styling**: CSS custom properties with responsive design
- **Security**: Path validation, type checking, and permission handling

### Performance
- **Lazy Loading**: Files loaded only when accessed
- **Efficient Rendering**: Optimized DOM manipulation
- **Caching**: Smart caching of directory listings
- **Error Handling**: Graceful error recovery and user feedback

### Browser Support
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile, Firefox Mobile
- **Progressive Enhancement**: Graceful degradation for older browsers

## Customization

### Theming
The editor uses CSS custom properties for easy theming:
```css
:root {
  --primary: 76 165 184;
  --teal: 92 184 183;
  --mint: 141 204 166;
  /* ... more colors */
}
```

### Configuration
- **Base Path**: Restrict access to specific directories
- **File Size Limits**: Configurable maximum file size
- **Allowed Extensions**: Customizable file type whitelist
- **Auto-save**: Configurable auto-save intervals

## Security Considerations

### Path Security
- **Validation**: All paths are validated and resolved
- **Sandboxing**: Optional base path restriction
- **Traversal Protection**: Prevents `../` attacks

### File Type Security
- **Whitelist**: Only allowed file types can be edited
- **Binary Detection**: Prevents editing of binary files
- **Size Limits**: Prevents resource exhaustion

### Permission Handling
- **Respect System Permissions**: File operations respect OS permissions
- **Graceful Failures**: Clear error messages for permission issues
- **Audit Trail**: All operations can be logged

## Development

### Setup
1. Ensure FastAPI is installed and running
2. The editor is automatically available at `/editor`
3. API endpoints are mounted at `/api/filesystem/`

### Testing
- **Unit Tests**: Test file operations and validation
- **Integration Tests**: Test API endpoints
- **UI Tests**: Test browser functionality

### Contributing
- Follow the existing code style and patterns
- Add appropriate error handling
- Update documentation for new features
- Test thoroughly on multiple browsers

## Changelog

### Latest Version
- ✨ Complete UI revamp with Syft branding
- 🎨 Pastel rainbow color scheme
- 📱 Improved responsive design
- 🔧 Fixed breadcrumb navigation
- 🚀 Enhanced performance and accessibility
- 🛡️ Strengthened security measures

### Previous Versions
- Basic file editing functionality
- Directory navigation
- Simple dark theme
- Core API endpoints

## License

This file editor is part of the SyftBox ecosystem and follows the same licensing terms as the main project. 