import { mdiContentSave, mdiDelete } from "@mdi/js";
import Icon from "@mdi/react";
import { Button, ButtonGroup, FloatingLabel, Form, OverlayTrigger, Tooltip } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Offcanvas from "react-bootstrap/Offcanvas";
import { useDispatch, useSelector } from "react-redux";

import { ServiceTypes } from "../config/data.js";
import { apiCall } from "../features/api.js";
import {
  failFlagStat,
  hideCreation,
  hideFlagArea,
  keepFlagBody,
  keepFlagHead,
  keepServices,
  passFlagStat,
  showFlagArea,
} from "../features/part.jsx";

async function saveUnit(dispatch) {
  let data;
  try {
    data = await apiCall({
      method: "POST",
      path: `/services`,
      body: {
        data: {
          name: document.getElementById("name-make").value.trim(),
          desc: document.getElementById("desc-make").value.trim(),
          type: document.getElementById("type-make").value.trim(),
        },
      },
    });
  } catch (error) {
    dispatch(hideCreation());
    dispatch(hideFlagArea());
    dispatch(keepFlagHead("Bind creation failed"));
    dispatch(keepFlagBody(`Encountered "${error.toString()}" response during creation`));
    dispatch(showFlagArea());
    dispatch(failFlagStat());
    return;
  } finally {
    dispatch(keepServices());
  }
  dispatch(hideCreation());
  dispatch(hideFlagArea());
  dispatch(keepFlagHead(`Bind #${data.uuid} created`));
  dispatch(keepFlagBody("Relevant information can be found on the dashboard"));
  dispatch(showFlagArea());
  dispatch(passFlagStat());
}

function Creation() {
  const show = useSelector((data) => data.area.creation);
  const dispatch = useDispatch();

  return (
    <Offcanvas
      className="bg-body-tertiary shadow-sm"
      style={{ height: "fit-content" }}
      show={show}
      onHide={() => dispatch(hideCreation())}
      placement="bottom"
      scroll={true}
      backdrop={true}
    >
      <Container>
        <Offcanvas.Body>
          <Card className="shadow-sm" border="tertiary" id="card-make">
            <Card.Header className="d-flex justify-content-between align-items-center bg-body-secondary p-1">
              <span className="monoelem fw-bold pt-1 ps-1">Create</span>
              <span className="pe-1">
                <ButtonGroup size="sm">
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>SAVE</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-success"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => saveUnit(dispatch)}
                    >
                      <Icon path={mdiContentSave} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>WIPE</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-danger"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => dispatch(hideCreation())}
                    >
                      <Icon path={mdiDelete} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                </ButtonGroup>
              </span>
            </Card.Header>
            <Card.Body className="p-2">
              <div className="row g-2">
                <div className="col-md-4 col-12">
                  <FloatingLabel className="small" controlId="name-make" label="Name">
                    <Form.Control className="monoelem" />
                  </FloatingLabel>
                </div>
                <div className="col-md-4 col-12">
                  <FloatingLabel className="small" controlId="desc-make" label="Description">
                    <Form.Control className="monoelem" />
                  </FloatingLabel>
                </div>
                <div className="col-md-4 col-12">
                  <FloatingLabel className="small" controlId="type-make" label="Service">
                    <Form.Select className="monoelem">
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
              </div>
            </Card.Body>
          </Card>
        </Offcanvas.Body>
      </Container>
    </Offcanvas>
  );
}

export default Creation;
