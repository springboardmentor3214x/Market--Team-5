
import React, { useState } from 'react';

import Registration from './registration/Registration';
import Login from './Login/Login';
import StockSearch from './stock-search/StockSearch';

import './App.css';

function App() {

  const [showLogin, setShowLogin] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // After successful registration
  const handleRegistrationSuccess = () => {
    setShowLogin(true);
  };

  // After successful login
  const handleLoginSuccess = () => {
    console.log("App: Login callback received");

    setIsLoggedIn(true);
  };

  // Logout
  const handleLogout = () => {
    localStorage.removeItem("access_token");

    setIsLoggedIn(false);
    setShowLogin(true);
  };

  return (
    <div className="app-container">

      {/* NAVBAR */}
      <nav className="navbar">

        <div className="brand">
          <h2>
            Stock<span>Research</span>
          </h2>
        </div>

        {!isLoggedIn ? (

          <div className="nav-buttons">

            <button
              className={!showLogin ? 'active' : ''}
              onClick={() => setShowLogin(false)}
            >
              Register
            </button>

            <button
              className={showLogin ? 'active' : ''}
              onClick={() => setShowLogin(true)}
            >
              Login
            </button>

          </div>

        ) : (

          <div className="nav-buttons">
            <button onClick={handleLogout}>
              Logout
            </button>
          </div>

        )}

      </nav>

      {/* MAIN CONTENT */}
      <main className="main-content">

        {isLoggedIn ? (

          <StockSearch />

        ) : (

          <>
            <div className="welcome-section">

              <h1>
                Welcome to Smart Stock Research
              </h1>

              <p>
                Make smarter investment decisions with
                AI-powered stock analysis and insights.
              </p>

            </div>

            <div className="form-section">

              {showLogin ? (

                <Login
                  onLoginSuccess={handleLoginSuccess}
                />

              ) : (

                <Registration
                  onRegistrationSuccess={handleRegistrationSuccess}
                />

              )}

            </div>
          </>

        )}

      </main>

      {/* FOOTER */}
      <footer className="footer">
        © 2026 AI-Powered Stock Research System
      </footer>

    </div>
  );
}

export default App;
