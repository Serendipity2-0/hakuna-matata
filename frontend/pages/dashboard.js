// pages/dashboard.js
import withAuth from '../components/withAuth';
import LogoutButton from '../components/LogoutButton';
import { useState, useEffect } from 'react';
import axios from '../utils/axios';

const DashboardPage = ({ userRole }) => {
  const [documents, setDocuments] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [currentPath, setCurrentPath] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [documentContent, setDocumentContent] = useState('');

  const [pathSegments, setPathSegments] = useState(['']);
  const [createDir, setCreateDir] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadError, setUploadError] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');
  const [showUploadForm, setShowUploadForm] = useState(false);

  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('/view-docs');
      setDocuments(response.data.documents);
      
      // Extract unique departments
      const uniqueDepartments = [...new Set(response.data.documents.map(doc => doc.department))];
      setDepartments(uniqueDepartments.filter(dept => dept !== 'root'));
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  // Get folders for current path
  const getCurrentFolders = () => {
    if (!selectedDepartment) return [];

    const departmentDocs = documents.filter(doc => doc.department === selectedDepartment);
    const currentFullPath = [selectedDepartment, ...currentPath].join('/');
    
    const folders = new Set();
    const currentLevel = currentPath.length + 1; // +1 because department is first level
    
    departmentDocs.forEach(doc => {
      // Split the path into segments
      const pathSegments = doc.path.split('/');
      
      // Only process if the path has enough segments and starts with current path
      if (pathSegments.length >= currentLevel && doc.path.startsWith(currentFullPath)) {
        // Get the segment at current level
        const segmentAtCurrentLevel = pathSegments[currentLevel];
        if (segmentAtCurrentLevel) {
          folders.add(segmentAtCurrentLevel);
        }
      }
    });

    return Array.from(folders);
  };

  // Handle folder/file selection
  const handlePathSelect = async (item) => {
    const newPath = [...currentPath, item];
    const fullPath = [selectedDepartment, ...newPath].join('/');
    
    // Check if it's a markdown file
    if (item.endsWith('.md')) {
      try {
        const response = await axios.get(`/view-doc/${fullPath}`);
        setSelectedDocument(item);
        setDocumentContent(response.data.content);
      } catch (error) {
        console.error('Error fetching document:', error);
      }
    } else {
      setCurrentPath(newPath);
      setSelectedDocument(null);
      setDocumentContent('');
    }
  };

  const handleAddPathSegment = () => {
    setPathSegments([...pathSegments, '']);
  };

  const handleRemovePathSegment = (index) => {
    const newSegments = [...pathSegments];
    newSegments.splice(index, 1);
    setPathSegments(newSegments);
  };

  const handlePathSegmentChange = (index, value) => {
    const newSegments = [...pathSegments];
    newSegments[index] = value;
    setPathSegments(newSegments);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    setUploadError('');
    setUploadSuccess('');

    if (!file) {
      setUploadError('Please select a file to upload.');
      return;
    }

    let filePath = '';
    if (userRole === 'Admin') {
      if (!selectedDepartment) {
        setUploadError('Please select a department.');
        return;
      }
      filePath += selectedDepartment + '/';
    }
    filePath += pathSegments.filter(segment => segment).join('/');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('file_path', filePath);
      formData.append('create_dir', createDir);

      const response = await axios.post('/upload-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });

      setUploadSuccess('File uploaded successfully!');
      setFile(null);
      setPathSegments(['']);
      setCreateDir(false);
      fetchDocuments(); // Refresh the document list
    } catch (error) {
      console.error('Upload error:', error);
      setUploadError(error.response?.data?.detail || 'An error occurred during upload.');
    }
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1>Dashboard</h1>
          <div className="header-actions">
            <button 
              onClick={() => setShowUploadForm(!showUploadForm)}
              className="upload-toggle-btn"
            >
              {showUploadForm ? 'Hide Upload Form' : 'Show Upload Form'}
            </button>
            <LogoutButton />
          </div>
        </div>
        <div className="department-nav">
          {departments.map(dept => (
            <button
              key={dept}
              onClick={() => {
                setSelectedDepartment(dept);
                setCurrentPath([]);
                setSelectedDocument(null);
              }}
              className={selectedDepartment === dept ? 'active' : ''}
            >
              {dept}
            </button>
          ))}
        </div>
      </header>

      <div className="content-container">
        {/* Upload Form */}
        {showUploadForm && (
          <div className="upload-form-container">
            <form onSubmit={handleUploadSubmit} className="upload-form">
              {userRole === 'Admin' && (
                <div className="form-group">
                  <label>Department:</label>
                  <select
                    value={selectedDepartment}
                    onChange={(e) => setSelectedDepartment(e.target.value)}
                    required
                  >
                    <option value="">-- Select Department --</option>
                    {departments.map((dept) => (
                      <option key={dept} value={dept}>
                        {dept}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              <div className="form-group">
                <label>File Path Segments:</label>
                {pathSegments.map((segment, index) => (
                  <div key={index} className="path-segment">
                    <input
                      type="text"
                      value={segment}
                      onChange={(e) => handlePathSegmentChange(index, e.target.value)}
                      placeholder="Enter path segment"
                      required
                    />
                    {index === pathSegments.length - 1 && (
                      <button type="button" onClick={handleAddPathSegment} className="icon-button">
                        +
                      </button>
                    )}
                    {pathSegments.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemovePathSegment(index)}
                        className="icon-button remove"
                      >
                        -
                      </button>
                    )}
                  </div>
                ))}
              </div>

              <div className="form-group checkbox">
                <label>
                  <input
                    type="checkbox"
                    checked={createDir}
                    onChange={(e) => setCreateDir(e.target.checked)}
                  />
                  Create directory if it doesn't exist
                </label>
              </div>

              <div className="form-group">
                <label>
                  Select File (.md only):
                  <input
                    type="file"
                    accept=".md"
                    onChange={handleFileChange}
                    required
                  />
                </label>
              </div>

              {uploadError && <p className="error">{uploadError}</p>}
              {uploadSuccess && <p className="success">{uploadSuccess}</p>}

              <button type="submit" className="submit-button">
                Upload File
              </button>
            </form>
          </div>
        )}

        {/* Sidebar */}
        {selectedDepartment && (
          <div className="sidebar">
            <div className="breadcrumb">
              <span onClick={() => {
                setCurrentPath([]);
                setSelectedDocument(null);
              }}>
                {selectedDepartment}
              </span>
              {currentPath.map((path, index) => (
                <span key={index}>
                  {' > '}
                  <span onClick={() => {
                    setCurrentPath(currentPath.slice(0, index + 1));
                    setSelectedDocument(null);
                  }}>
                    {path}
                  </span>
                </span>
              ))}
            </div>
            <div className="folder-list">
              {getCurrentFolders().map(folder => (
                <div
                  key={folder}
                  className="folder-item"
                  onClick={() => handlePathSelect(folder)}
                >
                  {folder}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="main-content">
          {selectedDocument ? (
            <div className="document-viewer">
              <h2>{selectedDocument}</h2>
              <pre>{documentContent}</pre>
            </div>
          ) : (
            <div className="welcome-message">
              {!selectedDepartment 
                ? "Please select a department from the header"
                : "Select a folder or document from the sidebar"}
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .dashboard-container {
          height: 100vh;
          display: flex;
          flex-direction: column;
        }
        .header {
          background: #f5f5f5;
          padding: 1rem;
          border-bottom: 1px solid #ddd;
        }
        .department-nav {
          display: flex;
          gap: 1rem;
          margin: 1rem 0;
        }
        .department-nav button {
          padding: 0.5rem 1rem;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          background: #fff;
        }
        .department-nav button.active {
          background: #0070f3;
          color: white;
        }
        .content-container {
          display: flex;
          flex: 1;
          overflow: hidden;
        }
        .sidebar {
          width: 250px;
          border-right: 1px solid #ddd;
          padding: 1rem;
          overflow-y: auto;
        }
        .breadcrumb {
          margin-bottom: 1rem;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid #ddd;
        }
        .breadcrumb span {
          cursor: pointer;
          color: #0070f3;
        }
        .folder-list {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .folder-item {
          padding: 0.5rem;
          cursor: pointer;
          border-radius: 4px;
        }
        .folder-item:hover {
          background: #f5f5f5;
        }
        .main-content {
          flex: 1;
          padding: 1rem;
          overflow-y: auto;
        }
        .document-viewer {
          background: white;
          padding: 1rem;
          border-radius: 4px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .document-viewer pre {
          white-space: pre-wrap;
          word-wrap: break-word;
        }
        .welcome-message {
          text-align: center;
          margin-top: 2rem;
          color: #666;
        }

        .header-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-actions {
          display: flex;
          gap: 1rem;
        }

        .upload-toggle-btn {
          padding: 0.5rem 1rem;
          background: #0070f3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .upload-form-container {
          background: #f9f9f9;
          padding: 1rem;
          border-bottom: 1px solid #ddd;
        }

        .upload-form {
          max-width: 600px;
          margin: 0 auto;
        }

        .form-group {
          margin-bottom: 1rem;
        }

        .path-segment {
          display: flex;
          gap: 0.5rem;
          margin-bottom: 0.5rem;
        }

        .icon-button {
          padding: 0.25rem 0.5rem;
          background: #0070f3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .icon-button.remove {
          background: #ff4444;
        }

        .checkbox {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .submit-button {
          width: 100%;
          padding: 0.5rem;
          background: #0070f3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .error {
          color: #ff4444;
          margin: 0.5rem 0;
        }

        .success {
          color: #4caf50;
          margin: 0.5rem 0;
        }
      `}</style>
    </div>
  );
};

export default withAuth(DashboardPage);