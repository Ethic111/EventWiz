import React, { useState } from "react";
import UserLogin from "./UserLogin";
import UserRegister1 from "./UserRegister1";

function User() {
  const [Ubooleanvalue, setUBoolean] = useState(true);

  return (
    <>
      <div>
        {Ubooleanvalue ? (
          <UserLogin setUserBoolean={setUBoolean} />
        ) : (
          <UserRegister1 setUserBoolean={setUBoolean} />
        )}
      </div>
    </>
  );
}

export default User;
