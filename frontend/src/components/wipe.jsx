import { useDispatch, useSelector } from "react-redux";
import Offcanvas from "react-bootstrap/Offcanvas";
import {
  failFlagStat,
  hideFlagArea,
  hideRevoking,
  keepFlagBody,
  keepFlagHead,
  keepServices,
  passFlagStat,
  showFlagArea,
} from "../features/part.jsx";
import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card";
import { Button, ButtonGroup, OverlayTrigger, Tooltip } from "react-bootstrap";
import Icon from "@mdi/react";
import { mdiCheckCircle, mdiCloseCircle } from "@mdi/js";
import { userManager } from "../config/oidc.js";

async function wipeUnit(dispatch, uuid) {
  try {
    const userdata = await userManager.getUser();
    if (userdata && !userdata.expired) {
      const resp = await fetch(`/api/v1/services/${uuid}/revoke`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${userdata?.access_token}`,
          Accept: "application/json",
        },
      });

      dispatch(keepServices());
      if (resp.ok) {
        const data = await resp.json();
        console.log("Result.", data);
        dispatch(hideRevoking());
        dispatch(hideFlagArea());
        dispatch(keepFlagHead(`Bind #${data.data.uuid} revoked`));
        dispatch(keepFlagBody("Relevant information can be found on the dashboard"));
        dispatch(showFlagArea());
        dispatch(passFlagStat());
      } else {
        dispatch(hideRevoking());
        dispatch(hideFlagArea());
        dispatch(keepFlagHead("Bind revocation failed"));
        dispatch(keepFlagBody(`Encountered "Status ${resp.status}" response during revocation`));
        dispatch(showFlagArea());
        dispatch(failFlagStat());
      }
    }
  } catch (expt) {
    console.log(expt);
  }
}

function Revoking() {
  const show = useSelector((data) => data.area.revoking);
  const uuid = useSelector((data) => data.area.binduuid);
  const dispatch = useDispatch();

  return (
    <Offcanvas
      className="bg-body-tertiary shadow-sm"
      style={{ height: "fit-content" }}
      show={show}
      onHide={() => dispatch(hideRevoking())}
      placement="bottom"
      scroll={true}
      backdrop={true}
    >
      <Container>
        <Offcanvas.Body>
          <Card className="shadow-sm" border="tertiary" id="card-wipe">
            <Card.Header className="d-flex justify-content-between align-items-center bg-body-secondary p-1">
              <span className="monoelem fw-bold pt-1 ps-1">Revoke</span>
              <span className="pe-1">
                <ButtonGroup size="sm">
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>ACCEPT</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-success"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => wipeUnit(dispatch, uuid)}
                    >
                      <Icon path={mdiCheckCircle} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>DECLINE</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-danger"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => dispatch(hideRevoking())}
                    >
                      <Icon path={mdiCloseCircle} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                </ButtonGroup>
              </span>
            </Card.Header>
            <Card.Body className="p-2">
              Are you certain that you wish to irreversibly revoke the bind #{uuid}?
            </Card.Body>
          </Card>
        </Offcanvas.Body>
      </Container>
    </Offcanvas>
  );
}

export default Revoking;
