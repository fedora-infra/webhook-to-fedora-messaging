import React from "react";
import { useEffect } from "react";
import { ListGroup } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import type { AppDispatch, RootState } from "../features/data.ts";
import { keepServices } from "../features/part.ts";
import UnitCard from "./unit.jsx";

function MainList() {
  const dispatch = useDispatch<AppDispatch>();
  const list = useSelector((state: RootState) => state.area.services);
  const user = useSelector((state: RootState) => state.auth.user);

  useEffect(() => {
    dispatch(keepServices());
  }, [dispatch]);

  return (
    <>
      <h2 className="headelem head">Webhook To Fedora Messaging</h2>
      {user ? (
        <>
          <p className="small">
            Welcome {user.nickname} - What shall we achieve today using your webhook powered Fedora Messaging workflow?
          </p>
          <ListGroup>
            <ListGroup.Item className="mb-3 small p-1">{list.length} bind(s) created.</ListGroup.Item>
          </ListGroup>
          {Array.isArray(list) && list.length > 0 ? (
            list.map((data) => <UnitCard data={data} key={`card-${crypto.randomUUID()}`} />)
          ) : (
            <p className="small">
              Make your first Fedora Messaging bind by linking your service webhook using the&nbsp;
              <span className="fw-bold">Create</span> option.
            </p>
          )}
        </>
      ) : (
        <p className="small">
          Sign in to get started with empowering your workflows by connecting your webhooks to Fedora Messaging.
        </p>
      )}
    </>
  );
}

export default MainList;
