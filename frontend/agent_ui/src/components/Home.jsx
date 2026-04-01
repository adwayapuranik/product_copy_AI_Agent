import { useNavigate } from 'react-router-dom'
import './Home.css'

function Home() {

    const navigate = useNavigate();
    const handleClick = () => {
        navigate("/instruction");
    }

    return (
        <div className="flex flex-col h-full items-center justify-center p-10">
            <div className="w-max">
                <h1 className="animate-typing overflow-hidden whitespace-nowrap border-r-4 border-r-white pr-11 pb-2 text-5xl text-white font-bold">
                    Welcome To Product Copy AI Agent
                </h1>
            </div>
            <div className="w-max">

                <p className='animate-typing overflow-hidden whitespace-nowrap text-center border-r-4 border-r-white pr-[33px] pb-2 text-xl text-white italic'>
                    AI AGENT that validates your Raw Product Copy against your Instruction Set and produces
                </p>
                <p className='animate-typing overflow-hidden whitespace-nowrap text-center border-r-4 border-r-white pr-9 pb-2 text-xl text-white italic'>
                    perfectly compliant Validated Product Copy in an easily downloadable excel format.
                </p>
            </div>
            <div className='animate-typing-1 overflow-hidden whitespace-nowrap text-center'>

                <div onClick={handleClick} className="relative inline-block text-xl mt-3 group ">
                    <span className="relative z-10 block px-6 py-3 overflow-hidden font-medium leading-tight text-gray-800 transition-colors duration-300 ease-out border-2 border-white cursor-pointer rounded-xl group-hover:text-white">
                        <span className="absolute inset-0 w-full h-full px-5 py-3 rounded-lg bg-gray-50"></span>
                        <span className="absolute left-0 w-48 h-48 -ml-2 transition-all duration-300 origin-top-right -rotate-90 -translate-x-full translate-y-12 bg-gray-900 group-hover:-rotate-180 ease"></span>
                        <span className="relative">Get Started</span>
                    </span>
                    <span className="absolute bottom-0 right-0 w-full h-12 -mb-1 -mr-1 transition-all duration-200 ease-linear bg-gray-900 rounded-lg group-hover:mb-0 group-hover:mr-0" data-rounded="rounded-lg"></span>
                </div>
            </div>
        </div>
    )
}

export default Home
