import './App.css';
import TodoList from './components/TodoList'
import Poisson from './components/Poisson';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <Link to="/todo">TodoList</Link>
        <Link to="/">Poisson</Link>
      </div>

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
