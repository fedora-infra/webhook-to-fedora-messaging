import ReactMarkdown from "react-markdown";

import discourse from "./fact/discourse.md?raw";
import fogo from "./fact/fogo.md?raw";
import gthb from "./fact/gthb.md?raw";
import gtlb from "./fact/gtlb.md?raw";

const body = {
  fogo: fogo,
  gthb: gthb,
  gtlb: gtlb,
  discourse,
};

const head = {
  fogo: "Setting up webhook binds from Forgejo repositories",
  gthb: "Setting up webhook binds from GitHub repositories",
  gtlb: "Setting up webhook binds from GitLab repositories",
  discourse: "Setting up webhook binds from Discourse forums",
};

function FactDocs({ bind }) {
  return (
    <div className="mdcustom">
      <h2 className="headelem head">{head[bind]}</h2>
      <div className="small">
        <ReactMarkdown>{body[bind]}</ReactMarkdown>
      </div>
    </div>
  );
}

export default FactDocs;
