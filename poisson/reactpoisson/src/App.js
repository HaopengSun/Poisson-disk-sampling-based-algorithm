import './App.css';
import Poisson from './components/Poisson';
import About from './components/About'
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Navbar, Container, Nav } from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap'

function App() {
  return (
    <Router>

      <Navbar bg="light" expand="lg">
        <Container>
          <Navbar.Brand href="/">Poisson-base Algorithm</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <LinkContainer to="/">
                <Nav.Link>Poisson List</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/about">
                <Nav.Link>About</Nav.Link>
              </LinkContainer>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Switch>
          <Route exact path="/">
            <Poisson />
          </Route>
          <Route path="/about">
            <About />
          </Route>
        </Switch>
    </Router>
  );
}

export default App;
