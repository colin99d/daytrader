import React, { Component } from "react";
import { ResponsiveLine } from '@nivo/line';

const theme={
    axis: {
      ticks: {
        text: {
          fontSize: 16,
        }
      }
    }
  }

  type portItem = {
    id: number,
    type: string,
    sign: number,
    strike: number
}

type HomeProps = {
    data: {
        time: Date,
        price: number,
        volume: number
    }
    portfolio: portItem[]
  }

class HedgingGraph extends Component<HomeProps, {} >{
    constructor(props: any) {
        super(props);
      }

    dataFunction(base: number, price: number) {
      var main = this.props.portfolio.find(item => item.id == 1);
      var optionsChange: number = 0;
      var change: number = price - base;
      this.props.portfolio.filter(item => item.id != 1).forEach(item => {
        if (item.type == "call") {
          let absChange: number = price > item.strike ? price - item.strike : 0;
          optionsChange += item.sign * absChange;
        } else if (item.type == "put") {
          let absChange: number = price < item.strike ? item.strike - price : 0;
          optionsChange += item.sign * absChange;
        }
      })
      return  (change * main.sign) + optionsChange;
    }

    getXValues() {
      var xList: number[] = Array.from(Array(101).keys())
      var min: number = this.props.data.price;
      var max: number = this.props.data.price;
      if (this.props.portfolio.length == 1) {
        min *= 0.5;
        max *= 1.5;
      } else if (this.props.portfolio.length > 1) {
        this.props.portfolio.forEach(item => {
          if (item.strike > max) {
            max = item.strike;
          }
          if (item.strike < min) {
            min = item.strike;
          }
          min *= 0.8;
          max *= 1.2;
        })
      }
      var range: number = max - min;
      console.log(range)
      console.log(xList)
      return xList.map(item => min + ((item/100)*range));
    }

    generateData() {
        var xVals: number[] = this.getXValues();
        var base: number = this.props.data.price;
        var beforeFees = [];
        xVals.forEach(item => {
          beforeFees.push({"x" : item, "y": this.dataFunction(base, item)});
        })
        return [{id: "Before Fees", data: beforeFees},]
    }

    render() {
        let values = this.props.data ? this.generateData() : null
      return (
        <div className= "w-full h-full">
            {this.props.data ?<div className="w-full h-full bg-white">
            <ResponsiveLine 
                theme={theme}
                data={values}
                margin={{ top: 50, right: 50, bottom: 100, left: 80 }}
                xScale={{ type: 'linear', stacked: false, min:"auto", max:"auto"}}
                yScale={{ type: 'linear', stacked: false, min:"auto", max:"auto"}}
                xFormat=">-$.3f"
                yFormat=">-$.3f"
                curve="linear"
                axisTop={null}
                axisBottom={{
                    //tickValues: this.getTickerDates()
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    format: ">-$.2f",
                    legendOffset: 36,
                    legendPosition: "middle"
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    format: ">-$.2f",
                    legendOffset: -45,
                    legendPosition: 'middle'
                }}
                enableGridX={false}
                //colors={{ scheme: 'spectral' }}
                lineWidth={3}
                enablePoints={false}
                pointSize={6}
                pointColor={{ theme: 'background' }}
                pointBorderWidth={1}
                pointBorderColor={{ from: 'serieColor' }}
                pointLabelYOffset={-12}
                useMesh={true}
                legends={[
                    {
                        anchor: 'bottom-left',
                        direction: 'column',
                        justify: false,
                        translateX: 0,
                        translateY: 90,
                        itemsSpacing: 2,
                        itemDirection: 'left-to-right',
                        itemWidth: 80,
                        itemHeight: 12,
                        itemOpacity: 0.75,
                        symbolSize: 12,
                        symbolShape: 'circle',
                        symbolBorderColor: 'rgba(0, 0, 0, .5)',
                        effects: [
                            {
                                on: 'hover',
                                style: {
                                    itemBackground: 'rgba(0, 0, 0, .03)',
                                    itemOpacity: 1
                                }
                            }
                        ]
                    }
                ]}
            /></div> : null}
    </div>
  )
}
}

export default HedgingGraph;