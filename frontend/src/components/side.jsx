import ListGroup from "react-bootstrap/ListGroup";
import { Link } from "react-router";
import { useDispatch, useSelector } from "react-redux";
import {
  failFlagStat,
  hideCreation,
  hideFlagArea,
  keepFlagBody,
  keepFlagHead,
  showCreation,
  showFlagArea,
} from "../features/part.jsx";

import Icon from "@mdi/react";
import { mdiHomeAccount, mdiBug, mdiPlusThick, mdiCodeJson, mdiWeb, mdiLinkCircleOutline } from "@mdi/js";

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
          to="/docs"
          target="_blank"
        >
          <Icon className="me-2" size={0.75} path={mdiWeb} />
          API
        </ListGroup.Item>
        <ListGroup.Item action className="small d-flex align-items-center ps-2 pe-2" as={Link} to="/forgejo">
          <Icon className="me-2" size={0.75} path={mdiLinkCircleOutline} />
          Forgejo
        </ListGroup.Item>
        <ListGroup.Item action className="small d-flex align-items-center ps-2 pe-2" as={Link} to="/github">
          <Icon className="me-2" size={0.75} path={mdiLinkCircleOutline} />
          GitHub
        </ListGroup.Item>
        <ListGroup.Item action className="small d-flex align-items-center ps-2 pe-2" as={Link} to="/gitlab">
          <Icon className="me-2" size={0.75} path={mdiLinkCircleOutline} />
          GitLab
        </ListGroup.Item>
      </ListGroup>
    </div>
  );
}

export default SideMenu;
