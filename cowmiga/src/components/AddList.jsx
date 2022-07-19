import React, { useState } from "react"
import { addDoc, collection } from 'firebase/firestore'
import { db } from '../lib/init-firebase'

export default function AddList() {
    const [name, setName] = useState('')

    function handleSubmit(e) {
        e.preventDefault()
        if (name === '') {
            return
        }
        const listRef = collection(db, 'movies')
        addDoc(listRef, { name }).then(response => { console.log(response) })
            .catch(error => {
                console.log(error.message)
            })
    }
    return (
        <div>
            <h4>AddList</h4>
            <form onSubmit={handleSubmit}>
                <label htmlFor='name'>Movie Name</label>
                <input
                    id='name'
                    type="text"
                    value={name}
                    onChange={e => setName(e.target.value)}
                />
                <button type='submit'>Add List</button>
            </form>
        </div>
    )
}