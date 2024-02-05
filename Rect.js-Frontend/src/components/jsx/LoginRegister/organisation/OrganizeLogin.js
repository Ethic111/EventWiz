import React,{useState,useEffect} from "react";
import { useNavigate } from "react-router-dom";
import "../../../css/LoginRegister/user/userLogin.css";
import api from "../../api";
import { toast } from "react-toastify";

function OrganizeLogin({ setOBoolean }) {
  const navigate = useNavigate();


  const [lFormData,setLFormData] = useState({
    username: "",
    pwd: "",
  });

  const handleInputChange = (event) => {
    setLFormData({
      ...lFormData,
      [event.target.name]: event.target.value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      const checking = await api.post("/organisationlogin/", lFormData);
      console.log(checking.data)
      if (checking.data.success != false) {
        // Use the navigate function to go to the home page
        localStorage.setItem('organisers', JSON.stringify(checking.data));

        navigate("/organisationevents");
      } else {
        toast.error("Wrong Username & Password!");
      }
      setLFormData({
        username: "",
        pwd: "",
      });
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };


  return (
    <>
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
                <h4 className="Uh4">Organisation Login</h4>
                <div className="mb-3">
                  <label htmlFor="username" className="form-label">
                    UserName:
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="username"
                    placeholder="Enter your username"
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
                    placeholder="Create a password"
                    name="pwd"
                    value={lFormData.pwd}
                    onChange={handleInputChange}
                  />
                </div>
                <button type="submit" className="btn submit-btn">
                  Login
                </button>
              </form>
              <div className="sign-in">
                <p className="userP">
                  Don't have an account?
                  <span
                    className="userloginstatement"
                    onClick={() => {
                      setOBoolean(false);
                    }}
                  >
                    Register
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

export default OrganizeLogin;
