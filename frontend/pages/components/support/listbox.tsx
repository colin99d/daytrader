import { Fragment, useState } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { CheckIcon, SelectorIcon } from '@heroicons/react/solid'

type keys = "sign" | "type" | "strike" | "selected"

type option = {
    value: string | number,
    text: string,
    icon?: HTMLSpanElement
    volume?: number
}

type ListProps = {
    options: option[],
    selected: any,
    handleChange: any,
    id: number,
    target: keys,
    title?: string,
    width: string,
    
}

function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
  }

  export default function List(props: ListProps) {
  

    function handleChange(selection) {
      if (props.target == "selected") {
        props.handleChange(selection);
      } else {
        console.log(props.selected)
        props.handleChange(props.id, props.target, selection);
        console.log(props.selected)
      }
    }

    return (
      <Listbox value={props.options ? props.options.find(item => item.value == props.selected[props.target]): null}
        onChange={(selection) => handleChange(selection)}>
        {({ open }) => (
          <>
            <div className="mt-1 relative">
            {props.title ? <Listbox.Label className="text-base font-medium text-gray-700 ">{props.title}{" "}</Listbox.Label> : null}
              <Listbox.Button 
                className={classNames("relative bg-white border border-gray-300 rounded py-0.5 shadow-sm text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm", props.width)}>
                <span className="flex items-center">
                  <span className="ml-1 block truncate">{props.options ? props.options.find(item => item.value == props.selected[props.target]).text : null}</span>
                </span>
                <span className="absolute inset-y-0 right-0 flex items-center pointer-events-none">
                  <SelectorIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
              </Listbox.Button>
  
              <Transition show={open} as={Fragment} leave="transition ease-in duration-100" leaveFrom="opacity-100" leaveTo="opacity-0">
                <Listbox.Options static
                  className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
                >
                  {props.options ? props.options.map((option, optionIdx) => (
                    <Listbox.Option value={option} key={optionIdx}
                      className={({ active }) =>
                        classNames(
                          active ? 'text-white bg-indigo-600' : 'text-gray-900',
                          'cursor-default select-none relative py-2 pl-3 pr-9'
                        )
                      }
                    >
                      {({ selected, active }) => (
                        <>
                          <div className="flex items-center">
                            <span className={classNames(selected ? 'font-semibold' : 'font-normal', 'ml-3 block truncate')}>
                              {option.text}
                            </span>
                            {props.target == "strike" ? <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"
                              className={classNames(option.volume > 1000 ? "text-green-500" : option.volume > 100 ? "text-yellow-500" : "text-red-500","absolute inset-y-0 right-0")}> 
                              <circle cx="8" cy="8" r="8"/>
                            </svg> : null}
                          </div>
  
                          {selected ? (
                            <span className={classNames(active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-10 right-10 flex items-center pr-4')}>
                              <CheckIcon className="h-5 w-5" aria-hidden="true" />
                            </span>
                          ) : null}
                        </>
                      )}
                    </Listbox.Option>
                  )): null}
                </Listbox.Options>
              </Transition>
            </div>
          </>
        )}
      </Listbox>
    )
  }