import { mdiCheckCircle, mdiCloseCircle } from "@mdi/js";
import Icon from "@mdi/react";
import React from "react";
import { Toast, ToastContainer } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import type { AppDispatch,RootState } from "../features/data.ts";
import { hideFlagArea } from "../features/part.ts";

const IconComponent = Icon as unknown as React.ComponentType<{ path: string; size?: number | string; className?: string }>;

function FlagArea() {
  const show = useSelector((state: RootState) => state.area.flagarea);
  const head = useSelector((state: RootState) => state.area.flaghead);
  const body = useSelector((state: RootState) => state.area.flagbody);
  const stat = useSelector((state: RootState) => state.area.flagstat);
  const dispatch = useDispatch<AppDispatch>();

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
            <IconComponent path={mdiCheckCircle} size={0.75} className="me-2" />
          ) : (
            <IconComponent path={mdiCloseCircle} size={0.75} className="me-2" />
          )}

          <strong className="me-auto">{head}</strong>
        </Toast.Header>
        <Toast.Body className="small">{body}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
}

export default FlagArea;
