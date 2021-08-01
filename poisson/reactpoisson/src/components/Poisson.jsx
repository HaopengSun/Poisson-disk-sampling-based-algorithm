import React, { useState } from "react";
import InputForm from './InputForm'

const Poisson = function(){
  const [showForm, setShowForm] = useState(false)

  const defaultParameter = {
    'title': '', 
    'description': '', 
    'unitsize': 0.05, 
    'width': 800,
    'height': 800,
    'sievesize': '',
    'minimumradius': 2,
    'finerpercent': '',
    'voidratio': 0.8,
    'cellsize': 5,
    'density': 0.001631
  }

  const [parameter, setParameter] = useState(defaultParameter)
  
  const createItem = function(){
    setShowForm(!showForm)
  }
  
  return(
    <div className='poisson'>
      <h2>Poisson Disk Sampling Algorithm</h2>
      <h5> Basic parameters that the algorithm requires to input have title, description, 
        unitsize, canvas size, sieve size, minimum radius, finer percent, void ratio, cell size, soil density.
      </h5>
      <h5>parameter obj: {JSON.stringify(parameter, null, 2)}</h5>
      <button className="btn btn-light" onClick={() => createItem()}>
        Set Parameters
      </button>
      {showForm && <InputForm setParameter={setParameter} defaultParameter={defaultParameter}/>}
    </div>
  )
}

export default Poisson


