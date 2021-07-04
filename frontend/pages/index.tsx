import React, { Component } from "react";
import Header from './components/header';
import Table from './components/table';
import Home from './components/home';
import Chat from './components/chat';
import Login from './components/login';
import Signup from './components/signup';
import Error from './components/error';

type pageOpts = "home" | "table" | "chat" | "login" | "signup"
type stock = {id: number, ticker: string};
type algorithms = {id: number, name: string};
type decision = {
  id: number, 
  stock: stock, 
  algorithm:algorithms,
  openPrice: number,
  closingPrice: number,
  confidence: number,
  tradeDate: Date,
  created_at: Date
}
type login = {
  password: string,
  username: string,
}

type signup = {
  password: string,
  username: string,
  first_name: string,
  last_name: string,
  email: string
}

type HomeState = {
  page: pageOpts,
  stocks: stock[],
  decisions: decision[],
  error: string,
  baseUrl: string,
  loggedIn: boolean,
  username: string,
  userId: number
}

class App extends Component<{}, HomeState> {
  constructor(props: any) {
    super(props);
    this.state = {
        page: "login",
        stocks: null,
        decisions: null,
        error: "",
        baseUrl: 'http://127.0.0.1:1337',
        loggedIn: false,
        username: '',
        userId: null,
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
    this.handleSignup = this.handleSignup.bind(this);
    this.handleLogout = this.handleLogout.bind(this);
    this.getFetch = this.getFetch.bind(this);
  }

  getFetch(endpoint:string, state: "stocks" | "decisions") {
    fetch(this.state.baseUrl + endpoint,  {
      headers: {Authorization: `Token ${localStorage.getItem('token')}`}
    })
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { error: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then((data: stock | decision) => this.setState({...this.state, [state]: data})
      );
  }

  handleClick (arg:pageOpts) {this.setState({page:arg})}


  componentDidMount() {
    if (localStorage.getItem('token')) {
      fetch(this.state.baseUrl + '/user/current_user/', {
        headers: {Authorization: `Token ${localStorage.getItem('token')}`}
      })
        .then((response) => {
          if (response.ok) {
            return response.json()
          } else {
            this.handleLogout();
            throw new Error('Something went wrong');
          }
        })
        .then(json => {
          console.log("We just reran token")
          console.log(json)
          this.setState({username: json.username, userId:json.id})
          this.getFetch("/api/stocks/", "stocks");
          this.getFetch("/api/decisions/", "decisions")
          this.setState({loggedIn: true, page: "home"})
        })
        .catch(error => {
          console.log(error)
        })
    } else {
      this.setState({loggedIn: false})
    }

  }

  handleLogin = (e, data: login) => {
    e.preventDefault();
    fetch(this.state.baseUrl + '/api-token-auth/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
    .then((response) => {
      if (response.ok) {
        return response.json()
      } else {
        this.setState({error: "Invalid password or username"})
        throw new Error('Invalid signup attempt');
      }
    })
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          loggedIn: true,
          username: json.username,
          page: "home",
          userId: json.id
        }, () => {
          this.getFetch("/api/stocks/", "stocks");
          this.getFetch("/api/decisions/", "decisions")
        });
      });

  };

  handleSignup(e, data: signup) {
    e.preventDefault();
    fetch(this.state.baseUrl + '/user/users/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          loggedIn: true,
          username: json.username,
          page: "home"
        },() => {
          this.getFetch("/api/stocks/", "stocks");
          this.getFetch("/api/decisions/", "decisions")
        });
      });
  };

  handleLogout() {
    localStorage.removeItem('token');
    this.setState({...this.state, loggedIn: false, username: '', page: "login" });
  };

  render() {
    let viewPage;
    if (this.state.page =="home" && this.state.loggedIn) {
      viewPage = <Home stocks={this.state.stocks} baseUrl={this.state.baseUrl} getFetch={this.getFetch}/>;
    } else if (this.state.page == "table" && this.state.loggedIn) {
      viewPage = <Table decisions={this.state.decisions}/>;
    } else if (this.state.page == "chat" && this.state.loggedIn) {
      viewPage = <Chat baseUrl={this.state.baseUrl} userId={this.state.userId}/>
    } else if (this.state.page == "login" && !this.state.loggedIn) {
      viewPage = <Login handleLogin={this.handleLogin} handleClick={this.handleClick} baseUrl={this.state.baseUrl} error={this.state.error}/>
    } else if (this.state.page == "signup" && !this.state.loggedIn) {
      viewPage = <Signup handleSignup={this.handleSignup} handleClick={this.handleClick}/>
    } else {
      viewPage = <Error />
    }
    return (
      <div className="absolute inset-0 bg-gray-200 pt-16">
        <Header handleClick={this.handleClick} page={this.state.page} username={this.state.username} handleLogout={this.handleLogout}/>
        {viewPage}
      </div>
    )
  }
}

export default App;