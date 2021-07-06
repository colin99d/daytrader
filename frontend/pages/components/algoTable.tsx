import React, { Component } from "react";

type stock = {id: number, ticker: string};
type algorithm = {
    id: number,
    name: string,
    description: string,
    public: boolean,
    created_at: Date,
  }
type decision = {
  id: number, 
  stock: stock, 
  algorithm:algorithm,
  openPrice: number,
  closingPrice: number,
  confidence: number,
  tradeDate: Date,
  created_at: Date
}

type TableProps = {
    algorithms: algorithm[]
  }

class Table extends Component<TableProps, {}> {
    constructor(props: any) {
        super(props);
        this.state = {
        };
      }

    round(value: number, decimals: number) {
        return Number(Math.round(Number(value+'e'+decimals))+'e-'+decimals);
      }

    render() {
      return (
        <div className="container mx-auto px-4 sm:px-8">
            <div className="py-8">
                <div>
                    <h2 className="text-2xl font-semibold leading-tight">Algorithms</h2>
                </div>
                <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4">
                    <div className="inline-block shadow rounded-lg min-w-full">
                        <table className="min-w-full">
                            <thead>
                                <tr>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Name</th>
                                    <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-xs font-semibold text-gray-600 uppercase text-left">Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                
                                {this.props.algorithms ? this.props.algorithms.map((item:algorithm )=> 
                                    <tr key={item.id}>
                                        <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">{item.name}</td>
                                        <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">{item.description}</td>
                                    </tr>
                                ) : null}
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