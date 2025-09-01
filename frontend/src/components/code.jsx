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
  hideReviving,
  keepFlagBody,
  keepFlagHead,
  keepServices,
  passFlagStat,
  showFlagArea,
} from "../features/part.jsx";

async function codeUnit(dispatch, uuid) {
  let data;
  try {
    data = await apiCall({ method: "PUT", path: `/services/${uuid}/regenerate` });
  } catch (error) {
    dispatch(hideReviving());
    dispatch(hideFlagArea());
    dispatch(keepFlagHead("Bind regeneration failed"));
    dispatch(keepFlagBody(`Encountered "${error.toString()}" response during regeneration`));
    dispatch(showFlagArea());
    dispatch(failFlagStat());
    return;
  } finally {
    dispatch(keepServices());
  }
  dispatch(hideReviving());
  dispatch(hideFlagArea());
  dispatch(keepFlagHead(`Bind #${data.uuid} regenerated`));
  dispatch(keepFlagBody("Relevant information can be found on the dashboard"));
  dispatch(showFlagArea());
  dispatch(passFlagStat());
}

function Reviving() {
  const show = useSelector((data) => data.area.reviving);
  const uuid = useSelector((data) => data.area.binduuid);
  const dispatch = useDispatch();

  return (
    <Offcanvas
      className="bg-body-tertiary shadow-sm"
      style={{ height: "fit-content" }}
      show={show}
      onHide={() => dispatch(hideReviving())}
      placement="bottom"
      scroll={true}
      backdrop={true}
    >
      <Container>
        <Offcanvas.Body>
          <Card className="shadow-sm" border="tertiary" id="card-wipe">
            <Card.Header className="d-flex justify-content-between align-items-center bg-body-secondary p-1">
              <span className="monoelem fw-bold pt-1 ps-1">Regenerate</span>
              <span className="pe-1">
                <ButtonGroup size="sm">
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>ACCEPT</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-success"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => codeUnit(dispatch, uuid)}
                    >
                      <Icon path={mdiCheckCircle} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>DECLINE</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-danger"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => dispatch(hideReviving())}
                    >
                      <Icon path={mdiCloseCircle} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                </ButtonGroup>
              </span>
            </Card.Header>
            <Card.Body className="p-2">
              <p className="mb-2">
                Are you certain that you wish to irreversibly regenerate the token for the bind #{uuid}?
              </p>
              <p className="mb-0">
                This action will disable all services using the existing token to access the endpoint.
              </p>
            </Card.Body>
          </Card>
        </Offcanvas.Body>
      </Container>
    </Offcanvas>
  );
}

export default Reviving;
