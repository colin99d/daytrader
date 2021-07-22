import React, { Component } from "react";

import CashFlowGraph from './cashflowGraph';
import HedgingGraph from './hedgingGraph';

type data = {
    cashflows: {id: string, data:{x:string,y:number}[]}[]
    info: {
        time: Date,
        price: number,
        volume: number
    }
}

type HomeProps = {
    stocks: {id: number, ticker: string}[],
    baseUrl: string,
    getFetch: (endpoint:string, state: "stocks" | "decisions") => void
  }

type HomeState = {
    ticker: string,
    error: string,
    data: data,
    tickerDisplay: string,
    view: "hedging" | "cashflow",
    portfolio: {id: number, type: string, sign: number,}[]
}

class Home extends Component<HomeProps, HomeState> {
    constructor(props: any) {
        super(props);
        this.state = {
            ticker: "",
            error: "",
            data: null,
            tickerDisplay: "",
            view: "hedging",
            portfolio: [{id: 1, type: "stock", sign: 1}]
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleErrors = this.handleErrors.bind(this);
        this.handlePortfolio = this.handlePortfolio.bind(this);
        this.changeView = this.changeView.bind(this);
      }
    handleChange(e:any, formKey:"ticker") {this.setState({[formKey]: e.target.value})}

    handlePortfolio(id: number, sign) {
        var oldItem = this.state.portfolio.find(item => item.id == id);
        oldItem.sign = sign;
        var newPort = this.state.portfolio.filter(item => item.id != id);
        newPort.push(oldItem);
        this.setState({portfolio: newPort});
    }

    changeView(view: "hedging" | "cashflow") {this.setState({view: view})}

    handleErrors(response: any): any {
        if (!response.ok) {
            this.setState({error:response.statusText});
        }
        return response;
    }

    postGeneric(endpoint:string, data: { [name: string]: string } | FormData): Promise<any>  {
        return fetch(this.props.baseUrl + endpoint, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
          .then(this.handleErrors)
          .then(response => response.json())
    }

    handleClick(): void {
        let url = this.props.baseUrl + "/cashflows/";
        let data  = new FormData();
        data.append('ticker', this.state.ticker)
        fetch(url, {method: 'post',body: data,})
        .then(response => response.json())
        .then(data => {this.setState({data: data, tickerDisplay: this.state.ticker, ticker:""})})
    }

    render() {
        let graph = this.state.view == "hedging"  ? <HedgingGraph data={this.state.data ? this.state.data.info : null} portfolio={this.state.portfolio}/> : 
            <CashFlowGraph data={this.state.data ? this.state.data.cashflows : null} />
        let activeButton: string = "bg-purple-600 hover:bg-purple-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-2/4";
        let inactiveButton: string = "bg-purple-300 hover:bg-purple-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-2/4";
      return (
        <div className="ml-3 w-screen flex  h-full">
            <div className="h-3/4">
                <p className="text-red-500">{this.state.error}</p>
                <div className="flex flex-row">
                <input onChange={(e) => {this.handleChange(e, 'ticker')}} value={this.state.ticker} type="text" name="ticker" maxLength={5} placeholder="Ticker"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mt-4" />
                <button onClick={() => {this.handleClick()}} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4">Submit</button>
                </div>
                <div className="bg-white shadow-md rounded mt-5 h-full">
                    <div className="flex flex-row">
                    <button onClick={() => {this.changeView("hedging")}} className={this.state.view == "hedging" ? activeButton : inactiveButton}>Hedging</button>
                    <button onClick={() => {this.changeView("cashflow")}} className={this.state.view == "cashflow" ? activeButton : inactiveButton}>Cashflows</button>
                    </div>
                    <div style={{display: this.state.view == "hedging" ? "" : "none"}}>
                        <li className="border list-none rounded-sm px-3 py-3">
                            Base: {' '}
                            <select className="border" value={this.state.portfolio.find(item => item.id ==1).sign} onChange={(e) => {this.handlePortfolio(1, e.target.value)}}>
                                <option value="1">Long</option>
                                <option value="-1">Short</option>
                                <option value="0">---</option>
                            </select>
                        </li>
                    </div>
                </div>
            </div>
            <div className="ml-5 h-3/4 w-full h-full">
            <h1 className="text-2xl font-bold leading-7 text-gray-900 text-center">{this.state.tickerDisplay.toUpperCase()}</h1>
            {graph}
    </div>
        </div>
  )
}
}

export default Home;