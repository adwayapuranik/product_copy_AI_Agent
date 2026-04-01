import { useState } from 'react'
import { useNavigate } from 'react-router-dom';

const InputUpload = ({ showAlert, setProgress }) => {

    const [File, setFile] = useState(null);
    const [fileName, setFileName] = useState(null);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        const uploadedFile = e.target.files[0];
        if (!uploadedFile) return;
        setFile(uploadedFile);
        setFileName(uploadedFile.name);
    }

    const blobToBase64 = (blob) =>
        new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
        });

    const handleUpload = async () => {

        if (!File) {
          showAlert("Please select a file", "alert");
          return;
        }
    
        setProgress(20);
        const formData = new FormData();
        formData.append("file", File);
    
        try {
          setProgress(40);
    
          const response = await fetch("http://localhost:8000/input-file/upload", {
            method: "POST",
            body: formData,
          });
    
          if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const detail = errorData.detail || `HTTP error! Status: ${response.status}`;
            throw new Error(detail);
          }
    
          const blob = await response.blob();
          const base64 = await blobToBase64(blob);
    
          showAlert("Input file was processed successfully", "success");
          const outputName = `validated_${fileName}`;
    
          setProgress(100);
          navigate("/Download", { state: { base64, filename: outputName } });
    
        } catch (error) {
          console.error("Input upload error:", error);
          showAlert(`Failed to process input file: ${error.message}`, "danger");
          setProgress(0);
        }
      };

    return (
        <div className='flex items-center justify-center h-full'>
            <form className='h-full flex flex-col justify-center w-1/3'>
                <div className="space-y-12 w-full">
                    <div className="">
                        <h2 className="text-base/7 font-semibold text-white">Input file</h2>
                        <p className="mt-1 text-sm/6 text-gray-400">
                            Please upload a valid input file below.
                        </p>

                        <div className="mt-5 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">

                            <div className="col-span-full">
                                <label htmlFor="cover-photo" className="block text-base/7 font-medium text-white">Upload input file</label>
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
                                            <p className="text-xs/5 text-gray-400">EXCEL, CSV</p>
                                        </div>
                                    </div>
                                    <input accept=".xlsx,.csv" id="dropzone-file" type="file" className="hidden cursor-pointer" onChange={handleFileChange} />
                                </label>
                            </div>
                        </div>
                        {(fileName != null) && (<div className='text-gray-400 pt-4 text-sm/6 flex flex-col'><p className='text-white text-base/7 font-semibold'>Selected input file</p>{fileName}</div>)}
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
    )
}

export default InputUpload
