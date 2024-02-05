import React, { useState, useEffect } from "react";
// import AdminNavbar from "./AdminNavbar";
import { useNavigate } from "react-router-dom";
import "../../css/Admin/AdminLogin.css";
import api from "../api";
import { toast } from "react-toastify";

function AdminLogin() {
  const [adminform, setAdminform] = useState({
    username: "",
    pwd: "",
  });

  const handleinputchange = (event) => {
    setAdminform({
      ...adminform,
      [event.target.name]: event.target.value,
    });
  };
  const navigate = useNavigate();
  const handleformsubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post("/adminlogin", adminform);
      if (response.data.success !== false) { 
        console.log(response.data)
        localStorage.setItem("admin", JSON.stringify(response.data[0]));
        navigate("/admin/home");
      }
      else{
        toast.error(response.data.error)
      }
      setAdminform({
        username: "",
        pwd: "",
      });
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <>
      {/* <div>{<AdminNavbar />}</div> */}
      <div className="adminloginmainbody">
        <div class="loginBox">
          {" "}
          <img
            class="user"
            src="https://i.ibb.co/yVGxFPR/2.png"
            height="100px"
            width="100px"
          />
          <h3 className="adminloginh3tag">Sign in here</h3>
          <form action="login.php" onSubmit={handleformsubmit}>
            <div class="inputBox">
              {" "}
              <input
                className="adminlogininput"
                id="username"
                type="text"
                name="username"
                placeholder="Username"
                onChange={handleinputchange}
                value={adminform.username}
              />{" "}
              <input
                className="adminlogininput"
                id="pwd"
                type="password"
                name="pwd"
                placeholder="Password"
                onChange={handleinputchange}
                value={adminform.pwd}
              />{" "}
            </div>{" "}
            <input className="adminlogininput" type="submit" value="Login" />
          </form>
        </div>
      </div>
    </>
  );
}

export default AdminLogin;
