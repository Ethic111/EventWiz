import React,{useState} from "react";
import OrganizeLogin from "./OrganizeLogin";
import OrganizeRegister1 from "./OrganizeRegister1";

function Organize() {
  const [Obooleanvalue, setOBoolean] = useState(true);

  return (
    <>
      <div>
        {Obooleanvalue ? (
          <OrganizeLogin setOBoolean={setOBoolean} />
        ) : (
          <OrganizeRegister1 setOBoolean={setOBoolean} />
        )}
      </div>
    </>
  );
}

export default Organize;
