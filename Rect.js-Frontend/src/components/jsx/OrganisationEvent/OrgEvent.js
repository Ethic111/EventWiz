import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import $ from "jquery";
import OrganisationNavbar from "../OrganisationNavbar";
import "../../css/OrganisationEvent/orgEvent.css";
import api from "../api";
import {
  FaArrowCircleRight,
  FaArrowCircleLeft,
  FaRupeeSign,
} from "react-icons/fa";
// import { TbClockPlay } from "react-icons/tb";

function OrgEvent() {
  const [details, setDetails] = useState();
  const [userData, setUserData] = useState(
    JSON.parse(localStorage.getItem("organisers"))
  );
  const [searchForm, setSearchform] = useState({
    event_title: "",
  });

  const [modalEaseIn, setModalEaseIn] = useState("");

  useEffect(() => {
    fetchAllPostdetails();

    $(".modal").each(function () {
      $(this).on("show.bs.modal", function () {
        const easeIn = $(this).attr("data-easein");
        setModalEaseIn(easeIn);

        if (["bounce"].includes(easeIn)) {
          $(".modal-dialog").velocity(`callout.${easeIn}`);
        } else {
          $(".modal-dialog").velocity(`transition.${easeIn}`);
        }
      });
    });
  }, []);

  const [isCol2Visible, setIsCol2Visible] = useState(true);

  const toggleCol2Visibility = () => {
    setIsCol2Visible(!isCol2Visible);
  };

  const fetchAllPostdetails = async () => {
    try {
      console.log(userData.clubname);
      const cname = userData.clubname; //Rajpath
      console.log(typeof cname); //string
      const response = await api.post("/geteventposts/", { clubname: cname });
      setDetails(response.data);
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching details:", error);
    }
  };

  const navigate = useNavigate();
  const handlepostdetails = (post) => {
    // console.log(JSON.stringify(post))
    navigate("/organisationevents/detailedview", {
      state: JSON.stringify(post),
    });
  };

  const handledeletepost = async (post) => {
    console.log("deleting button");
    try {
      const response = await api.delete(`/deleteeventposts/${post._id}`);
      console.log(response);
      fetchAllPostdetails();
    } catch {
      alert("Error in Deleting");
    }
  };

  // /////////////

  const [lFormData, setLFormData] = useState({
    event_start_date: "",
    event_end_date: "",
    minprice: "",
    maxprice: "",
    venue_city: "",
  });

  function formatDateForInput(dateString) {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      return ""; // Invalid date, return an empty string
    }
    return date.toISOString().split("T")[0];
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setLFormData({
      ...lFormData,
      [name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    // Filter out key-value pairs with empty values
    const filteredFormData = {};
    for (const key in lFormData) {
      if (lFormData[key] !== "") {
        filteredFormData[key] = lFormData[key];
      }
    }
    console.log("Filtered form:");
    console.log(filteredFormData);

    // Now you can use filteredFormData in your API call
    try {
      console.log("Inside try for api calling:");
      const data = {"clubname": userData["clubname"],"filteredFormData": filteredFormData}
      const checking = await api.post("/orgfilters/", data);
      console.log(checking);
      if (checking.data.success !== false) {
        console.log(checking.data);
        setDetails(checking.data);
      } else {
        alert(checking.data.error);
      }

      // Rest of your code...
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  const handleformreset = () => {
    setLFormData({
      event_start_date: "",
      event_end_date: "",
      minprice: "",
      maxprice: "",
      venue_city: "",
    });
    setSearchform({
      event_title: "",
    });
    fetchAllPostdetails();
  };

  const handleSearchInputChange = (e) => {
    const { name, value } = e.target;
    setSearchform({
      ...searchForm,
      [name]: value,
    });
  };
  const handlesearchSubmit = async (event) => {
    event.preventDefault();

    const data = {
      clubname: userData["clubname"],
      title: searchForm["event_title"],
    };
    console.log("handle search submit");
    try {
      // console.log("hi");
      // const cname = orgData._id; //Rajpath
      // // console.log(typeof cname); //string
      const response = await api.post("/organisationeventpostsbytitle/", data);
      setDetails(response.data);
      // console.log(response.data);
    } catch (error) {
      console.error("Error fetching details:", error);
    }
  };
  // {
  //   "event_start_date": "",
  //   "event_end_date": "",
  //   "minprice": "210",
  //   "maxprice": "6590",
  //   "venue_city":""
  // }

  // const handleLoad = () =>{
  //   console.log("helo")
  // }
  return (
    <>
      <div>{<OrganisationNavbar />}</div>
      {/* <div>
        <Link to="/organisationevents/addpost">
          <button className="addpostbtn">Add New Post</button>
        </Link>
      </div> */}
      <div style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
        }}>
        <div>
          <Link to="/organisationevents/addpost">
            <button className="addpostbtn">Add New Post</button>
          </Link>
        </div>
        <div className="mt-0">
          <form className="form-inline my-lg-0 " onSubmit={handlesearchSubmit}>
            <div className="row">
              <div className="col-10 p-2">
                <input
                  className="form-control"
                  name="event_title"
                  type="text"
                  placeholder="Search"
                  aria-label="Search"
                  onChange={handleSearchInputChange}
                  value={searchForm.event_title}
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
            </div>
          </form>
        </div>
      </div>
      <hr />
      <div>
        <div className="loginmainEventdiv">
          <div className="row">
            {isCol2Visible ? (
              <div
                className="col-2"
                style={{
                  backgroundColor: "#0000",
                  color: "#0e2643",
                  cursor: "pointer",
                }}
              >
                <div className="d-flex flex-column align-items-end ">
                  <FaArrowCircleLeft
                    className="mt-2"
                    onClick={toggleCol2Visibility}
                    style={{ fontSize: "2.2rem" }}
                  />
                </div>
                <br />
                <div className="row">
                  <p className="col-6 card_title">Filter</p>
                  <div className="col-6">
                    <div className="d-grid">
                      <button className="addpostbtn" onClick={handleformreset}>
                        Reset
                      </button>
                    </div>
                  </div>
                </div>

                <form onSubmit={handleFormSubmit} style={{ margin: "0px" }}>
                  <div className="row gy-3 overflow-hidden">
                    <div className="col">
                      <div className="form-floating mb-3">
                        <input
                          onChange={handleInputChange}
                          type="date"
                          className="form-control"
                          id="event_start_date"
                          placeholder=""
                          name="event_start_date"
                          value={formatDateForInput(lFormData.event_start_date)}
                        />
                        <label
                          htmlFor="event_start_date"
                          className="form-label"
                        >
                          Start Date
                        </label>
                      </div>
                    </div>
                    <div className="col">
                      <div className="form-floating mb-3">
                        <input
                          onChange={handleInputChange}
                          type="date"
                          className="form-control"
                          id="event_end_date"
                          placeholder=""
                          name="event_end_date"
                          value={formatDateForInput(lFormData.event_end_date)}
                        />
                        <label htmlFor="event_end_date" className="form-label">
                          End Date
                        </label>
                      </div>
                    </div>
                    <div className="col">
                      Price
                      <div className="row">
                        <div className="col-6">
                          <div className="form-floating mb-3">
                            <input
                              onChange={handleInputChange}
                              type="number"
                              step="0.01"
                              className="form-control"
                              id="minprice"
                              placeholder=""
                              name="minprice"
                              value={lFormData.minprice}
                            />
                            <label htmlFor="minprice" className="form-label">
                              Min
                            </label>
                          </div>
                        </div>
                        <div className="col-6">
                          <div className="form-floating mb-3">
                            <input
                              onChange={handleInputChange}
                              type="number"
                              step="0.01"
                              className="form-control"
                              id="maxprice"
                              placeholder=""
                              name="maxprice"
                              value={lFormData.maxprice}
                            />
                            <label htmlFor="maxprice" className="form-label">
                              Max
                            </label>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="col-12">
                      <div className="form-floating mb-3">
                        <input
                          onChange={handleInputChange}
                          type="text"
                          className="form-control"
                          id="venue_city"
                          placeholder=""
                          name="venue_city"
                          value={lFormData.venue_city}
                        />
                        <label htmlFor="venue_city" className="form-label">
                          Venue City
                        </label>
                      </div>
                    </div>
                    <div className="col-12">
                      <div className="d-grid">
                        <button className="addpostbtn" type="submit">
                          Apply
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            ) : (
              <div className="col-12" style={{ cursor: "pointer" }}>
                <FaArrowCircleRight
                  className=" mt-2"
                  onClick={toggleCol2Visibility}
                  style={{ fontSize: "2.2rem" }}
                />
              </div>
            )}
            <div className={isCol2Visible ? "col-10" : "col-12"}>
              <br />
              <div className="row">
                {details && details.length ? (
                  details.map((post) => (
                    <div
                      key={post._id}
                      className={
                        isCol2Visible
                          ? "col-4 maincardbody"
                          : "col-3 maincardbody"
                      }
                    >
                      <div class="main">
                        <ul class="orgeventcards">
                          <li class="orgeventcards_item">
                            <div class="orgeventcard">
                              <div class="orgeventcard_image">
                                <img
                                  className="orgeventmaincardimage"
                                  src={post.event_image}
                                  alt="event image"
                                  onClick={() => handlepostdetails(post)}
                                  style={{ cursor: "pointer" }}
                                />
                                <span class="card_price cardspantag">
                                  <span>
                                    <FaRupeeSign />
                                    {post.ticket_price}
                                  </span>
                                </span>
                              </div>
                              <div class="orgeventcard_content">
                                <h2
                                  class="orgeventcard_title"
                                  onClick={() => handlepostdetails(post)}
                                  style={{ cursor: "pointer" }}
                                >
                                  {post.event_title}
                                </h2>
                                <div class="orgeventcard_text">
                                  <p class="cardptag">{post.event_highlight}</p>
                                  <p class="cardptag">
                                    Venue: {post.venue_name}
                                  </p>
                                  <span class="cardptag">
                                    Venue City: {post.venue_city}
                                  </span>
                                  <p class="cardptag">
                                    Event Type:
                                    <strong> {post.type} </strong>{" "}
                                  </p>
                                  <hr className="cardhrtag" />
                                  <p class="cardptag">
                                    Event Dates:
                                    <strong>
                                      {" "}
                                      {post.event_start_date}{" "}
                                    </strong>{" "}
                                    <span> TO </span>
                                    <strong> {post.event_end_date}</strong>
                                  </p>
                                  <button
                                    className="deletepostbtn"
                                    onClick={() => handledeletepost(post)}
                                  >
                                    Delete
                                  </button>
                                </div>
                              </div>
                            </div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  ))
                ) : (
                  <p>No Records...</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default OrgEvent;
{
  /**/
}
