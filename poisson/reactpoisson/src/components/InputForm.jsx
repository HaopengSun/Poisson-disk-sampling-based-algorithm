import React, { useState } from "react";

const InputForm = function(props){
    const [name, setName] = useState('')
    const defaultParameter = props.defaultParameter

    const submitName = function(){
        props.setParameter({...defaultParameter, name})
    }

    return(
        <form className='inputform' onSubmit={(event) => {
            event.preventDefault();
            submitName()
        }}>
            <label>
                Name:<input className='formlabel' type="text" name="name" value={name} onChange={(event) => setName(event.target.value)}/>
            </label>
            <input className="btn btn-light formlabel" type="submit" value="Submit" />
        </form>
    )
}

export default InputForm
