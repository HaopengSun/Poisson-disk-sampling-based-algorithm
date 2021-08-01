import './App.css';
import TodoList from './components/TodoList'
import Poisson from './components/Poisson';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
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
                <Nav.Link>Poisson</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/todo">
                <Nav.Link>TodoList</Nav.Link>
              </LinkContainer>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Switch>
          <Route path="/todo">
            <TodoList />
          </Route>
          <Route path="/">
            <Poisson />
          </Route>
        </Switch>
    </Router>
  );
}

export default App;
