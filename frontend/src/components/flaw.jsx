import { useState } from "react";

import { flawText } from "../config/data.js";

function Mistaken() {
  const [text] = useState(() => {
    const time = Math.floor(Date.now() / 1000);
    return flawText[time % flawText.length];
  });

  return (
    <>
      <h2 className="headelem head">Resource unavailable</h2>
      <p className="small">{text}</p>
    </>
  );
}

export default Mistaken;
