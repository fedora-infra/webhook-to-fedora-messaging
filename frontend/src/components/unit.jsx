import { mdiContentSave, mdiDelete, mdiRefreshCircle } from "@mdi/js";
import Icon from "@mdi/react";
import { isEqual } from "lodash";
import { useState } from "react";
import { Button, ButtonGroup, FloatingLabel, Form, OverlayTrigger, Tooltip } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import { useDispatch, useSelector } from "react-redux";

import { ServiceTypes } from "../config/data.js";
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
} from "../features/part.jsx";

function UnitCard({ data }) {
  const dispatch = useDispatch();
  const username = useSelector((data) => (data.auth.user ? data.auth.user.preferred_username : ""));

  const cleanupData = (data) => ({
    name: data.name,
    desc: data.desc,
    type: data.type,
    user: username,
  });

  const [formData, setFormData] = useState(cleanupData(data));

  const onChange = (e) => {
    const fieldName = e.target.name;
    const fieldValue = e.target.value;
    setFormData({ ...formData, [fieldName]: fieldValue });
  };

  const onSave = (e) => {
    e.preventDefault();
    if (isEqual(formData, cleanupData(data))) {
      dispatch(hideFlagArea());
      dispatch(keepFlagHead("Bind updating failed"));
      dispatch(keepFlagBody("Attempt updating again after making some changes"));
      dispatch(showFlagArea());
      dispatch(failFlagStat());
    } else {
      // cleanup the data
      dispatch(prepPrevData(cleanupData(data)));
      dispatch(prepNextData(formData));
      dispatch(prepBindUuid(data.uuid));
      dispatch(showUpdating());
    }
  };

  return (
    <Card className="shadow-sm mb-3" border="tertiary" id={`card-${data.uuid}`}>
      <form onSubmit={onSave}>
        <Card.Header className="d-flex justify-content-between align-items-center bg-body-secondary p-1">
          <span className="monoelem fw-bold pt-1 ps-1">{data.uuid}</span>
          <span className="pe-1">
            <ButtonGroup size="sm">
              <OverlayTrigger placement="bottom" overlay={<Tooltip>UPDATE</Tooltip>}>
                <Button
                  size="sm"
                  variant="outline-success"
                  className="d-flex justify-content-center align-items-center"
                  type="submit"
                >
                  <Icon path={mdiContentSave} size={0.75} />
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
                  <Icon path={mdiRefreshCircle} size={0.75} />
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
                  <Icon path={mdiDelete} size={0.75} />
                </Button>
              </OverlayTrigger>
            </ButtonGroup>
          </span>
        </Card.Header>
        <Card.Body className="p-2">
          <div className="row g-2">
            <div className="col-md-6 col-12">
              <FloatingLabel className="small" controlId={`name-${data.uuid}`} label="Name">
                <Form.Control className="monoelem" name="name" onChange={onChange} value={formData.name || ""} />
              </FloatingLabel>
            </div>
            <div className="col-md-6 col-12">
              <FloatingLabel className="small" controlId={`desc-${data.uuid}`} label="Description">
                <Form.Control className="monoelem" name="desc" onChange={onChange} value={formData.desc || ""} />
              </FloatingLabel>
            </div>
            <div className="col-md-6 col-12">
              <FloatingLabel className="small" controlId={`link-${data.uuid}`} label="Endpoint">
                <Form.Control className="monoelem" value={data.webhook_url} readOnly={true} />
              </FloatingLabel>
            </div>
            <div className="col-md-6 col-12">
              <FloatingLabel className="small" controlId={`code-${data.uuid}`} label="Token">
                <Form.Control className="monoelem" value={data.token} readOnly={true} />
              </FloatingLabel>
            </div>
            <div className="col-md-6 col-12">
              <FloatingLabel className="small" controlId={`type-${data.uuid}`} label="Service">
                <Form.Select className="monoelem" name="type" onChange={onChange} value={formData.type}>
                  {Object.keys(ServiceTypes)
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
                <Form.Control className="monoelem" name="user" onChange={onChange} value={formData.user || ""} />
              </FloatingLabel>
            </div>
          </div>
        </Card.Body>
      </form>
    </Card>
  );
}

export default UnitCard;
