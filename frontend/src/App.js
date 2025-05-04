import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import BusinessSetup from './pages/BusinessSetup';
import MessageHistory from './pages/MessageHistory';
import ContextUpload from './pages/ContextUpload';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/business/setup" element={<BusinessSetup />} />
            <Route path="/messages/:phoneNumber" element={<MessageHistory />} />
            <Route path="/context/upload" element={<ContextUpload />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 