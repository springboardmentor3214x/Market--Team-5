
import React, { useState } from 'react';
import './Login.css';

export default function Login() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email,
            password
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Login failed. Please try again."
        );
      }

      setSuccess(data.message || "Login successful!");

      setEmail("");
      setPassword("");

      // Store token if backend returns one
      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
      }

    } catch (err) {

      setError(
        err.message === "Failed to fetch"
          ? "Unable to connect to server. Please try again."
          : err.message
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">

      <form
        className="login-form"
        onSubmit={handleSubmit}
      >

        <h2>Login</h2>

        <label>Enter your email:</label>

        <input
          type="email"
          value={email}
          placeholder="Enter your email"
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Password:</label>

        <input
          type="password"
          value={password}
          placeholder="Enter your password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && (
          <p style={{ color: "red" }}>
            {error}
          </p>
        )}

        {success && (
          <p style={{ color: "green" }}>
            {success}
          </p>
        )}

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

      </form>

    </div>
  );
}
