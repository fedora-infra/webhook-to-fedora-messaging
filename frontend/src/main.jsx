import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import Callback from "./components/call.jsx";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/core.css";
import { Provider } from "react-redux";
import { data } from "./features/data.jsx";
import Navigation from "./components/navi.jsx";
import SideMenu from "./components/side.jsx";
import Container from "react-bootstrap/Container";
import MainList from "./components/list.jsx";
import Creation from "./components/make.jsx";
import FlagArea from "./components/flag.jsx";
import Revoking from "./components/wipe.jsx";
import Updating from "./components/edit.jsx";
import ModeWrap from "./components/mode.jsx";
import Mistaken from "./components/flaw.jsx";
import Reviving from "./components/code.jsx";
import FactDocs from "./components/fact.jsx";

createRoot(document.getElementById("root")).render(
  <Provider store={data}>
    <ModeWrap>
      <BrowserRouter basename={import.meta.env.BASE_URL}>
        <Navigation />
        <Container>
          <div className="row g-3">
            <div className="col-12 col-lg-2 pt-3">
              <div className="sticky-md-top side">
                <SideMenu />
              </div>
            </div>
            <div className="col-12 col-lg-10 pt-3">
              <Routes>
                <Route element={<MainList />} path="/" />
                <Route element={<Callback />} path="/callback" />
                <Route element={<FactDocs bind="fogo" />} path="/forgejo" />
                <Route element={<FactDocs bind="gthb" />} path="/github" />
                <Route element={<FactDocs bind="gtlb" />} path="/gitlab" />
                <Route element={<Mistaken />} path="*" />
              </Routes>
            </div>
          </div>
          <FlagArea />
        </Container>
        <Creation />
        <Revoking />
        <Updating />
        <Reviving />
      </BrowserRouter>
    </ModeWrap>
  </Provider>
);
