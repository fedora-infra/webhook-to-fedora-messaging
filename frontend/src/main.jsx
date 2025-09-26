import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/core.css";

import Container from "react-bootstrap/Container";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { BrowserRouter, Route, Routes } from "react-router";

import Callback from "./components/call.jsx";
import Reviving from "./components/code.jsx";
import Updating from "./components/edit.jsx";
import FactDocs from "./components/fact.jsx";
import FlagArea from "./components/flag.jsx";
import Mistaken from "./components/flaw.jsx";
import MainList from "./components/list.jsx";
import Creation from "./components/make.jsx";
import ModeWrap from "./components/mode.jsx";
import Navigation from "./components/navi.jsx";
import SideMenu from "./components/side.jsx";
import Revoking from "./components/wipe.jsx";
import { ServiceTypes } from "./config/data.js";
import { data } from "./features/data.jsx";

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
                {Object.keys(ServiceTypes)
                  .sort()
                  .map((serviceType) => (
                    <Route key={serviceType} element={<FactDocs bind={serviceType} />} path={`/${serviceType}`} />
                  ))}
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
