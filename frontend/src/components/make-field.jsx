import { FloatingLabel, Form } from "react-bootstrap";

import { ServiceTypes } from "../config/data.js";

function MakeField({ name, label, value, onChange, serviceType }) {
  return (
    <div className="col-md-4 col-12">
      <FloatingLabel className="small" controlId={`${name}-make`} label={label}>
        <Form.Control className="monoelem" name={name} onChange={onChange} value={value || ""} />
      </FloatingLabel>
      {ServiceTypes[serviceType] &&
        ServiceTypes[serviceType]["helpText"] &&
        ServiceTypes[serviceType]["helpText"][name] && (
          <Form.Text muted>
            <span dangerouslySetInnerHTML={{ __html: ServiceTypes[serviceType]["helpText"][name] }} />
          </Form.Text>
        )}
    </div>
  );
}

export default MakeField;
