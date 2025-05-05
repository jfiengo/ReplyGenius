import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';
import ThemeToggle from '../components/ThemeToggle';
import { ThemeContext } from '../context/ThemeContext';

const Home = () => {
  const { isDarkMode } = useContext(ThemeContext);
  
  return (
    <div className="home-container">
      <div className="theme-toggle-wrapper">
        <ThemeToggle />
      </div>
      
      <header className="hero-section">
        <div className="hero-content">
          <h1>ReplyGenius</h1>
          <h2>The SMS AI platform built for business</h2>
          <p>ReplyGenius enables businesses to automatically respond to customer inquiries with AI that understands your services and products.</p>
          <div className="hero-buttons">
            <Link to="/signup" className="btn btn-primary">Get Started</Link>
            <Link to="/demo" className="btn btn-secondary">Request Demo</Link>
          </div>
        </div>
      </header>

      <section className="features-section">
        <div className="content-container">
          <h2>How it works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>Connect Your Number</h3>
              <p>We provision a dedicated business phone number or connect to your existing one.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📄</div>
              <h3>Upload Business Context</h3>
              <p>Add documents, FAQs, and service details to train your AI assistant.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI Responds to Customers</h3>
              <p>Our AI handles customer inquiries instantly, 24/7, sounding natural and helpful.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Monitor & Improve</h3>
              <p>Track performance and fine-tune responses through the dashboard.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="api-section">
        <div className="content-container">
          <h2>Simple Integration</h2>
          <div className="api-content">
            <div className="api-text">
              <p>Integrate ReplyGenius into your existing systems with our straightforward API.</p>
              <ul>
                <li>REST API for seamless integration</li>
                <li>Webhook support for real-time events</li>
                <li>SDKs for popular programming languages</li>
                <li>Detailed documentation and examples</li>
              </ul>
              <Link to="/docs" className="btn btn-text">Explore the API →</Link>
            </div>
            <div className="api-code">
              <pre>
                <code>
{`curl -X POST https://api.replygenius.com/v1/messages \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "business_id": "bus_28vGxP9KqL",
    "to": "+15551234567",
    "message": "Thank you for your inquiry!"
  }'`}
                </code>
              </pre>
            </div>
          </div>
        </div>
      </section>

      <section className="benefits-section">
        <div className="content-container">
          <h2>Why businesses choose ReplyGenius</h2>
          <div className="benefits-grid">
            <div className="benefit-item">
              <h3>Save Time</h3>
              <p>Automate responses to common inquiries and free up your team for high-value tasks.</p>
            </div>
            <div className="benefit-item">
              <h3>Never Miss a Lead</h3>
              <p>Respond to potential customers instantly, even outside business hours.</p>
            </div>
            <div className="benefit-item">
              <h3>Consistent Service</h3>
              <p>Deliver the same high-quality responses to every customer, every time.</p>
            </div>
            <div className="benefit-item">
              <h3>Scale Effortlessly</h3>
              <p>Handle increasing message volumes without adding support staff.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="testimonial-section">
        <div className="content-container">
          <div className="testimonial">
            <p className="quote">"ReplyGenius has transformed how we handle customer inquiries. Our response time went from hours to seconds, and our customers love the instant support."</p>
            <div className="author">
              <p className="name">Michael Rodriguez</p>
              <p className="title">Operations Director, GreenCut Lawn Services</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="content-container">
          <h2>Ready to automate your customer communications?</h2>
          <p>Get started with ReplyGenius today and experience the power of AI-driven SMS responses.</p>
          <div className="cta-buttons">
            <Link to="/signup" className="btn btn-primary">Sign Up Now</Link>
            <Link to="/pricing" className="btn btn-secondary">View Pricing</Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;