import React from "react";
import { mdiContentSave, mdiDelete, mdiRefreshCircle } from "@mdi/js";
import Icon from "@mdi/react";
import { Button, ButtonGroup, FloatingLabel, Form, OverlayTrigger, Tooltip, Card } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import { ServiceTypes } from "../config/data.ts";
import type { AppDispatch, RootState } from "../features/data.ts";
const IconComponent = Icon as unknown as React.ComponentType<{ path: string; size?: number | string; className?: string }>;
import {
  failFlagStat,
  hideFlagArea,
  keepFlagBody,
  keepFlagHead,
  prepBindUuid,
  prepNextData,
  prepPrevData,
  showFlagArea,
  showReviving,
  showRevoking,
  showUpdating,
} from "../features/part.ts";

interface UnitCardProps {
  data: any;
}

function UnitCard({ data }: UnitCardProps) {
  const dispatch = useDispatch<AppDispatch>();
  const username = useSelector((state: RootState) => (state.auth.user ? state.auth.user.preferred_username : ""));

  return (
    <Card className="shadow-sm mb-3" border="tertiary" id={`card-${data.uuid}`}>
      <Card.Header className="d-flex justify-content-between align-items-center bg-body-secondary p-1">
        <span className="monoelem fw-bold pt-1 ps-1">{data.uuid}</span>
        <span className="pe-1">
          <ButtonGroup size="sm">
            <OverlayTrigger placement="bottom" overlay={<Tooltip>UPDATE</Tooltip>}>
              <Button
                size="sm"
                variant="outline-success"
                className="d-flex justify-content-center align-items-center"
                onClick={() => {
                  if (
                    data.name === (document.getElementById(`name-${data.uuid}`) as HTMLInputElement | null)?.value &&
                    data.desc === (document.getElementById(`desc-${data.uuid}`) as HTMLInputElement | null)?.value &&
                    data.type === (document.getElementById(`type-${data.uuid}`) as HTMLSelectElement | null)?.value &&
                    username === (document.getElementById(`user-${data.uuid}`) as HTMLInputElement | null)?.value
                  ) {
                    dispatch(hideFlagArea());
                    dispatch(keepFlagHead("Bind updating failed"));
                    dispatch(keepFlagBody("Attempt updating again after making some changes"));
                    dispatch(showFlagArea());
                    dispatch(failFlagStat());
                  } else {
                    dispatch(prepPrevData({ name: data.name, desc: data.desc, type: data.type, user: username }));
                    dispatch(
                      prepNextData({
                        name: (document.getElementById(`name-${data.uuid}`) as HTMLInputElement | null)?.value ?? "",
                        desc: (document.getElementById(`desc-${data.uuid}`) as HTMLInputElement | null)?.value ?? "",
                        type: (document.getElementById(`type-${data.uuid}`) as HTMLSelectElement | null)?.value ?? "",
                        user: (document.getElementById(`user-${data.uuid}`) as HTMLInputElement | null)?.value ?? "",
                      })
                    );
                    dispatch(prepBindUuid(data.uuid));
                    dispatch(showUpdating());
                  }
                }}
              >
                <IconComponent path={mdiContentSave} size={0.75} />
              </Button>
            </OverlayTrigger>
            <OverlayTrigger placement="bottom" overlay={<Tooltip>REGENERATE</Tooltip>}>
              <Button
                size="sm"
                variant="outline-primary"
                className="d-flex justify-content-center align-items-center"
                onClick={() => {
                  dispatch(prepBindUuid(data.uuid));
                  dispatch(showReviving());
                }}
              >
                <IconComponent path={mdiRefreshCircle} size={0.75} />
              </Button>
            </OverlayTrigger>
            <OverlayTrigger placement="bottom" overlay={<Tooltip>REVOKE</Tooltip>}>
              <Button
                size="sm"
                variant="outline-danger"
                className="d-flex justify-content-center align-items-center"
                onClick={() => {
                  dispatch(prepBindUuid(data.uuid));
                  dispatch(showRevoking());
                }}
              >
                <IconComponent path={mdiDelete} size={0.75} />
              </Button>
            </OverlayTrigger>
          </ButtonGroup>
        </span>
      </Card.Header>
      <Card.Body className="p-2">
        <div className="row g-2">
          <div className="col-md-6 col-12">
            <FloatingLabel className="small" controlId={`name-${data.uuid}`} label="Name">
              <Form.Control className="monoelem" defaultValue={data.name} />
            </FloatingLabel>
          </div>
          <div className="col-md-6 col-12">
            <FloatingLabel className="small" controlId={`desc-${data.uuid}`} label="Description">
              <Form.Control className="monoelem" defaultValue={data.desc} />
            </FloatingLabel>
          </div>
          <div className="col-md-6 col-12">
            <FloatingLabel className="small" controlId={`link-${data.uuid}`} label="Endpoint">
              <Form.Control className="monoelem" defaultValue={data.webhook_url} readOnly={true} />
            </FloatingLabel>
          </div>
          <div className="col-md-6 col-12">
            <FloatingLabel className="small" controlId={`code-${data.uuid}`} label="Token">
              <Form.Control className="monoelem" defaultValue={data.token} readOnly={true} />
            </FloatingLabel>
          </div>
          <div className="col-md-6 col-12">
            <FloatingLabel className="small" controlId={`type-${data.uuid}`} label="Service">
              <Form.Select className="monoelem" defaultValue={data.type}>
                {(Object.keys(ServiceTypes) as Array<keyof typeof ServiceTypes>)
                  .sort()
                  .map((serviceType) => (
                    <option key={serviceType} value={serviceType}>
                      {ServiceTypes[serviceType].name}
                    </option>
                  ))}
              </Form.Select>
            </FloatingLabel>
          </div>
          <div className="col-md-6 col-12">
            <FloatingLabel className="small" controlId={`user-${data.uuid}`} label="Owner">
              <Form.Control className="monoelem" defaultValue={username} />
            </FloatingLabel>
          </div>
        </div>
      </Card.Body>
    </Card>
  );
}

export default UnitCard;
