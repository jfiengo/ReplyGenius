import React, { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';
import './ThemeToggle.css';
import LightDarkIcon from '../assets/light_dark_mode.png';

const ThemeToggle = () => {
  const { isDarkMode, toggleTheme } = useContext(ThemeContext);

  return (
    <div className="theme-toggle">
    <button 
        className="toggle-button" 
        onClick={toggleTheme}
        aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
      >
        <img 
          src={LightDarkIcon} 
          alt={isDarkMode ? "Switch to light mode" : "Switch to dark mode"} 
          className={`theme-icon ${isDarkMode ? 'dark-mode' : 'light-mode'}`}
          width="24"
          height="24"
        />
      </button>
    </div>
  );
};

export default ThemeToggle;