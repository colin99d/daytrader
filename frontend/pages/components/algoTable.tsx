import React, { Component } from "react";
import Modal from './algoModal';

type stock = {id: number, ticker: string};
type algorithm = {
    id: number,
    name: string,
    description: string,
    public: boolean,
    created_at: Date,
    user_selected: boolean
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
    algorithms: algorithm[],
    decisions: decision[],
    baseUrl: string,
    getFetch: (endpoint:string, state: "stocks" | "decisions" | "algorithms") => void
  }

type TableState = {
    activeAlgo: number
}

class Table extends Component<TableProps, TableState> {
    constructor(props: any) {
        super(props);
        this.state = {
            activeAlgo: null,
        };
        this.handleClick = this.handleClick.bind(this);
      }

    round(value: number, decimals: number) {
        return Number(Math.round(Number(value+'e'+decimals))+'e-'+decimals);
      }

    handleClick(id:number) {
        this.setState({activeAlgo:id})
    }

    render() {
        var is_selected:string = "px-5 py-5 border-b border-gray-200 bg-blue-500 text-sm text-white"
        var not_selected:string = "px-5 py-5 border-b border-gray-200 bg-white text-sm"
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
                                    <tr key={item.id} onClick={() => this.handleClick(item.id)}>
                                        <td className={item.user_selected ? is_selected : not_selected}>{item.name}</td>
                                        <td className={item.user_selected ? is_selected : not_selected}>{item.description}</td>
                                    </tr>
                                ) : null}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <Modal activeAlgo={this.state.activeAlgo} handleClick={this.handleClick} algorithm={this.state.activeAlgo ? this.props.algorithms.filter(item => item.id == this.state.activeAlgo)[0] : null}
            decisions={this.props.decisions ? this.props.decisions.filter(item => item.algorithm.id == this.state.activeAlgo) : null} baseUrl={this.props.baseUrl} getFetch={this.props.getFetch}/>
        </div>
  )
}
}

export default Table;