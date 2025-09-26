import { mdiContentSave, mdiDelete } from "@mdi/js";
import Icon from "@mdi/react";
import { useState } from "react";
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

function Creation() {
  const show = useSelector((data) => data.area.creation);
  const dispatch = useDispatch();
  const defaultFormData = {
    // Default value is the first in the select options
    type: Object.keys(ServiceTypes).sort()[0],
  };

  const [formData, setFormData] = useState(defaultFormData);

  const onChange = (e) => {
    const fieldName = e.target.name;
    const fieldValue = e.target.value;
    setFormData({ ...formData, [fieldName]: fieldValue });
  };

  async function saveUnit(e) {
    e.preventDefault();
    let data;
    try {
      data = await apiCall({
        method: "POST",
        path: `/services`,
        body: {
          data: formData,
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
    setFormData(defaultFormData);
  }

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
            <form onSubmit={saveUnit}>
              <Card.Header className="d-flex justify-content-between align-items-center bg-body-secondary p-1">
                <span className="monoelem fw-bold pt-1 ps-1">Create</span>
                <span className="pe-1">
                  <ButtonGroup size="sm">
                    <OverlayTrigger placement="bottom" overlay={<Tooltip>SAVE</Tooltip>}>
                      <Button
                        size="sm"
                        variant="outline-success"
                        className="d-flex justify-content-center align-items-center"
                        type="submit"
                      >
                        <Icon path={mdiContentSave} size={0.75} />
                      </Button>
                    </OverlayTrigger>
                    <OverlayTrigger placement="bottom" overlay={<Tooltip>WIPE</Tooltip>}>
                      <Button
                        size="sm"
                        variant="outline-danger"
                        className="d-flex justify-content-center align-items-center"
                        onClick={() => {
                          dispatch(hideCreation());
                          setFormData(defaultFormData);
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
                  <div className="col-md-4 col-12">
                    <FloatingLabel className="small" controlId="name-make" label="Name">
                      <Form.Control className="monoelem" name="name" onChange={onChange} value={formData.name || ""} />
                    </FloatingLabel>
                  </div>
                  <div className="col-md-4 col-12">
                    <FloatingLabel className="small" controlId="desc-make" label="Description">
                      <Form.Control className="monoelem" name="desc" onChange={onChange} value={formData.desc || ""} />
                    </FloatingLabel>
                  </div>
                  <div className="col-md-4 col-12">
                    <FloatingLabel className="small" controlId="type-make" label="Service">
                      <Form.Select className="monoelem" name="type" onChange={onChange} value={formData.type || ""}>
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
            </form>
          </Card>
        </Offcanvas.Body>
      </Container>
    </Offcanvas>
  );
}

export default Creation;
