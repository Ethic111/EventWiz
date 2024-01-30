// AdminOrgDetailed.js
import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import $ from "jquery";
import AdminNavbar from "./AdminNavbar";
import "../../css/OrganisationEvent/orgEvent.css";
import api from "../api";
import "../../css/Admin/AdminOrdDetail.css";
import { GrPowerReset } from "react-icons/gr";

function AdminOrgDetailed() {
  const [details, setDetails] = useState();
  const [searchForm, setSearchform] = useState({
    clubname: "",
  });

  const location = useLocation();
  const orgData = JSON.parse(location.state);
  console.log(orgData);
  // if (orgData){

  //   setDetails(orgData.memtype)
  // }
  const memtype = orgData.memtype;
  console.log(memtype);
  useEffect(() => {
    fetchAllOrgdetails();
  }, []);

  const fetchAllOrgdetails = async () => {
    try {
      //   console.log(userData.clubname);
      //   const cname = userData.clubname; //Rajpath
      //   console.log(typeof cname); //string
      const response = await api.get("/allorganisations");
      setDetails(response.data);
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching details:", error);
    }
  };

  const navigate = useNavigate();
  const handleorgdetails = (org) => {
    // console.log(JSON.stringify(org))
    navigate("/admin/orgdetailspage", {
      state: JSON.stringify(org),
    });
  };

  // /////////////

  const handleformreset = () => {
    setSearchform({
      clubname: "",
    });
    fetchAllOrgdetails();
  };

  const handleSearchInputChange = (event) => {
    // const { name, value } = e.target;
    setSearchform({
      ...searchForm,
      [event.target.name]: event.target.value,
    });
  };
  const handlesearchSubmit = async (event) => {
    event.preventDefault();

    const data = {
      clubname: searchForm["clubname"],
    };
    console.log("handle search submit");
    try {
      const response = await api.post("/searchingorgbyname", data);
      if (response.data.success !== false) {
        console.log(response.data);
        setDetails(response.data);
      } else {
        alert(response.data.error);
      }
      // console.log(response.data);
    } catch (error) {
      console.error("Error fetching details:", error);
    }
  };

  return (
    <>
      <div>{<AdminNavbar />}</div>

      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
        }}
      >
        <div className="mt-1">
          <Link to="/organisationevents/addpost">
            <button className="addpostbtn">Member Data</button>
          </Link>
        </div>
        <div className="mt-0">
          <form className="form-inline my-lg-0 " onSubmit={handlesearchSubmit}>
            <div className="row">
              <div className="col-8 p-2">
                <input
                  className="form-control"
                  name="clubname"
                  type="text"
                  placeholder="Search"
                  aria-label="Search"
                  onChange={handleSearchInputChange}
                  value={searchForm.clubname}
                />
              </div>
              <div className="col-2 p-2">
                <button
                  className="btn btn-outline-success my-2 my-sm-0 membersearchicon"
                  type="submit"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    className="bi bi-search"
                    viewBox="0 0 16 16"
                  >
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
                  </svg>
                </button>
              </div>
              <div className="col-2">
                <button className="addorgbtn" onClick={handleformreset}>
                  <GrPowerReset
                    style={{
                      height: "1.2rem",
                      width: "1.2rem",
                    }}
                  />
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
      <hr />
      <div>
        <div className="loginmainEventdiv">
          <div className="row">
            <div className="col-12">
              <br />
              <div>
                <section class="light">
                  <div class="container py-2">
                    <article class="postcard light blue">
                      <a class="postcard__img_link" href="#">
                        <img
                          class="postcard__img"
                          src="https://picsum.photos/1000/1000"
                          alt="Image Title"
                        />
                      </a>
                      <div class="postcard__text t-dark">
                        <h1 class="postcard__title blue">
                          <h4>{orgData.clubname}</h4>
                        </h1>
                        <div class="postcard__subtitle small">
                          <strong>{orgData.ownname}</strong>
                          <br />
                          <strong> {orgData.email}</strong>
                        </div>
                        <div class="postcard__bar"></div>
                        <div class="postcard__preview-txt">{orgData.desc}</div>
                        <br />
                        <div class="row">
                          <span className="col">
                            <strong>Contact Number:</strong> {orgData.pnumber}
                          </span>
                          <span className="col">
                            <strong>City:</strong> {orgData.city}
                          </span>
                        </div>
                        <br />
                        <div class="">
                          <strong>Address:</strong> {orgData.address}
                        </div>
                        <div >
                          <br />
                          <strong>Membership Type & Price</strong>
                         <br/>
                         <br/>
                            {memtype && memtype.length ? (
                              memtype.map((type) => (
                                <li>
                                  <span>
                                    {type.type} {"-->"} {type.price}
                                  </span>
                                </li>
                              ))
                            ) : (
                              <p>No Membership Types...</p>
                            )}
                          
                        </div>
                      </div>
                    </article>
                  </div>
                </section>
              </div>
              {/* <div className="row">
                    <div className="col-4 maincardbody">
                      <div class="col">
                        <section
                          class="mx-auto my-5"
                          style={{ maxWidth: "23rem" }}
                        >
                          <div class="card testimonial-card mt-2 mb-3">
                            <div class="card-up aqua-gradient"></div>
                            <div class="avatar mx-auto white">
                              <img
                                src="https://mdbootstrap.com/img/Photos/Avatars/img%20%2831%29.jpg"
                                class="rounded-circle img-fluid"
                                alt="woman avatar"
                                style={{ cursor: "pointer" }}
                              />
                            </div>
                            <div class="card-body text-center">
                              <h4
                                class="card-title font-weight-bold"
                                style={{ cursor: "pointer" }}
                              >
                                {orgData.clubname}
                              </h4>
                              <hr />
                              <p>
                                <strong>Email: {orgData.email}</strong>
                              </p>
                              <p>
                                <i class="fas fa-quote-left"></i>
                                <span style={{ marginLeft: "5px" }}>
                                  {orgData.address}
                                </span>
                              </p>
                            </div>
                          </div>
                        </section>
                      </div>
                    </div>
              </div> */}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default AdminOrgDetailed;
{
  /**/
}
