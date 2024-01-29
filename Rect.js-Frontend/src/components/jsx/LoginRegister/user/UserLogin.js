import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../Navbar";
import "../../../css/LoginRegister/user/userLogin.css";
import api from "../../api";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function UserLogin({ setUserBoolean }) {
  const navigate = useNavigate();
  const [details, setDetails] = useState([]);

  const [lFormData, setLFormData] = useState({
    clubname: "",
    username: "",
    pwd: "",
  });

  useEffect(() => {
    fetchAllClubDetails();
  }, []);

  const fetchAllClubDetails = async () => {
    try {
      const response = await api.get("/clubnames/");
      setDetails(response.data);
    } catch (error) {
      console.error("Error fetching details:", error);
    }
  };

  const handleInputChange = (event) => {
    
    setLFormData({
      ...lFormData,
      [event.target.name]: event.target.value,
    });
  };

  const handleFormSubmit = async (event) => {
    // debugger
    event.preventDefault();
    console.log(lFormData)
    
    try {
      const checking = await api.post("/userlogin/", lFormData);
      console.log(checking.data);
      if (checking.data.success !== false) {
        // Use the navigate function to go to the home page
        // console.log("form data: "+ JSON.stringify(lFormData))
        localStorage.setItem("users", JSON.stringify(checking.data));

        navigate("/");
      } else {
        // toast.error(checking.data.error);
        alert(checking.data.error)
      }
      setLFormData({
        clubname: "",
        username: "",
        pwd: "",
      });
    } catch (error) {
      toast.error("Error submitting form:");
      console.error("Error submitting form:", error);
    }
  };

  return (
    <>
      <div>{<Navbar />}</div>
      <div className="UserloginBody">
        <div className="container">
          <header className="Uheader row text-center"></header>
          <main className="Umain main row">
            <div className="left col">
              <img
                src="https://img.freepik.com/premium-vector/young-woman-enjoy-sitting-reading-book-hygge-concept-vector-illustration_194708-2078.jpg"
                alt="girl-reading-a-book"
                className="Uimg"
              />
            </div>
            <div className="right col">
              <form className="UserForm sign-up" onSubmit={handleFormSubmit}>
                <h4 className="Uh4">User Login</h4>
                <div className="mb-3">
                  {/* <label htmlFor="clubname" className="form-label">
                    Clubname
                  </label>
                  <input
                    onChange={handleInputChange}
                    type="text"
                    className="form-control"
                    id="clubname"
                    placeholder="Enter your clubname"
                    name="clubname"
                    value={lFormData.clubname}
                    required
                  /> */}
                  <label htmlFor="clubname" className="form-label">
                    Select Clubname: 
                  </label>
                  <select
                    onChange={handleInputChange}
                    className="form-select"
                    id="clubname"
                    name="clubname"
                    value={lFormData.clubname}
                    required
                  >
                    
                    <option value="None">None</option>
                    {details.map((club) => (
                      <option key={club} value={club}>
                        {club}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label htmlFor="username" className="form-label">
                    UserName
                  </label>
                  <input
                    onChange={handleInputChange}
                    type="text"
                    className="form-control"
                    id="username"
                    placeholder="Enter your username"
                    name="username"
                    value={lFormData.username}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="pwd" className="form-label">
                    Password
                  </label>
                  <input
                    onChange={handleInputChange}
                    type="password"
                    className="form-control"
                    id="pwd"
                    placeholder="Enter your password"
                    name="pwd"
                    value={lFormData.pwd}
                    required
                  />
                </div>
                <button type="submit" className="btn submit-btn">
                  Login
                </button>
              </form>

              <div className="sign-in">
                <p className="userP">
                  Don't have an account?{" "}
                  <span
                    onClick={() => {
                      setUserBoolean(false);
                    }}
                  >
                    <span className="userloginstatement">Register</span>
                  </span>
                </p>
              </div>
            </div>
          </main>
        </div>
      </div>
    </>
  );
}

export default UserLogin;
