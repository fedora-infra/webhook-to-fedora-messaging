import { useEffect, useState } from "react";
import React from "react";
import ReactMarkdown from "react-markdown";

import { ServiceTypes } from "../config/data.ts";

interface FactDocsProps {
  bind: keyof typeof ServiceTypes;
}

function FactDocs({ bind }: FactDocsProps) {
  const [mdDoc, setMdDoc] = useState("");
  useEffect(() => {
    import(`./fact/${bind}.md?raw`).then((loadedDoc) => setMdDoc(loadedDoc.default));
  }, [bind]);

  return (
    <div className="mdcustom">
      <h2 className="headelem head">Setting up webhook binds from {ServiceTypes[bind].title}</h2>
      <div className="small">
        <ReactMarkdown>{mdDoc}</ReactMarkdown>
      </div>
    </div>
  );
}

export default FactDocs;
