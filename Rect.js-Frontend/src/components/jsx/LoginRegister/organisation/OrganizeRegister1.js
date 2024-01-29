import React, { useState, useEffect } from "react";
import "../../../css/LoginRegister/organisation/organizeRegister1.css";
import api from "../../api"

function OrganizeRegister1({setOBoolean}) {
  
  const [lFormData,setLFormData] = useState({
    clubname: "",
    ownname: "",
    email: "",
    address: "",
    city: "",
    pnumber: "",
    desc:"",
    memtype: [],
    members: [],
    username:"",
    pwd:"",
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
      await api.post("/organisationregistration/", lFormData);
      
      setLFormData({
        clubname: "",
        ownname: "",
        email: "",
        address: "",
        city: "",
        pnumber: "",
        desc:"",
        memtype: [],
        members: [],
        username:"",
        pwd:"",
      });
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log("step1" + event.target.name);
    if (file) {
        const reader = new FileReader();
        console.log("step2" + event.target.name);
        reader.onload = (e) => {
          console.log("step3" + e.target.name + event.target.name);
            const fileContent = e.target.result;
            
            try {
              console.log("step4" + event.target.name);
                // Parse the JSON content and update the 'members' field in your state
                const jsonData = JSON.parse(fileContent);
                setLFormData({
                    ...lFormData,
                    [event.target.name]: jsonData,
                });
            } catch (error) {
                console.error('Error parsing JSON file:', error);
            }
        };

        reader.readAsText(file);
    }
};

 
  return (
    <>
        <div className="OrgloginBody">
          <div className="container">
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
                  <h4 className="Oh4">Organisation Registration</h4>
                  <div className="orgsign-in">
                    <p className="orgP">
                      Want to Login?{" "}
                      
                        <span className="orgloginstatement" onClick={() => {
                      setOBoolean(true);
                    }}>Login</span>
                      
                    </p>
                  </div>
                  <div className="mb-3">
                    <label htmlFor="clubname" className="form-label">
                      Name
                    </label>
                    <input
                      onChange={handleInputChange}
                      type="text"
                      className="form-control"
                      id="clubname"
                      placeholder="Enter your name"
                      name="clubname"
                      value={lFormData.clubname}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="ownername" className="form-label">
                      Owner Name
                    </label>
                    <input
                    onChange={handleInputChange}
                      type="text"
                      className="form-control"
                      id="ownername"
                      placeholder="Enter owner name"
                      name="ownname"
                      value={lFormData.ownname}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                      Email
                    </label>
                    <input
                    onChange={handleInputChange}
                      type="email"
                      className="form-control"
                      id="email"
                      placeholder="Enter your email"
                      name="email"
                      value={lFormData.email}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="address" className="form-label">
                      Address
                    </label>
                    <input
                    onChange={handleInputChange}
                      type="text"
                      className="form-control"
                      id="address"
                      placeholder="Enter your address"
                      name="address"
                      value={lFormData.address}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="city" className="form-label">
                      City Name
                    </label>
                    <input
                    onChange={handleInputChange}
                      type="text"
                      className="form-control"
                      id="city"
                      placeholder="Enter your city name"
                      name="city"
                      value={lFormData.city}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="pnumber" className="form-label">
                      Phone Number:
                    </label>
                    <input
                    onChange={handleInputChange}
                      type="number"
                      className="form-control"
                      id="number"
                      placeholder="Enter your number"
                      name="pnumber"
                      value={lFormData.pnumber}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="desc" className="form-label">
                      Organisation Description
                    </label>
                    <textarea
                    onChange={handleInputChange}
                      className="form-control"
                      id="desc"
                      placeholder="Enter description"
                      name="desc"
                      value={lFormData.desc}
                    ></textarea>
                  </div>
                  <div className="mb-3">
                    <label htmlFor="memtype" className="form-label">
                      Membership Type .json File
                    </label>
                    <input
                      type="file"
                      className="form-control"
                      id="memtype"
                      accept=".json"
                      onChange={handleFileChange}
                      multiple={false}
                      name="memtype"
                      
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="members" className="form-label">
                    Members .json File
                    </label>
                    <input
                      type="file"
                      className="form-control"
                      id="members"
                      accept=".json"
                      onChange={handleFileChange}
                      multiple={false}
                      name="members"
                    />
                  </div>

                  <div className="orgsign-in">
                    <p className="orgP">Lets Create Username & Password </p>
                  </div>

                  <div className="mb-3">
                    <label htmlFor="username" className="form-label">
                      UserName:
                    </label>
                    <input
                    onChange={handleInputChange}
                      type="text"
                      className="form-control"
                      id="username"
                      placeholder="Enter your user name"
                      name="username"
                      value={lFormData.username}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="pwd" className="form-label">
                      Password:
                    </label>
                    <input
                    onChange={handleInputChange}
                      type="password"
                      className="form-control"
                      id="pwd"
                      placeholder="Enter your password"
                      name="pwd"
                      value={lFormData.pwd}
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

export default OrganizeRegister1;
