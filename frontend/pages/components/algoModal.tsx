import React, { Component } from "react";
import { Fragment } from 'react'
import { Dialog, Transition } from '@headlessui/react'

import Table from './table';

type stock = {id: number, ticker: string};
type algorithm = {
    id: number,
    name: string,
    description: string,
    public: boolean,
    created_at: Date,
  }
  type user_type = {
    username: string,
    id: number,
    selected_algo: algorithm,
    daily_emails: boolean
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

type ModalProps ={
    activeAlgo: number,
    algorithm: algorithm | null,
    handleClick: (id:number) => void,
    decisions: decision[],
    baseUrl: string,
    updateUser: (object: user_type) => void,
}

class Modal extends Component<ModalProps, {}> {
    private subscribe;
    constructor(props: any) {
      super(props);
      this.state = {};
      this.subscribe = React.createRef();
      this.handleClose = this.handleClose.bind(this);
    }

    updateUser() {
        fetch(this.props.baseUrl + "/user/update_algo?algo=" + this.props.activeAlgo.toString(),  {
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
            .then((json) => {
                this.props.updateUser(json);
            })
    }

    
    handleClose(value:boolean,subscribe:boolean=false){
        if(subscribe) {
            this.updateUser()
        }
        if (!value) {
            this.props.handleClick(null);
        }
    }

    render() {
        return (
            <Transition.Root show={this.props.activeAlgo != null} as={Fragment}>
            <Dialog as="div" static className="fixed z-10 inset-0 overflow-y-auto" open={this.props.activeAlgo != null} onClose={this.handleClose} initialFocus={this.subscribe}>
                <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <Transition.Child as={Fragment} enter="ease-out duration-300" enterFrom="opacity-0" enterTo="opacity-100" leave="ease-in duration-200" leaveFrom="opacity-100" leaveTo="opacity-0">
                    <Dialog.Overlay className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
                </Transition.Child>

                {/* This element is to trick the browser into centering the modal contents. */}
                <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">
                    &#8203;
                </span>
                <Transition.Child as={Fragment} enter="ease-out duration-300" enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enterTo="opacity-100 translate-y-0 sm:scale-100" 
                leave="ease-in duration-200" leaveFrom="opacity-100 translate-y-0 sm:scale-100" leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
                    <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                    <div className="bg-white pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div className="sm:flex sm:items-start">
                        <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                            <Dialog.Title as="h3" className="text-lg leading-6 font-medium text-gray-900">{this.props.algorithm ? this.props.algorithm.name : null}</Dialog.Title>
                            <div className="mt-2">
                                <p className="text-sm text-gray-500">{this.props.algorithm ? this.props.algorithm.description : null}</p>
                                <Table decisions={this.props.decisions}/>
                            </div>
                        </div>
                        </div>
                    </div>
                    <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                        <button type="button" onClick={() => this.handleClose(false,true)} ref={this.subscribe}
                        className="mt-3 w-full inline-flex bg-blue-500 justify-center rounded-md shadow-sm px-4 py-2 bg-white text-base font-medium text-white sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                        Subscribe
                        </button>
                    </div>
                    </div>
                </Transition.Child>
                </div>
            </Dialog>
            </Transition.Root>
        )
        }
}

export default Modal;