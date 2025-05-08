import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import styles from './Dashboard.module.css';
// Make sure you have Bootstrap installed:
// npm install bootstrap
// And imported in your main index.js or App.js file:
// import 'bootstrap/dist/css/bootstrap.min.css';

const Dashboard = () => {
  // Sample data - in a real app, this would come from your backend
  const [files, setFiles] = useState([
    { id: 1, name: 'business_faq.pdf', size: '1.2 MB', uploadDate: '2025-05-01' },
    { id: 2, name: 'product_details.docx', size: '850 KB', uploadDate: '2025-05-03' },
    { id: 3, name: 'service_info.txt', size: '120 KB', uploadDate: '2025-05-07' }
  ]);
  
  const [conversations, setConversations] = useState([
    { id: 101, customer: 'John Doe', phone: '+15551234567', lastMessage: 'When are you open today?', time: '10:30 AM', unread: true },
    { id: 102, customer: 'Alice Smith', phone: '+15559876543', lastMessage: 'Thanks for the information!', time: 'Yesterday', unread: false },
    { id: 103, customer: 'Bob Johnson', phone: '+15552345678', lastMessage: 'Is the blue model in stock?', time: 'May 6', unread: true },
    { id: 104, customer: 'Emily Wilson', phone: '+15553456789', lastMessage: "I'd like to schedule an appointment.", time: 'May 5', unread: false }
  ]);
  
  const fileInputRef = useRef(null);

  // Handle file upload
  const handleFileUpload = (e) => {
    const uploadedFiles = Array.from(e.target.files);
    
    if (uploadedFiles.length > 0) {
      const newFiles = uploadedFiles.map((file, index) => {
        return {
          id: Date.now() + index, // Generate unique ID
          name: file.name,
          size: formatFileSize(file.size),
          uploadDate: new Date().toISOString().split('T')[0]
        };
      });
      
      setFiles([...newFiles, ...files]);
      
      // Reset file input
      e.target.value = null;
    }
  };

  // Format file size
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else if (bytes < 1073741824) return (bytes / 1048576).toFixed(1) + ' MB';
    else return (bytes / 1073741824).toFixed(1) + ' GB';
  };

  // Handle file deletion
  const deleteFile = (id) => {
    setFiles(files.filter(file => file.id !== id));
  };

  // Trigger file input dialog
  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className={`dashboard-container ${styles.dashboardContainer}`}>
      <div className="container-fluid p-0">
        {/* Banner */}
        <header className={`shadow-sm sticky-top ${styles.loomGradient}`}>
          <div className="container-fluid px-4">
            <div className="row py-3 align-items-center">
              <div className="col">
                <h1 className="h3 m-0 text-white fw-bold">ReplyGenius</h1>
              </div>
              <div className="col-auto">
                <Link to="/profile" className="btn btn-outline-light text-white d-flex align-items-center">
                  <div className="rounded-circle bg-white text-primary d-flex align-items-center justify-content-center me-2" style={{ width: '36px', height: '36px' }}>
                    <span>JS</span>
                  </div>
                  <span className="d-none d-md-inline">View Profile</span>
                </Link>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container-fluid px-4 py-4">
          <div className="row g-4">

            {/* Conversations List */}
            <div className="col-12">
              <div className="card shadow-sm">
                <div className="card-body">
                  <h2 className="card-title h5 mb-1">Recent Conversations</h2>
                  <p className="text-muted small mb-4">
                    View and manage conversations with your customers.
                  </p>
                  
                  {conversations.length > 0 ? (
                    <div className="list-group mb-3">
                      {conversations.map(conversation => (
                        <Link 
                          to={`/conversation/${conversation.id}`} 
                          key={conversation.id} 
                          className="list-group-item list-group-item-action d-flex py-3 px-3 border rounded mb-2"
                        >
                          <div className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-3 flex-shrink-0" style={{ width: '48px', height: '48px' }}>
                            {conversation.customer.substring(0, 2)}
                          </div>
                          <div className="flex-grow-1 min-width-0">
                            <div className="d-flex justify-content-between align-items-center mb-1">
                              <span className="fw-medium">{conversation.customer}</span>
                              <small className="text-muted">{conversation.time}</small>
                            </div>
                            <div className="text-muted small mb-1">{conversation.phone}</div>
                            <div className="small text-truncate d-flex align-items-center">
                              <span className="text-truncate">{conversation.lastMessage}</span>
                              {conversation.unread && (
                                <span className="ms-2 bg-primary rounded-circle flex-shrink-0" style={{ width: '8px', height: '8px' }}></span>
                              )}
                            </div>
                          </div>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-4 text-muted">
                      <p>No conversations yet</p>
                    </div>
                  )}
                  
                  <div className="text-center">
                    <Link to="/conversations" className="text-decoration-none text-primary fw-medium">
                      View All Conversations →
                    </Link>
                  </div>
                </div>
              </div>
            </div>
            {/* Business Information Section */}
            <div className="col-12">
              <div className="card shadow-sm">
                <div className="card-body">
                  <h2 className="card-title h5 mb-1">Business Information</h2>
                  <p className="text-muted small mb-4">
                    Upload documents about your business to help AI generate more accurate responses.
                  </p>
                  
                  {/* File Upload Box */}
                  <div 
                    className="border border-2 border-dashed rounded p-4 text-center bg-light mb-4 cursor-pointer"
                    onClick={triggerFileInput}
                    style={{ cursor: 'pointer' }}
                  >
                    <div className="py-3">
                      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary mb-3">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="17 8 12 3 7 8"></polyline>
                        <line x1="12" y1="3" x2="12" y2="15"></line>
                      </svg>
                      <p className="mb-1 fw-medium">Drop files here or click to upload</p>
                      <p className="text-muted small mb-0">Supported formats: PDF, DOC, DOCX, TXT, CSV</p>
                      <input 
                        type="file" 
                        ref={fileInputRef} 
                        onChange={handleFileUpload} 
                        className="d-none"
                        multiple
                      />
                    </div>
                  </div>
                  
                  {/* File List */}
                  <div className="mt-4">
                    <h3 className="h6 mb-3">Uploaded Documents</h3>
                    
                    {files.length > 0 ? (
                      <div className="list-group">
                        {files.map(file => (
                          <div key={file.id} className="list-group-item list-group-item-action d-flex align-items-center position-relative border rounded mb-2">
                            <div className="text-primary me-3">
                              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                                <line x1="16" y1="13" x2="8" y2="13"></line>
                                <line x1="16" y1="17" x2="8" y2="17"></line>
                                <polyline points="10 9 9 9 8 9"></polyline>
                              </svg>
                            </div>
                            <div className="flex-grow-1">
                              <div className="fw-medium">{file.name}</div>
                              <div className="small text-muted">
                                <span className="me-2">{file.size}</span>
                                <span>Uploaded on {file.uploadDate}</span>
                              </div>
                            </div>
                            <button 
                              className="btn btn-sm btn-outline-danger delete-file-btn opacity-0 position-absolute end-0 me-2"
                              onClick={(e) => {
                                e.preventDefault();
                                deleteFile(file.id);
                              }}
                              aria-label={`Delete ${file.name}`}
                              style={{ transition: 'opacity 0.2s ease' }}
                            >
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="3 6 5 6 21 6"></polyline>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                                <line x1="10" y1="11" x2="10" y2="17"></line>
                                <line x1="14" y1="11" x2="14" y2="17"></line>
                              </svg>
                            </button>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center py-4 text-muted">
                        <p>No documents uploaded yet</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;