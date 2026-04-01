import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';

function InstructionUpload({ showAlert, setProgress }) {

    const [File, setFile] = useState(null);
    const [trigger, setTrigger] = useState(false);
    const navigate = useNavigate();
    const [fileName, setFileName] = useState(null);
    const [exists, setExists] = useState(false);
    // let exists = true;

    const handleFileChange = (e) => {
        const uploadedFile = e.target.files[0];
        if (!uploadedFile) return;
        setFile(uploadedFile);
        setFileName(uploadedFile.name);
    }

    const handleUpload = async () => {
        if (trigger) {
            showAlert("Please acknowledge the alert", "alert");
            return;
        }
        if (!File) { 
            showAlert("Please select a file", "alert");
            return;
        }
        
        setProgress(20);
        const formData = new FormData();
        formData.append("file", File); 
    
        try {
            setProgress(40);
            
            const response = await fetch("http://localhost:8000/instructions/upload", { 
                method: "POST",
                body: formData,
            });
    
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Upload successful:", data);
                
            showAlert("Instruction file uploaded successfully", "success");
            setProgress(100);
            navigate("/input");
            
        } catch (error) {
            showAlert(`Error occurred while uploading Instruction file: ${error.message}`, "danger");
            console.error("Upload error:", error);
            setProgress(0);
        }
    };    

    useEffect(() => {
        const checkFileExistence = async () => {
            try {
                const response = await fetch("http://localhost:8000/prompt-history/exists", {
                    method: "GET",
                });
                console.log("Testing the Connection !!")
                console.log(response)

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                console.log("Checking the json format for response")
                console.log(response.json)

                const data = await response.json(); 
                const fileExists = data.exists; 

                if (fileExists) {
                    setTrigger(true);
                } else {
                    showAlert("No Instruction file found", "alert");
                    navigate("/instruction");
                }
            } catch (error) {
                showAlert("Failed to check for instruction file", "danger");
                console.error("Fetch error:", error);
            }
        };

        checkFileExistence();
        
    }, []);

    const HandleYesClick = () => {
        setTrigger(false);
    }

    const HandleNoClick = () => {
        setTrigger(false);
        navigate("/input");
    }

    return (
        <>
            <div className='flex items-center justify-center h-full'>
                <form className='h-full flex flex-col justify-center w-1/3'>
                    {trigger && <div className='flex'>
                        <div id="alert-additional-content-1" className="shadow-xl p-4 mb-4 text-white border border-blue-300 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-white dark:border-white w-full" role="alert">
                            <div className="flex items-center">
                                <svg className="shrink-0 w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z" />
                                </svg>
                                <span className="sr-only">Info</span>
                                <h3 className="text-lg font-medium">Alert</h3>
                            </div>
                            <div className="mt-2 mb-4 text-sm">
                                Do you want to update the instruction file?
                            </div>
                            <div className="flex">
                                <button onClick={HandleYesClick} type="button" className="cursor-pointer inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-white hover:text-blue-800 focus:outline-hidden focus:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-white dark:hover:text-blue-400 dark:focus:text-blue-400">Yes</button>
                                <button type="button" onClick={HandleNoClick} className="cursor-pointer inline-flex items-center gap-x-2 text-sm ml-3 font-semibold rounded-lg border border-transparent text-white hover:text-blue-800 focus:outline-hidden focus:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-white dark:hover:text-blue-400 dark:focus:text-blue-400">No</button>
                            </div>
                        </div>
                    </div>}
                    <div className="space-y-12 w-full">
                        <div>
                            <h2 className="text-base/7 font-semibold text-white">Instruction file</h2>
                            {exists && <p className="mt-1 text-sm/6 text-gray-400">
                                Please upload a valid instruction file below.
                            </p>}

                            {!exists && <p className="mt-1 text-sm/6 text-gray-400">
                                Please upload a valid instruction file below as instruction file doesn't exist.
                            </p>}

                            <div className="mt-5 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">

                                <div className="col-span-full">
                                    <label htmlFor="cover-photo" className="block text-base/7 font-medium text-white">Upload instruction file</label>
                                    <label htmlFor="dropzone-file" className="relative cursor-pointer rounded-md bg-transparent font-semibold text-indigo-400 focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-indigo-500 hover:text-indigo-300">
                                        <div className="mt-2 flex justify-center rounded-lg border border-dashed border-white/25 px-6 py-10">
                                            <div className="text-center flex items-center flex-col">
                                                <svg className="w-8 h-8 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                                                    <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
                                                </svg>
                                                <div className="mt-4 flex text-sm/6 text-gray-400">
                                                    <span>Upload a file</span>
                                                    <p className="pl-1">or drag and drop</p>
                                                </div>
                                                <p className="text-xs/5 text-gray-400">TXT, PDF or DOCX</p>
                                            </div>
                                        </div>
                                        {!trigger && <input accept=".docx,.pdf,.txt" id="dropzone-file" type="file" className="hidden cursor-pointer" onChange={handleFileChange} />}
                                    </label>
                                </div>
                            </div>
                            {(fileName != null) && (<div className='text-gray-400 pt-4 text-sm/6 flex flex-col'><p className='text-white text-base/7 font-semibold'>Selected instruction file</p>{fileName}</div>)}
                        </div>
                    </div>
                    <div onClick={handleUpload} className="relative mt-6 group flex items-start gap-x-6 w-30">
                        <span className="relative z-10 block px-6 py-3 overflow-hidden font-medium leading-tight text-gray-800 transition-colors duration-300 ease-out border-2 border-white cursor-pointer rounded-xl group-hover:text-white">
                            <span className="absolute inset-0 w-full h-full px-5 py-3 rounded-lg bg-gray-50"></span>
                            <span className="absolute left-0 w-40 h-40 -ml-2 transition-all duration-300 origin-top-right -rotate-90 -translate-x-full translate-y-12 bg-gray-900 group-hover:-rotate-180 ease"></span>
                            <span className="relative">Upload</span>
                        </span>
                        <span className="absolute bottom-0 right-0 w-full h-12 -mb-1 -mr-1 transition-all duration-200 ease-linear bg-gray-900 rounded-lg group-hover:mb-0 group-hover:mr-0" data-rounded="rounded-lg"></span>
                    </div>
                </form>
            </div>
        </>
    )
}
export default InstructionUpload
