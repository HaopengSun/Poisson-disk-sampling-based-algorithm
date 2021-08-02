import React, { useState, useEffect } from "react";
import axios from 'axios'
import poseParameter from '../helper/poseData'

const InputForm = function(props){
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [unitsize, setUnitsize] = useState(undefined)
  const [width, setWidth] = useState(undefined)
  const [height, setHeight] = useState(undefined)
  const [sievesize, setSievesize] = useState('')
  const [minimumradius, setMinimumradius] = useState(undefined)
  const [voidratio, setVoidratio] = useState(undefined)
  const [cellsize, setCellsize] = useState(undefined)
  const [density, setDensity] = useState(undefined)
  const [id, setId] = useState(0)
  const [finerpercent, setFinerpercent] = useState('')
  const defaultParameter = props.defaultParameter

  useEffect(() => {
    axios.get('/api/algorithms/')
    .then(function (response) {
      setId(response.data.length + 1);
    })
    .catch(function (error) {
      console.log(error);
    })
  }, [])

  const submitParameter = function(){
    const newParameter = {...defaultParameter, finerpercent, title, description, unitsize, width, height, sievesize, cellsize, density, voidratio, id}
    props.setParameter(newParameter)
    poseParameter(newParameter)
  }

  const onReset = function(){
    setTitle('')
    setDescription('')
    setUnitsize(0)
    setWidth(0)
    setHeight(0)
    setSievesize('')
    setMinimumradius(0)
    setVoidratio(0)
    setCellsize(0)
    setDensity(0)
    setFinerpercent('')
  }

  return(
    <>
    <form className='inputform' id="input" onSubmit={(event) => {
      event.preventDefault();
      submitParameter();
    }}>
      <div className='subinput'>
        <label>
            Title: <input className='formlabel' type="text" name="name"
            value={title} onChange={(event) => setTitle(event.target.value)}/>
        </label>
        <label>
            Description: <input className='formlabel' type="text" name="description"
            value={description} onChange={(event) => setDescription(event.target.value)}/>
        </label>
      </div>

      <label>
        Unit Size: <input className='formlabel' type="number" name="unitsize" step="0.01"
        value={unitsize} onChange={(event) => setUnitsize(event.target.value)}/>
      </label>
      <div className='subinput'>
        <label>
            Canvas width: <input className='formlabel' type="number" name="width"
            value={width} onChange={(event) => setWidth(event.target.value)}/>
        </label>
        <label>
            Canvas height: <input className='formlabel' type="number" name="height"
            value={height} onChange={(event) => setHeight(event.target.value)}/>
        </label>
      </div>
      <div className='subinput'>
        <label>
          Sieve size: <input className='formlabel' type="text" name="sievesize"
          value={sievesize} onChange={(event) => setSievesize(event.target.value)}/>
        </label>
        <label>
          Minimum radius: <input className='formlabel' type="number" name="minimumradius"
          value={minimumradius} onChange={(event) => setMinimumradius(event.target.value)}/>
        </label>
      </div>
      <label>
          Finer percent: <input className='formlabel' type="text" name="finerpercent"
          value={finerpercent} onChange={(event) => setFinerpercent(event.target.value)}/>
      </label>
      <div className='subinput'>
        <label>
          void ratio: <input className='formlabel' type="number" name="voidratio"  step="0.01"
          value={voidratio} onChange={(event) => setVoidratio(event.target.value)}/>
        </label>
        <label>
          Cell size: <input className='formlabel' type="number" name="cellsize"
          value={cellsize} onChange={(event) => setCellsize(event.target.value)}/>
        </label>
        <label>
          Density: <input className='formlabel' type="number" name="density" step="0.01"
          value={density} onChange={(event) => setDensity(event.target.value)}/>
        </label>
      </div>
      <div className="inputformbutton">
        <input className="btn btn-light formlabel" type="submit" value="Submit" />
        <input className="btn btn-light formlabel" onClick={() => onReset()} type="button" value="Reset" />
      </div>
    </form>
    </>
  )
}

export default InputForm
