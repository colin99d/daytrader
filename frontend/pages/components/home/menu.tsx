import React, { Component } from "react";
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/solid'

import Listbox from '../support/listbox';

type dropdowns = "selectStock" | "selectView" | "selectHedge"

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

type MenuProps = {
    handlePortfolio: (id: number, key: "sign" | "type" | "strike", value: any,) => void
    changeView: (view: "hedging" | "cashflow") => void,
    handleChange: (e: any, formKey:"ticker") => void,
    unixToDate: (unix: number | "") => string,
    handleRemove: (id: number) => void,
    handleOptions: (e: any) => void,
    handleClick: () => void,
    handleAdd: () => void,
    view: "hedging" | "cashflow",
    portfolio: portItem[],
    data: data,
    error: string,
    ticker: string,
}

type MenuState = {
    show: {
        selectStock: boolean,
        selectView: boolean,
        selectHedge: boolean,
    }
}

class Menu extends Component<MenuProps, MenuState> {
    constructor(props: any) {
        super(props);
        this.state = {
            show: {
                selectStock: true,
                selectView: false,
                selectHedge: false
            }
        }
      }

    handleClick(name: dropdowns) {
        var oldVal = this.state.show[name];
        var newDict = this.state.show;
        newDict[name] = !oldVal;
        this.setState({show: newDict});
    }
    
  render() {
    let expValue: number | "" = this.props.data ? this.props.data.options ? this.props.data.options.expiration : "" : ""
    let activeButton: string = "bg-purple-600 hover:bg-purple-800 text-white font-bold py-2 px-4 focus:outline-none focus:shadow-outline list-none";
    let inactiveButton: string = "bg-purple-300 hover:bg-purple-500 text-white font-bold py-2 px-4 focus:outline-none focus:shadow-outline list-none";
    let chevCls: string = "w-6 h-6 float-right align-middle";
    let expiration: number = this.props.data ? this.props.data.options ? this.props.data.options.expiration : null : null
    let expOptions: {value: number, text: string}[] = this.props.data ? 
        this.props.data.options.expirations.map(function(elem, idx) {
            return {
                key: idx,
                value: elem,
                text: this.props.unixToDate(elem),
            }
          }.bind(this)) : [{value: null, text:"---"}]
    return (
        <div className="h-5/6 w-3/6 md:w-2/6 lg:w-1/6 overflow-y-scroll">
            {/* Choose a stock to analyze */}
            <div className="bg-white shadow-md rounded mt-5 h-full">
            <li onClick={() => {this.handleClick("selectStock")}} className="border list-none rounded-sm px-3 py-3">Stock
                {this.state.show.selectStock ? <ChevronUpIcon className={chevCls}/> : <ChevronDownIcon className={chevCls}/>} 
            </li>
                <div style={{display: this.state.show.selectStock ? "" : "none"}}>
                <p className="text-red-500">{this.props.error}</p>
                <div className="flex flex-row mb-4">
                    <input onChange={(e) => {this.props.handleChange(e, 'ticker')}} value={this.props.ticker} type="text" name="ticker" maxLength={5} placeholder="Ticker"
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline rounded-r-none" />
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline rounded-l-none"
                        onClick={() => {this.props.handleClick()}}>Submit</button>
                    </div>
                </div>
            {/* Choose a view */}
            <li onClick={() => {this.handleClick("selectView")}} className="border list-none rounded-sm px-3 py-3">View
                {this.state.show.selectView ? <ChevronUpIcon className={chevCls}/> : <ChevronDownIcon className={chevCls}/>} 
            </li> 
            <div style={{display: this.state.show.selectView ? "" : "none"}}>
                <li onClick={() => {this.props.changeView("hedging")}} className={this.props.view == "hedging" ? activeButton : inactiveButton}>Hedging</li>
                <li onClick={() => {this.props.changeView("cashflow")}} className={this.props.view == "cashflow" ? activeButton : inactiveButton}>Cashflow</li>
            </div>

            {/* Look at Hedging view */}
            <li onClick={() => {this.handleClick("selectHedge")}} className="border list-none rounded-sm px-3 py-3">Hedging
                {this.state.show.selectHedge ? <ChevronUpIcon className={chevCls}/> : <ChevronDownIcon className={chevCls}/>} 
            </li> 
            <div style={{display: this.props.view == "hedging" && this.state.show.selectHedge ? "" : "none"}}>

                <li className="border list-none rounded-sm px-3 py-3">
                    <Listbox options={expOptions} selected={{selected: expiration}} width="w-24"
                    handleChange={this.props.handleOptions} id={1} target={"selected"} title="Expires:"/>
                </li>
                <li className="border list-none rounded-sm px-3 py-3">
                <Listbox options={[{value: 1, text: "Long"}, {value: -1, text: "Short"}, {value: 0, text: "---"}]} width="w-14"
                    selected={this.props.portfolio.find(item => item.id == 1)} handleChange={this.props.handlePortfolio} id={1} target="sign" title="Asset:"/>
                    <svg xmlns="http://www.w3.org/2000/svg"  className="bi bi-plus-circle-fill float-right text-green-500 cursor-pointer" 
                        viewBox="0 0 16 16" width="16" height="16" fill="currentColor" onClick={this.props.handleAdd}>
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
                    </svg>
                </li>
                {this.props.portfolio.filter(item => item.id != 1).map(item => 
                <li className="border list-none rounded-sm px-3 py-3">
                    <Listbox options={[{value: 1, text: "Long"}, {value: -1, text: "Short"}]} width="w-14" id={item.id} target="sign"
                        selected={item} handleChange={this.props.handlePortfolio} />

                    <Listbox options={[{value: "call", text: "Call"}, {value: "put", text: "put"}]} width="w-12" id={item.id} target="type"
                        selected={item} handleChange={this.props.handlePortfolio} />

                    <Listbox options={this.props.data.options[item.type+"s"].map(function(item) { return {value: item.strike, text:"$"+item.strike.toString(), volume: item.volume}})}
                        selected={item} handleChange={this.props.handlePortfolio} width="w-24" id={item.id} target="strike"/>
            
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-dash-circle-fill float-right text-red-500 cursor-pointer" viewBox="0 0 16 16">
                        <path onClick={() => this.props.handleRemove(item.id)} d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/>
                    </svg>
                </li> 
                    )}
            </div>
        </div>
    </div>
    );
  }
}



export default Menu;