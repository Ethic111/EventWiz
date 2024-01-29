import React, { useState, useEffect } from "react";
import { Link, Navigate } from "react-router-dom";
// import { useNavigate } from "react-router-dom";
import "../css/Navbar.css";
function Navbar() {
  const [isNavOpen, setNavOpen] = useState(false);
  
  const [userData, setUserData] = useState(
    JSON.parse(localStorage.getItem("users"))
  );

  // const userData = JSON.parse(localStorage.getItem("users"));

  const handleNavOpenClick = () => {
    setNavOpen(true);
  };

  const handleNavCloseClick = () => {
    setNavOpen(false);
  };

  // const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      localStorage.clear();
      setUserData(null);
      // navigate("/home")
      // window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      
      <div className="container">
        <nav className={`nav ${isNavOpen ? "openNav" : ""}`}>
          <i
            className="uil uil-bars navOpenBtn"
            onClick={handleNavOpenClick}
          ></i>
          <Link to="/" className="logo">
            EventWiz
          </Link>
          <ul className="nav-links">
            <i
              className="uil uil-times navCloseBtn"
              onClick={handleNavCloseClick}
            ></i>
            <li>
              <Link to="/home">Home</Link>
            </li>
            <li>
              <Link to="/aboutus">About Us</Link>
            </li>
            <li>
              <Link to="/events">Events</Link>
            </li>
            <li>
              <Link to="/">Subscribe</Link>
            </li>
            <li>
              {userData?.email ? (
                <Link to="/home" onClick={handleSignOut}>
                  Logout {userData.username}
                </Link>
              ) : (
                <Link to="/loginregister">Login/Register</Link>
              )}
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
}

export default Navbar;
