import { useState } from "react";

export default function Navbar({ showDirection }) {
  const [open, setOpen] = useState(false);

  const ToggleIcon = () => setOpen(!open);

  const ToggleIconAndHand = () => {
    setOpen(!open);
    showDirection();
  }
  return (
    <nav className="absolute w-full z-50">
      <div className="max-w-7xl flex flex-wrap items-center justify-between mx-auto p-4">
        <a href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
          <img
            src="/logo.png"
            className="h-2.5"
            alt="Flowbite Logo"
          />
          <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">
            Product Copy Agent
          </span>
        </a>
        <button onClick={ToggleIcon} className="relative w-10 h-10 focus:outline-none cursor-pointer">
          <span className={`block absolute h-0.5 w-6 bg-white transform transition duration-300 ease-in-out ${open ? "rotate-45 top-4" : "top-2"}`}></span>
          <span className={`block absolute h-0.5 w-6 bg-white transform transition duration-300 ease-in-out ${open ? "opacity-0" : "top-4"}`}></span>
          <span className={`block absolute h-0.5 w-6 bg-white transform transition duration-300 ease-in-out ${open ? "-rotate-45 top-4" : "top-6"}`}></span>
        </button>
        <div className={`w-full transition-all duration-800 ease-in-out overflow-hidden ${open ? "max-h-40" : "max-h-0"}`}>
          <ul className="flex flex-col font-medium mt-4 rounded-lg bg-gray-50 dark:bg-black dark:border-gray-700">
            <li>
              <a href="/" onClick={ToggleIcon} className="block py-2 px-3 text-white rounded-sm hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white" aria-current="page">Home</a>
            </li>
            <li>
              <a onClick={ToggleIconAndHand} className="block py-2 px-3 text-white rounded-sm hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white">Contact</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
