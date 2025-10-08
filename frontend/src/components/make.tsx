import { mdiContentSave, mdiDelete } from "@mdi/js";
import Icon from "@mdi/react";
import React from "react";
import { Button, ButtonGroup, Card, Container, FloatingLabel, Form, Offcanvas,OverlayTrigger, Tooltip } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import { ServiceTypes } from "../config/data.ts";
import { apiCall } from "../features/api.ts";
import type { AppDispatch, RootState } from "../features/data.ts";
const IconComponent = Icon as unknown as React.ComponentType<{ path: string; size?: number | string }>;
import {
  failFlagStat,
  hideCreation,
  hideFlagArea,
  keepFlagBody,
  keepFlagHead,
  keepServices,
  passFlagStat,
  showFlagArea,
} from "../features/part.ts";

async function saveUnit(dispatch: AppDispatch) {
  let data;
  try {
    data = await apiCall({
      method: "POST",
      path: `/services`,
      body: {
        data: {
          name: (document.getElementById("name-make") as HTMLInputElement | null)?.value.trim() ?? "",
          desc: (document.getElementById("desc-make") as HTMLInputElement | null)?.value.trim() ?? "",
          type: (document.getElementById("type-make") as HTMLSelectElement | null)?.value.trim() ?? "",
        },
      },
    });
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : String(error);
    dispatch(hideCreation());
    dispatch(hideFlagArea());
    dispatch(keepFlagHead("Bind creation failed"));
    dispatch(keepFlagBody(`Encountered "${errMsg}" response during creation`));
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
  const show = useSelector((state: RootState) => state.area.creation);
  const dispatch = useDispatch<AppDispatch>();

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
                      <IconComponent path={mdiContentSave} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>WIPE</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-danger"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => dispatch(hideCreation())}
                    >
                      <IconComponent path={mdiDelete} size={0.75} />
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
              </div>
            </Card.Body>
          </Card>
        </Offcanvas.Body>
      </Container>
    </Offcanvas>
  );
}

export default Creation;
