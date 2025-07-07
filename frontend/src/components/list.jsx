import ListGroup from "react-bootstrap/ListGroup";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { keepServices } from "../features/part.jsx";
import UnitCard from "./unit.jsx";

function MainList() {
  const dispatch = useDispatch();
  const list = useSelector((data) => data.area.services);
  const user = useSelector((data) => data.auth.user);

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
