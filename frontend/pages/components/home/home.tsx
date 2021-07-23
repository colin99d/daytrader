import React, { Component } from "react";

import CashFlowGraph from './cashflowGraph';
import HedgingGraph from './hedgingGraph';

type portItem = {
    id: number,
    type: "stock" | "call" | "put",
    sign: -1 | 0 | 1,
    strike: number,
    cost: number
}

type option = {
    contractSymbol: string,
    strike: number,
    currency: string,
    lastPrice: number,
    change: number,
    percentChange: number,
    volume: number,
    openInterest: number,
    bid: number,
    ask: number,
    contractSize: string,
    expiration: number,
    lastTradeDate: number,
    impliedVolatility: number,
    inTheMoney: boolean,
}

type data = {
    cashflows: {id: string, data:{x:string,y:number}[]}[]
    info: {
        time: Date,
        price: number,
        volume: number
    }
    options: {
        expirations: number[],
        expiration: number,
        calls: option[],
        puts: option[]
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
    portfolio: portItem[],
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
            portfolio: [{id: 1, type: "stock", sign: 1, strike: null, cost: 0}],
        };
        this.handleAdd = this.handleAdd.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleErrors = this.handleErrors.bind(this);
        this.handlePortfolio = this.handlePortfolio.bind(this);
        this.changeView = this.changeView.bind(this);
      }
    handleChange(e: any, formKey:"ticker") {this.setState({...this.state, [formKey]: e.target.value})}

    handlePortfolio(id: number, key: "sign" | "type" | "strike", value: any) {
        var oldItem: portItem = this.state.portfolio.find(item => item.id == id);
        //Refactor below
        if (key=="sign"){oldItem["sign"]=value}
        else if (key=="type"){oldItem["type"]=value}
        else if (key=="strike"){oldItem["strike"]=value}
        //Refactor above
        if (id > 1 && oldItem.sign != 0 ) {
            var newCost: number = this.state.data.options[oldItem.type + "s"].find(item => item.strike == oldItem.strike).lastPrice
            newCost *= oldItem.sign
            oldItem.cost = newCost;
        }
        var newPort = this.state.portfolio.filter(item => item.id != id);
        newPort.push(oldItem);
        this.setState({portfolio: newPort});
    }

    handleOptions(e: any) {
        console.log("Start")
        var expDate: number = e.target.value;
        let url = this.props.baseUrl + "/cashflows/";
        let data  = new FormData();
        data.append('ticker', this.state.tickerDisplay);
        data.append('expiration', expDate.toString());
        fetch(url, {method: 'post',body: data,})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var oldData = this.state.data;
            oldData.options = data.options;
            this.setState({data: oldData})
        })
    }

    changeView(view: "hedging" | "cashflow") {this.setState({view: view})}

    handleErrors(response: any): any {
        if (!response.ok) {
            this.setState({error:response.statusText});
        }
        return response;
    }

    handleAdd() {
        if (this.state.data) {
            var ids: number[] = this.state.portfolio.map(item => item.id);
            var newId: number = Math.max(...ids) + 1;
            var portfolios = this.state.portfolio
            portfolios.push({id: newId, type:"call", sign: 1, strike: this.state.data.options.calls[0].strike, 
                cost: this.state.data.options.calls[0].lastPrice})
            this.setState({portfolio: portfolios})
        } 
    }

    handleRemove(id: number) {
        var newPort: portItem[] = this.state.portfolio.filter(item => item.id != id);
        this.setState({portfolio: newPort});
    }

    unixToDate(unix: number | "") {
        if (unix == null || unix == "") {
            return null
        }
        var dateObject = new Date (unix*1000);
        return dateObject.toLocaleDateString();
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
        let expValue: number | "" = this.state.data ? this.state.data.options ? this.state.data.options.expiration : "" : ""
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
                            Expiration: {' '}
                            <select className="border" onChange={(e) => {this.handleOptions(e)}} value={expValue}>
                                {this.state.data ? this.state.data.options ? this.state.data.options.expirations.map(item =>
                                    <option value={item}>{this.unixToDate(item)}</option>
                                ) : null : null}
                
                            </select>
                        </li>
                        <li className="border list-none rounded-sm px-3 py-3">
                            Base: {' '}
                            <select className="border" value={this.state.portfolio.find(item => item.id ==1).sign} onChange={(e) => {this.handlePortfolio(1, "sign", e.target.value)}}>
                                <option value="1">Long</option>
                                <option value="-1">Short</option>
                                <option value="0">---</option>
                            </select>
                            
                            <svg xmlns="http://www.w3.org/2000/svg"  className="bi bi-plus-circle-fill float-right text-green-500 cursor-pointer" 
                                viewBox="0 0 16 16" width="16" height="16" fill="currentColor" onClick={this.handleAdd}>
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
                            </svg>
                        </li>
                        {this.state.portfolio.filter(item => item.id != 1).map(item => 
                            <li className="border list-none rounded-sm px-3 py-3">
                            <select className="border" value={item.sign} onChange={(e) => {this.handlePortfolio(item.id, "sign", e.target.value)}}>
                                <option value="1">Long</option>
                                <option value="-1">Short</option>
                                <option value="0">---</option>
                            </select>

                            <select className="border" value={item.type} onChange={(e) => {this.handlePortfolio(item.id, "type", e.target.value)}}>
                                <option value="call">Call</option>
                                <option value="put">Put</option>
                            </select>
                    
                            <select className="border" value={item.strike} onChange={(e) => {this.handlePortfolio(item.id, "strike", e.target.value)}}>
                                {item.type == "call" ? this.state.data.options.calls.map(item => <option value={item.strike}>${item.strike}</option>) :
                                this.state.data.options.puts.map(item => <option value={item.strike}>${item.strike}</option>)}
                            </select>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-dash-circle-fill float-right text-red-500 cursor-pointer" viewBox="0 0 16 16">
                                <path onClick={() => this.handleRemove(item.id)} d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/>
                            </svg>
                        </li> 
                        )}
                    </div>
                </div>
            </div>
            <div className="ml-5 w-full h-5/6">
            {this.state.tickerDisplay ?  <h1 className="text-2xl font-bold leading-7 text-gray-900 text-center">{this.state.tickerDisplay.toUpperCase() + " - " + this.unixToDate(expValue)}</h1> : null}
           
            {graph}
    </div>
        </div>
  )
}
}

export default Home;

//