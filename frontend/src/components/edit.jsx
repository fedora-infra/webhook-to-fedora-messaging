import { mdiCheckCircle, mdiCloseCircle } from "@mdi/js";
import Icon from "@mdi/react";
import { Button, ButtonGroup, OverlayTrigger, Tooltip } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Offcanvas from "react-bootstrap/Offcanvas";
import { useDispatch, useSelector } from "react-redux";

import { apiCall } from "../features/api.js";
import {
  failFlagStat,
  hideFlagArea,
  hideUpdating,
  keepFlagBody,
  keepFlagHead,
  keepServices,
  passFlagStat,
  showFlagArea,
} from "../features/part.jsx";
import DiffCard from "./diff.jsx";

async function editUnit(dispatch, uuid) {
  let data;
  try {
    data = await apiCall({
      method: "PUT",
      path: `/services/${uuid}`,
      body: {
        data: {
          name: document.getElementById(`name-${uuid}`).value,
          type: document.getElementById(`type-${uuid}`).value,
          desc: document.getElementById(`desc-${uuid}`).value,
          username: document.getElementById(`user-${uuid}`).value,
        },
      },
    });
  } catch (error) {
    dispatch(hideUpdating());
    dispatch(hideFlagArea());
    dispatch(keepFlagHead("Bind updating failed"));
    dispatch(keepFlagBody(`Encountered "${error.toString()}" response during updating`));
    dispatch(showFlagArea());
    dispatch(failFlagStat());
    return;
  } finally {
    dispatch(keepServices());
  }
  dispatch(hideUpdating());
  dispatch(hideFlagArea());
  dispatch(keepFlagHead(`Bind #${data.uuid} updated`));
  dispatch(keepFlagBody("Relevant information can be found on the dashboard"));
  dispatch(showFlagArea());
  dispatch(passFlagStat());
}

function Updating() {
  const show = useSelector((data) => data.area.updating);
  const uuid = useSelector((data) => data.area.binduuid);
  const prev = useSelector((data) => data.area.prevdata);
  const next = useSelector((data) => data.area.nextdata);

  const dispatch = useDispatch();

  return (
    <Offcanvas
      className="bg-body-tertiary shadow-sm"
      style={{ height: "fit-content" }}
      show={show}
      onHide={() => dispatch(hideUpdating())}
      placement="bottom"
      scroll={true}
      backdrop={true}
    >
      <Container>
        <Offcanvas.Body>
          <Card className="shadow-sm" border="tertiary" id="card-wipe">
            <Card.Header className="d-flex justify-content-between align-items-center bg-body-secondary p-1">
              <span className="monoelem fw-bold pt-1 ps-1">Update</span>
              <span className="pe-1">
                <ButtonGroup size="sm">
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>ACCEPT</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-success"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => editUnit(dispatch, uuid)}
                    >
                      <Icon path={mdiCheckCircle} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>DECLINE</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-danger"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => dispatch(hideUpdating())}
                    >
                      <Icon path={mdiCloseCircle} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                </ButtonGroup>
              </span>
            </Card.Header>
            <Card.Body className="p-2">
              Are you certain that you wish to irreversibly update the bind #{uuid}?
              <div className="row g-2 pt-2">
                <div className="col-12 col-lg-6">
                  <DiffCard stat={false} data={prev} />
                </div>
                <div className="col-12 col-lg-6">
                  <DiffCard stat={true} data={next} />
                </div>
              </div>
            </Card.Body>
          </Card>
        </Offcanvas.Body>
      </Container>
    </Offcanvas>
  );
}

export default Updating;
