import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import OrganisationNavbar from "../OrganisationNavbar";
import "../../css/OrganisationEvent/OrganisationMembership.css";

function OrganisationMemberships() {
  const [memTypeTable, setMemTypetable] = useState([]);
  const [orgData, setOrgData] = useState(
    JSON.parse(localStorage.getItem("organisers"))
  );
  const [showAddMembership, setShowAddMembership] = useState(false);
  const [newMembershipForm, setNewMembershipForm] = useState({
    type: "",
    price: "",
  });

  const navigate = useNavigate();

  const fetchAllMembershipdetails = async () => {
    try {
      const cname = orgData.clubname;
      const response = await api.post("/organisationgetallmembership/", {
        clubname: cname,
      });
      setMemTypetable(response.data);
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching details:", error);
    }
  };

  useEffect(() => {
    fetchAllMembershipdetails();
  }, []);

  const handleAddMembershipClick = () => {
    setShowAddMembership(!(showAddMembership));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewMembershipForm({
      ...newMembershipForm,
      [name]: value,
    });
  };

  const handleAddMembershipSubmit = async (e) => {
    e.preventDefault();
    console.log(newMembershipForm);
    try {
      const data = {
        formdata: newMembershipForm,
        clubID: orgData._id,
      };
      const response = await api.post("/organisationaddnewmemtype", data);
      if (response.data.success !== false){

        setShowAddMembership(false);
      }
      else{
        alert(response.data.error)
      }
      setNewMembershipForm({
        type: "",
        price: "",
      });
      fetchAllMembershipdetails();
    } catch (error) {
      console.error("Error adding membership:", error);
      toast.error("Error adding membership. Please try again.");
    }
  };

  return (
    <div>
      <OrganisationNavbar />
      <div>
        <button className="addpostbtn mt-3" onClick={handleAddMembershipClick}>
          Add New Membership
        </button>
      </div>
      <div className="container">
        {showAddMembership && (
          <form onSubmit={handleAddMembershipSubmit}>
            <div className="row gy-3 overflow-hidden">
              <div className="col-4">
                <div className="form-floating mb-3">
                  <input
                    onChange={handleInputChange}
                    type="text"
                    className="form-control"
                    id="type"
                    placeholder=""
                    name="type"
                    value={newMembershipForm.type}
                  />
                  <label htmlFor="type" className="form-label">
                    Type
                  </label>
                </div>
              </div>
              <div className="col-4">
                <div className="form-floating mb-3">
                  <input
                    onChange={handleInputChange}
                    type="number"
                    className="form-control"
                    id="price"
                    placeholder=""
                    name="price"
                    value={newMembershipForm.price}
                  />
                  <label htmlFor="price" className="form-label">
                    Price
                  </label>
                </div>
              </div>
              <div className="col-4">
                <div>
                  <button type="submit" className="memtypesavesubmitbtn">
                    Save
                  </button>
                </div>
              </div>
            </div>
          </form>
        )}

        {memTypeTable && memTypeTable.length ? (
          <table className="table table-bordered m-3">
            <thead>
              <tr>
                <th scope="col" className="tablehead align-middle">
                  Sno
                </th>
                <th scope="col" className="tablehead align-middle">
                  Membership Type
                </th>
                <th scope="col" className="tablehead align-middle">
                  Price
                </th>
                <th scope="col" className="tablehead align-middle">
                  Update
                </th>
                <th scope="col" className="tablehead align-middle">
                  Delete
                </th>
              </tr>
            </thead>
            <tbody>
              {memTypeTable.map((type, index) => (
                <tr key={type.memberid}>
                  <td className="trtext">{index + 1}</td>
                  <td className="trtext">{type.type}</td>
                  <td className="trtext">{type.price}</td>
                  <td className="trtext">
                    <button
                      className="addmembtn"
                      // onClick={() => handlememberupdate(type)}
                    >
                      Update
                    </button>
                  </td>
                  <td className="trtext">
                    <button
                      className="addmembtn"
                      // onClick={() => deleteMember(type)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No Records...</p>
        )}
      </div>
    </div>
  );
}

export default OrganisationMemberships;
