import React, { useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom';

function AdminNavbar() {
  const location = useLocation();
  const isHomeActive = location.pathname === '/admin/home';
  const [userData, setUserData] = useState(
    JSON.parse(localStorage.getItem("admin"))
  );
  const handleSignOut = async () => {
    try {
      localStorage.clear();
      setUserData(null);
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <>
    <nav className="navbar navbar-dark navbar-expand-lg  fixed-top " style={{ backgroundColor: "#0e2643" }}>
        <div className="container-fluid">
          <Link to="/admin/home" className="navbar-brand ms-5" >EventWiz</Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse justify-content-end me-5" id="navbarNav">
            <ul className="navbar-nav ">
              <li className="nav-item">
                <NavLink to="/admin/home" className={`nav-link ${isHomeActive ? 'font-weight-bold' : ''}`}>Home</NavLink>
              </li>
              <li className="nav-item">
                <NavLink to="/admin/allusers" className={`nav-link ${isHomeActive ? 'font-weight-bold' : ''}`}>User</NavLink>
              </li>
              <li className="nav-item">
                <NavLink to="/admin/allorg" className={`nav-link ${isHomeActive ? 'font-weight-bold' : ''}`}>Organisation</NavLink>
              </li>
              <li className="nav-item">
                <NavLink to="/admin/accepetrejectorg" className={`nav-link ${isHomeActive ? 'font-weight-bold' : ''}`}>Authorization</NavLink>
              </li>
              <li className="nav-item">
                {userData?.username ? (
                  <NavLink to="/home" onClick={handleSignOut} className={`nav-link ${!isHomeActive ? 'font-weight-bold' : ''}`}>Logout {userData.username}
                  </NavLink>
                ) : (
                  <NavLink to="*"></NavLink>
                )}

              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  )
}

export default AdminNavbar