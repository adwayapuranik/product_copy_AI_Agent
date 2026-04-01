import { useLocation } from "react-router-dom";

function DownloadFile({ showAlert, setProgress }) {
  const { state } = useLocation();
  const { base64, filename } = state || {};

  if (!base64) return <div className="h-lvh flex flex-col justify-center items-center"><p className="text-white font-bold text-2xl">No file received!</p></div>;
  const excelFile = base64ToFile(base64, filename || "file.xlsx");

  function base64ToFile(base64, filename) {
    const arr = base64.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, { type: mime });
  }


  const downloadFile = () => {
    try {
      setProgress(40);
      const url = URL.createObjectURL(excelFile);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename || "download.xlsx";
      link.click();
      URL.revokeObjectURL(url);
      showAlert("File Downloaded successfully", "success");
      setProgress(100);
    } catch (error) {
      showAlert("error while downloading the file", "danger");
      console.log(error);
    }
  };

  return (
    <div className="h-full w-lvw flex justify-center items-center flex-col text-2xl">
      <h2 className="text-white font-bold">Excel File Has Been Generated</h2>
      <div className='text-white m-4 font-bold flex text-xl'><p className='text-white font-bold'>File Name :</p>{excelFile.name}</div>
      <div onClick={downloadFile} className="relative inline-block text-xl group ">
        <span className="relative z-10 block px-6 py-3 overflow-hidden font-medium leading-tight text-gray-800 transition-colors duration-300 ease-out border-2 border-white cursor-pointer rounded-xl group-hover:text-white">
          <span className="absolute inset-0 w-full h-full px-5 py-3 rounded-lg bg-gray-50"></span>
          <span className="absolute left-0 w-48 h-48 -ml-2 transition-all duration-300 origin-top-right -rotate-90 -translate-x-full translate-y-12 bg-gray-900 group-hover:-rotate-180 ease"></span>
          <span className="relative">Download</span>
        </span>
        <span className="absolute bottom-0 right-0 w-full h-12 -mb-1 -mr-1 transition-all duration-200 ease-linear bg-gray-900 rounded-lg group-hover:mb-0 group-hover:mr-0" data-rounded="rounded-lg"></span>
      </div>
    </div>
  );
}

export default DownloadFile;