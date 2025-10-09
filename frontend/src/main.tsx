import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/core.css";

import { Container } from "react-bootstrap";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { BrowserRouter, Route, Routes } from "react-router";

import Callback from "./components/call.tsx";
import Reviving from "./components/code.tsx";
import Updating from "./components/edit.tsx";
import FactDocs from "./components/fact.tsx";
import FlagArea from "./components/flag.tsx";
import Mistaken from "./components/flaw.jsx";
import MainList from "./components/list.tsx";
import Creation from "./components/make.tsx";
import ModeWrap from "./components/mode.tsx";
import Navigation from "./components/navi.tsx";
import SideMenu from "./components/side.tsx";
import Revoking from "./components/wipe.tsx";
import { ServiceTypes } from "./config/data.ts";
import { data } from "./features/data.ts";

const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Root element with id 'root' not found");

createRoot(rootElement).render(
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
                {(Object.keys(ServiceTypes) as Array<keyof typeof ServiceTypes>)
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
