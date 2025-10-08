import { ListGroup } from "react-bootstrap";

import { ServiceTypes } from "../config/data.ts";

interface DiffData {
  name: string;
  desc: string;
  type: keyof typeof ServiceTypes;
  user: string;
}

interface DiffCardProps {
  stat: boolean;
  data: DiffData;
}

function DiffCard({ stat, data }: DiffCardProps) {
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
        <span className="text-truncate">{ServiceTypes[data.type].name}</span>
      </ListGroup.Item>
      <ListGroup.Item className="ps-2 pe-2 d-flex justify-content-between align-items-start">
        <span className="fw-bold">Owner. </span>
        <span className="text-truncate">{data.user}</span>
      </ListGroup.Item>
    </ListGroup>
  );
}

export default DiffCard;
