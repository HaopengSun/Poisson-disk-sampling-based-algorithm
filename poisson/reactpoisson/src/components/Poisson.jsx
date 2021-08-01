import React, { useState } from "react";
import InputForm from './InputForm'

const Poisson = function(){
  const [showForm, setShowForm] = useState(false)

  const createItem = function(){
    setShowForm(!showForm)
  }
  return(
    <div>
      <h2>Poisson Disk Sampling Algorithm</h2>
      <button className="btn btn-primary" onClick={() => createItem()}>
        Add task
      </button>
      {showForm && <InputForm />}
    </div>
  )
}

export default Poisson