import loading from '../assets/loading.gif'

const Spinner = () => {
    return (
        <div className=" h-lvh flex flex-col justify-center items-center">
            <img className="my-3" src={loading} alt="loading" />
            <div className='text-white font-bold text-xl'>Its going to take a while</div>
        </div>
    )
}

export default Spinner