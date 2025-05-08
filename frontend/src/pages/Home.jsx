import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Home.module.css';

const Home = () => {
  return (
    <div className={`home-container ${styles.homeContainer}`}>
      {/* Loom-style Top Banner */}
      <div className={styles.topBanner}>
        <span>Never miss a lead. </span>
        <Link to="/signup" className={styles.loomBtn} style={{marginLeft: '1.5rem'}}>Get ReplyGenius</Link>
      </div>
      
      {/* Hero Section with Loom Gradient */}
      <header className={`py-5 ${styles.loomGradient}`}> 
        <div className="container-fluid text-center py-5">
          <h1 className="display-2 fw-bold mb-3">ReplyGenius</h1>
          <h2 className="h3 fw-semibold mb-4">Automatically respond to customers with AI-powered messages using your business information.</h2>
          <p className="lead mb-4">Empower your team and customers with instant, AI-enhanced communication. Automate, personalize, and scale your business conversations.</p>
          <div className="d-flex justify-content-center gap-3 mb-4">
            <Link to="/signup" className={styles.loomBtn}>Get Started</Link>
            <Link to="/demo" className="btn btn-outline-light btn-lg">See Demo</Link>
          </div>
        </div>
      </header>

      <section className="py-5">
        <div className={`container-fluid ${styles.sectionBg}`}> 
          <h2 className="text-center mb-5">How it works</h2>
          <div className="row justify-content-center">
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.featureCard}`}>
                <div className="display-4 mb-3">📱</div>
                <h3 className="h5 mb-2">Connect Your Number</h3>
                <p>We provision a dedicated business phone number or connect to your existing one.</p>
              </div>
            </div>
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.featureCard}`}>
                <div className="display-4 mb-3">📧</div>
                <h3 className="h5 mb-2">Connect Your Email</h3>
                <p>We provision a dedicated business email or connect to your existing one.</p>
              </div>
            </div>
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.featureCard}`}>
                <div className="display-4 mb-3">📄</div>
                <h3 className="h5 mb-2">Upload Business Context</h3>
                <p>Add documents, FAQs, and service details to train your AI assistant.</p>
              </div>
            </div>
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.featureCard}`}>
                <div className="display-4 mb-3">🤖</div>
                <h3 className="h5 mb-2">AI Responds to Customers</h3>
                <p>Our AI handles customer inquiries instantly, 24/7, sounding natural and helpful.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-5">
        <div className={`container-fluid ${styles.sectionBg}`}> 
          <h2 className="text-center mb-5">Simple Integration</h2>
          <div className="row align-items-center justify-content-center">
            <div className="col-12 col-lg-6 mb-4 mb-lg-0">
              <div className={`rounded-3 p-4 h-100 ${styles.sectionBg}`}> 
                <h4 className="mb-3">Integrate ReplyGenius into your existing systems with our straightforward API.</h4>
                <ul className="list-unstyled mb-4">
                  <li>REST API for seamless integration</li>
                  <li>Webhook support for real-time events</li>
                  <li>SDKs for popular programming languages</li>
                  <li>Detailed documentation and examples</li>
                </ul>
                <Link to="/docs" className="btn btn-link p-0">Explore the API →</Link>
              </div>
            </div>
            <div className="col-12 col-lg-6">
              <div className={`bg-dark text-white rounded-3 p-4 ${styles.apiCode}`}> 
                <pre className="mb-0"><code>{`curl -X POST https://api.replygenius.com/v1/messages \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "bus_28vGxP9KqL",
    "to": "+15551234567",
    "message": "Thank you for your inquiry!"
  }'`}</code></pre>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-5">
        <div className={`container-fluid ${styles.sectionBg}`}> 
          <h2 className="text-center mb-5">Why businesses choose ReplyGenius</h2>
          <div className="row justify-content-center">
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.benefitCard}`}>
                <h3 className="h5 mb-2">Save Time</h3>
                <p>Automate responses to common inquiries and free up your team for high-value tasks.</p>
              </div>
            </div>
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.benefitCard}`}>
                <h3 className="h5 mb-2">Never Miss a Lead</h3>
                <p>Respond to potential customers instantly, even outside business hours.</p>
              </div>
            </div>
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.benefitCard}`}>
                <h3 className="h5 mb-2">Consistent Service</h3>
                <p>Deliver the same high-quality responses to every customer, every time.</p>
              </div>
            </div>
            <div className="col-12 col-md-6 col-lg-3 mb-4">
              <div className={`card h-100 text-center p-4 ${styles.benefitCard}`}>
                <h3 className="h5 mb-2">Scale Effortlessly</h3>
                <p>Handle increasing message volumes without adding support staff.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-5">
        <div className={`container-fluid ${styles.sectionBg}`}> 
          <div className={`mx-auto mb-5 ${styles.testimonial} card p-4 text-center`} style={{maxWidth: 700}}>
            <p className="fs-4 fst-italic mb-3">ReplyGenius has transformed how we handle customer inquiries. Our response time went from hours to seconds, and our customers love the instant support.</p>
            <div className="author">
              <p className="fw-bold mb-0">Michael Rodriguez</p>
              <p className="text-muted">Operations Director, GreenCut Lawn Services</p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-5 min-vh-100 d-flex flex-column justify-content-between">
        <div className={`container-fluid text-center ${styles.sectionPrimary} flex-grow-1 d-flex flex-column justify-content-center`}>
          <h2 className="mb-3 mt-3">Ready to automate your customer communications?</h2>
          <p className="lead mb-4">Get started with ReplyGenius today and experience the power of AI-driven responses and lead generation.</p>
          <div className="d-flex justify-content-center gap-3 mb-1">
            <Link to="/signup" className={styles.loomBtn}>Sign Up Now</Link>
            <Link to="/pricing" className="btn btn-outline-light btn-lg">View Pricing</Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;