import React, { Component } from "react";

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

type TableProps = {
    decisions: decision[]
  }

type TableState = {
}

class Table extends Component<TableProps, {}> {
    constructor(props: any) {
        super(props);
        this.state = {
        };
      }

    round(value: number, decimals: number) {
        return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
      }

    render() {
      return (
        <div className="container mx-auto px-4 sm:px-8">
            <div className="py-8">
                <div>
                    <h2 className="text-2xl font-semibold leading-tight">Past Picks</h2>
                </div>
                <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4">
                    <div className="inline-block shadow rounded-lg min-w-full">
                        <table className="min-w-full">
                            <thead>
                                <tr>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Date</th>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Ticker</th>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Open</th>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Close</th>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Gain</th>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Confidence</th>
                                </tr>
                            </thead>
                            <tbody>
                                
                                {this.props.decisions.map((item:decision )=> 
                                    <tr key={item.id}>
                                        <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">{new Date(item.tradeDate).toLocaleDateString("en-US")}</td>
                                        <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">{item.stock.ticker}</td>
                                        <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">${this.round(item.openPrice,3)}</td>
                                        <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">${this.round(item.closingPrice,3)}</td>
                                        <td className={"px-5 py-5 border-b border-gray-200 bg-white text-sm " + (item.closingPrice > item.openPrice ? "text-green-500" : "text-red-500")}>{this.round(((item.closingPrice - item.openPrice)/item.openPrice)*100,2)}%</td>
                                        <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">{item.confidence}%</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
  )
}
}

export default Table;