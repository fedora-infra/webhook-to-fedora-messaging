import ReactMarkdown from "react-markdown";
import fogo from "../assets/docs/fogo.md?raw";
import gthb from "../assets/docs/gthb.md?raw";
import gtlb from "../assets/docs/gtlb.md?raw";

const body = {
  fogo: fogo,
  gthb: gthb,
  gtlb: gtlb,
};

const head = {
  fogo: "Setting up webhook binds from Forgejo repositories",
  gthb: "Setting up webhook binds from GitHub repositories",
  gtlb: "Setting up webhook binds from GitLab repositories",
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
