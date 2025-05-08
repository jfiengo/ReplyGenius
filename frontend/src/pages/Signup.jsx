import React, { useState } from 'react';
import styles from './Home.module.css';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    // TODO: Integrate with backend and Stripe
    // For now, just simulate a delay
    setTimeout(() => {
      setLoading(false);
      alert('Signup submitted! (Backend integration needed)');
    }, 1000);
  };

  return (
    <div className={styles.loomGradient} style={{minHeight: '100vh', minWidth: '100vw', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{maxWidth: 420, width: '100%'}} className="d-flex flex-column align-items-center justify-content-center">
        <div className="text-center mb-4">
          <h2 className="fw-bold mb-2" style={{color: '#fff'}}>Sign Up for ReplyGenius</h2>
          <p className="mb-0" style={{color: '#f3e8ff'}}>Create your account to get started</p>
        </div>
        <form onSubmit={handleSubmit} className="card p-4 shadow-lg border-0 w-100" style={{borderRadius: 20}}>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">Email address</label>
            <input
              type="email"
              className="form-control"
              id="email"
              required
              value={email}
              onChange={e => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              id="password"
              required
              minLength={8}
              value={password}
              onChange={e => setPassword(e.target.value)}
              autoComplete="new-password"
            />
            <div className="form-text">Must be at least 8 characters.</div>
          </div>
          {error && <div className="alert alert-danger">{error}</div>}
          <button type="submit" className={`w-100 mt-2 ${styles.loomBtn}`} disabled={loading}>
            {loading ? 'Signing up...' : 'Sign Up & Continue'}
          </button>
        </form>
      </div>
    </div>
  );
} 