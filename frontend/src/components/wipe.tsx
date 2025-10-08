import React from "react";
import { mdiCheckCircle, mdiCloseCircle } from "@mdi/js";
import Icon from "@mdi/react";
import { Button, ButtonGroup, OverlayTrigger, Tooltip, Card, Container, Offcanvas } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import { apiCall } from "../features/api.ts";
import {
  failFlagStat,
  hideFlagArea,
  hideRevoking,
  keepFlagBody,
  keepFlagHead,
  keepServices,
  passFlagStat,
  showFlagArea,
} from "../features/part.ts";

const IconComponent = Icon as unknown as React.ComponentType<{ path: string; size?: number | string; className?: string }>;

async function wipeUnit(dispatch: import("../features/data.ts").AppDispatch, uuid: string) {
  let data2;
  try {
    data2 = await apiCall({ method: "PUT", path: `/services/${uuid}/revoke` });
  } catch (error: unknown) {
    const errMsg = error instanceof Error ? error.message : String(error);
    dispatch(keepServices());
    dispatch(hideRevoking());
    dispatch(hideFlagArea());
    dispatch(keepFlagHead("Bind revocation failed"));
    dispatch(keepFlagBody(`Encountered "${errMsg}" response during revocation`));
    dispatch(showFlagArea());
    dispatch(failFlagStat());
    return;
  } finally {
    dispatch(keepServices());
  }
  dispatch(hideRevoking());
  dispatch(hideFlagArea());
  dispatch(keepFlagHead(`Bind #${data2.uuid} revoked`));
  dispatch(keepFlagBody("Relevant information can be found on the dashboard"));
  dispatch(showFlagArea());
  dispatch(passFlagStat());
}

function Revoking() {
  const show = useSelector((state: import("../features/data.ts").RootState) => state.area.revoking);
  const uuid = useSelector((state: import("../features/data.ts").RootState) => state.area.binduuid);
  const dispatch = useDispatch<import("../features/data.ts").AppDispatch>();

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
                      <IconComponent path={mdiCheckCircle} size={0.75} />
                    </Button>
                  </OverlayTrigger>
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>DECLINE</Tooltip>}>
                    <Button
                      size="sm"
                      variant="outline-danger"
                      className="d-flex justify-content-center align-items-center"
                      onClick={() => dispatch(hideRevoking())}
                    >
                      <IconComponent path={mdiCloseCircle} size={0.75} />
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
