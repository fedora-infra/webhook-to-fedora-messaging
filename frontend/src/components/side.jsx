import { mdiBug, mdiCodeJson, mdiHomeAccount, mdiLinkCircleOutline, mdiPlusThick, mdiWeb } from "@mdi/js";
import Icon from "@mdi/react";
import ListGroup from "react-bootstrap/ListGroup";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router";

import { ServiceTypes } from "../config/data";
import {
  failFlagStat,
  hideCreation,
  hideFlagArea,
  keepFlagBody,
  keepFlagHead,
  showCreation,
  showFlagArea,
} from "../features/part.jsx";

function SideMenu() {
  const dispatch = useDispatch();
  const user = useSelector((data) => data.auth.user);

  return (
    <div className="sticky-md-top side">
      <ListGroup variant="flush">
        <ListGroup.Item action className="small d-flex align-items-center ps-2 pe-2" as={Link} to="/">
          <Icon className="me-2" size={0.75} path={mdiHomeAccount} />
          Home
        </ListGroup.Item>
        <ListGroup.Item
          action
          className="small d-flex align-items-center ps-2 pe-2"
          as={Link}
          to="https://pagure.io/fedora-infrastructure/issues"
          target="_blank"
        >
          <Icon className="me-2" size={0.75} path={mdiBug} />
          Report
        </ListGroup.Item>
        <ListGroup.Item
          action
          className="small d-flex align-items-center ps-2 pe-2"
          as={Link}
          to="https://github.com/fedora-infra/webhook-to-fedora-messaging"
          target="_blank"
        >
          <Icon className="me-2" size={0.75} path={mdiCodeJson} />
          Source
        </ListGroup.Item>
        <ListGroup.Item
          action
          className="small d-flex align-items-center ps-2 pe-2"
          onClick={() => {
            if (user) {
              dispatch(showCreation());
            } else {
              dispatch(hideCreation());
              dispatch(hideFlagArea());
              dispatch(keepFlagHead("Bind creation failed"));
              dispatch(keepFlagBody("You need to be logged in first"));
              dispatch(showFlagArea());
              dispatch(failFlagStat());
            }
          }}
        >
          <Icon className="me-2" size={0.75} path={mdiPlusThick} />
          Create
        </ListGroup.Item>
      </ListGroup>
      <br />
      <ListGroup variant="flush">
        <ListGroup.Item
          action
          className="small d-flex align-items-center ps-2 pe-2"
          as={Link}
          to={`${import.meta.env.VITE_API_URL}/docs`}
          target="_blank"
        >
          <Icon className="me-2" size={0.75} path={mdiWeb} />
          API
        </ListGroup.Item>
        {Object.keys(ServiceTypes)
          .sort()
          .map((serviceType) => (
            <ListGroup.Item
              key={serviceType}
              action
              className="small d-flex align-items-center ps-2 pe-2"
              as={Link}
              to={`/${serviceType}`}
            >
              <Icon className="me-2" size={0.75} path={mdiLinkCircleOutline} />
              {ServiceTypes[serviceType].name}
            </ListGroup.Item>
          ))}
      </ListGroup>
    </div>
  );
}

export default SideMenu;
