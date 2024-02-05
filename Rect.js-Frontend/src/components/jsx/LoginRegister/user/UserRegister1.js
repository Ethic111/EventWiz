import React, { useState } from "react";
import "../../../css/LoginRegister/user/userRegistration1.css";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import { toast } from "react-toastify";

function UserRegister1({ setUserBoolean }) {
  const [lFormData, setLFormData] = useState({
    name: "",
    email: "",
    pnumber: "",
    gender: "",
    username: "",
    pwd: "",
  });

  const navigate = useNavigate();

  const handleInputChange = (event) => {
    setLFormData({
      ...lFormData,
      [event.target.name]: event.target.value,
    });
  };

  const handleFormSubmit = async (event) => {
    console.log(lFormData)
    event.preventDefault();
    try {
      const checking = await api.post("/userregistration/", lFormData);
      console.log(checking.data)
      if (checking.data.success != false) {
        // Use the navigate function to go to the home page
        // console.log("form data: "+ JSON.stringify(lFormData))
        localStorage.setItem("users", JSON.stringify(checking.data));
        navigate("/");
        setLFormData({
          name: "",
          email: "",
          pnumber: "",
          gender: "",
          username: "",
          pwd: "",
        });
      } else {
        // toast.error(checking.data.error);
        toast.error(checking.data.error)
      }

      
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <>
      <div className="OrgloginBody">
        <div className="container">
          <header className="Orgheader row text-center"></header>
          <main className="Orgmain main row">
            <div className="left col">
              <img
                src="https://img.freepik.com/premium-vector/young-woman-enjoy-sitting-reading-book-hygge-concept-vector-illustration_194708-2078.jpg"
                alt="girl-reading-a-book"
                className="Orgimg"
              />
            </div>
            <div className="right col">
              <form className="OrgForm sign-up" onSubmit={handleFormSubmit}>
                <h4 className="Oh4">User Registration</h4>
                <div className="orgsign-in">
                  <p className="orgP">
                    Want to Login?{" "}
                    <span
                      onClick={() => {
                        setUserBoolean(true);
                      }}
                    >
                      <span className="orgloginstatement ">Login</span>
                    </span>{" "}
                  </p>
                </div>
                <div className="mb-3">
                  <label htmlFor="name" className="form-label">
                    Name
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="name"
                    placeholder="Enter your name"
                    name="name"
                    value={lFormData.name}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">
                    Email
                  </label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    placeholder="Enter your email"
                    name="email"
                    value={lFormData.email}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="pnumber" className="form-label">
                    Phone Number:
                  </label>
                  <input
                    type="number"
                    className="form-control"
                    id="pnumber"
                    placeholder="Enter your number"
                    name="pnumber"
                    value={lFormData.pnumber}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="gender" className="form-label mx-2">
                    Gender
                  </label>
                  <input
                    type="radio"
                    name="gender"
                    value="Male"
                    checked={lFormData.gender === "Male"}
                    className="mx-2"
                    onChange={handleInputChange}
                  />
                  Male
                  <input
                    type="radio"
                    name="gender"
                    value="Female"
                    checked={lFormData.gender === "Female"}
                    className="mx-2"
                    onChange={handleInputChange}
                  />
                  Female
                </div>

                <div className="orgsign-in">
                  <p className="orgP">Lets Create Username & Password </p>
                </div>

                <div className="mb-3">
                  <label htmlFor="username" className="form-label">
                    UserName:
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="username"
                    placeholder="Enter your user name"
                    name="username"
                    value={lFormData.username}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="pwd" className="form-label">
                    Password:
                  </label>
                  <input
                    type="password"
                    className="form-control"
                    id="pwd"
                    placeholder="Enter your password"
                    name="pwd"
                    value={lFormData.pwd}
                    onChange={handleInputChange}
                  />
                </div>
                <button type="submit" className="btn submit-btn">
                  Register
                </button>
              </form>
            </div>
          </main>
        </div>
      </div>
    </>
  );
}

export default UserRegister1;
