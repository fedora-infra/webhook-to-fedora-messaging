import { mdiCheckCircle, mdiCloseCircle } from "@mdi/js";
import Icon from "@mdi/react";
import { Toast, ToastContainer } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import { hideFlagArea } from "../features/part.jsx";

function FlagArea() {
  const show = useSelector((data) => data.area.flagarea);
  const head = useSelector((data) => data.area.flaghead);
  const body = useSelector((data) => data.area.flagbody);
  const stat = useSelector((data) => data.area.flagstat);
  const dispatch = useDispatch();

  return (
    <ToastContainer position="top-center" className="p-4" style={{ position: "fixed", zIndex: 2000 }}>
      <Toast
        className="align-items-center d-inline-block m-1"
        show={show}
        onClose={() => dispatch(hideFlagArea())}
        delay={4000}
        autohide
      >
        <Toast.Header>
          {stat ? (
            <Icon path={mdiCheckCircle} size={0.75} className="me-2" />
          ) : (
            <Icon path={mdiCloseCircle} size={0.75} className="me-2" />
          )}

          <strong className="me-auto">{head}</strong>
        </Toast.Header>
        <Toast.Body className="small">{body}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
}

export default FlagArea;
