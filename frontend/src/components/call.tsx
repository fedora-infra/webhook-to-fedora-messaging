import { useEffect } from "react";
import { useDispatch } from "react-redux";
import type { AppDispatch } from "../features/data.ts";
import { useNavigate } from "react-router";

import { userManager } from "../config/oidc.ts";
import { loadUserData } from "../features/auth.ts";

function Callback() {
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

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
