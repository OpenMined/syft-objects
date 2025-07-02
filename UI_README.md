# Syft Objects UI

A web-based user interface for viewing and managing syft objects from the distributed file system.

## Features

- **Browse Objects**: View all syft objects in a clean table format
- **Search & Filter**: Search by keywords and filter by email addresses
- **Object Details**: View detailed information about each object including:
  - Metadata and permissions
  - File paths and existence status
  - Creation/update timestamps
  - File previews (when available)
- **Real-time Status**: Monitor SyftBox connection status
- **Refresh**: Manually refresh the objects collection

## Usage

### Running the UI

The UI is integrated into the syft-objects package and can be launched using the provided `run.sh` script:

```bash
./run.sh
```

This will:
1. Set up a Python virtual environment
2. Install backend dependencies
3. Install frontend dependencies 
4. Build the frontend
5. Start the combined backend/frontend server

The UI will be available at `http://localhost:8003` (or the port specified by `SYFTBOX_ASSIGNED_PORT`).

### SyftUI Integration

This UI is designed to work with SyftUI (the SyftBox app system). When deployed through SyftUI:
- The UI will automatically use the assigned port
- SyftBox integration will be automatically configured
- Objects will be loaded from the connected datasites

### API Endpoints

The backend provides a REST API with the following endpoints:

- `GET /api/status` - Get application and SyftBox status
- `GET /api/objects` - List objects with search/filter support
- `GET /api/objects/{uid}` - Get detailed object information  
- `GET /api/objects/refresh` - Refresh the objects collection
- `GET /api/metadata/emails` - Get unique email addresses
- `GET /api/metadata/names` - Get unique object names

### Object Information

The UI displays the following information for each syft object:

- **Index**: Position in the collection
- **Name**: Human-readable object name
- **Email**: Owner's email (extracted from syft:// URLs)
- **File Status**: Whether private and mock files exist
- **Creation Date**: When the object was created
- **Permissions**: Read/write permissions for different file types
- **Metadata**: Additional object metadata
- **File Previews**: Content preview for text files

## Architecture

- **Backend**: FastAPI server with syft-objects integration
- **Frontend**: Next.js React application with Tailwind CSS
- **Integration**: Follows syft-reviewer-allowlist methodology for SyftUI compatibility

## Development

### Backend Development

The backend is a FastAPI application in `backend/main.py`. It provides:
- REST API for object management
- SyftBox integration
- Static file serving for the frontend

### Frontend Development

The frontend is a Next.js application in the `frontend/` directory:

```bash
cd frontend
npm install
npm run dev    # Development server
npm run build  # Production build
```

### Dependencies

Backend dependencies are managed through `pyproject.toml`:
- FastAPI for the web server
- syft-objects for object management
- loguru for logging
- uvicorn for ASGI server

Frontend dependencies are managed through `package.json`:
- Next.js for the React framework  
- Tailwind CSS for styling
- Lucide React for icons

## Troubleshooting

### No Objects Displayed

- Check that SyftBox is running and connected
- Verify that datasites have objects in their `public/objects/` or `private/objects/` directories
- Use the "Refresh" button to reload objects

### Frontend Not Loading

- Ensure the frontend was built: `cd frontend && npm run build`
- Check that Node.js and npm are installed
- Verify no port conflicts on the assigned port

### Backend Errors

- Check that syft-objects package is properly installed
- Verify SyftBox client is available and configured
- Check logs for detailed error messages 