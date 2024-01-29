// AdminNavbar
import React, { useState, useEffect } from "react";
import { Link, Navigate } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "../../css/OrganisationNavbar.css";

function AdminNavbar() {
  const [isNavOpen, setNavOpen] = useState(false);
  const [adminData, setAdminData] = useState(
    JSON.parse(localStorage.getItem('admin'))
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
      setAdminData(null);
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
          <Link to="/admin/home" className="logo">
            EventWiz
          </Link>
          <ul className="nav-links">
            <i
              className="uil uil-times navCloseBtn"
              onClick={handleNavCloseClick}
            ></i>
            <li>
              <Link to="/admin/allorg">Organisation</Link>
            </li>
            <li>
              <Link to="/admin/userdetails">User</Link>
            </li>
            <li>
              <Link to="/admin/accepetrejectorg">Authorization</Link>
            </li>
            {/* <li>
              <Link to="/organisationevents/otherevents">Other Events</Link>
            </li> */}
            <li>
              <Link to="/home" onClick={handleSignOut}>
                Logout {adminData.username}
                
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
}

export default AdminNavbar;
