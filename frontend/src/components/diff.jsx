import ListGroup from "react-bootstrap/ListGroup";
import { typeName } from "../config/data.js";

function DiffCard({ stat, data }) {
  return (
    <ListGroup>
      <ListGroup.Item className="ps-2 fw-bold" variant={stat ? "success" : "danger"}>
        {stat ? "MODIFIED" : "EXISTING"}
      </ListGroup.Item>
      <ListGroup.Item className="ps-2 pe-2 d-flex justify-content-between align-items-start">
        <span className="fw-bold">Name. </span>
        <span className="text-truncate">{data.name}</span>
      </ListGroup.Item>
      <ListGroup.Item className="ps-2 pe-2 d-flex justify-content-between align-items-start">
        <span className="fw-bold">Description. </span>
        <span className="text-truncate">{data.desc}</span>
      </ListGroup.Item>
      <ListGroup.Item className="ps-2 pe-2 d-flex justify-content-between align-items-start">
        <span className="fw-bold">Type. </span>
        <span className="text-truncate">{typeName[data.type]}</span>
      </ListGroup.Item>
      <ListGroup.Item className="ps-2 pe-2 d-flex justify-content-between align-items-start">
        <span className="fw-bold">Owner. </span>
        <span className="text-truncate">{data.user}</span>
      </ListGroup.Item>
    </ListGroup>
  );
}

export default DiffCard;
