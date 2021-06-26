import React, { Component } from "react";
import Header from './components/header';
import Table from './components/table';
import Home from './components/home';
import Chat from './components/chat';
import Login from './components/login';
import Signup from './components/signup';
import Error from './components/error';

type page = "home" | "table" | "chat" | "login" | "signup"
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

type HomeState = {
  page: page,
  stocks: stock[],
  decisions: decision[],
  error: string,
  baseUrl: string,
  loggedIn: boolean,
  username: string,
}

class App extends Component<{}, HomeState> {
  constructor(props: any) {
    super(props);
    this.state = {
        page: "login",
        stocks: null,
        decisions: null,
        error: "",
        baseUrl: "http://192.168.1.72:8000",
        loggedIn: localStorage.getItem('token') ? true : false,
        username: '',
    };
    this.handleClick = this.handleClick.bind(this);
    this.getFetch = this.getFetch.bind(this);
  }

  getFetch(endpoint:string, state: "stocks" | "decisions") {
    fetch(this.state.baseUrl + endpoint)
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

  handleClick (arg:page) {this.setState({page:arg})}


  componentDidMount() {
    this.getFetch("/api/stocks/", "stocks");
    this.getFetch("/api/decisions/", "decisions")
    if (this.state.loggedIn) {
      fetch('http://localhost:8000/core/current_user/', {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(json => {
          this.setState({ username: json.username });
        });
    }
  }

  handleLogin = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/token-auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          loggedIn: true,
          username: json.user.username
        });
      });
  };

  handleSignup(e, data) {
    e.preventDefault();
    fetch('http://localhost:8000/user/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          loggedIn: true,
          username: json.username
        });
      });
  };

  handleLogout() {
    localStorage.removeItem('token');
    this.setState({ loggedIn: false, username: '' });
  };

  render() {
    let page;
    if (this.state.page =="home" && this.state.loggedIn) {
      page = <Home stocks={this.state.stocks} baseUrl={this.state.baseUrl} getFetch={this.getFetch}/>;
    } else if (this.state.page == "table" && this.state.loggedIn) {
      page = <Table decisions={this.state.decisions}/>;
    } else if (this.state.page == "chat" && this.state.loggedIn) {
      page = <Chat />
    } else if (this.state.page == "login") {
      page = <Login handleLogin={this.handleLogin}/>
    } else if (this.state.page == "signup") {
      page = <Signup handleSignup={this.handleSignup}/>
    } else {
      page = <Error />
    }
    return (
      <div className="h-screen w-screen">
        <Header handleClick={this.handleClick} page={this.state.page} />
        <div className="bg-gray-200 h-full w-full">
          {page}
        </div>
      </div>
    )
  }
}

export default App;