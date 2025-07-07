import Offcanvas from "react-bootstrap/Offcanvas";
import {
  hideCreation,
  hideFlagArea,
  keepFlagBody,
  keepFlagHead,
  passFlagStat,
  failFlagStat,
  showFlagArea,
  keepServices,
} from "../features/part.jsx";
import { useDispatch, useSelector } from "react-redux";
import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card";
import { Button, ButtonGroup, FloatingLabel, Form, OverlayTrigger, Tooltip } from "react-bootstrap";
import Icon from "@mdi/react";
import { mdiContentSave, mdiDelete } from "@mdi/js";
import { userManager } from "../config/oidc.js";

async function saveUnit(dispatch) {
  try {
    const userdata = await userManager.getUser();
    if (userdata && !userdata.expired) {
      const resp = await fetch("/api/v1/services", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${userdata?.access_token}`,
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data: {
            name: document.getElementById("name-make").value.trim(),
            desc: document.getElementById("desc-make").value.trim(),
            type: document.getElementById("type-make").value.trim(),
          },
        }),
      });

      dispatch(keepServices());
      if (resp.ok) {
        const data = await resp.json();
        console.log("Result.", data);
        dispatch(hideCreation());
        dispatch(hideFlagArea());
        dispatch(keepFlagHead(`Bind #${data.data.uuid} created`));
        dispatch(keepFlagBody("Relevant information can be found on the dashboard"));
        dispatch(showFlagArea());
        dispatch(passFlagStat());
      } else {
        dispatch(hideCreation());
        dispatch(hideFlagArea());
        dispatch(keepFlagHead("Bind creation failed"));
        dispatch(keepFlagBody(`Encountered "Status ${resp.status}" response during creation`));
        dispatch(showFlagArea());
        dispatch(failFlagStat());
      }
    }
  } catch (expt) {
    console.log(expt);
  }
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
                      <option value="github">GitHub</option>
                      <option value="gitlab">GitLab</option>
                      <option value="forgejo">Forgejo</option>
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
