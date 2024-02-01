import React, { useState, useEffect } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
// import "../css/OrganisationNavbar.css";

function OrganisationNavbar() {
  const location = useLocation();
  const isHomeActive = location.pathname === "/organisationevents";
  const [isNavOpen, setNavOpen] = useState(false);
  const [orgData, setOrgData] = useState(
    JSON.parse(localStorage.getItem("organisers"))
  );

  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      localStorage.clear();
      setOrgData(null);
      navigate("/");
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div>
        <nav
          className="navbar navbar-dark navbar-expand-lg  fixed-top "
          style={{ backgroundColor: "#0e2643" }}
        >
          <div className="container-fluid">
            <Link to="/organisationevents" className="navbar-brand ms-5">
              EventWiz
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div
              className="collapse navbar-collapse justify-content-end me-5"
              id="navbarNav"
            >
              <ul className="navbar-nav">
                {/* <li className="nav-item">
                  <NavLink
                    to="/organisationevents"
                    className={`nav-link ${
                      isHomeActive ? "font-weight-bold" : ""
                    }`}
                  >
                    Home
                  </NavLink>
                </li> */}
                {/*  */}
                <li className="nav-item">
                  <NavLink
                    to="/organisationevents/orgevents"
                    className={`nav-link ${
                      isHomeActive ? "font-weight-bold" : ""
                    }`}
                  >
                    Event
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink
                    to="/organisationevents/organizationmemberdetails"
                    className={`nav-link ${
                      isHomeActive ? "font-weight-bold" : ""
                    }`}
                  >
                    Member Data
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink
                    to="/organisationevents/organisationmemberships"
                    className={`nav-link ${
                      isHomeActive ? "font-weight-bold" : ""
                    }`}
                  >
                    Membership
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink
                    to="/organisationevents/authorization"
                    className={`nav-link ${
                      isHomeActive ? "font-weight-bold" : ""
                    }`}
                  >
                    Authorization
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink
                    to="/organisationevents/otherevents"
                    className={`nav-link ${
                      isHomeActive ? "font-weight-bold" : ""
                    }`}
                  >
                    Other Events
                  </NavLink>
                </li>
                <li className="nav-item">
                  {orgData?.email ? (
                    <NavLink
                      to="/"
                      onClick={handleSignOut}
                      className={`nav-link ${
                        !isHomeActive ? "font-weight-bold" : ""
                      }`}
                    >
                      Logout {orgData.username}
                    </NavLink>
                  ) : (
                    <NavLink
                      to="/loginregister"
                      className={`nav-link ${
                        !isHomeActive ? "font-weight-bold" : ""
                      }`}
                    >
                      Login/Register
                    </NavLink>
                  )}
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </div>
    </>
  );
}

export default OrganisationNavbar;
