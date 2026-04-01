
function Footer() {
    return (
        <footer className=" bottom-0 left-0 z-20 p-4 bg-[#484343] shadow-sm md:flex md:items-center md:justify-between md:p-6 absolute w-full">
            <span className="text-sm text-white sm:text-center">© 2025 <a className="hover:underline">Product Copy Agent</a>. All Rights Reserved.
            </span>
            <ul className="flex-wrap items-center mt-3 text-sm font-medium text-white sm:mt-0">
                <li className='flex'>
                    <div className="hover:underline">Contact :</div>
                    <div className='px-1'>madhavi.shankar@saks.com |</div>
                    <div>vishal_karda@saks.com</div>
                </li>
            </ul>
        </footer>

    )
}

export default Footer
