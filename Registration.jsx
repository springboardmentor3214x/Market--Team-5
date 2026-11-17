
import React, { useState } from 'react';
import './Registration.css';

export default function Registration() {

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (password.length < 8) {
      setError("Password must contain at least 8 characters.");
      return;
    }

    if (confirmPassword.length < 8) {
      setError("Confirm password must contain at least 8 characters.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Password and Confirm Password do not match.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            username,
            email,
            password,
            confirmPassword
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {

        if (Array.isArray(data.detail)) {

          const messages = data.detail.map((err) => {

            const field = err.loc[err.loc.length - 1];

            if (err.type === "string_too_short") {
              if (field === "confirmPassword") {
                return "Confirm password must contain at least 8 characters.";
              }

              if (field === "password") {
                return "Password must contain at least 8 characters.";
              }

              if (field === "username") {
                return "Username must contain at least 2 characters.";
              }
            }

            if (err.msg.includes("uppercase")) {
              return "Password must contain at least one uppercase letter.";
            }

            if (err.msg.includes("number")) {
              return "Password must contain at least one number.";
            }

            if (field === "email") {
              return "Please enter a valid email address.";
            }

            return err.msg;
          });

          throw new Error([...new Set(messages)].join(" "));
        }

        throw new Error(
          data.detail || "Registration failed. Please try again."
        );
      }

      setSuccess(data.message);

      setUsername("");
      setEmail("");
      setPassword("");
      setConfirmPassword("");

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
    <div className="registration-container">

      <form
        className="registration-form"
        onSubmit={handleSubmit}
      >

        <h2>Create Account</h2>

        <label>Enter your name:</label>

        <input
          type="text"
          value={username}
          placeholder="Enter your name"
          onChange={(e) => setUsername(e.target.value)}
          minLength={2}
          maxLength={50}
          required
        />

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
          placeholder="Enter the password"
          onChange={(e) => setPassword(e.target.value)}
          minLength={8}
          maxLength={128}
          required
        />

        <label>Confirm password:</label>

        <input
          type="password"
          value={confirmPassword}
          placeholder="Confirm your password"
          onChange={(e) => setConfirmPassword(e.target.value)}
          minLength={8}
          maxLength={128}
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
          {loading ? "Registering..." : "Register"}
        </button>

      </form>

    </div>
  );
}
