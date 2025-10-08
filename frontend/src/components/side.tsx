import React from "react";
import { mdiBug, mdiCodeJson, mdiHomeAccount, mdiLinkCircleOutline, mdiPlusThick, mdiWeb } from "@mdi/js";
import Icon from "@mdi/react";
import { ListGroup } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router";

import { ServiceTypes } from "../config/data.ts";
import type { AppDispatch, RootState } from "../features/data.ts";
import {
  failFlagStat,
  hideCreation,
  hideFlagArea,
  keepFlagBody,
  keepFlagHead,
  showCreation,
  showFlagArea,
} from "../features/part.ts";

const IconComponent = Icon as unknown as React.ComponentType<{ path: string; size?: number | string; className?: string }>;


function SideMenu() {
  const dispatch = useDispatch<AppDispatch>();
  const user = useSelector((state: RootState) => state.auth.user);

  return (
    <div className="sticky-md-top side">
      <ListGroup variant="flush">
          <ListGroup.Item action className="small d-flex align-items-center ps-2 pe-2" as={Link} to="/">
          <IconComponent className="me-2" size={0.75} path={mdiHomeAccount} />
          Home
        </ListGroup.Item>
        <ListGroup.Item
          action
          className="small d-flex align-items-center ps-2 pe-2"
          as={Link}
          to="https://pagure.io/fedora-infrastructure/issues"
          target="_blank"
        >
          <IconComponent className="me-2" size={0.75} path={mdiBug} />
          Report
        </ListGroup.Item>
        <ListGroup.Item
          action
          className="small d-flex align-items-center ps-2 pe-2"
          as={Link}
          to="https://github.com/fedora-infra/webhook-to-fedora-messaging"
          target="_blank"
        >
          <IconComponent className="me-2" size={0.75} path={mdiCodeJson} />
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
          <IconComponent className="me-2" size={0.75} path={mdiPlusThick} />
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
          <IconComponent className="me-2" size={0.75} path={mdiWeb} />
          API
        </ListGroup.Item>
        {(Object.keys(ServiceTypes) as Array<keyof typeof ServiceTypes>)
          .sort()
          .map((serviceType) => (
            <ListGroup.Item
              key={serviceType}
              action
              className="small d-flex align-items-center ps-2 pe-2"
              as={Link}
              to={`/${serviceType}`}
            >
              <IconComponent className="me-2" size={0.75} path={mdiLinkCircleOutline} />
              {ServiceTypes[serviceType].name}
            </ListGroup.Item>
          ))}
      </ListGroup>
    </div>
  );
}

export default SideMenu;
