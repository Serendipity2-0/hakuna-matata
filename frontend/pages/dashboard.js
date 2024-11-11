// pages/dashboard.js
import withAuth from '../components/withAuth';
import LogoutButton from '../components/LogoutButton';
import { useState, useEffect } from 'react';
import axios from '../utils/axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

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

  const [expandedFolders, setExpandedFolders] = useState(new Set());

  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, [userRole]);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('/view-docs');
      setDocuments(response.data.documents);
      
      if (userRole === 'Admin') {
        // Extract unique departments for admin
        const uniqueDepartments = [...new Set(response.data.documents.map(doc => doc.department))];
        setDepartments(uniqueDepartments.filter(dept => dept !== 'root'));
      } else {
        // For non-admin users, set their department automatically
        const userDepartment = response.data.department;
        setSelectedDepartment(userDepartment);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  // Modified getCurrentFolders to get items at specific path
  const getItemsAtPath = (path) => {
    if (!selectedDepartment) return { folders: [], files: [] };

    const departmentDocs = documents.filter(doc => doc.department === selectedDepartment);
    const currentFullPath = path.join('/');
    
    const folders = new Set();
    const files = new Set();
    
    departmentDocs.forEach(doc => {
      // Remove department from path for comparison
      const relativePath = doc.path.substring(selectedDepartment.length + 1);
      const segments = relativePath.split('/');
      
      // Check if this document is in the current path
      const currentPathStr = path.slice(1).join('/'); // Remove department from comparison
      if (relativePath.startsWith(currentPathStr)) {
        // Get the next segment after current path
        const nextSegmentIndex = path.length - 1;
        const nextSegment = segments[nextSegmentIndex];
        
        if (nextSegment) {
          if (nextSegment.endsWith('.md')) {
            files.add(nextSegment);
          } else {
            folders.add(nextSegment);
          }
        }
      }
    });

    return {
      folders: Array.from(folders),
      files: Array.from(files)
    };
  };

  const toggleFolder = (folderPath) => {
    const pathKey = folderPath.join('/');
    setExpandedFolders(prev => {
      const newSet = new Set(prev);
      if (newSet.has(pathKey)) {
        newSet.delete(pathKey);
      } else {
        newSet.add(pathKey);
      }
      return newSet;
    });
  };

  const FolderTree = ({ path = [selectedDepartment] }) => {
    const { folders, files } = getItemsAtPath(path);
    const pathKey = path.join('/');
    const isExpanded = expandedFolders.has(pathKey);
    const isRoot = path.length === 1;

    return (
      <div className="folder-tree">
        {!isRoot && (
          <div 
            className="folder-item"
            onClick={(e) => {
              e.stopPropagation();
              toggleFolder(path);
            }}
          >
            <span className="folder-icon">{isExpanded ? '▼' : '▶'}</span>
            <span className="folder-name">{path[path.length - 1]}</span>
          </div>
        )}
        
        {(isRoot || isExpanded) && (
          <div className="folder-content" style={{ marginLeft: '20px' }}>
            {folders.map(folder => (
              <FolderTree 
                key={`${pathKey}/${folder}`} 
                path={[...path, folder]} 
              />
            ))}
            {files.map(file => (
              <div 
                key={file}
                className="file-item"
                onClick={() => handlePathSelect([...path, file].join('/'))}
              >
                <span className="file-icon">📄</span>
                <span className="file-name">{file}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  // Handle folder/file selection
  const handlePathSelect = async (fullPath) => {
    try {
      const response = await axios.get(`/view-doc/${fullPath}`);
      setSelectedDocument(fullPath.split('/').pop()); // Get filename
      setDocumentContent(response.data.content);
    } catch (error) {
      console.error('Error fetching document:', error);
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
        {/* Only show department navigation for Admin */}
        {userRole === 'Admin' && (
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
        )}
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

        {/* Modified Sidebar */}
        {selectedDepartment && (
          <div className="sidebar">
            <div className="folder-browser">
              <FolderTree />
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="main-content">
          {selectedDocument ? (
            <div className="document-viewer">
              <h2>{selectedDocument}</h2>
              <div className="markdown-content">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    // Custom components for markdown elements
                    h1: ({node, ...props}) => <h1 className="md-h1" {...props} />,
                    h2: ({node, ...props}) => <h2 className="md-h2" {...props} />,
                    h3: ({node, ...props}) => <h3 className="md-h3" {...props} />,
                    p: ({node, ...props}) => <p className="md-p" {...props} />,
                    ul: ({node, ...props}) => <ul className="md-ul" {...props} />,
                    ol: ({node, ...props}) => <ol className="md-ol" {...props} />,
                    li: ({node, ...props}) => <li className="md-li" {...props} />,
                    code: ({node, inline, ...props}) => (
                      <code className={`md-code ${inline ? 'inline' : 'block'}`} {...props} />
                    ),
                    pre: ({node, ...props}) => <pre className="md-pre" {...props} />,
                    blockquote: ({node, ...props}) => <blockquote className="md-blockquote" {...props} />,
                    table: ({node, ...props}) => <table className="md-table" {...props} />,
                    th: ({node, ...props}) => <th className="md-th" {...props} />,
                    td: ({node, ...props}) => <td className="md-td" {...props} />,
                  }}
                >
                  {documentContent}
                </ReactMarkdown>
              </div>
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

      <style jsx global>{`
        /* Markdown Styles */
        .markdown-content {
          padding: 20px;
          line-height: 1.6;
          color: #333;
        }

        .md-h1 {
          font-size: 2em;
          margin-bottom: 0.5em;
          padding-bottom: 0.3em;
          border-bottom: 1px solid #eaecef;
        }

        .md-h2 {
          font-size: 1.5em;
          margin-top: 1em;
          margin-bottom: 0.5em;
          padding-bottom: 0.3em;
          border-bottom: 1px solid #eaecef;
        }

        .md-h3 {
          font-size: 1.25em;
          margin-top: 1em;
          margin-bottom: 0.5em;
        }

        .md-p {
          margin-bottom: 1em;
        }

        .md-ul, .md-ol {
          padding-left: 2em;
          margin-bottom: 1em;
        }

        .md-li {
          margin-bottom: 0.5em;
        }

        .md-code {
          font-family: 'Consolas', 'Monaco', 'Andale Mono', monospace;
          background-color: #f6f8fa;
          border-radius: 3px;
          padding: 0.2em 0.4em;
        }

        .md-code.block {
          display: block;
          padding: 1em;
          margin: 1em 0;
          overflow-x: auto;
        }

        .md-pre {
          background-color: #f6f8fa;
          border-radius: 3px;
          padding: 16px;
          overflow: auto;
        }

        .md-blockquote {
          padding: 0 1em;
          color: #6a737d;
          border-left: 0.25em solid #dfe2e5;
          margin: 1em 0;
        }

        .md-table {
          border-collapse: collapse;
          width: 100%;
          margin: 1em 0;
        }

        .md-th, .md-td {
          padding: 6px 13px;
          border: 1px solid #dfe2e5;
        }

        .md-th {
          background-color: #f6f8fa;
          font-weight: 600;
        }

        /* Syntax highlighting */
        .md-code .keyword {
          color: #d73a49;
        }

        .md-code .string {
          color: #032f62;
        }

        .md-code .comment {
          color: #6a737d;
        }

        /* Links */
        .markdown-content a {
          color: #0366d6;
          text-decoration: none;
        }

        .markdown-content a:hover {
          text-decoration: underline;
        }

        /* Images */
        .markdown-content img {
          max-width: 100%;
          height: auto;
        }
      `}</style>

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

        .folder-tree {
          font-family: monospace;
          user-select: none;
          -webkit-user-select: none; /* Safari */
          -moz-user-select: none; /* Firefox */
          -ms-user-select: none; /* IE10+/Edge */
        }

        .folder-item {
          padding: 4px 0;
          display: flex;
          align-items: center;
          cursor: pointer;
        }

        .folder-icon {
          margin-right: 8px;
          font-size: 12px;
          width: 12px;
          display: inline-block;
          color: #0070f3;
          cursor: pointer;
          pointer-events: none;
        }

        .folder-name {
          color: #0070f3;
          cursor: pointer;
          pointer-events: none;
        }

        .folder-content {
          border-left: 1px dashed #ccc;
          margin-left: 6px;
          padding-left: 14px;
        }

        .file-item {
          padding: 4px 0;
          display: flex;
          align-items: center;
          cursor: pointer;
        }

        .file-icon {
          margin-right: 8px;
          font-size: 14px;
          pointer-events: none;
        }

        .file-name {
          color: #666;
          cursor: pointer;
          pointer-events: none;
        }

        .file-item:hover .file-name {
          color: #0070f3;
        }

        .document-viewer {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .document-viewer h2 {
          margin-bottom: 20px;
          padding-bottom: 10px;
          border-bottom: 1px solid #eee;
        }

        .document-viewer pre {
          white-space: pre-wrap;
          word-wrap: break-word;
          font-family: inherit;
          line-height: 1.6;
        }
      `}</style>
    </div>
  );
};

export default withAuth(DashboardPage);