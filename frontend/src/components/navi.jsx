import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import { userManager } from "../config/oidc.js";
import { useSelector, useDispatch } from "react-redux";
import { loadUserData, wipeUserData } from "../features/auth.jsx";
import Image from "react-bootstrap/Image";
import NavDropdown from "react-bootstrap/NavDropdown";
import Icon from "@mdi/react";
import { mdiWeatherSunny, mdiWeatherNight, mdiMemory, mdiPower } from "@mdi/js";
import { prepTintMode } from "../features/part.jsx";
import { useEffect } from "react";

function Navigation() {
  const dispatch = useDispatch();
  const user = useSelector((data) => data.auth.user);
  const disp = useSelector((data) => data.auth.disp);
  const mode = useSelector((data) => data.area.tintmode);
  const status = useSelector((data) => data.auth.status);

  useEffect(() => {
    if (status === "idle") {
      dispatch(loadUserData());
    }
  }, [dispatch, status]);

  const handleSignin = async () => {
    await userManager.signinRedirect();
  };

  const handleSignout = async () => {
    await userManager.removeUser();
    dispatch(wipeUserData());
  };

  return (
    <Navbar bg="body-secondary" className="shadow-sm fixed-top p-0">
      <Container>
        <Navbar.Brand className="d-flex align-items-center flex-grow-1">
          <img
            alt=""
            src={`${import.meta.env.BASE_URL}fedora.svg`}
            width="30"
            height="30"
            className="d-inline-block align-top p-0 logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text className="p-0">
            <NavDropdown
              title={
                <Icon
                  path={mode === "lite" ? mdiWeatherSunny : mode === "dark" ? mdiWeatherNight : mdiMemory}
                  size={1}
                />
              }
              drop="down"
              align="end"
              className="p-0 pe-2"
            >
              <NavDropdown.Item
                onClick={() => dispatch(prepTintMode("auto"))}
                className="small d-flex align-items-center p-1"
              >
                <Icon className="me-1" size={0.75} path={mdiMemory} />
                System
              </NavDropdown.Item>
              <NavDropdown.Item
                onClick={() => {
                  dispatch(prepTintMode("lite"));
                  document.body.setAttribute("data-bs-theme", "light");
                }}
                className="small d-flex align-items-center p-1"
              >
                <Icon className="me-1" size={0.75} path={mdiWeatherSunny} />
                Light
              </NavDropdown.Item>
              <NavDropdown.Item
                onClick={() => {
                  dispatch(prepTintMode("dark"));
                  document.body.setAttribute("data-bs-theme", "dark");
                }}
                className="small d-flex align-items-center p-1"
              >
                <Icon className="me-1" size={0.75} path={mdiWeatherNight} />
                Dark
              </NavDropdown.Item>
            </NavDropdown>
          </Navbar.Text>
          <Navbar.Text className="p-0">
            <NavDropdown title={<Image src={disp} rounded />} drop="down" align="end" className="p-0">
              {user ? (
                <NavDropdown.Item onClick={handleSignout} className="small d-flex align-items-center p-1">
                  <Icon className="me-1" size={0.75} path={mdiPower} />
                  Sign out
                </NavDropdown.Item>
              ) : (
                <NavDropdown.Item onClick={handleSignin} className="small d-flex align-items-center p-1">
                  <Icon className="me-1" size={0.75} path={mdiPower} />
                  Sign in
                </NavDropdown.Item>
              )}
            </NavDropdown>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigation;
