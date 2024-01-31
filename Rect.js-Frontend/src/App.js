import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/jsx/HomePage";
import Home from "./components/jsx/Home";
import About from "./components/jsx/About";
import NotFound from "./components/jsx/NotFound";
import Eventpage1 from "./components/jsx/UserEvent/Eventpage1";
import LoginPage from "./components/jsx/LoginRegister/LoginPage";
import OrganisationEvent from "./components/jsx/OrganisationEvent/OrganisationEvent";
import OrgAddPost from "./components/jsx/OrganisationEvent/OrgAddPost"
import OrgEvent from "./components/jsx/OrganisationEvent/OrgEvent";
import { ToastContainer } from "react-toastify";
import EventDetailedView from "./components/jsx/OrganisationEvent/EventDetailedView";
import OrgMemberDetails from "./components/jsx/OrganisationEvent/OrgMemberDetails";
import OrgAddMember from "./components/jsx/OrganisationEvent/OrgAddMember";
import UpdateMemberDetail from "./components/jsx/OrganisationEvent/UpdateMemberDetail";
import OrganisationMemberships from "./components/jsx/OrganisationEvent/OrganisationMemberships";
import OrgOtherEvents from "./components/jsx/OrganisationEvent/OrgOtherEvents";
import AdminLogin from "./components/jsx/Admin/AdminLogin";
import AdminHome from "./components/jsx/Admin/AdminHome";
import AdminOrg from "./components/jsx/Admin/AdminOrg";
import AdminOrgDetailed from "./components/jsx/Admin/AdminOrgDetailed";
import AdminUser from "./components/jsx/Admin/AdminUser";
import AdminAuthority from "./components/jsx/Admin/AdminAuthority";
import AdminAuthorityOrgDetails from "./components/jsx/Admin/AdminAuthorityOrgDetails";
// import Admin  from "./Admin/Views/Admin";


function App() {
  return (
    <>
    <ToastContainer/>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/home" element={<Home />} />
          <Route path="/events" element={<Eventpage1/>} />
          <Route path="/loginregister" element={<LoginPage />} />
          <Route path="/aboutus" element={<About />} />
          {/* Organisation----------------------------------- */}
          <Route path="/organisationevents" element={<OrganisationEvent/>} />
          <Route path="/organisationevents/addpost" element={<OrgAddPost/>} />
          <Route path="/organisationevents/orgevents" element={<OrgEvent/>} />
          <Route path="/organisationevents/detailedview" element={<EventDetailedView/>} />
          <Route path="/organisationevents/organizationmemberdetails" element={<OrgMemberDetails/>} />
          <Route path="/organisationevents/organizationupdatememberdetails" element={<UpdateMemberDetail/>} />
          <Route path="/organisationevents/organizationaddmember" element={<OrgAddMember/>} />
          <Route path="/organisationevents/organisationmemberships" element={<OrganisationMemberships/>} />
          <Route path="/organisationevents/otherevents" element={<OrgOtherEvents/>} />
          {/* ----------------------------------- */}
         
         {/* Admin------------------------------------ */}
         <Route path="/admin" element={<AdminLogin/>} />
         <Route path="/admin/home" element={<AdminHome/>} />
         <Route path="/admin/allorg" element={<AdminOrg/>} />
         <Route path="/admin/orgdetailspage" element={<AdminOrgDetailed/>} />
         <Route path="/admin/allusers" element={<AdminUser/>} />
         <Route path="/admin/accepetrejectorg" element={<AdminAuthority/>} />
         <Route path="/admin/appliedorgdetails" element={<AdminAuthorityOrgDetails/>} />
         
         {/* ----------------------------------------- */}
          <Route path="*" element={<NotFound/>} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
