import React, { useState } from 'react'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../lib/init-firebase'
import { useEffect } from 'react'


export default function List() {

    const [movies, setMovies] = useState([])

    useEffect(() => {
        getMovies()
    }, [])

    useEffect(() => {
        console.log(movies)
    }, [movies])

    function getMovies() {
        const listRef = collection(db, 'movies')
        getDocs(listRef).then(response => {
            console.log(response.docs)
            const movs = response.docs.map(doc => ({
                data: doc.data(),
                id: doc.id,
            }))
            setMovies(movs)
        })
            .catch(error => console.log(error.message))
    }

    return (
        <div>
            <h4>List Movies NICE</h4>
            <button onClick={() => getMovies()}>Refresh movies</button>
            <ul>
                {movies.map(movie => <li key={movie.id}>{movie.data.name}</li>)}
            </ul>

        </div>
    )
}
