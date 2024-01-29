import React, { useState, useEffect } from "react";
import { Link, Navigate } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "../css/OrganisationNavbar.css";

function OrganisationNavbar() {
  const [isNavOpen, setNavOpen] = useState(false);
  const [userData, setUserData] = useState(
    JSON.parse(localStorage.getItem('organisers'))
  );

  const handleNavOpenClick = () => {
    setNavOpen(true);
  };

  const handleNavCloseClick = () => {
    setNavOpen(false);
  };

//   const handleaddpostbtn = () => {
//     navigate("/organisationevents/addpost")
//   }
  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      localStorage.clear();
      setUserData(null);
      navigate("/");
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
          <Link to="/organisationevents" className="logo">
            EventWiz
          </Link>
          <ul className="nav-links">
            <i
              className="uil uil-times navCloseBtn"
              onClick={handleNavCloseClick}
            ></i>
            <li>
              <Link to="/organisationevents/orgevents">Events</Link>
            </li>
            {/* <li>
              <Link to="/organisationevents/addpost"><button  className="btn addpostbtn">+</button></Link>
            </li> */}
            <li>
              <Link to="/organisationevents/organizationmemberdetails">Member Data</Link>
            </li>
            <li>
              <Link to="/organisationevents/organisationmemberships">Memberships</Link>
            </li>
            <li>
              <Link to="/organisationevents/otherevents">Other Events</Link>
            </li>
            <li>
              <Link to="/home" onClick={handleSignOut}>
                Logout {userData.username}
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
}

export default OrganisationNavbar;
