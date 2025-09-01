import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router";

import { userManager } from "../config/oidc.js";
import { loadUserData } from "../features/auth.jsx";

function Callback() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    userManager
      .signinRedirectCallback()
      .then(() => {
        dispatch(loadUserData());
        navigate("/");
      })
      .catch((expt) => {
        console.error("OIDC callback error", expt);
      });
  }, [dispatch, navigate]);

  return (
    <>
      <h2 className="headelem head">Webhook To Fedora Messaging</h2>
      <p className="small">Please wait while we sign you in</p>
    </>
  );
}

export default Callback;
